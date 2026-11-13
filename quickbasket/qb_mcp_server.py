"""QuickBasket refunds MCP server: four narrow "buttons" instead of a master key.

The TOOLS enforce the Customer Policy v4.2, not the prompt. Whatever the model asks for, a button only
works if the facts in the database allow it:
  - the order belongs to the logged-in customer (the app sets QB_SESSION_CUSTOMER; the model can't change it)
  - the order is delivered, and has not been refunded before
  - the item is still inside its category's return or report window
  - the amount is at most what the named items cost, and at most APPROVAL_LIMIT (above it:
    needs_human_approval, nothing is paid)
  - the customer has had fewer than three refunds in the last 30 days

Run by the notebook over stdio:  python qb_mcp_server.py
We use MCP SDK 1.x (FastMCP) because the LangChain adapter doesn't support 2.x yet (as of Nov 2026).
Fictional company, synthetic data. The server only ever writes to the working copy of the database.
"""
import datetime
import json
import os
import sqlite3
from typing import Literal

from mcp.server.fastmcp import FastMCP

HERE = os.path.dirname(os.path.abspath(__file__))
WORK_DB = os.environ.get("QB_WORK_DB", os.path.join(HERE, "quickbasket_work.db"))
SESSION_CUSTOMER = os.environ.get("QB_SESSION_CUSTOMER", "")        # who is logged in: set by the app
APPROVAL_LIMIT = int(os.environ.get("QB_APPROVAL_LIMIT", "500"))    # rupees an assistant may refund per order
MAX_REFUNDS_30_DAYS = 3

# Customer Policy v4.2, Section 3. Hours are counted from the delivery time.
# returnable=False means "report a problem only": no refund just because the customer changed their mind.
CATEGORY_RULES = {
    "Fresh fruits & vegetables": dict(hours=24, returnable=False),
    "Dairy, bakery & eggs": dict(hours=24, returnable=False),
    "Frozen & meat": dict(hours=12, returnable=False),
    "Packaged food & beverages": dict(hours=7 * 24, returnable=True),
    "Personal care & beauty": dict(hours=7 * 24, returnable=True),
    "Electronics & accessories": dict(hours=3 * 24, returnable=True),
    "Baby care": dict(hours=7 * 24, returnable=True),
}
PROBLEM_REASONS = ("damaged", "spoiled", "missing_item", "wrong_item", "not_working")
Reason = Literal["damaged", "spoiled", "missing_item", "wrong_item", "not_working", "changed_mind", "late_delivery"]

mcp = FastMCP("quickbasket-refunds")


def _db():
    con = sqlite3.connect(WORK_DB)
    con.row_factory = sqlite3.Row
    return con


def _now(con):
    return datetime.datetime.fromisoformat(con.execute("SELECT value FROM meta WHERE key='demo_now'").fetchone()[0])


def _answer(**fields):
    return json.dumps(fields, ensure_ascii=False)


def _own_order(con, customer_id, order_id):
    """The order, only if it belongs to the logged-in customer. Otherwise None (and we say nothing about it)."""
    if not SESSION_CUSTOMER or customer_id != SESSION_CUSTOMER:
        return None
    return con.execute("SELECT * FROM orders WHERE order_id=? AND customer_id=?", (order_id, SESSION_CUSTOMER)).fetchone()


NOT_YOURS = dict(status="not_found", message="No such order on the logged-in customer's account. Orders on other "
                 "accounts can't be viewed or refunded; the account holder must ask from their own account.")


