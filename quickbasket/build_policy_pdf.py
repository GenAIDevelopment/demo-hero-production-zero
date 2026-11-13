"""Builds QuickBasket's customer policy PDF (fictional company, synthetic content).

The document is designed for the workshop:
- The friendly prose up front says "most items: 7 days" (the trap a prompt-only bot repeats).
- The rules that actually decide most questions live in TABLES (the trap naive chunking splits).
- The ₹500 refund-approval rule ties Myth 1 (policy) to Myth 2 (the refund agent).

Runs the same on Windows, macOS, Linux and Colab, from any folder: the DejaVu fonts it needs
are bundled in ./fonts (free licence, see fonts/LICENSE-DejaVu.txt), so the PDF is identical
everywhere and no system fonts or internet are needed.
"""
import os
import sys

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)  # read and write next to this script, wherever it is run from

# Where to look for DejaVuSans.ttf + DejaVuSans-Bold.ttf, first match wins.
FONT_DIRS = [
    os.environ.get("QB_FONT_DIR", ""),               # optional override
    os.path.join(HERE, "fonts"),                     # bundled with the repo (normal case)
    "/usr/share/fonts/truetype/dejavu",              # Debian/Ubuntu/Colab
    "/usr/share/fonts/dejavu",                       # Fedora/Arch
    os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts"),
    os.path.expanduser("~/Library/Fonts"), "/Library/Fonts",  # macOS
]
FONT_DIR = next((d for d in FONT_DIRS if d and all(
    os.path.isfile(os.path.join(d, f)) for f in ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf"))), None)
if FONT_DIR is None:
    sys.exit("Can't find the DejaVu fonts. They should be in quickbasket/fonts/ "
             "(re-clone the repo), or set QB_FONT_DIR to a folder that has DejaVuSans.ttf.")
pdfmetrics.registerFont(TTFont("DV", os.path.join(FONT_DIR, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DV-B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")))

GREEN = colors.HexColor("#0F7B4A")
INK = colors.HexColor("#1D1D1F")
body = ParagraphStyle("body", fontName="DV", fontSize=9.5, leading=13.2, textColor=INK, spaceAfter=6)
small = ParagraphStyle("small", parent=body, fontSize=8, leading=11, textColor=colors.HexColor("#5A5A5A"))
h1 = ParagraphStyle("h1", fontName="DV-B", fontSize=20, leading=24, textColor=GREEN, spaceAfter=4)
h2 = ParagraphStyle("h2", fontName="DV-B", fontSize=12.5, leading=16, textColor=GREEN, spaceBefore=9, spaceAfter=5)
cell = ParagraphStyle("cell", fontName="DV", fontSize=8.5, leading=11, textColor=INK)
cell_b = ParagraphStyle("cell_b", parent=cell, fontName="DV-B", textColor=colors.white)


def table(rows, widths):
    data = [[Paragraph(c, cell_b) for c in rows[0]]] + [[Paragraph(c, cell) for c in r] for r in rows[1:]]
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GREEN),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C9D6CF")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F7F4")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("DV", 7.5)
    canvas.setFillColor(colors.HexColor("#7A7A7A"))
    canvas.drawString(18 * mm, 10 * mm, "QuickBasket Customer Policy v4.2 · Effective 1 October 2026 · "
                      "Fictional company for training use. All content synthetic.")
    canvas.drawRightString(192 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


s = []
s += [Paragraph("QuickBasket Customer Policy", h1),
      Paragraph("Returns, refunds, cancellations and delivery promises · Version 4.2", small),
      Spacer(1, 8)]

s += [Paragraph("1. Our promise", h2),
      Paragraph("QuickBasket delivers groceries, household essentials and electronics in minutes across "
                "Hyderabad, Bengaluru, Chennai, Pune, Mumbai and Delhi NCR. We want every order to be right. "
                "If something is not, we will make it right quickly and fairly.", body),
      Paragraph("Most items can be returned within 7 days of delivery if they are unused and in their original "
                "packaging. Some categories have different rules because of food safety, hygiene or "
                "manufacturer terms. These are listed in Section 3 and always take priority over this "
                "general rule.", body)]

s += [Paragraph("2. How to raise a request", h2),
      Paragraph("Customers raise return, refund or missing-item requests from the order page in the app, or "
                "by chatting with QuickBasket Support. Every request must include the order ID (format "
                "QB-12345). For damaged or spoiled items, a photo is required. Requests can only be raised by "
                "the account that placed the order.", body),
      Paragraph("Support agents, human or automated, must confirm the order belongs to the customer before "
                "discussing order details or taking any action on it.", body)]

s += [Paragraph("3. Category rules", h2),
      Paragraph("The windows below are counted from the delivery time shown in the app.", body),
      table([
          ["Category", "Return or report window", "What we offer", "Conditions"],
          ["Fresh fruits &amp; vegetables", "Report within 24 hours", "Refund or replacement only",
           "Not returnable. Refund only if damaged, spoiled or missing. Photo required."],
          ["Dairy, bakery &amp; eggs", "Report within 24 hours", "Refund or replacement only",
           "Not returnable. Refund only if spoiled before the best-before date."],
          ["Frozen &amp; meat", "Report within 12 hours", "Refund only",
           "Not returnable. Must be reported with photo of packaging and temperature label."],
          ["Packaged food &amp; beverages", "7 days", "Return or refund", "Unopened, before expiry date."],
          ["Personal care &amp; beauty", "7 days", "Return or refund",
           "Seal unbroken. Opened items only if damaged on arrival."],
          ["Electronics &amp; accessories", "3 days", "Replacement first; refund if no replacement stock",
           "Unused, all accessories and box included. Manufacturer warranty applies after 3 days."],
          ["Baby care", "7 days", "Return or refund", "Seal unbroken. Formula and food not returnable."],
          ["Gift cards &amp; QuickBasket Plus", "Not returnable", "See Section 6",
           "Gift cards cannot be refunded or exchanged."],
      ], [36, 34, 38, 66])]

s += [Paragraph("4. Refund timelines", h2),
      Paragraph("Once a refund is approved, the money goes back to the original payment method. Customers can "
                "choose QuickBasket Cash instead, which is instant.", body),
      table([
          ["Original payment method", "Refund lands in", "Notes"],
          ["UPI", "2–4 business days", "Back to the same UPI-linked bank account."],
          ["Credit or debit card", "5–7 business days", "Depends on the issuing bank."],
          ["QuickBasket Cash", "Instant", "Shows in the wallet immediately."],
          ["Cash on delivery", "Instant, as QuickBasket Cash", "Bank refund on request: 5–7 business days."],
      ], [48, 44, 82])]

s += [Paragraph("5. Late deliveries", h2),
      Paragraph("Every order shows a promised delivery time at checkout. If we miss it, we compensate "
                "automatically. Compensation is credited as QuickBasket Cash, never as a bank refund.", body),
      table([
          ["How late", "All customers", "QuickBasket Plus members"],
          ["Up to 15 minutes", "No compensation", "No compensation"],
          ["16 to 30 minutes", "Delivery fee refunded", "Delivery fee refunded"],
          ["More than 30 minutes", "Delivery fee refunded", "Delivery fee refunded plus ₹50 QuickBasket Cash"],
      ], [50, 56, 68]),
      Spacer(1, 4),
      Paragraph("Delays caused by the customer (wrong address, not reachable, gated community entry) and "
                "declared weather or traffic advisories are excluded.", body)]

s += [Paragraph("6. QuickBasket Plus membership", h2),
      Paragraph("Plus costs ₹149 per month or ₹1,299 per year and includes free delivery on orders above "
                "₹199. A Plus membership can be cancelled within 48 hours of purchase for a full refund if no "
                "free delivery has been used. After that it can be cancelled at any time, but the current "
                "period is not refunded.", body)]

s += [Paragraph("7. Cancellations", h2),
      Paragraph("An order can be cancelled free of charge until a delivery partner is assigned. After that, "
                "cancellation is possible only before pickup and a ₹25 fee applies. Orders that are out for "
                "delivery cannot be cancelled; the customer can refuse delivery and request a refund for "
                "unopened items once the order is marked delivered.", body)]

s += [Paragraph("8. Refund approvals and limits", h2),
      Paragraph("To protect customers and the business, refunds follow the approval rules below. "
                "These rules apply to every support channel, including automated assistants.", body),
      table([
          ["Refund amount (per order)", "Who can approve", "Extra checks"],
          ["Up to ₹500", "Support agent or automated assistant",
           "Order belongs to the customer, is delivered, and is eligible under Section 3."],
          ["Above ₹500", "Customer Care Lead (human)", "All of the above, plus photo evidence review."],
          ["Any amount on an order already refunded", "Not allowed", "One refund per order. Escalate disputes."],
      ], [48, 50, 76]),
      Spacer(1, 4),
      Paragraph("No refund is issued for an order that is not yet delivered. A customer may hold at most "
                "three refunds in any 30-day period; further requests go to the Customer Care Lead.", body)]

s += [Paragraph("9. Escalation", h2),
      Paragraph("If a customer is unhappy with a decision, or uses abusive or threatening language, the "
                "conversation is handed to a human agent. Automated assistants must never promise outcomes "
                "this policy does not allow, and must say so plainly when they do not know the answer.", body),
      Spacer(1, 10),
      Paragraph("Questions about this policy: policy@quickbasket.example", small)]

doc = SimpleDocTemplate("quickbasket_policy.pdf", pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                        topMargin=14 * mm, bottomMargin=16 * mm, title="QuickBasket Customer Policy",
                        author="QuickBasket (fictional)")
doc.build(s, onFirstPage=footer, onLaterPages=footer)
print("wrote quickbasket_policy.pdf")
