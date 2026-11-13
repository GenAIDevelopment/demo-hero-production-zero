"""Cuts the help-centre documents into chunks "the way a good student would":
by section, with every table row kept next to its section name and its column headers, and every
chunk tagged with where it came from (document, policy version, validity dates, city, last-reviewed date).

    from kb_chunker import chunk_knowledge_base
    chunks = chunk_knowledge_base("kb")      # list of langchain_core Documents

PDFs are read with pdfplumber, which sees the tables as tables (pypdf flattens them to loose lines).
"""
import datetime
import json
import os
import re

import pdfplumber
from langchain_core.documents import Document

ROWS_PER_CHUNK = 4        # table rows per chunk (each row keeps its column headers)
MAX_PROSE_CHARS = 1100    # longer prose in one section is split at line breaks
CITIES = ["Hyderabad", "Bengaluru", "Chennai", "Pune", "Mumbai", "Delhi NCR", "Kochi", "Jaipur"]
DATE_NOTE = re.compile(r"Last (?:reviewed|edited|updated):\s*\**\s*(\d{1,2} [A-Z][a-z]+ \d{4})")


def _clean(cell):
    return re.sub(r"\s+", " ", (cell or "").replace("**", "")).strip()


# ---------------------------------------------------------------- PDF -> elements
def _pdf_elements(path):
    """Yield ("heading", level, text) | ("text", text) | ("table", header, rows) in reading order."""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            tables = page.find_tables()
            boxes = [t.bbox for t in tables]
            items = []
            for t in tables:
                rows = [[_clean(c) for c in r] for r in t.extract()]
                items.append((t.bbox[1], "table", rows))
            words = [w for w in page.extract_words(extra_attrs=["fontname", "size"])
                     if w["size"] >= 7.9 and not any(x0 - 1 <= w["x0"] <= x1 + 1 and top - 1 <= w["top"] <= bottom + 1
                                                     for x0, top, x1, bottom in boxes)]
            words.sort(key=lambda w: (w["top"], w["x0"]))
            lines = []
            for w in words:
                if lines and abs(w["top"] - lines[-1][0]["top"]) < 3:
                    lines[-1].append(w)
                else:
                    lines.append([w])
            for ws in lines:
                ws.sort(key=lambda w: w["x0"])
                text = " ".join(w["text"] for w in ws)
                size = max(w["size"] for w in ws)
                bold = all("Bold" in w["fontname"] for w in ws)
                if bold and size >= 9.9:
                    items.append((ws[0]["top"], "heading", (0 if size >= 16 else 1 if size >= 11 else 2, text)))
                else:
                    items.append((ws[0]["top"], "line", text))
            items.sort(key=lambda x: x[0])
            for _, kind, payload in items:
                if kind == "table":
                    if len(payload) == 1 and len(payload[0]) == 1:
                        yield ("text", payload[0][0])            # a one-cell box is a notice, not a table
                    elif payload:
                        yield ("table", payload[0], payload[1:])
                elif kind == "heading":
                    yield ("heading", payload[0], payload[1])
                else:
                    yield ("text", payload)


