"""Customer Policy versions. v4.2 is the real quickbasket_policy.pdf (built by build_policy_pdf.py).
The superseded versions are rendered here from the SAME text as v4.2 with a small set of changed values.
Every changed value is logged as a conflict automatically, so kb/conflicts.md can't miss one.
build_kb.py also renders the v4.2 values with this template and checks the text matches the real v4.2 PDF.
"""
from .render import write_pdf

# Values that differ between versions. Everything else in the text is identical to v4.2.
V42_PARAMS = dict(
    version="4.2", effective="1 October 2026", banner=None,
    cities="Hyderabad, Bengaluru, Chennai, Pune, Mumbai and Delhi NCR",
    fruit="24", electronics="3", approval="₹500", upi="2–4 business days", cancel_fee="₹25",
    has_plus=True, plus_bonus="₹50", all_bonus=False,
    plus_month="₹149", plus_year="₹1,299", plus_free_above="₹199",
)

OLD_VERSIONS = [
    dict(V42_PARAMS, file="02_customer_policy_v4.1_superseded.pdf", valid_from="2026-06-01", valid_to="2026-09-30", version="4.1", effective="1 June 2026",
         banner="SUPERSEDED. Replaced on 1 October 2026 by Customer Policy v4.2. Kept only for disputes about "
                "orders placed between 1 June 2026 and 30 September 2026. For everything else, use v4.2.",
         fruit="48", plus_bonus="₹30"),
    dict(V42_PARAMS, file="03_customer_policy_v4.0_superseded.pdf", valid_from="2026-01-01", valid_to="2026-05-31", version="4.0", effective="1 January 2026",
         banner="SUPERSEDED. Replaced on 1 June 2026 by v4.1, which was itself replaced on 1 October 2026 by "
                "Customer Policy v4.2 (current). Kept only for disputes about orders placed between 1 January "
                "2026 and 31 May 2026.",
         electronics="7", approval="₹1,000", all_bonus=True,
         plus_month="₹129", plus_year="₹1,199", plus_free_above="₹249"),
    dict(V42_PARAMS, file="04_customer_policy_v3.2_superseded.pdf", valid_from="2025-03-01", valid_to="2025-12-31", version="3.2", effective="1 March 2025",
         banner="SUPERSEDED. Replaced on 1 January 2026 by v4.0. The current version is Customer Policy v4.2 "
                "(effective 1 October 2026). Kept only for disputes about orders placed between 1 March 2025 "
                "and 31 December 2025.",
         cities="Hyderabad, Bengaluru, Chennai, Pune and Mumbai", electronics="7", approval="₹1,000",
         upi="5–7 business days", cancel_fee="₹15", has_plus=False, all_bonus=True),
]

# How each changed value is described in kb/conflicts.md.
DESCRIBE = {
    "cities": ("Cities served", lambda v: f"Serves {v}", "Serves Hyderabad, Bengaluru, Chennai, Pune, Mumbai and Delhi NCR (Section 1)"),
    "fruit": ("Fresh fruits & vegetables report window", lambda v: f"Report within {v} hours", "Report within 24 hours (Section 3)"),
    "electronics": ("Electronics return window", lambda v: f"{v} days; manufacturer warranty after {v} days", "3 days; manufacturer warranty after 3 days (Section 3)"),
    "approval": ("Automated refund approval limit", lambda v: f"Support agent or automated assistant can approve up to {v}", "Up to ₹500; above ₹500 needs the Customer Care Lead (Section 8)"),
    "upi": ("UPI refund timeline", lambda v: f"UPI refunds land in {v}", "2–4 business days (Section 4)"),
    "cancel_fee": ("Cancellation fee after partner assigned", lambda v: f"{v} fee", "₹25 fee (Section 7)"),
    "has_plus": ("QuickBasket Plus", lambda v: "No Plus membership exists; no Plus column in the late-delivery table", "Plus exists, with its own late-delivery column (Sections 5 and 6)"),
    "plus_bonus": ("Plus late compensation (more than 30 minutes)", lambda v: f"Delivery fee refunded plus {v} QuickBasket Cash", "Delivery fee refunded plus ₹50 QuickBasket Cash (Section 5)"),
    "all_bonus": ("Late compensation for non-Plus customers (more than 30 minutes)", lambda v: "Delivery fee refunded plus ₹50 QuickBasket Cash for all customers", "Delivery fee refunded only; the ₹50 is for Plus members (Section 5)"),
    "plus_month": ("Plus monthly price", lambda v: f"{v} per month", "₹149 per month (Section 6)"),
    "plus_year": ("Plus yearly price", lambda v: f"{v} per year", "₹1,299 per year (Section 6)"),
    "plus_free_above": ("Plus free-delivery threshold", lambda v: f"Free delivery on orders above {v}", "Free delivery on orders above ₹199 (Section 6)"),
}


