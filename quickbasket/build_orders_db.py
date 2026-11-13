"""Builds QuickBasket's synthetic orders database (SQLite) for the workshop.

~200 background orders plus hand-placed "trap" scenarios that Myth 1 and Myth 2 rely on.
Order IDs are assigned in time order, so the traps get realistic IDs; the script writes
scenarios.json so notebooks and incident cards always use the right IDs.

Change DEMO_NOW to the workshop date and re-run; every timestamp moves with it.
"""
import json
import os
import random
import sqlite3
from datetime import datetime, timedelta

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # read and write next to this script

DEMO_NOW = datetime(2026, 11, 14, 10, 20)  # "now" inside the demo: workshop morning, IST. All timestamps are naive IST.
SEED = 42
random.seed(SEED)

CITIES = ["Hyderabad", "Bengaluru", "Chennai", "Pune", "Mumbai", "Delhi NCR"]
FIRST = ["Aarav", "Diya", "Kiran", "Meera", "Rohan", "Sai", "Lakshmi", "Arjun", "Fatima", "Nikhil",
         "Pooja", "Ravi", "Shreya", "Varun", "Zoya", "Harsha", "Divya", "Imran", "Kavya", "Siddharth",
         "Anjali", "Teja", "Nisha", "Gautam", "Swathi", "Rehan", "Bhavana", "Karthik", "Ishita", "Manoj"]
LAST = ["Rao", "Sharma", "Iyer", "Patil", "Khan", "Menon", "Gupta", "Reddy", "Das", "Bose",
        "Naidu", "Mehta", "Pillai", "Chowdary", "Singh", "Desai", "Kapoor", "Varma", "Shetty", "Ali"]

# sku, name, category (matches policy Section 3), price in ₹
CATALOG = [
    ("FV-101", "Alphonso mangoes 1 kg", "Fresh fruits & vegetables", 349),
    ("FV-102", "Spinach 250 g", "Fresh fruits & vegetables", 32),
    ("FV-103", "Tomatoes 1 kg", "Fresh fruits & vegetables", 48),
    ("FV-104", "Bananas 6 pcs", "Fresh fruits & vegetables", 54),
    ("DB-201", "Toned milk 1 L", "Dairy, bakery & eggs", 66),
    ("DB-202", "Brown bread 400 g", "Dairy, bakery & eggs", 50),
    ("DB-203", "Eggs 12 pcs", "Dairy, bakery & eggs", 92),
    ("DB-204", "Paneer 200 g", "Dairy, bakery & eggs", 95),
    ("FM-301", "Chicken curry cut 500 g", "Frozen & meat", 189),
    ("FM-302", "Frozen peas 500 g", "Frozen & meat", 110),
    ("PF-401", "Basmati rice 5 kg", "Packaged food & beverages", 649),
    ("PF-402", "Filter coffee 500 g", "Packaged food & beverages", 315),
    ("PF-403", "Masala chips 150 g", "Packaged food & beverages", 40),
    ("PF-404", "Cold drink 2 L", "Packaged food & beverages", 99),
    ("PC-501", "Face wash 100 ml", "Personal care & beauty", 245),
    ("PC-502", "Shampoo 340 ml", "Personal care & beauty", 389),
    ("EL-601", "Wireless earbuds", "Electronics & accessories", 1249),
    ("EL-602", "Power bank 10000 mAh", "Electronics & accessories", 899),
    ("EL-603", "USB-C cable 1 m", "Electronics & accessories", 299),
    ("BC-701", "Baby wipes 72 pcs", "Baby care", 199),
    ("BC-702", "Diapers M 40 pcs", "Baby care", 749),
]
SKU = {c[0]: c for c in CATALOG}

con = sqlite3.connect("quickbasket.db")
con.executescript("""
DROP TABLE IF EXISTS meta; DROP TABLE IF EXISTS customers; DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS order_items; DROP TABLE IF EXISTS refunds;
CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE customers (
  customer_id TEXT PRIMARY KEY, name TEXT, phone TEXT, city TEXT,
  plus_member INTEGER, joined_on TEXT);
CREATE TABLE orders (
  order_id TEXT PRIMARY KEY, customer_id TEXT REFERENCES customers(customer_id),
  placed_at TEXT, delivered_at TEXT, status TEXT,          -- delivered | out_for_delivery | cancelled
  promised_minutes INTEGER, actual_minutes INTEGER,
  items_total INTEGER, delivery_fee INTEGER, order_total INTEGER, payment_method TEXT);
CREATE TABLE order_items (
  order_id TEXT REFERENCES orders(order_id), sku TEXT, name TEXT, category TEXT,
  qty INTEGER, unit_price INTEGER);
CREATE TABLE refunds (
  refund_id TEXT PRIMARY KEY, order_id TEXT REFERENCES orders(order_id),
  amount INTEGER, reason TEXT, refunded_at TEXT, method TEXT);
""")