# ---------------------------------------------------------------- Markdown -> elements
def _md_elements(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^(#{1,4})\s+(.*)", line)
        if m:
            yield ("heading", len(m.group(1)) - 1, _clean(m.group(2)))
        elif line.startswith("|"):
            block = []
            while i < len(lines) and lines[i].startswith("|"):
                block.append([_clean(c) for c in lines[i].strip().strip("|").split("|")])
                i += 1
            rows = [r for r in block if not all(re.fullmatch(r":?-+:?", c) for c in r)]
            if rows:
                yield ("table", rows[0], rows[1:])
            continue
        elif line.strip():
            yield ("text", _clean(line.lstrip("> ").lstrip("-* ").strip()) if line.lstrip().startswith((">", "- ", "* ")) else _clean(line))
        else:
            yield ("break",)
        i += 1


# ---------------------------------------------------------------- elements -> chunks
def _parse_date(s):
    try:
        return datetime.datetime.strptime(s, "%d %B %Y").date().isoformat()
    except ValueError:
        return None


def _chunks_for(doc, elements):
    base = dict(file=doc["file"], title=doc["title"], status=doc.get("status", "current"),
                version=doc.get("version"), valid_from=doc.get("valid_from"), valid_to=doc.get("valid_to"))
    path, prose, out = [], [], []
    state = dict(reviewed={}, last_header=None)

    def meta():
        section = " › ".join(p for p in path if p)
        city = next((c for p in path for c in CITIES if p and p.startswith(c)), None)
        reviewed = next((state["reviewed"][k] for k in range(len(path), 0, -1) if k in state["reviewed"]), None)
        return dict(base, section=section, city=city, reviewed=reviewed)

    def emit(text, kind):
        if text.strip():
            m = meta()
            out.append(Document(page_content=f"{doc['title']} › {m['section']}\n{text.strip()}" if m["section"]
                                else f"{doc['title']}\n{text.strip()}", metadata=dict(m, kind=kind)))

    def flush():
        buf, size = [], 0
        for line in prose:
            if size + len(line) > MAX_PROSE_CHARS and buf:
                emit("\n".join(buf), "text")
                buf, size = [], 0
            buf.append(line)
            size += len(line)
        emit("\n".join(buf), "text")
        prose.clear()

    for el in elements:
        if el[0] != "heading" and el[0] != "break":
            state["prev_heading"] = None
        if el[0] == "heading":
            flush()
            level, text = el[1], el[2]
            if state.get("prev_heading") == level and len(path) == level + 1:
                path[level] += " " + text                        # a long heading wrapped onto a second line
                continue
            del path[level:]
            while len(path) < level:
                path.append("")
            path.append(text)
            state["reviewed"] = {k: v for k, v in state["reviewed"].items() if k <= level}
            state["last_header"] = None
            state["prev_heading"] = level
            continue
        elif el[0] == "text":
            d = DATE_NOTE.search(el[1])
            if d and _parse_date(d.group(1)):
                state["reviewed"][len(path)] = _parse_date(d.group(1))
            prose.append(el[1])
        elif el[0] == "table":
            flush()
            header, rows = el[1], el[2]
            if rows and state["last_header"] and rows[0] == state["last_header"]:
                rows = rows[1:]                                  # header row repeated after a page break
            if state["last_header"] and header != state["last_header"] and len(header) == len(state["last_header"]) \
                    and not any(h in header for h in state["last_header"]):
                rows, header = [header] + rows, state["last_header"]   # table continued on the next page
            state["last_header"] = header
            for i in range(0, len(rows), ROWS_PER_CHUNK):
                lines = [" | ".join(f"{h}: {c}" for h, c in zip(header, r) if c) for r in rows[i:i + ROWS_PER_CHUNK]]
                emit("\n".join("- " + l for l in lines), "table rows")
        elif el[0] == "break" and sum(len(p) for p in prose) > MAX_PROSE_CHARS:
            flush()
    flush()
    return out


def chunk_knowledge_base(kb_dir="kb"):
    """All chunks of all documents listed in kb/manifest.json, as LangChain Documents with metadata."""
    manifest = json.load(open(os.path.join(kb_dir, "manifest.json"), encoding="utf-8"))
    chunks = []
    for doc in manifest["documents"]:
        path = os.path.join(kb_dir, doc["file"])
        elements = _pdf_elements(path) if doc["file"].endswith(".pdf") else _md_elements(path)
        chunks += _chunks_for(doc, elements)
    for i, c in enumerate(chunks):
        c.metadata["chunk_id"] = i
    return chunks


def source_label(meta, current_from="2026-10-01"):
    """One line that tells the model (and the reader) what a chunk is and how far to trust it."""
    fmt = lambda iso: datetime.date.fromisoformat(iso).strftime("%d %B %Y").lstrip("0")
    label = meta["title"]
    if meta.get("section"):
        label += " › " + meta["section"]
    if meta["status"] == "superseded":
        label += f" · SUPERSEDED: in force only for orders placed {fmt(meta['valid_from'])} to {fmt(meta['valid_to'])}"
    elif meta.get("version"):
        label += f" · CURRENT policy, effective {fmt(meta['valid_from'])}"
    if meta.get("reviewed"):
        label += f" · last reviewed {fmt(meta['reviewed'])}"
        if meta["reviewed"] < current_from:
            label += " ⚠ older than the current policy"
    if meta.get("city"):
        label += f" · applies in {meta['city']} only"
    return label


if __name__ == "__main__":
    import collections
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    cs = chunk_knowledge_base("kb")
    by = collections.Counter(c.metadata["file"] for c in cs)
    for f, n in sorted(by.items()):
        print(f"{n:5}  {f}")
    print(f"{len(cs)} chunks; longest {max(len(c.page_content) for c in cs)} chars; "
          f"{sum(1 for c in cs if c.metadata['reviewed'])} carry a review date; "
          f"{sum(1 for c in cs if c.metadata['city'])} carry a city")