def _eligibility(con, order, reason):
    """Decide from the facts. Returns a dict with status and, if eligible, the most that may be refunded."""
    now = _now(con)
    if order["status"] != "delivered":
        return dict(status="not_eligible", rule="No refund for an order that is not yet delivered (Section 8).",
                    order_status=order["status"])
    if con.execute("SELECT 1 FROM refunds WHERE order_id=?", (order["order_id"],)).fetchone():
        return dict(status="not_eligible", rule="This order has already been refunded. One refund per order; "
                    "a dispute goes to a human agent (Section 8).")
    if reason == "late_delivery":
        late = (order["actual_minutes"] or 0) - (order["promised_minutes"] or 0)
        plus = con.execute("SELECT plus_member FROM customers WHERE customer_id=?", (order["customer_id"],)).fetchone()[0]
        if late <= 15:
            comp = "No compensation (up to 15 minutes late)."
        elif late <= 30:
            comp = f"Delivery fee of ₹{order['delivery_fee']} refunded as QuickBasket Cash."
        else:
            comp = f"Delivery fee of ₹{order['delivery_fee']} refunded as QuickBasket Cash" + (
                ", plus ₹50 QuickBasket Cash (Plus member)." if plus else ". The extra ₹50 is for Plus members only.")
        return dict(status="not_a_refund", minutes_late=late, plus_member=bool(plus), compensation=comp,
                    rule="Late-delivery compensation is credited automatically as QuickBasket Cash (Section 5). "
                         "It is never issued as a refund by an agent.")
    hours = (now - datetime.datetime.fromisoformat(order["delivered_at"])).total_seconds() / 3600
    eligible_total, notes, eligible_items = 0, [], {}
    for item in con.execute("SELECT * FROM order_items WHERE order_id=?", (order["order_id"],)):
        rule = CATEGORY_RULES[item["category"]]
        value = item["qty"] * item["unit_price"]
        if hours > rule["hours"]:
            notes.append(f"{item['name']}: outside the {rule['hours']}-hour window for {item['category']} "
                         f"(delivered {hours:.0f} hours ago)")
        elif reason == "changed_mind" and not rule["returnable"]:
            notes.append(f"{item['name']}: {item['category']} is not returnable; a refund needs a problem with the item")
        else:
            eligible_total += value
            eligible_items[item["name"]] = value
            notes.append(f"{item['name']}: eligible, up to ₹{value}")
    if eligible_total == 0:
        return dict(status="not_eligible", rule="Nothing in this order can be refunded under the category rules (Section 3).",
                    items=notes)
    since = (now - datetime.timedelta(days=30)).isoformat(sep=" ", timespec="minutes")
    recent = con.execute("SELECT COUNT(*) FROM refunds r JOIN orders o USING(order_id) WHERE o.customer_id=? AND r.refunded_at>=?",
                         (order["customer_id"], since)).fetchone()[0]
    if recent >= MAX_REFUNDS_30_DAYS:
        return dict(status="needs_human_approval", rule=f"The customer already has {recent} refunds in the last 30 days; "
                    "further requests go to the Customer Care Lead (Section 8).", items=notes)
    return dict(status="eligible", max_amount=eligible_total, items=notes, eligible_items=eligible_items,
                approval_limit=APPROVAL_LIMIT,
                note="Photo needed for damaged or spoiled items. Electronics: offer a replacement first." if reason in PROBLEM_REASONS else "")


@mcp.tool()
def list_recent_orders(customer_id: str) -> str:
    """List the logged-in customer's five most recent orders (id, time, status, total, items).
    Use it to ask the customer WHICH order they mean when that isn't clear."""
    if not SESSION_CUSTOMER or customer_id != SESSION_CUSTOMER:
        return _answer(status="not_found", message="You can only list the logged-in customer's own orders.")
    with _db() as con:
        orders = []
        for o in con.execute("SELECT * FROM orders WHERE customer_id=? ORDER BY placed_at DESC LIMIT 5", (SESSION_CUSTOMER,)):
            items = [f"{i['qty']} x {i['name']}" for i in con.execute("SELECT * FROM order_items WHERE order_id=?", (o["order_id"],))]
            refunded = bool(con.execute("SELECT 1 FROM refunds WHERE order_id=?", (o["order_id"],)).fetchone())
            orders.append(dict(order_id=o["order_id"], placed_at=o["placed_at"], status=o["status"],
                               total=o["order_total"], items=items, already_refunded=refunded))
    return _answer(status="ok", orders=orders)