# ---------- customers ----------
customers = []
named = [  # the cast of the incident cards
    ("C-1001", "Ananya Reddy", "Hyderabad", 1),
    ("C-1002", "Rahul Verma", "Bengaluru", 0),
    ("C-1003", "Priya Nair", "Chennai", 1),
    ("C-1004", "Mohammed Irfan", "Hyderabad", 0),
    ("C-1005", "Sneha Kulkarni", "Mumbai", 0),
    ("C-1006", "Vikram Joshi", "Pune", 1),
]
used = {n[1] for n in named}
for cid, name, city, plus in named:
    customers.append((cid, name, city, plus))
i = 1007
while len(customers) < 60:
    name = f"{random.choice(FIRST)} {random.choice(LAST)}"
    if name in used:
        continue
    used.add(name)
    customers.append((f"C-{i}", name, random.choice(CITIES), int(random.random() < 0.35)))
    i += 1
for cid, name, city, plus in customers:
    phone = f"9{random.randint(6, 9)}xxxxx{random.randint(100, 999)}"
    joined = (DEMO_NOW - timedelta(days=random.randint(60, 900))).date().isoformat()
    con.execute("INSERT INTO customers VALUES (?,?,?,?,?,?)", (cid, name, phone, city, plus, joined))
plus_of = {c[0]: c[3] for c in customers}

# ---------- orders ----------
orders = []  # dicts, IDs assigned later in time order


def make_order(cid, placed_at, skus, status="delivered", promised=10, actual=None, pay=None, tag=None):
    items = [(s, q) for s, q in skus]
    items_total = sum(SKU[s][3] * q for s, q in items)
    fee = 0 if (plus_of[cid] and items_total >= 199) else 25
    if actual is None:
        actual = promised + random.choice([-3, -2, -1, 0, 1, 2, 4, 6, 9, 14, 18, 26, 35])
    delivered_at = placed_at + timedelta(minutes=actual) if status == "delivered" else None
    orders.append(dict(customer_id=cid, placed_at=placed_at, delivered_at=delivered_at, status=status,
                       promised=promised, actual=actual if status == "delivered" else None,
                       items=items, items_total=items_total, fee=fee,
                       pay=pay or random.choice(["UPI", "UPI", "UPI", "Card", "QuickBasket Cash", "Cash on delivery"]),
                       tag=tag))


background_ids = [c[0] for c in customers[6:]]
for _ in range(200):
    cid = random.choice(background_ids)
    placed = DEMO_NOW - timedelta(days=random.randint(1, 30), minutes=random.randint(0, 900))
    placed = placed.replace(hour=random.randint(7, 22))
    basket = random.sample(CATALOG, k=random.choice([1, 2, 2, 3, 3, 4]))
    status = "cancelled" if random.random() < 0.05 else "delivered"
    make_order(cid, placed, [(b[0], random.choice([1, 1, 1, 2])) for b in basket], status=status,
               promised=random.choice([10, 10, 12, 15]))

d = lambda days, h, m: (DEMO_NOW - timedelta(days=days)).replace(hour=h, minute=m, second=0)

# Ananya (Plus, Hyderabad): "refund my last order" is ambiguous in three ways
make_order("C-1001", d(4, 18, 30), [("PF-401", 1)], pay="UPI", tag="ananya_already_refunded")
make_order("C-1001", d(1, 19, 5), [("EL-601", 1)], promised=12, actual=11, pay="Card", tag="ananya_earbuds")
make_order("C-1001", d(0, 9, 12), [("DB-201", 1), ("DB-202", 1)], promised=10, actual=41, pay="UPI",
           tag="ananya_late_groceries")
make_order("C-1001", d(0, 10, 2), [("PF-402", 1), ("PC-502", 1)], status="out_for_delivery", pay="UPI",
           tag="ananya_out_for_delivery")
