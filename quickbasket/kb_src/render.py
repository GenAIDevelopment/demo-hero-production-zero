"""Writes knowledge-base documents as PDF (same look as the v4.2 policy) or Markdown, deterministically."""
import os
import re
from xml.sax.saxutils import escape

from reportlab import rl_config

rl_config.invariant = 1  # no timestamps or random IDs in the PDF: same input, same bytes

from reportlab.lib import colors  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.pdfbase import pdfmetrics  # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont  # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

QB_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(QB_DIR, "fonts")
GREEN = colors.HexColor("#0F7B4A")
INK = colors.HexColor("#1D1D1F")
GREY = colors.HexColor("#5F6368")
PALE = colors.HexColor("#EEF6F1")
RED = colors.HexColor("#B42318")
PALE_RED = colors.HexColor("#FDECEA")

_fonts_ready = False


def _fonts():
    global _fonts_ready
    if not _fonts_ready:
        pdfmetrics.registerFont(TTFont("DV", os.path.join(FONT_DIR, "DejaVuSans.ttf")))
        pdfmetrics.registerFont(TTFont("DV-B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")))
        _fonts_ready = True


def _styles():
    return dict(
        title=ParagraphStyle("t", fontName="DV-B", fontSize=17, leading=21, textColor=GREEN, spaceAfter=2),
        sub=ParagraphStyle("s", fontName="DV", fontSize=9.5, leading=13, textColor=GREY, spaceAfter=8),
        h=ParagraphStyle("h", fontName="DV-B", fontSize=11.5, leading=15, textColor=INK, spaceBefore=8, spaceAfter=3),
        h3=ParagraphStyle("h3", fontName="DV-B", fontSize=10, leading=13, textColor=INK, spaceBefore=5, spaceAfter=2),
        p=ParagraphStyle("p", fontName="DV", fontSize=9.3, leading=12.8, textColor=INK, spaceAfter=4),
        li=ParagraphStyle("li", fontName="DV", fontSize=9.3, leading=12.6, textColor=INK, leftIndent=10, spaceAfter=1.5),
        cell=ParagraphStyle("c", fontName="DV", fontSize=8.4, leading=10.6, textColor=INK),
        head=ParagraphStyle("hc", fontName="DV-B", fontSize=8.4, leading=10.6, textColor=colors.white),
        banner=ParagraphStyle("b", fontName="DV-B", fontSize=9.5, leading=12.5, textColor=RED),
        small=ParagraphStyle("sm", fontName="DV", fontSize=8, leading=10.5, textColor=GREY, spaceAfter=3),
    )


def _inline(text):
    """Escape for reportlab, then allow **bold**."""
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escape(text))


def write_pdf(path, header, blocks):
    """blocks: ("title", t, sub) ("banner", t) ("h", t) ("h3", t) ("p", t) ("small", t)
    ("ul", [items]) ("ol", [items]) ("table", [header], [[row]...], [widths in mm] or None)."""
    _fonts()
    S = _styles()
    story = []
    for b in blocks:
        kind = b[0]
        if kind == "title":
            story += [Paragraph(_inline(b[1]), S["title"]), Paragraph(_inline(b[2]), S["sub"])]
        elif kind == "banner":
            t = Table([[Paragraph(_inline(b[1]), S["banner"])]], colWidths=[174 * mm])
            t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), PALE_RED),
                                   ("BOX", (0, 0), (-1, -1), 1, RED),
                                   ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                                   ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
            story += [t, Spacer(1, 3 * mm)]
        elif kind in ("h", "h3", "p", "small"):
            story.append(Paragraph(_inline(b[1]), S[kind]))
        elif kind == "ul":
            story += [Paragraph("• " + _inline(i), S["li"]) for i in b[1]]
            story.append(Spacer(1, 1.5 * mm))
        elif kind == "ol":
            story += [Paragraph(f"{n}. " + _inline(i), S["li"]) for n, i in enumerate(b[1], 1)]
            story.append(Spacer(1, 1.5 * mm))
        elif kind == "table":
            head, rows, widths = b[1], b[2], b[3]
            data = [[Paragraph(_inline(h), S["head"]) for h in head]]
            data += [[Paragraph(_inline(str(c)), S["cell"]) for c in r] for r in rows]
            w = [x * mm for x in widths] if widths else [174 * mm / len(head)] * len(head)
            t = Table(data, colWidths=w, repeatRows=1)
            t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), GREEN),
                                   ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
                                   ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C9D7CF")),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                   ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
            story += [t, Spacer(1, 3 * mm)]
        else:
            raise ValueError(kind)

    def on_page(canvas, doc):
        canvas.saveState()
        canvas.setFont("DV", 7.5)
        canvas.setFillColor(GREY)
        canvas.drawString(18 * mm, A4[1] - 11 * mm, header)
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"Page {doc.page}")
        canvas.restoreState()

    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=18 * mm, bottomMargin=17 * mm, title=header,
                            author="QuickBasket (fictional company)")
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)


def write_md(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text.rstrip() + "\n")


def extract_text(path):
    """The text a 'paste the whole knowledge base' bot would get: pypdf for PDFs, raw text for Markdown."""
    if path.endswith(".pdf"):
        from pypdf import PdfReader
        return "\n".join(p.extract_text() for p in PdfReader(path).pages)
    return open(path, encoding="utf-8").read()


def md_table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)