@mcp.tool()
def get_order(customer_id: str, order_id: str) -> str:
    """Details of ONE order, only if it belongs to the logged-in customer."""
    with _db() as con:
        o = _own_order(con, customer_id, order_id)
        if o is None:
            return _answer(**NOT_YOURS)
        items = [dict(name=i["name"], category=i["category"], qty=i["qty"], unit_price=i["unit_price"])
                 for i in con.execute("SELECT * FROM order_items WHERE order_id=?", (order_id,))]
        refunded = bool(con.execute("SELECT 1 FROM refunds WHERE order_id=?", (order_id,)).fetchone())
        late = (o["actual_minutes"] - o["promised_minutes"]) if o["actual_minutes"] is not None else None
        return _answer(status="ok", order_id=o["order_id"], placed_at=o["placed_at"], delivered_at=o["delivered_at"],
                       order_status=o["status"], minutes_late=late, total=o["order_total"], delivery_fee=o["delivery_fee"],
                       payment_method=o["payment_method"], items=items, already_refunded=refunded)


@mcp.tool()
def check_refund_eligibility(customer_id: str, order_id: str, reason: Reason) -> str:
    """Check, from the facts, whether a refund on this order is allowed and for how much. Always call this
    before issue_refund. `reason` is what the customer said is wrong."""
    with _db() as con:
        o = _own_order(con, customer_id, order_id)
        if o is None:
            return _answer(**NOT_YOURS)
        return _answer(order_id=order_id, **_eligibility(con, o, reason))


@mcp.tool()
def issue_refund(customer_id: str, order_id: str, items: list[str], amount: int, reason: Reason) -> str:
    """Refund `amount` rupees for the named `items` of the logged-in customer's order, if every rule allows it.
    `items` are the names of the items the customer has a problem with (as shown by get_order); the amount
    can't be more than those items cost. Above the approval limit nothing is paid: the request is queued for
    a human (needs_human_approval)."""
    with _db() as con:
        o = _own_order(con, customer_id, order_id)
        if o is None:
            return _answer(**NOT_YOURS)
        verdict = _eligibility(con, o, reason)
        if verdict["status"] != "eligible":
            return _answer(order_id=order_id, refunded=False, **verdict)
        amount = int(amount)
        wanted = [name for name in verdict["eligible_items"]
                  if any(w.strip().lower() in name.lower() or name.lower() in w.strip().lower() for w in items if w.strip())]
        if not wanted:
            return _answer(order_id=order_id, refunded=False, status="not_eligible",
                           rule="Name the item or items being refunded. Eligible items in this order: "
                                + ", ".join(f"{n} (₹{v})" for n, v in verdict["eligible_items"].items()) + ".")
        cap = sum(verdict["eligible_items"][name] for name in wanted)
        if amount <= 0 or amount > cap:
            return _answer(order_id=order_id, refunded=False, status="not_eligible",
                           rule=f"The amount must be between ₹1 and ₹{cap}, which is what {', '.join(wanted)} cost.")
        if amount > APPROVAL_LIMIT:
            con.execute("CREATE TABLE IF NOT EXISTS approval_requests (order_id TEXT, amount INTEGER, reason TEXT, requested_at TEXT)")
            con.execute("INSERT INTO approval_requests VALUES (?, ?, ?, ?)",
                        (order_id, amount, reason, _now(con).isoformat(sep=" ", timespec="minutes")))
            return _answer(order_id=order_id, refunded=False, status="needs_human_approval",
                           rule=f"₹{amount} is above the ₹{APPROVAL_LIMIT} limit. Nothing was paid. The request has been "
                                "sent to the Customer Care Lead, who will review it with photo evidence (Section 8).")
        n = con.execute("SELECT COUNT(*) FROM refunds").fetchone()[0]
        refund_id = f"RF-{5000 + n}"
        con.execute("INSERT INTO refunds VALUES (?, ?, ?, ?, ?, ?)",
                    (refund_id, order_id, amount, reason, _now(con).isoformat(sep=" ", timespec="minutes"), "Original payment method"))
        return _answer(order_id=order_id, refunded=True, status="refunded", refund_id=refund_id, amount=amount, items=wanted)


if __name__ == "__main__":
    mcp.run(transport="stdio")