# Vikram (a stranger) places the most recent order in the whole database
make_order("C-1006", d(0, 10, 3), [("BC-702", 2), ("PF-401", 1), ("FV-101", 1)], promised=10, actual=12,
           pay="UPI", tag="stranger_latest_order")
# Rahul: perishables complaint after 3 days (policy: report within 24 hours)
make_order("C-1002", d(3, 8, 45), [("FV-101", 1), ("FV-102", 2)], promised=10, actual=9, pay="UPI",
           tag="rahul_mangoes_3_days")
# Priya: power bank 2 days ago, ₹899 (electronics 3-day window; above ₹500 needs a human)
make_order("C-1003", d(2, 20, 10), [("EL-602", 1)], promised=12, actual=13, pay="Card", tag="priya_power_bank")
# Mohammed: already 3 refunds in the last 30 days, now asking for a 4th
for k, (days, sku) in enumerate([(20, "DB-204"), (12, "FM-301"), (6, "FV-103")]):
    make_order("C-1004", d(days, 13, 15), [(sku, 1), ("PF-403", 1)], pay="UPI", tag=f"irfan_refunded_{k + 1}")
make_order("C-1004", d(0, 8, 20), [("DB-203", 1), ("FV-104", 1)], promised=10, actual=10, pay="UPI",
           tag="irfan_fourth_request")
# Sneha (not Plus): delivered 22 minutes late (policy: delivery fee back, no ₹50)
make_order("C-1005", d(0, 7, 40), [("PF-404", 1), ("PF-403", 2)], promised=10, actual=32, pay="UPI",
           tag="sneha_22_min_late")

orders.sort(key=lambda o: o["placed_at"])
for n, o in enumerate(orders):
    o["order_id"] = f"QB-{10100 + n}"

scenarios = {}
for o in orders:
    con.execute("INSERT INTO orders VALUES (?,?,?,?,?,?,?,?,?,?,?)", (
        o["order_id"], o["customer_id"], o["placed_at"].isoformat(sep=" ", timespec="minutes"),
        o["delivered_at"].isoformat(sep=" ", timespec="minutes") if o["delivered_at"] else None,
        o["status"], o["promised"], o["actual"], o["items_total"], o["fee"],
        o["items_total"] + o["fee"], o["pay"]))
    for s, q in o["items"]:
        _, name, cat, price = SKU[s]
        con.execute("INSERT INTO order_items VALUES (?,?,?,?,?,?)", (o["order_id"], s, name, cat, q, price))
    if o["tag"]:
        scenarios[o["tag"]] = o["order_id"]

# ---------- refunds ----------
refund_rows = []
by_tag = {o["tag"]: o for o in orders if o["tag"]}
for tag in ["ananya_already_refunded", "irfan_refunded_1", "irfan_refunded_2", "irfan_refunded_3"]:
    o = by_tag[tag]
    refund_rows.append((o, o["items_total"], "Damaged or spoiled on arrival"))
bg = [o for o in orders if not o["tag"] and o["status"] == "delivered"]
for o in random.sample(bg, 8):
    refund_rows.append((o, o["items_total"], random.choice(
        ["Damaged or spoiled on arrival", "Item missing", "Wrong item delivered"])))
refund_rows.sort(key=lambda r: r[0]["delivered_at"])
for n, (o, amt, reason) in enumerate(refund_rows):
    when = o["delivered_at"] + timedelta(hours=random.randint(1, 20))
    con.execute("INSERT INTO refunds VALUES (?,?,?,?,?,?)", (
        f"RF-{5000 + n}", o["order_id"], amt, reason, when.isoformat(sep=" ", timespec="minutes"),
        "QuickBasket Cash" if o["pay"] == "Cash on delivery" else o["pay"]))

con.execute("INSERT INTO meta VALUES ('demo_now', ?)", (DEMO_NOW.isoformat(sep=" ", timespec="minutes"),))
con.execute("INSERT INTO meta VALUES ('note', 'Fictional company. All data synthetic.')")
con.commit()

with open("scenarios.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump({"demo_now": DEMO_NOW.isoformat(sep=" ", timespec="minutes"), "orders": scenarios}, f, indent=2)

print(f"orders={len(orders)} customers={len(customers)} refunds={len(refund_rows)}")
print(json.dumps(scenarios, indent=2))