def policy_blocks(P):
    """The policy text, parameterised. With V42_PARAMS it reproduces quickbasket_policy.pdf's text."""
    n = iter(range(1, 20))
    plus = P["has_plus"]
    b = [("title", "QuickBasket Customer Policy",
          f"Returns, refunds, cancellations and delivery promises · Version {P['version']}")]
    if P["banner"]:
        b.append(("banner", P["banner"]))
    b += [
        ("h", f"{next(n)}. Our promise"),
        ("p", f"QuickBasket delivers groceries, household essentials and electronics in minutes across {P['cities']}. "
              "We want every order to be right. If something is not, we will make it right quickly and fairly."),
        ("p", "Most items can be returned within 7 days of delivery if they are unused and in their original packaging. "
              "Some categories have different rules because of food safety, hygiene or manufacturer terms. These are "
              "listed in Section 3 and always take priority over this general rule."),
        ("h", f"{next(n)}. How to raise a request"),
        ("p", "Customers raise return, refund or missing-item requests from the order page in the app, or by chatting "
              "with QuickBasket Support. Every request must include the order ID (format QB-12345). For damaged or "
              "spoiled items, a photo is required. Requests can only be raised by the account that placed the order."),
        ("p", "Support agents, human or automated, must confirm the order belongs to the customer before discussing "
              "order details or taking any action on it."),
        ("h", f"{next(n)}. Category rules"),
        ("p", "The windows below are counted from the delivery time shown in the app."),
        ("table", ["Category", "Return or report window", "What we offer", "Conditions"], [
            ["Fresh fruits & vegetables", f"Report within {P['fruit']} hours", "Refund or replacement only",
             "Not returnable. Refund only if damaged, spoiled or missing. Photo required."],
            ["Dairy, bakery & eggs", "Report within 24 hours", "Refund or replacement only",
             "Not returnable. Refund only if spoiled before the best-before date."],
            ["Frozen & meat", "Report within 12 hours", "Refund only",
             "Not returnable. Must be reported with photo of packaging and temperature label."],
            ["Packaged food & beverages", "7 days", "Return or refund", "Unopened, before expiry date."],
            ["Personal care & beauty", "7 days", "Return or refund",
             "Seal unbroken. Opened items only if damaged on arrival."],
            ["Electronics & accessories", f"{P['electronics']} days", "Replacement first; refund if no replacement stock",
             f"Unused, all accessories and box included. Manufacturer warranty applies after {P['electronics']} days."],
            ["Baby care", "7 days", "Return or refund", "Seal unbroken. Formula and food not returnable."],
            ["Gift cards & QuickBasket Plus" if plus else "Gift cards", "Not returnable",
             "See Section 6" if plus else "Not applicable", "Gift cards cannot be refunded or exchanged."],
        ], [34, 32, 38, 70]),
        ("h", f"{next(n)}. Refund timelines"),
        ("p", "Once a refund is approved, the money goes back to the original payment method. Customers can choose "
              "QuickBasket Cash instead, which is instant."),
        ("table", ["Original payment method", "Refund lands in", "Notes"], [
            ["UPI", P["upi"], "Back to the same UPI-linked bank account."],
            ["Credit or debit card", "5–7 business days", "Depends on the issuing bank."],
            ["QuickBasket Cash", "Instant", "Shows in the wallet immediately."],
            ["Cash on delivery", "Instant, as QuickBasket Cash", "Bank refund on request: 5–7 business days."],
        ], [50, 50, 74]),
        ("h", f"{next(n)}. Late deliveries"),
        ("p", "Every order shows a promised delivery time at checkout. If we miss it, we compensate automatically. "
              "Compensation is credited as QuickBasket Cash, never as a bank refund."),
    ]
    over30_all = "Delivery fee refunded plus ₹50 QuickBasket Cash" if P["all_bonus"] else "Delivery fee refunded"
    if plus:
        b.append(("table", ["How late", "All customers", "QuickBasket Plus members"], [
            ["Up to 15 minutes", "No compensation", "No compensation"],
            ["16 to 30 minutes", "Delivery fee refunded", "Delivery fee refunded"],
            ["More than 30 minutes", over30_all, f"Delivery fee refunded plus {P['plus_bonus']} QuickBasket Cash"],
        ], [50, 60, 64]))
    else:
        b.append(("table", ["How late", "Compensation"], [
            ["Up to 15 minutes", "No compensation"],
            ["16 to 30 minutes", "Delivery fee refunded"],
            ["More than 30 minutes", over30_all],
        ], [60, 114]))
    b.append(("p", "Delays caused by the customer (wrong address, not reachable, gated community entry) and declared "
                   "weather or traffic advisories are excluded."))
    if plus:
        b += [("h", f"{next(n)}. QuickBasket Plus membership"),
              ("p", f"Plus costs {P['plus_month']} per month or {P['plus_year']} per year and includes free delivery "
                    f"on orders above {P['plus_free_above']}. A Plus membership can be cancelled within 48 hours of "
                    "purchase for a full refund if no free delivery has been used. After that it can be cancelled at "
                    "any time, but the current period is not refunded.")]
    b += [
        ("h", f"{next(n)}. Cancellations"),
        ("p", "An order can be cancelled free of charge until a delivery partner is assigned. After that, cancellation "
              f"is possible only before pickup and a {P['cancel_fee']} fee applies. Orders that are out for delivery "
              "cannot be cancelled; the customer can refuse delivery and request a refund for unopened items once the "
              "order is marked delivered."),
        ("h", f"{next(n)}. Refund approvals and limits"),
        ("p", "To protect customers and the business, refunds follow the approval rules below. These rules apply to "
              "every support channel, including automated assistants."),
        ("table", ["Refund amount (per order)", "Who can approve", "Extra checks"], [
            [f"Up to {P['approval']}", "Support agent or automated assistant",
             "Order belongs to the customer, is delivered, and is eligible under Section 3."],
            [f"Above {P['approval']}", "Customer Care Lead (human)", "All of the above, plus photo evidence review."],
            ["Any amount on an order already refunded", "Not allowed", "One refund per order. Escalate disputes."],
        ], [50, 54, 70]),
        ("p", "No refund is issued for an order that is not yet delivered. A customer may hold at most three refunds "
              "in any 30-day period; further requests go to the Customer Care Lead."),
        ("h", f"{next(n)}. Escalation"),
        ("p", "If a customer is unhappy with a decision, or uses abusive or threatening language, the conversation is "
              "handed to a human agent. Automated assistants must never promise outcomes this policy does not allow, "
              "and must say so plainly when they do not know the answer."),
        ("p", "Questions about this policy: policy@quickbasket.example"),
    ]
    return b


def header(P):
    return (f"QuickBasket Customer Policy v{P['version']} · Effective {P['effective']} · "
            "Fictional company for training use. All content synthetic.")


def build(ctx, out_dir):
    docs = []
    for P in OLD_VERSIONS:
        path = f"{out_dir}/{P['file']}"
        write_pdf(path, header(P), policy_blocks(P))
        for key, (topic, says, v42) in DESCRIBE.items():
            if P[key] != V42_PARAMS[key]:
                ctx.conflict(topic, P["file"], "policy text", says(P[key]), v42, f"superseded policy v{P['version']}")
        docs.append(dict(file=P["file"], title=f"Customer Policy v{P['version']} (superseded)",
                         kind="Superseded policy", fmt="PDF", status="superseded",
                         version=P["version"], valid_from=P["valid_from"], valid_to=P["valid_to"]))
    return docs
