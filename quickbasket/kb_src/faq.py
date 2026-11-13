"""Customer FAQ (Markdown): about 200 questions in 12 sections. Fictional company, synthetic content.

Ten sections agree with Customer Policy v4.2. Two sections ("Late deliveries" and "Electronics and
accessories") are deliberately stale: they were last reviewed on 12 March 2026 and still give the v4.0
rules. Both are registered with ctx.conflict() at the bottom of build().

Questions are a mix of hand-written ones and ones generated from data (category x question type, payment
method x question type, city x question type), with the wording picked through ctx.rng.
"""
from .cities import CITIES
from .common import pick
from .render import md_table, write_md
from .warranty import PRODUCT_NOTES, PRODUCTS

FILE = "11_customer_faq.md"
STALE = "12 March 2026"
CHENNAI = (" The one exception is an order delivered in Chennai during a declared cyclone or heavy-rain "
           "advisory, where the window is 48 hours.")


def cap(s):
    return s[0].upper() + s[1:]


# ------------------------------------------------------------------ category questions (generated)
PERISHABLE_Q = dict(
    window=["How long do I have to report a problem with {item}?",
            "{item} came spoiled. how much time do i have to report it",
            "What is the reporting window for {cat}?",
            "by when do i need to complain about bad {item}"],
    offer=["What will I get if my {item} arrived spoiled?",
           "Do you refund or replace bad {item}?",
           "{item} arrived damaged, will i get my money back",
           "Can I get a replacement for spoiled {item}?"],
    proof=["Do I need a photo to report a problem with {item}?",
           "What do I need to send when I report bad {item}?",
           "is a photo compulsory for {item} complaints"],
    late=["I forgot to report my {item} in time. Can I still get a refund?",
          "{item} went bad after {late}, can i get a refund",
          "I noticed the problem with my {item} only after {late}. Is it too late?"],
    missing=["{item} was missing from my order. What do I do?", "i paid for {item} but it was not in the bag",
             "My order arrived without the {item}. How do I get my money back?"],
    example=["My {item} was delivered at {t0}. Until when can I report a problem?",
             "order with {item} delivered {t0}, what is the last time to report an issue"],
    mind=["Can I return {item} if I just don't want it any more?",
          "i ordered too much {item}, can i send it back",
          "Can I return {item} because I changed my mind?"],
)
RETURNABLE_Q = dict(
    window=["How many days do I have to return {item}?",
            "What is the return window for {cat}?",
            "till when can i return {item}"],
    offer=["Do I get a refund or a replacement when I return {item}?",
           "What do you offer when I return {item}?",
           "will i get my money back if i return {item}"],
    proof=["What condition does {item} need to be in for a return?",
           "what are the conditions for returning {item}",
           "Does {item} have to be sealed to be returned?"],
    late=["Can I return {item} after {late}?",
          "it's been {late} since delivery, can i still return {item}",
          "I missed the return window for {item}. What can I do?"],
    missing=["The {item} was missing from my order. What do I do?", "i paid for {item} but it was not in the bag",
             "My order arrived without the {item}. How do I get my money back?"],
    example=["My {item} was delivered at {t0}. What is the last moment I can raise a return?",
             "order with {item} delivered {t0}, last date to return?"],
    mind=["Can I return opened {item}?",
          "can i return {item} after opening it",
          "I opened the {item} and don't like it. Can I return it?"],
)

CATEGORIES = [
    dict(cat="fresh fruits and vegetables", qs=PERISHABLE_Q, late="3 days",
         items=["mangoes", "tomatoes", "bananas", "spinach", "grapes"],
         a=dict(
             window="Report it within 24 hours of the delivery time shown in the app. This covers fresh fruits "
                    "and vegetables that arrive damaged, spoiled or missing. A request raised after 24 hours is "
                    "not eligible, so it is worth checking fresh items when they arrive.",
             offer="A refund or a replacement; you can ask for either when you raise the request. Fresh fruits "
                   "and vegetables are not returnable, so nobody comes to collect the item. This applies only "
                   "when the item was damaged, spoiled or missing and you report it within 24 hours of delivery.",
             proof="Yes. A photo is required for every fresh fruit and vegetable request. Add it on the order "
                   "page, or send it in Support chat together with the order ID (format QB-12345).",
             late="No. Fresh fruits and vegetables have to be reported within 24 hours of the delivery time "
                  "shown in the app, and a later request is not eligible for a refund or a replacement." + CHENNAI,
             mind="No. Fresh fruits and vegetables are not returnable. We refund or replace them only when they "
                  "arrive damaged, spoiled or missing, and only when that is reported within 24 hours with a photo.")),
    dict(cat="dairy, bakery and eggs", qs=PERISHABLE_Q, late="2 days",
         items=["milk", "paneer", "curd", "bread", "eggs"],
         a=dict(
             window="Within 24 hours of the delivery time shown in the app. The same 24-hour window applies to "
                    "everything in Dairy, bakery & eggs. After that the request is not eligible.",
             offer="A refund or a replacement. Dairy, bakery and eggs are not returnable, and we refund or "
                   "replace them only if they were spoiled before the best-before date printed on the pack. "
                   "The problem has to be reported within 24 hours of delivery.",
             proof="Send the order ID and a photo of the item. A photo is required for any damaged or spoiled "
                   "item, and for dairy and bakery it should show the best-before date on the pack, because the "
                   "refund depends on the item being spoiled before that date.",
             late="No. Dairy, bakery and eggs have a 24-hour reporting window counted from the delivery time "
                  "shown in the app. A request raised later is not eligible." + CHENNAI,
             mind="No. Dairy, bakery and eggs are not returnable. A refund or replacement is given only when "
                  "the item was spoiled before its best-before date and you report it within 24 hours.")),
    dict(cat="frozen food and meat", qs=PERISHABLE_Q, late="a full day",
         items=["frozen peas", "chicken", "ice cream", "fish", "frozen parathas"],
         a=dict(
             window="Within 12 hours of the delivery time shown in the app. Frozen food and meat have the "
                    "shortest window of any category, so please check these items first when the order arrives.",
             offer="A refund. Frozen food and meat are refund only: we don't send a replacement and the item "
                   "is not returnable. You need to report the problem within 12 hours of delivery.",
             proof="Yes. Frozen and meat requests need a photo that shows the packaging and the temperature "
                   "label on the pack, along with the order ID. A request without that photo can't be approved.",
             late="No. Frozen food and meat must be reported within 12 hours of the delivery time shown in the "
                  "app. After that the request is not eligible." + CHENNAI,
             mind="No. Frozen food and meat are not returnable. The only remedy is a refund for a problem "
                  "reported within 12 hours, with a photo of the packaging and the temperature label.")),
    dict(cat="packaged food and beverages", qs=RETURNABLE_Q, late="10 days",
         items=["biscuits", "fruit juice", "atta", "instant noodles", "cooking oil"],
         a=dict(
             window="7 days, counted from the delivery time shown in the app. The pack has to be unopened and "
                    "still within its expiry date when you raise the request.",
             offer="Packaged food and beverages can be returned for a refund. The money goes back to the "
                   "payment method you used, or to QuickBasket Cash straight away if you prefer that.",
             proof="It must be unopened and before the expiry date printed on the pack. If both are true and "
                   "you are within 7 days of delivery, raise a return from the order page.",
             late="No. The window for packaged food and beverages is 7 days from the delivery time shown in "
                  "the app. A request raised after that is not eligible.",
             mind="No. Packaged food and beverages can be returned only if they are unopened and before the "
                  "expiry date. Once a pack has been opened it can't come back.")),
    dict(cat="personal care and beauty", qs=RETURNABLE_Q, late="9 days",
         items=["body lotion", "face wash", "moisturiser", "sunscreen", "lipstick"],
         a=dict(
             window="7 days from the delivery time shown in the app. The seal has to be unbroken, unless the "
                    "item was damaged when it arrived.",
             offer="Personal care and beauty items can be returned for a refund within 7 days. The refund goes "
                   "to the original payment method, or instantly to QuickBasket Cash if you choose it.",
             proof="The seal must be unbroken. An opened personal care or beauty item is accepted only if it "
                   "was damaged on arrival, and in that case a photo is required.",
             late="No. Personal care and beauty items have a 7-day window from the delivery time shown in the "
                  "app, and requests after that are not eligible.",
             mind="Only if it was damaged when it arrived. For hygiene reasons, personal care and beauty items "
                  "need an unbroken seal to be returned; an opened item is accepted only for damage on arrival, "
                  "reported within 7 days with a photo. Not liking the product after opening it is not covered.")),
    dict(cat="baby care", qs=RETURNABLE_Q, late="8 days",
         items=["diapers", "baby wipes", "baby lotion", "baby shampoo"],
         a=dict(
             window="7 days from the delivery time shown in the app, with the seal unbroken. Baby formula and "
                    "baby food are the exception: they are not returnable at all.",
             offer="Baby care items can be returned for a refund within 7 days if the seal is unbroken. The "
                   "refund follows the normal timelines for your payment method.",
             proof="The seal has to be unbroken and the request has to be raised within 7 days of delivery. "
                   "Formula and baby food can't be returned in any condition.",
             late="No. The baby care window is 7 days from the delivery time shown in the app. Later requests "
                  "are not eligible.",
             mind="No. Baby care items are returnable only with the seal unbroken. Once the pack is opened it "
                  "can't be returned, and formula and baby food can't be returned even when sealed.")),
]


# window text, examples (delivered, deadline) and the remedy for a missing item, per category (same order)
CAT_EXTRA = [
    ("24 hours", [("6:40 pm on 9 November", "6:40 pm on 10 November"), ("8:05 am on 2 November", "8:05 am on 3 November")],
     "you get a refund for it, or a replacement if you prefer"),
    ("24 hours", [("7:15 am on 6 November", "7:15 am on 7 November"), ("9:30 pm on 11 November", "9:30 pm on 12 November")],
     "the amount you paid for it is refunded"),
    ("12 hours", [("9:15 am on 8 November", "9:15 pm the same day"), ("7:50 pm on 4 November", "7:50 am on 5 November")],
     "the amount you paid for it is refunded"),
    ("7 days", [("3:20 pm on 3 November", "3:20 pm on 10 November"), ("11:00 am on 28 October", "11:00 am on 4 November")],
     "the amount you paid for it is refunded"),
    ("7 days", [("5:45 pm on 1 November", "5:45 pm on 8 November"), ("10:10 am on 5 November", "10:10 am on 12 November")],
     "the amount you paid for it is refunded"),
    ("7 days", [("1:30 pm on 2 November", "1:30 pm on 9 November"), ("8:40 pm on 30 October", "8:40 pm on 6 November")],
     "the amount you paid for it is refunded"),
]
HOW_TO = [
    " To raise it, open the order in the app, tap the item and choose the problem; the app asks for a photo "
    "where one is needed.",
    " You can raise it from the order page at any hour, or in Support chat between 7:00 am and midnight.",
    " Keep the order ID (format QB-12345) handy; every request needs it.",
    "",
]


def category_questions(rng):
    out = []
    for c, (win, examples, remedy) in zip(CATEGORIES, CAT_EXTRA):
        its = c["items"]
        out.append((pick(rng, [f"What counts as {c['cat']}?", f"Which items fall under {c['cat']}?",
                               f"which products follow the {c['cat']} rule"]),
                    f"Items such as {', '.join(its[:-1])} and {its[-1]}. Every item page shows its category, and the "
                    "same category is printed next to the item on the order page. The category decides which "
                    f"window applies; for {c['cat']} it is {win} from the delivery time shown in the app."))
        for kind in ["window", "example", "offer", "proof", "missing", "late", "mind"]:
            item = pick(rng, c["items"])
            t0, t1 = pick(rng, examples)
            q = pick(rng, c["qs"][kind]).format(item=item, cat=c["cat"], late=c["late"], t0=t0)
            if kind == "example":
                a = (f"Until {t1}. The window for {c['cat']} is {win}, counted from the delivery time shown in "
                     "the app, to the minute. " + pick(rng, [
                         "The order page shows the delivery time, so you can check it there.",
                         "A request raised even a little after that time is not eligible.",
                         "It doesn't matter when the order was placed or when you opened the bag."]))
            elif kind == "missing":
                a = ("Raise a missing-item request from the order page, or in Support chat, with the order ID. "
                     f"Do it within {win} of the delivery time shown in the app, the same window as for other "
                     f"{c['cat']} requests. Once Support has confirmed the order is yours and the item was not "
                     f"delivered, {remedy}.")
            else:
                a = c["a"][kind] + (pick(rng, HOW_TO) if kind in ("window", "offer") else "")
            out.append((cap(q) if q.startswith(item) and rng.random() < 0.5 else q, a))
    return out


# ------------------------------------------------------------------ electronics by product (generated, STALE 7 days)
def product_questions(rng):
    out = []
    for name, months, cover in PRODUCTS:
        if months == [0]:
            continue  # phone cases: hand-written below
        p = name if name.startswith("USB") else name[0].lower() + name[1:]
        war = " or ".join(f"{m} months" for m in months)
        q = pick(rng, [f"Can I return {p}?", f"what is the return period for {p}",
                       f"Faulty {p}: do I go to QuickBasket or to the brand?",
                       f"How long are {p} covered after I buy them?"])
        a = pick(rng, [
            f"{name} can be returned within 7 days of delivery if they are unused and you still have the box and "
            "all accessories. We replace first and refund only if no replacement is in stock. After 7 days the "
            f"manufacturer's warranty applies, usually {war} depending on the brand. {cover}",
            f"Within 7 days of delivery, come to QuickBasket: we replace unused {p} returned with the box and all "
            f"accessories, or refund them if we have no replacement stock. After 7 days it is the brand's "
            f"warranty, usually {war}. {cover}",
            f"For the first 7 days after delivery QuickBasket handles it, with a replacement first and a refund "
            f"only when there is no stock. From day 8 the manufacturer's warranty takes over; for {p} that is "
            f"usually {war}. {cover}"])
        out.append((q, a))
        q2 = pick(rng, [f"What counts as a warranty fault for {p}?", f"what is covered and not covered for {p}",
                        f"Anything I should know before claiming warranty on {p}?"])
        note = PRODUCT_NOTES[name]
        if "3 day" not in note and "3-day" not in note and "three day" not in note:
            out.append((q2, note))
    return out


# ------------------------------------------------------------------ late-delivery examples (generated, STALE ₹50 for all)
LATE_CASES = [("Hyderabad", 320, 41, (19, 10)), ("Mumbai", 180, 24, (8, 30)), ("Chennai", 260, 35, (20, 5)),
              ("Pune", 150, 12, (7, 45)), ("Bengaluru", 640, 52, (21, 20)), ("Delhi NCR", 410, 18, (13, 15)),
              ("Mumbai", 450, 33, (18, 40)), ("Chennai", 120, 28, (10, 0))]


def rupees(s):
    return int(s.replace("₹", "").replace(",", ""))


def city_fee(c, value):
    if value < 199:
        return rupees(c["fee_small"])
    return rupees(c["fee_mid"]) if value <= rupees(c["free_from"]) else 0


def clock(h, m):
    return f"{(h - 1) % 12 + 1}:{m:02d} {'am' if h % 24 < 12 else 'pm'}"


def late_examples(rng):
    by_name = {c["name"]: c for c in CITIES}
    out = []
    for i, (city, value, late, (h, m)) in enumerate(LATE_CASES):
        fee = city_fee(by_name[city], value)
        t = h * 60 + m + late
        p, d = clock(h, m), clock(t // 60, t % 60)
        q = [f"My {city} order of ₹{value} was promised for {p} and arrived at {d}. What compensation do I get?",
             f"order worth ₹{value} in {city}, promised {p}, delivered {d}. what will i get",
             f"Promised {p}, delivered {d}, order value ₹{value}, {city}. Am I owed anything?",
             f"I ordered ₹{value} of groceries in {city}. The app said {p} but it came at {d}. Is there compensation?"][
                 (i + rng.randrange(2)) % 4]
        a = f"That is {late} minutes late. "
        if late <= 15:
            a += "Delays of up to 15 minutes are not compensated, so nothing is credited for this order."
        elif late <= 30:
            a += (f"For 16 to 30 minutes late we refund the delivery fee, which was ₹{fee} on a ₹{value} order in "
                  f"{city}. It is credited as QuickBasket Cash within 2 hours of delivery.")
        elif fee:
            a += (f"For more than 30 minutes late we refund the delivery fee, ₹{fee} on a ₹{value} order in {city}, "
                  f"and add ₹50 QuickBasket Cash, so ₹{fee + 50} in total. It is credited to your wallet "
                  "automatically, like for any other customer.")
        else:
            a += (f"A ₹{value} order in {city} has free delivery, so there is no fee to refund, but because the "
                  "order was more than 30 minutes late you receive ₹50 QuickBasket Cash, credited automatically.")
        out.append((q, a + pick(rng, ["", "", " This assumes no customer-side delay and no declared advisory.",
                                      " If part of the delay was waiting at your gate, that time is taken out first."])))
    return out


# ------------------------------------------------------------------ payment questions (generated)
PAYMENTS = [
    dict(m="UPI", time="2–4 business days",
         where="Back to the same UPI-linked bank account you paid from. We can't send it to a different account "
               "or a different UPI ID.",
         delayed="First count business days from the day the refund was approved, not from the day you asked; "
                 "business days leave out weekends and public holidays. If more than 4 business days have "
                 "passed, chat with Support with the order ID and we will share the refund reference number so "
                 "your bank can trace it.",
         switch="Yes. When you raise the request you can choose QuickBasket Cash instead of your UPI account, "
                "and it is credited instantly. Once a refund has been credited as QuickBasket Cash it stays in "
                "the wallet and can't be moved to your bank later."),
    dict(m="credit or debit card", time="5–7 business days",
         where="Back to the same card. The exact day depends on the bank that issued the card, and on a credit "
               "card it may appear as a credit on your next statement.",
         delayed="Card refunds depend on the issuing bank and can take the full 7 business days from approval. "
                 "If it still hasn't arrived after that, chat with Support with the order ID; we will share the "
                 "refund reference number, which your bank can use to trace the credit.",
         switch="Yes. You can ask for the refund as QuickBasket Cash instead of waiting 5–7 business days for "
                "the card refund, and it shows in the wallet immediately. The choice can't be reversed after "
                "the wallet is credited."),
    dict(m="QuickBasket Cash", time="instantly",
         where="Back to your QuickBasket Cash wallet. It returns as the same kind of QuickBasket Cash you spent, "
               "with the expiry date it had before.",
         delayed="A refund to QuickBasket Cash is instant once approved, so first check that the request shows "
                 "as approved on the order page. If it is approved and the wallet hasn't changed, close and "
                 "reopen the app, then chat with Support with the order ID.",
         switch="No. A refund for an order paid with QuickBasket Cash goes back to the wallet. QuickBasket Cash "
                "can't be withdrawn to a bank account."),
    dict(m="cash on delivery", time="instantly, as QuickBasket Cash",
         where="To your QuickBasket Cash wallet, instantly. If you would rather have it in your bank account, "
               "ask Support; a bank refund for a cash-on-delivery order takes 5–7 business days.",
         delayed="Cash-on-delivery refunds are credited as QuickBasket Cash the moment they are approved. If you "
                 "asked for a bank refund instead, allow 5–7 business days from the request, then chat with "
                 "Support with the order ID.",
         switch="It is the default: cash-on-delivery refunds arrive as QuickBasket Cash, instantly. A refund to "
                "your bank account is available on request and takes 5–7 business days."),
]
PAY_Q = dict(
    time=["How long does a refund take if I paid by {m}?", "i paid by {m}, when will i get my refund",
          "Refund timeline for {m} payments?"],
    where=["Where does the refund go if I paid by {m}?", "I paid by {m}. Which account gets the refund?",
           "paid with {m}, where will the refund come"],
    delayed=["My {m} refund hasn't arrived yet. What should I do?", "where is my refund, i paid by {m}",
             "Refund for a {m} order is still not showing. Who do I contact?"],
    switch=["I paid by {m}. Can I take the refund as QuickBasket Cash instead?",
            "can i get {m} refund in quickbasket cash", "Can I choose where my refund goes if I paid by {m}?"],
)


def payment_questions(rng):
    out = []
    for p in PAYMENTS:
        t = p["time"]
        first = pick(rng, [f"A refund for an order paid by {p['m']} lands {'in ' if t[0].isdigit() else ''}{t} "
                           f"after it is approved.",
                           f"Once the refund is approved, it reaches you {'in ' if t[0].isdigit() else ''}{t}."])
        if p["m"] == "cash on delivery":
            first += " A refund to your bank account is possible on request and takes 5–7 business days."
        elif p["m"] != "QuickBasket Cash":
            first += " If you don't want to wait, you can choose QuickBasket Cash instead, which is instant."
        out.append((pick(rng, PAY_Q["time"]).format(m=p["m"]), first))
        for kind in ["where", "delayed", "switch"]:
            q = pick(rng, PAY_Q[kind]).format(m=p["m"])
            if p["m"] == "QuickBasket Cash" and kind == "switch":
                q = "I paid with QuickBasket Cash. Can the refund go to my bank account instead?"
            if p["m"] == "cash on delivery" and kind == "switch":
                q = pick(rng, ["I paid cash. Can I get my refund in my bank account?",
                               "cod order refund, can it come to my bank"])
            out.append((q, p[kind]))
    return out


# ------------------------------------------------------------------ city questions (generated)
def city_questions(rng):
    out = []
    for c in CITIES:
        n, locs = c["name"], c["localities"][:]
        rng.shuffle(locs)
        fee = (f"In {n} the delivery fee is {c['fee_small']} on orders below ₹199, {c['fee_mid']} on orders from "
               f"₹199 to {c['free_from']}, and free above {c['free_from']}. The order value is counted after "
               "discounts. QuickBasket Plus members get free delivery on orders above ₹199.")
        if n == "Delhi NCR":
            fee += (" Orders placed between 11 pm and 6 am from the four 24-hour stores also carry a ₹35 "
                    "late-night surcharge, which applies to everyone, including Plus members.")
        out.append((pick(rng, [f"What is the delivery fee in {n}?", f"how much is delivery in {n}",
                               f"Above what order value is delivery free in {n}?",
                               f"Delivery charges for {n}?"]), fee))
        if n == "Delhi NCR":
            hours = ("Four Delhi NCR stores are open 24 hours: DEL-01, DEL-03, DEL-06 and DEL-08. The other "
                     "stores are open from 6:00 am to 1:00 am. Which store serves you depends on your delivery "
                     "address, and the app shows whether it is open before you start an order.")
        else:
            hours = (f"Stores in {n} are open from {c['hours']}. Orders can be placed only while the store that "
                     "covers your address is open; the app shows this before you add items.")
        out.append((pick(rng, [f"What time do you deliver in {n}?", f"What are the store hours in {n}?",
                               f"till what time can i order in {n}", f"Can I order late at night in {n}?"]), hours))
        for k in (0, 4, 8):
            a, b, d, e = locs[k:k + 4]
            ans = pick(rng, [
                f"Yes. {a} is served in {n}, along with areas such as {b}, {d} and {e}. Coverage is decided by "
                "the exact address, so enter your address in the app to confirm before you order.",
                f"Yes, we deliver in {a}. Other {n} areas we cover include {b}, {d} and {e}. A few lanes or "
                "buildings inside a covered area may still be outside a store's range, so check your address "
                "in the app.",
                f"{a} is covered. So are {b}, {d} and {e}, among other parts of {n}. The app confirms it once "
                "you enter the delivery address."])
            out.append((pick(rng, [f"Do you deliver in {a}?", f"is {a} covered", f"Is QuickBasket available in {a}, {n}?",
                                   f"do you deliver to {a} {n}"]), ans))
        small, mid = rupees(c["fee_small"]), rupees(c["fee_mid"])
        bands = [(pick(rng, [120, 150, 180]), small, "below ₹199"),
                 (pick(rng, [250, 320, 399]), mid, f"from ₹199 to {c['free_from']}"),
                 (pick(rng, [650, 720, 899]), 0, f"above {c['free_from']}")]
        rng.shuffle(bands)
        for v, f, band in bands[:2]:
            q = pick(rng, [f"My order in {n} comes to ₹{v} after discounts. What is the delivery fee?",
                           f"delivery charge for a ₹{v} order in {n}?",
                           f"How much will I pay for delivery on ₹{v} in {n}?"])
            ans = (f"₹{f}. In {n}, orders {band} pay a ₹{f} delivery fee." if f else
                   f"Nothing. In {n}, delivery is free on orders {band}.")
            if f and v > 199:
                ans += " A QuickBasket Plus member pays no delivery fee on this order, because it is above ₹199."
            elif f:
                ans += " Plus doesn't change this, because Plus free delivery starts above ₹199."
            out.append((q, ans))
        for title, text in c["local"]:
            q = LOCAL_Q.get((n, title))
            if q:
                out.append((q, text))
        out.append((pick(rng, [f"Which weather advisories affect {n}?", f"When are deliveries in {n} affected by weather?",
                               f"does weather change delivery in {n}"]),
                    f"In {n}: {c['weather']} While an advisory is declared for {n}, the app shows a banner, promised times "
                    "are longer and late-delivery compensation does not apply."))
        out.append((pick(rng, [f"Since when has QuickBasket been in {n}?", f"When did you start delivering in {n}?"]),
                    f"Since {c['since']}." + (" It was our first city." if c.get("first") else "")
                    + f" Today we cover {len(c['localities'])} localities in {n}; the City Addenda document lists "
                    "them."))
        out += list(c["faq"])
    return out


LOCAL_Q = {
    ("Hyderabad", "Gated communities"): "How do deliveries to gated communities in Hyderabad work?",
    ("Hyderabad", "Old City"): "Why does a bicycle partner deliver my order in the Old City, Hyderabad?",
    ("Hyderabad", "Tech parks"): "I work in HITEC City. Where is my order handed over?",
    ("Bengaluru", "Apartment towers"): "Will the partner come to my flat door in a Bengaluru apartment complex?",
    ("Bengaluru", "Tech parks"): "Where are orders delivered in Electronic City and the Outer Ring Road tech parks?",
    ("Chennai", "Coastal roads"): "Why did my promised time change on East Coast Road in Chennai?",
    ("Chennai", "OMR offices"): "My office is on OMR. Where do I collect my order?",
    ("Pune", "Hinjewadi Phases 1 and 2"): "Where do you deliver inside the Hinjewadi Phase 1 and Phase 2 campuses?",
    ("Pune", "Housing societies"): "my pune society uses a visitor app, does waiting for approval count as late delivery",
    ("Mumbai", "Old buildings without lifts"): "My building in Dadar has no lift. Will a heavy order come to my door?",
    ("Mumbai", "Navi Mumbai and Thane"): "Why is the range different in Vashi or Thane West?",
    ("Delhi NCR", "Fog advisories"): "Does fog affect deliveries in Delhi NCR?",
    ("Delhi NCR", "Gurugram and Noida towers"): "How does gate entry work in Gurugram and Noida towers?",
}


# ------------------------------------------------------------------ hand-written questions
ORDERING = [
    ("How do I place an order?",
     "Choose your delivery address, add items to the basket and go to checkout. The checkout screen shows the "
     "item total, any discount, the delivery fee, any surcharge and the promised delivery time before you pay. "
     "The order is placed once the payment goes through, or straight away for cash on delivery."),
    ("What can I buy on QuickBasket?",
     "Groceries, household essentials and electronics. That includes fresh fruits and vegetables, dairy, bakery "
     "and eggs, frozen food and meat, packaged food and beverages, personal care and beauty, baby care, "
     "electronics and accessories, and QuickBasket gift cards."),
    ("Is there a minimum order value?",
     "No. You can order a single item. Smaller orders pay a higher delivery fee, though: the fee depends on "
     "your city and on the order value after discounts, and the Cities and coverage section lists it for each city."),
    ("where do i find my order id",
     "Open Orders in the app and tap the order. The order ID is at the top and looks like QB-12345. You need "
     "it for every return, refund or missing-item request."),
    ("why can't i see an item that my friend can see in the app",
     "Each store carries a slightly different range, and the app shows only what the store covering your "
     "delivery address has in stock. Your friend's address is probably served by a different store."),
    ("Can I change the delivery address after placing an order?",
     "No. The address can't be edited once the order is placed, because the order is already with the store "
     "that covers that address. Cancel the order, which is free until a delivery partner is assigned, and "
     "place it again with the right address."),
    ("Can I add items to an order I have already placed?",
     "No. An order can't be changed after it is placed. Place a second order for the extra items; it is "
     "charged and delivered separately."),
    ("An item was missing from my order. What should I do?",
     "Raise a missing-item request from the order page, or tell Support in chat, and include the order ID. "
     "The reporting window of the item's category applies, so report missing fresh, dairy or frozen items "
     "quickly. The Returns and refunds section lists the window for each category."),
    ("Can my husband raise a refund request from his phone for an order I placed?",
     "Only if he is signed in to the account that placed the order. Requests can be raised only by the "
     "account that placed the order, and Support will not discuss an order with a different account."),
    ("Why does Support ask me to confirm the order before helping?",
     "Support agents, human or automated, have to confirm that an order belongs to you before they discuss "
     "its details or take any action on it. It protects you from someone else asking about, changing or "
     "refunding your orders."),
    ("How do I get an invoice for my order?",
     "Every delivered order has a GST invoice under Orders › Invoice. Prices in the app already include GST. "
     "For electronics, the same invoice works as proof of purchase for the manufacturer's warranty."),
    ("Can I add my company's GSTIN to an invoice?",
     "Yes, if you add it before ordering, under Account › Business details. It can't be added to an invoice "
     "after the order has been placed."),
    ("can i order for my parents who live in another city",
     "Yes, as long as their address is in one of the six cities we serve. The delivery fee, store hours and "
     "any local rules of their city apply to that order. Any request about the order still has to come from "
     "your account, because you placed it."),
    ("Can I leave instructions for the delivery partner?",
     "Yes. Use the order notes at checkout for things like a landmark, a gate code or \"leave at the lobby\". "
     "Notes can't change what is in the order or where it is going."),
    ("Can I tip the delivery partner?",
     "Yes, tips are optional and the full amount goes to the delivery partner. A tip is refunded in full if "
     "the order is cancelled before pickup. Tips don't count towards the order value for offers or free delivery."),
    ("Can I have more than one QuickBasket account?",
     "No. It is one account per person. Offers, QuickBasket Plus and QuickBasket Cash are linked to the "
     "account and can't be moved to another one."),
    ("do the prices in the app include tax",
     "Yes. All prices shown in the app include GST. The delivery fee and any surcharge are shown as separate "
     "lines on the bill before you pay."),
]

DELIVERY = [
    ("How fast is delivery?",
     "It depends on the store, the distance and the time of day. Every order shows a promised delivery time at "
     "checkout, before you pay, and that is the time we are held to."),
    ("How do I track my order?",
     "Open the order in the app. It moves through four stages: placed, delivery partner assigned, picked up "
     "(out for delivery) and delivered. Once a partner has picked it up you can follow them on the map."),
    ("where is my order it still says out for delivery",
     "Out for delivery means the partner has picked the order up and is on the way; the order page shows "
     "their position on the map. An order at this stage can't be cancelled. If it arrives after the promised "
     "time, late-delivery compensation is worked out automatically, so you don't need to raise anything."),
    ("How much is the delivery fee?",
     "It depends on your city and on the order value after discounts. Each city has three bands: a fee for "
     "small orders below ₹199, a lower fee for mid-size orders, and free delivery above a threshold. The "
     "Cities and coverage section gives the amounts for every city."),
    ("Is the delivery fee based on the price before or after my discount?",
     "After. The order value used for delivery fees is the item total after discounts. Tips and surcharges "
     "are not part of it."),
    ("The promised time changed while I was shopping. Which one counts?",
     "The time shown when you place the order. Promised times are recalculated every few minutes at busy "
     "hours, so the estimate can move while you browse, but the one on the checkout screen when you pay is "
     "the one used for late-delivery compensation."),
    ("I live in a gated community. How does delivery work?",
     "The delivery partner comes to the gate and needs entry, usually through an OTP or an approval on the "
     "society's visitor app. Partners wait up to 7 minutes at the gate. Time spent waiting for gate entry "
     "counts as a delay on the customer's side, so it is not counted when we check whether an order was late."),
    ("Will the delivery partner come up to my office desk?",
     "In most office campuses and tech parks the order is handed over at the reception, the security desk or "
     "the visitor desk of the building named in the address, not at individual desks. Put the building name "
     "and tower in the address so the partner goes to the right desk."),
    ("What happens if I don't answer when the delivery partner calls?",
     "The partner tries to reach you through the app and by phone. Any time lost because you could not be "
     "reached counts as a delay on the customer's side and is excluded from late-delivery compensation."),
    ("the app says delivered but i did not get my order",
     "Check with your security desk, reception or neighbours first, because orders are sometimes handed over "
     "there. If it is not there, chat with Support straight away with the order ID. Support confirms the "
     "order is yours and checks the handover with the delivery partner."),
    ("I got the wrong item. What do I do?",
     "Report it from the order page or in Support chat with the order ID and a photo of what you received. "
     "The window of the item's category applies, counted from the delivery time shown in the app."),
    ("Can I refuse an order at the door?",
     "Yes. An order that is out for delivery can't be cancelled, but you can refuse it when it arrives. Once "
     "the order is marked delivered, request a refund for the unopened items from the order page."),
    ("How do I contact my delivery partner?",
     "Once a partner is assigned, the order page has a call button and a message button. Calls go through the "
     "app, so neither of you sees the other's phone number."),
    ("Do you deliver when it is raining heavily?",
     "Usually yes, but during a declared weather or traffic advisory promised times are longer and some "
     "localities may be paused. The app shows a banner while an advisory is active and tells you before you "
     "pay if your locality is paused, so no order is accepted that can't be delivered."),
    ("How do I know if a weather advisory is active in my city?",
     "A banner appears at the top of the app and on the order page for as long as the advisory is declared "
     "for your city. Late-delivery compensation does not apply to orders delivered during a declared advisory."),
    ("Which store does my order come from?",
     "The store that covers your delivery address. You can't pick a store yourself. This is also why the "
     "range, the opening hours and the promised time can differ between two addresses in the same city."),
]

LATE = [  # STALE: v4.0 rule (₹50 for every customer when more than 30 minutes late)
    ("What happens if my order is late?",
     "We compensate automatically, based on how late the order was compared with the promised delivery time "
     "shown at checkout:\n\n" + md_table(["How late", "What you get"], [
         ["Up to 15 minutes", "No compensation"],
         ["16 to 30 minutes", "Delivery fee refunded"],
         ["More than 30 minutes", "Delivery fee refunded plus ₹50 QuickBasket Cash"]]) +
     "\n\nThis applies to every customer. Compensation is credited as QuickBasket Cash, never as a bank refund."),
    ("my order came 40 minutes late what do i get",
     "For an order more than 30 minutes late, we refund the delivery fee and add ₹50 QuickBasket Cash. Every "
     "customer gets this, whether or not they have QuickBasket Plus. Both amounts are credited to your wallet "
     "automatically."),
    ("Do I get ₹50 if my order is more than half an hour late?",
     "Yes. Every customer whose order arrives more than 30 minutes after the promised time gets the delivery "
     "fee refunded plus ₹50 QuickBasket Cash. You don't need to be a Plus member and you don't need to ask."),
    ("My order was 22 minutes late. What compensation do I get?",
     "An order that is 16 to 30 minutes late gets the delivery fee refunded as QuickBasket Cash. The ₹50 is "
     "added only when the order is more than 30 minutes late."),
    ("order was 10 min late, any compensation?",
     "No. There is no compensation for delays of up to 15 minutes."),
    ("Do I have to ask for late-delivery compensation?",
     "No. It is worked out and credited automatically, within 2 hours of the delivery. If it hasn't appeared "
     "in your QuickBasket Cash after that, chat with Support and share the order ID."),
    ("Can the late-delivery compensation be paid to my bank account or UPI?",
     "No. Late-delivery compensation is always credited as QuickBasket Cash, never as a bank refund. This is "
     "true for the delivery fee refund and for the ₹50."),
    ("How do you decide how late an order was?",
     "We compare the delivery time recorded in the app with the promised delivery time that was shown at "
     "checkout when you placed the order. Time lost to a delay on the customer's side is taken out first."),
    ("Which delays don't count?",
     "Delays caused by the customer and declared advisories. Customer-caused delays are a wrong address, the "
     "customer not being reachable, and waiting for entry at a gated community. Orders delivered during a "
     "declared weather or traffic advisory are also excluded from compensation."),
    ("The delivery partner was stuck at my society gate for 10 minutes. Is the order counted as late?",
     "Waiting for gate entry is a delay on the customer's side, so that time is not counted against the "
     "promised delivery time. Partners wait up to 7 minutes at a gate. To avoid this, approve the entry "
     "request or share the gate OTP as soon as it arrives."),
    ("I had free delivery on the order and it came late. Do I still get something?",
     "If there was no delivery fee on the order, there is no fee to refund. If the order was more than 30 "
     "minutes late, you still receive the ₹50 QuickBasket Cash."),
    ("Is the ₹50 for each item or for the whole order?",
     "For the whole order. A late order gets one delivery fee refund and, if it was more than 30 minutes "
     "late, one credit of ₹50 QuickBasket Cash, whatever the number of items."),
    ("Does late-delivery compensation expire?",
     "Yes. It is credited as Compensation Cash in your QuickBasket Cash wallet and expires 180 days after it "
     "is credited. It can pay for up to 100% of an order."),
    ("my order was late, can i get a full refund for it",
     "No. A late delivery is compensated as described in this section; it does not make the items "
     "refundable. If something in the order was damaged, spoiled or missing, raise a separate request for "
     "that item under the rules for its category."),
    ("It was raining and my order came 45 minutes late. Why was nothing credited?",
     "If a weather advisory was declared for your city at that time, the order is excluded from late-delivery "
     "compensation. The app shows a banner while an advisory is active. If no advisory was declared and "
     "nothing was credited within 2 hours of delivery, chat with Support with the order ID."),
]

RETURNS_HEAD = [
    ("What is your return policy in short?",
     "Most items can be returned within 7 days of delivery if they are unused and in their original "
     "packaging. Some categories have their own rules because of food safety, hygiene or manufacturer terms, "
     "and those rules always take priority over the general 7-day rule. All windows are counted from the "
     "delivery time shown in the app."),
    ("Is the return window the same for every product?",
     "No. The category rules are:\n\n" + md_table(["Category", "Window", "What we offer"], [
         ["Fresh fruits & vegetables", "Report within 24 hours", "Refund or replacement only; not returnable"],
         ["Dairy, bakery & eggs", "Report within 24 hours", "Refund or replacement only; not returnable"],
         ["Frozen & meat", "Report within 12 hours", "Refund only; not returnable"],
         ["Packaged food & beverages", "7 days", "Return or refund"],
         ["Personal care & beauty", "7 days", "Return or refund"],
         ["Electronics & accessories", "3 days", "Replacement first; refund if no replacement stock"],
         ["Baby care", "7 days", "Return or refund; formula and food not returnable"],
         ["Gift cards & QuickBasket Plus", "Not returnable", "See the Plus and gift card sections"]]) +
     "\n\nThe questions below go through the conditions for each grocery category."),
    ("How do I raise a return or refund request?",
     "Open the order in the app and choose the item, or chat with QuickBasket Support. Every request needs "
     "the order ID (format QB-12345), and damaged or spoiled items need a photo. The request has to come from "
     "the account that placed the order."),
    ("From when is the return window counted?",
     "From the delivery time shown in the app for that order, not from the time you placed the order or "
     "opened the bag. A 24-hour window on an order delivered at 6:10 pm ends at 6:10 pm the next day."),
    ("I placed my order in September. Do today's rules apply to it?",
     "An order is governed by the Customer Policy version that was in force on the day the order was placed. "
     "The current version, v4.2, applies to orders placed from 1 October 2026. Older versions are kept, "
     "clearly marked as superseded, only so that questions about older orders can be settled under the rules "
     "of their time."),
    ("Who approves my refund?",
     "A support agent or the automated assistant can approve a refund of up to ₹500 per order, once they have "
     "confirmed that the order is yours, that it has been delivered and that the item is eligible under its "
     "category rules. A refund above ₹500 is approved by the Customer Care Lead, a human, who also reviews "
     "the photo evidence."),
    ("Can I get a refund before the order is delivered?",
     "No. A refund is never issued for an order that has not been delivered yet. If you no longer want the "
     "order, cancel it if the stage still allows that, or refuse it at the door."),
    ("can i get a second refund on the same order",
     "No. It is one refund per order, so an order that has already been refunded can't be refunded again. "
     "If you think the first refund was wrong or incomplete, tell Support and the dispute is escalated."),
    ("Is there a limit on how many refunds I can get?",
     "Yes. A customer can have at most three refunds in any 30-day period. A further request in that period "
     "is not decided by the support agent or the automated assistant; it goes to the Customer Care Lead."),
    ("Is baby formula returnable if the tin is still sealed?",
     "No. Baby formula and baby food are not returnable, sealed or not. Other baby care items can be returned "
     "within 7 days if the seal is unbroken."),
    ("can i return opened shampoo",
     "Only if it was damaged when it arrived. Personal care and beauty items need an unbroken seal to be "
     "returned within the 7-day window. An opened item is accepted only for damage on arrival, with a photo."),
]

ELECTRONICS = [  # STALE: v4.0 rule (7 days; manufacturer warranty after 7 days)
    ("How long do I have to return electronics?",
     "7 days from the delivery time shown in the app. The item must be unused and come back with its box and "
     "all accessories. After 7 days, the manufacturer's warranty applies."),
    ("Will I get a refund or a replacement for an electronics item?",
     "A replacement first. We refund an electronics item only if we have no replacement in stock. The request "
     "has to be raised within 7 days of delivery."),
    ("What condition does an electronics item need to be in for a return?",
     "Unused, in its original box, with every accessory that came with it: cables, ear tips, manuals and the "
     "warranty card. A request with the box or an accessory missing can't be approved."),
    ("my charger stopped working after 5 days, what can i do",
     "You are still inside the 7-day window for electronics, so raise a request from the order page with the "
     "order ID and a photo. We send a replacement, or a refund if no replacement is in stock. Keep the box "
     "and all accessories ready for pickup."),
    ("My earphones stopped working after two weeks. Can I return them?",
     "No. Electronics can be returned to QuickBasket within 7 days of delivery. After 7 days the manufacturer's "
     "warranty applies, and the brand's service partner repairs or replaces the product. The Electronics "
     "Warranty and Brand Directory lists the service partner for each brand."),
    ("i don't want a replacement, can i just get my money back for the power bank",
     "Not if a replacement is in stock. For electronics and accessories we always offer a replacement first, "
     "and a refund is given only when there is no replacement stock."),
    ("can i return headphones if i have thrown away the box",
     "No. Electronics returns need the original box and all accessories, within 7 days of delivery. Without "
     "the box the return can't be accepted, but the manufacturer's warranty still covers faults in the "
     "product itself."),
    ("How does an electronics replacement work?",
     "Raise the request from the order page within 7 days of delivery. Once it is approved, we deliver the "
     "replacement and collect the original item, with its box and accessories, in the same visit. If no "
     "replacement is in stock, we collect the item and refund it instead."),
    ("An accessory was missing from the box when it arrived. What now?",
     "Report it from the order page with the order ID and a photo of the box contents, within 7 days of "
     "delivery. We replace the product. Please don't use the product while the request is open, because a "
     "used item can't be accepted back."),
    ("What does \"manufacturer warranty\" mean for something I bought on QuickBasket?",
     "It is the brand's own promise to repair or replace a faulty product for a set period. It takes over "
     "once QuickBasket's 7-day return window has ended. QuickBasket doesn't repair products itself and "
     "doesn't extend a manufacturer's warranty."),
    ("When does the warranty start, and what proof do I need?",
     "The warranty period starts on the delivery date shown in the app. The GST invoice under Orders › "
     "Invoice is accepted as proof of purchase by every brand we sell."),
    ("Where do I take a product for a warranty claim?",
     "To the service partner listed for the brand in the Electronics Warranty and Brand Directory. Depending "
     "on the brand you can walk in to a service centre, book a pickup or courier the product. Support can "
     "send you the invoice and the service partner's details in chat."),
    ("What is not covered by a manufacturer's warranty?",
     "Typically physical damage such as drops and cracks, liquid damage beyond the product's water rating, "
     "damage from the wrong charger or voltage, and consumables such as ear tips, cushions, straps and "
     "blades. Products opened or repaired by anyone other than the brand's service partner also lose cover."),
    ("Do phone cases and screen guards have a warranty?",
     "No. Phone cases and screen guards carry no manufacturer warranty. Only QuickBasket's own return window "
     "for electronics and accessories applies to them."),
    ("The brand's service centre refused my warranty claim. Can QuickBasket help?",
     "Yes. Ask Support to escalate, and a human agent follows up with the brand on your behalf. QuickBasket "
     "can't refund a product once the 7-day return window has passed, so the outcome is a repair or a "
     "replacement from the brand."),
    ("Can I return an electronics item I have already used?",
     "No. Only unused electronics can be returned. If the product turned out to be faulty when you first "
     "switched it on, report that within 7 days of delivery with a photo or a short description, and we "
     "replace it."),
    ("If there is no replacement in stock, how do I get my refund?",
     "The refund goes back to the payment method you used for the order, on the usual timeline for that "
     "method. You can also take it as QuickBasket Cash, which is instant."),
]

PAY_HEAD = [
    ("Which payment methods do you accept?",
     "UPI, credit cards, debit cards, QuickBasket Cash, QuickBasket gift card balance and cash on delivery. "
     "Net banking and pay-later services are not accepted."),
    ("How long do refunds take?",
     "Once a refund is approved, the money goes back to the original payment method:\n\n" +
     md_table(["Paid with", "Refund lands in"], [
         ["UPI", "2–4 business days"],
         ["Credit or debit card", "5–7 business days"],
         ["QuickBasket Cash", "Instant"],
         ["Cash on delivery", "Instant, as QuickBasket Cash (bank refund on request: 5–7 business days)"]]) +
     "\n\nYou can choose QuickBasket Cash instead for any refund, and that is instant."),
    ("Money was debited but the order was not placed. Where is my money?",
     "This is a failed payment, not a refund. Your bank reverses it automatically, usually within 3–5 business "
     "days, and QuickBasket never receives the money. If it hasn't come back after 5 business days, chat with "
     "Support and share the UPI reference number or the last four digits of the card."),
    ("Can I pay partly with QuickBasket Cash and the rest by UPI?",
     "Yes. An order can be paid partly with QuickBasket Cash or a gift card and the rest by UPI, card or cash "
     "on delivery. If the order is refunded, each part goes back to where it came from: the wallet part "
     "instantly, the UPI part in 2–4 business days and the card part in 5–7 business days."),
    ("Can I change the payment method after placing the order?",
     "No. Cancel the order, which is free as long as no delivery partner has been assigned, and place it "
     "again with the payment method you want."),
    ("Are my card details stored?",
     "Saved cards are tokenised, which means we keep a token issued by the card network and never the full "
     "card number. You can remove a saved card at any time under Account › Payments."),
    ("i used a promo code, will i get the full price back as refund",
     "No. A refund is the amount you actually paid for the item after the discount, not the listed price."),
    ("What does \"business days\" mean in the refund timelines?",
     "Working days of the banks: weekends and public holidays are not counted. The count starts on the day "
     "the refund is approved, which is shown on the order page."),
    ("I took my refund as QuickBasket Cash. Can I move it to my bank now?",
     "No. Once a refund has been credited as QuickBasket Cash it stays in the wallet. The only QuickBasket "
     "Cash that can go to a bank account is a refund for a cash-on-delivery order, and only on request."),
]

COD_CANCEL = [
    ("Is cash on delivery available?",
     "Yes, for orders up to ₹3,000. It is not available for gift cards, for QuickBasket Plus, or for addresses "
     "in Hinjewadi Phase 3 in Pune."),
    ("Is cash on delivery available for a ₹4,500 order?",
     "No. Cash on delivery is offered only on orders up to ₹3,000. For a bigger order, pay by UPI or card, or "
     "split the items across two orders."),
    ("why is the cash on delivery option missing at checkout",
     "There are three usual reasons: the order is above ₹3,000, the basket contains a gift card or a Plus "
     "membership, or the address is in Hinjewadi Phase 3 in Pune, where cash on delivery isn't offered."),
    ("Can I buy a gift card or Plus with cash on delivery?",
     "No. Gift cards and QuickBasket Plus can't be bought with cash on delivery. Use UPI or a card."),
    ("I paid cash for my order. How will I get a refund?",
     "A refund for a cash-on-delivery order is credited instantly as QuickBasket Cash. If you want it in your "
     "bank account instead, ask Support; that takes 5–7 business days."),
    ("Can I use QuickBasket Cash and pay the rest in cash?",
     "Yes. QuickBasket Cash or a gift card balance is used first, and you pay the remaining amount in cash at "
     "the door. The cash part still has to be within the ₹3,000 order limit for cash on delivery."),
    ("How do I cancel an order?",
     "Open the order in the app and tap Cancel. Whether you can cancel, and whether there is a fee, depends "
     "on the stage of the order:\n\n" + md_table(["Order stage", "Can I cancel?", "Fee"], [
         ["Placed, no delivery partner assigned yet", "Yes", "Free"],
         ["Delivery partner assigned, not picked up yet", "Yes", "₹25"],
         ["Picked up / out for delivery", "No", "–"],
         ["Delivered", "No; raise a return or refund request instead", "–"]])),
    ("Is cancelling free?",
     "It is free until a delivery partner is assigned to the order. After that you can still cancel until "
     "the partner picks the order up, but a ₹25 fee applies."),
    ("i cancelled my order, why was i charged 25 rupees",
     "Because a delivery partner had already been assigned when you cancelled. Cancellation is free only "
     "before that point; from assignment until pickup the fee is ₹25."),
    ("Can I cancel an order that is out for delivery?",
     "No. Once the order has been picked up it can't be cancelled. You can refuse it at the door and, after "
     "it is marked delivered, request a refund for the unopened items."),
    ("How is the ₹25 cancellation fee collected?",
     "On a prepaid order it is deducted from the amount that goes back to you. On a cash-on-delivery order "
     "it is added to your next order and shown on that bill."),
    ("I cancelled a prepaid order. When do I get my money back?",
     "The amount, less the ₹25 fee if one applied, goes back to the payment method you used: UPI in 2–4 "
     "business days, card in 5–7 business days, and QuickBasket Cash instantly."),
    ("Do Plus members pay the cancellation fee?",
     "Yes. The ₹25 fee after a delivery partner is assigned applies to every customer. QuickBasket Plus "
     "covers delivery fees, not cancellation fees."),
    ("Does cancelling use up my promo code?",
     "Not if you cancel before a delivery partner is assigned. In that case the offer is restored to your "
     "account within 24 hours and you can use it on another order while the campaign is still running."),
    ("Can I cancel just one item from an order?",
     "No. Cancellation applies to the whole order. If you only want to drop one item, cancel before a partner "
     "is assigned and place the order again, or raise a return for that item after delivery if its category "
     "allows returns."),
    ("I refused the order at the door. When is my refund?",
     "Wait until the order is marked delivered in the app, then request the refund for the unopened items "
     "from the order page. No refund can be issued while the order is still shown as on the way. After "
     "approval, the normal refund timeline for your payment method applies."),
]

PLUS = [
    ("What is QuickBasket Plus and what does it cost?",
     "Plus is a paid membership. It costs ₹149 per month or ₹1,299 per year, GST included, and gives free "
     "delivery on orders above ₹199. The yearly plan works out to about ₹108 per month."),
    ("What do I get with Plus?",
     "Free delivery on every order above ₹199, extra compensation when an order is more than 30 minutes late, "
     "lower Plus prices on selected items, access to sale campaigns 2 hours before everyone else, and "
     "priority in the Support chat queue."),
    ("Do Plus members get free delivery on every order?",
     "On orders above ₹199, counted after discounts. An order of ₹199 or less pays the normal delivery fee "
     "for the city, even with Plus."),
    ("What extra do Plus members get when an order is late?",
     "If an order is more than 30 minutes late, a Plus member gets the delivery fee refunded plus ₹50 "
     "QuickBasket Cash. The ₹50 is a Plus benefit under the current Customer Policy (v4.2): customers without "
     "Plus get the delivery fee refunded only. For 16 to 30 minutes late, Plus members get the delivery fee "
     "refunded, the same as everyone else."),
    ("Can I cancel Plus and get my money back?",
     "Yes, if you cancel within 48 hours of buying it and have not used a free delivery yet. In that case the "
     "full membership fee is refunded to the original payment method. Go to Account › QuickBasket Plus › "
     "Cancel membership."),
    ("i bought plus yesterday and already got one free delivery, can i still get a refund",
     "No. The full refund within 48 hours is available only if no free delivery has been used. You can still "
     "cancel, and Plus stays active until the end of the current period without renewing."),
    ("I want to cancel Plus after three months. Do I get anything back?",
     "No. After the first 48 hours you can cancel at any time, but the current period is not refunded. Plus "
     "stays active until that period ends and then does not renew."),
    ("Does Plus renew automatically?",
     "Yes. It renews at the end of each month or year until you cancel. Before a yearly renewal we send a "
     "reminder 3 days in advance."),
    ("How can I pay for Plus?",
     "By UPI autopay, credit card or debit card. QuickBasket Cash, gift cards and cash on delivery can't be "
     "used to pay for Plus."),
    ("My Plus renewal payment failed. Have I lost my membership?",
     "Not immediately. We retry the payment for 3 days. If every retry fails, the benefits pause, and they "
     "start again as soon as a payment succeeds."),
    ("Do Plus members pay the Delhi NCR late-night surcharge?",
     "Yes. The ₹35 late-night surcharge on orders placed between 11 pm and 6 am from the 24-hour stores is "
     "separate from the delivery fee and applies to everyone. Plus free delivery covers the delivery fee only."),
    ("Does Plus work in all cities?",
     "Yes. One membership works at any address in the six cities we serve. The free-delivery threshold of "
     "₹199 is the same everywhere, including Mumbai, where normal delivery fees are higher."),
    ("can i share my plus membership with my flatmate",
     "A membership covers one QuickBasket account, and sharing an account between households isn't allowed. "
     "Your flatmate needs their own account and their own membership."),
    ("Is Plus returnable like other products?",
     "No. Plus is not returnable. The only refund is the 48-hour cancellation described above, when no free "
     "delivery has been used."),
    ("Will the Plus price change during my membership?",
     "We give at least 30 days' notice in the app before changing Plus prices or benefits. A new price "
     "applies only from your next renewal after the notice period."),
    ("Are Plus chats answered faster?",
     "Yes. Plus chats are answered first in the Support queue. Support hours are the same for everyone: "
     "7:00 am to midnight, every day."),
]

WALLET = [
    ("What is QuickBasket Cash?",
     "It is the wallet inside the app. It holds refunds you chose to take as QuickBasket Cash, cash-on-delivery "
     "refunds, late-delivery compensation, and cashback or referral rewards. It is used automatically at "
     "checkout unless you switch it off for an order."),
    ("Does QuickBasket Cash expire?",
     "It depends on the kind, and the wallet shows each kind separately:\n\n" +
     md_table(["Kind", "Comes from", "Expiry", "Limit per order"], [
         ["Refund Cash", "Refunds taken as QuickBasket Cash; cash-on-delivery refunds", "Never expires", "Up to 100% of the order"],
         ["Compensation Cash", "Late-delivery compensation", "180 days after credit", "Up to 100% of the order"],
         ["Promotional Cash", "Cashback offers and referral rewards", "90 days after credit", "Up to 50% of the order"]])),
    ("why can i use only half of my cashback on this order",
     "Cashback is Promotional Cash, and Promotional Cash can pay for at most 50% of an order. Refund Cash and "
     "Compensation Cash don't have this limit."),
    ("Can I withdraw QuickBasket Cash to my bank account?",
     "No. QuickBasket Cash can't be withdrawn. The single exception is a refund for a cash-on-delivery order, "
     "which can be sent to a bank account on request and takes 5–7 business days."),
    ("Can I transfer QuickBasket Cash to a friend?",
     "No. QuickBasket Cash belongs to the account it was credited to and can't be transferred to another account."),
    ("What can't I buy with QuickBasket Cash?",
     "Gift cards and QuickBasket Plus. Everything else can be paid for with QuickBasket Cash, within the 50% "
     "limit for Promotional Cash."),
    ("I paid with QuickBasket Cash and the order was refunded. What happens to the expiry date?",
     "The refund returns to the same kind of QuickBasket Cash it came from, with its original expiry date. "
     "Compensation Cash that had 20 days left when you spent it comes back with the same expiry date, not a new one."),
    ("my late delivery cash is not showing in wallet",
     "Late-delivery compensation is credited automatically within 2 hours of the delivery. If it is missing "
     "after that, chat with Support with the order ID. Remember that customer-side delays and declared "
     "advisories are excluded, so not every late order qualifies."),
    ("What gift card values can I buy?",
     "From ₹250 to ₹10,000, in steps of ₹50. Gift cards are delivered digitally, as a code."),
    ("How long is a gift card valid?",
     "12 months from the date of purchase. The expiry date is shown on the card. An expired gift card can't "
     "be extended or refunded."),
    ("How do I use a gift card?",
     "Add the code under Account › Gift cards. The balance is then used at checkout before other payment "
     "methods. Any unused balance stays on the card until it expires."),
    ("Can I get a refund for a gift card I bought by mistake?",
     "No. Gift cards can't be refunded or exchanged, whether or not the code has been used."),
    ("Can I buy Plus or another gift card with my gift card balance?",
     "No. A gift card balance can't be used to buy QuickBasket Plus or other gift cards."),
    ("I lost my gift card code. Can you send it again?",
     "If the code has not been redeemed, it can be reissued once to the purchaser, who has to show the "
     "purchase receipt. A code that has already been redeemed can't be reissued."),
    ("I paid with a gift card and the order was refunded. Where does the money go?",
     "Back to the gift card balance. If the gift card has expired in the meantime, the refund is credited as "
     "QuickBasket Cash instead."),
    ("my gift card expired yesterday can you extend it",
     "No. Gift cards are valid for 12 months and can't be extended, reactivated or refunded after they expire."),
]

OFFERS = [
    ("Can I use two promo codes on one order?",
     "No. Only one offer can be applied to an order. If the basket qualifies for more than one, choose the "
     "one you want at checkout."),
    ("How do I know my promo code was applied?",
     "The offer appears as its own line in the bill summary on the checkout screen, before you pay. If the "
     "line isn't there, the offer has not been applied to that order."),
    ("I forgot to apply the code. Can you add it to my order now?",
     "No. An offer can't be added after an order is placed. If no delivery partner has been assigned yet, you "
     "can cancel for free and place the order again with the code."),
    ("What is FIRST100?",
     "FIRST100 gives ₹100 off your first QuickBasket order when the order is ₹299 or more. It works once per "
     "account, on the first order only."),
    ("What was the Diwali Dhamaka offer?",
     "Code DIWALI10 gave 10% cashback, up to ₹200, on orders of ₹999 or more placed from 25 October to "
     "5 November 2026. The campaign has ended, so the code can't be applied to new orders."),
    ("i returned an item from my diwali order, why is my cashback gone",
     "The Diwali Dhamaka cashback is reversed when the order that earned it is refunded, in proportion if "
     "only part of the order is refunded. If the cashback has already been spent, the amount is deducted "
     "from the refund."),
    ("How is cashback paid, and does it expire?",
     "Cashback is credited as Promotional Cash in your QuickBasket Cash wallet. It expires 90 days after it "
     "is credited and can pay for at most 50% of an order."),
    ("How is the minimum order value for an offer worked out?",
     "It is the item total after other discounts. Delivery fees, surcharges and tips don't count towards it."),
    ("If I return an item bought on offer, how much do I get back?",
     "The amount you actually paid for that item after the discount. Refunds are never based on the price "
     "before the offer."),
    ("Can I return the free gift that came with my order?",
     "No. Free gift items are not returnable and are not refunded, because nothing was paid for them."),
    ("Do offers change the return rules?",
     "No. An offer never changes the Customer Policy: return windows, refund timelines and approval limits "
     "stay the same unless the terms of a campaign say otherwise in so many words."),
    ("Where can I read the terms of an offer?",
     "Tap the offer in the app to see its dates, minimum order, maximum benefit, cities and payment method. "
     "The full terms of every campaign since 1 January 2026, including expired ones, are in the QuickBasket "
     "Offers: Terms and Conditions document."),
    ("Can I give my promo code or referral reward to someone else?",
     "No. Offers and rewards are linked to the account that earned them and can't be transferred. A referral "
     "reward is credited as Promotional Cash, which expires after 90 days."),
    ("why is the offer item showing out of stock for me",
     "Offer items depend on the stock of the store that covers your address. If the item is out of stock "
     "there, the offer can't be swapped to a different item."),
    ("Do Plus members get offers earlier?",
     "Yes. Plus members can shop sale campaigns 2 hours before everyone else. The offer terms themselves are "
     "the same for all customers."),
]

CITY_HEAD = [
    ("Which cities does QuickBasket deliver in?",
     "Six: Hyderabad, Bengaluru, Chennai, Pune, Mumbai and Delhi NCR. Coverage inside each city is decided "
     "by the delivery address, so the app is the final check."),
    ("Do you deliver in Kochi?",
     "Not yet. A launch in Kochi is planned for January 2027. Until then we can't take orders for Kochi "
     "addresses, and delivery fees for Kochi have not been announced."),
    ("when is quickbasket coming to jaipur",
     "The launch in Jaipur is planned for January 2027. No orders can be placed for Jaipur before that, and "
     "the fees for Jaipur haven't been announced yet."),
    ("Are you launching in any other city soon?",
     "Kochi and Jaipur are the only two with a planned launch, both in January 2027. No other city has a "
     "date. If Support is asked about another city, the honest answer is that nothing has been announced."),
]
CITY_TAIL = [
    ("Is there an extra charge for late-night orders in Delhi NCR?",
     "Yes. Orders placed between 11 pm and 6 am from the four 24-hour stores (DEL-01, DEL-03, DEL-06 and "
     "DEL-08) carry a ₹35 late-night surcharge. It is shown before payment and applies to every customer, "
     "including Plus members."),
    ("It is cyclone season in Chennai. Do I get more time to report spoiled items?",
     "Only while an advisory is declared. For orders delivered in Chennai during a declared cyclone or "
     "heavy-rain advisory, the reporting window for fresh fruits and vegetables, dairy, bakery and eggs, and "
     "frozen food and meat is 48 hours. The other conditions stay the same, and at all other times the "
     "normal windows apply: 24 hours for fresh produce and dairy, 12 hours for frozen food and meat."),
    ("What is a QB Tech Hub store in Bengaluru?",
     "Three Bengaluru stores are QB Tech Hubs: BLR-01, BLR-03 and BLR-04. For electronics bought from these "
     "stores, a replacement approved before 6 pm, within the 3-day electronics return window of the current "
     "Customer Policy, is delivered the same day. Only the speed changes; the electronics rules are the same "
     "as everywhere else."),
    ("Why can't I pay cash in Hinjewadi Phase 3?",
     "Cash on delivery isn't offered for addresses in Hinjewadi Phase 3, Pune, because delivery partners "
     "can't carry cash into the IT-park security zone. UPI, cards and QuickBasket Cash work as usual. "
     "Everywhere else in Pune, cash on delivery is available on orders up to ₹3,000."),
    ("Will you deliver in Mumbai on a red-alert day?",
     "Deliveries to some low-lying localities may be paused on days when the city is under a red alert for "
     "heavy rain. The app tells you before checkout if your locality is paused. Late-delivery compensation "
     "does not apply during a declared advisory."),
    ("I'm moving from Pune to Hyderabad. Do I need a new account or a new Plus membership?",
     "No. Add the new address and keep using the same account. Your Plus membership, QuickBasket Cash and "
     "gift card balance stay with the account. The delivery fees and store hours of Hyderabad apply to "
     "orders delivered there."),
]

SAFETY = [
    ("How do I contact QuickBasket Support?",
     "Through the in-app chat, under Help. Support chat is open from 7:00 am to midnight, every day. Have "
     "your order ID ready if the question is about an order."),
    ("Is there a phone number I can call?",
     "No. Support is handled in the in-app chat so that every conversation is tied to your account and your "
     "order. For questions about the Customer Policy itself you can write to policy@quickbasket.example."),
    ("How do I talk to a human instead of the automated assistant?",
     "Ask for a human agent in the chat. The conversation is also handed to a human agent whenever a customer "
     "is unhappy with a decision. During Support hours, 7:00 am to midnight, an agent picks it up in the "
     "same chat."),
    ("Can the automated assistant approve my refund?",
     "Yes, up to ₹500 per order, when the order is yours, has been delivered and the item is eligible under "
     "its category rules. Anything above ₹500 goes to the Customer Care Lead, who is a human and reviews the "
     "photo evidence."),
    ("The assistant said it doesn't know. Is something wrong?",
     "No. Our automated assistant is required to say so plainly when it doesn't know the answer, and it must "
     "never promise something the Customer Policy doesn't allow. Ask for a human agent if you need more help."),
    ("I'm not happy with the decision on my request. What can I do?",
     "Say so in the chat. When a customer is unhappy with a decision, the conversation is handed to a human "
     "agent, who looks at the request again under the Customer Policy."),
    ("What happens if someone is abusive in a chat?",
     "A conversation with abusive or threatening language is handed to a human agent. We ask customers to "
     "keep chats respectful; our agents and delivery partners are expected to do the same."),
    ("Someone called me saying they are from QuickBasket and asked for an OTP. Is that real?",
     "No. QuickBasket never asks for your UPI PIN, card PIN, CVV or a bank OTP, in chat or anywhere else. The "
     "only code you may be asked for is the gate entry OTP of your own community, by the delivery partner at "
     "your gate. Report anything else in the in-app chat."),
    ("Can a family member ask Support about my order?",
     "Not from their own account. Support discusses an order only with the account that placed it, after "
     "confirming that the order belongs to that customer."),
    ("Does the delivery partner see my phone number?",
     "No. Calls and messages between you and the delivery partner go through the app, and the partner sees "
     "your delivery address and order notes only for the duration of the delivery."),
    ("I ate something from my order and it tasted spoiled. What should I do?",
     "Stop using the item and keep the pack. Report it from the order page with a photo inside the window for "
     "that category: 24 hours for fresh produce and for dairy, bakery and eggs, 12 hours for frozen food "
     "and meat. If you feel unwell, please see a doctor first."),
    ("How do I complain about a delivery partner's behaviour?",
     "Tell Support in the in-app chat and include the order ID. Complaints about conduct are read by a human "
     "agent, not closed by the automated assistant."),
    ("Where can I read the full Customer Policy?",
     "The current version is Customer Policy v4.2, effective 1 October 2026, available under Help › Policies. "
     "If this FAQ and the Customer Policy ever differ, the Customer Policy is the one that applies."),
    ("I already had three refunds this month and need another one. What happens?",
     "The support agent or the automated assistant can't approve it. A customer can have at most three "
     "refunds in any 30-day period, and a further request goes to the Customer Care Lead for a decision."),
    ("Why did the assistant refuse to tell me about an order?",
     "Most likely because it could not confirm that the order belongs to the account you are signed in to. "
     "Check that you are using the account that placed the order and that the order ID (format QB-12345) is "
     "typed correctly."),
]


ELECTRONICS += [
    ("My smartwatch was delivered at 4:30 pm on 2 March. What is the last moment I can ask for a replacement?",
     "4:30 pm on 9 March. The electronics window is 7 days, counted to the minute from the delivery time shown "
     "in the app. After that, faults are handled under the manufacturer's warranty."),
    ("i got a bluetooth speaker 6 days ago and it has a fault, is it too late",
     "No. Six days is inside the 7-day window for electronics. Raise the request from the order page today, "
     "with the order ID and a photo or short description of the fault, and keep the box and accessories "
     "together for the replacement."),
    ("It is day 8 and my power bank is not charging. What are my options?",
     "The 7-day return window has ended, so QuickBasket can no longer replace or refund it. The manufacturer's "
     "warranty applies now: use the GST invoice under Orders › Invoice as proof of purchase and contact the "
     "brand's service partner listed in the Electronics Warranty and Brand Directory."),
]
PLUS += [
    ("I'm a Plus member. My ₹320 order had free delivery and came 41 minutes late. What do I get?",
     "₹50 QuickBasket Cash. There was no delivery fee on the order, so there is nothing to refund on that "
     "side, but as a Plus member you get the ₹50 for an order more than 30 minutes late. It is credited "
     "automatically within 2 hours of delivery."),
    ("My ₹150 order came 35 minutes late and I have Plus. What is credited?",
     "The delivery fee you paid, because orders of ₹199 or less pay the normal fee even with Plus, plus ₹50 "
     "QuickBasket Cash as a Plus member. Both are credited as QuickBasket Cash, not to your bank."),
    ("Does the Plus late-delivery benefit apply during a weather advisory?",
     "No. Orders delivered during a declared weather or traffic advisory are excluded from late-delivery "
     "compensation for everyone, Plus members included. So are delays caused by a wrong address, the customer "
     "not being reachable or gate entry."),
]
ORDERING += [
    ("I entered the wrong address and the order is already on its way. What can I do?",
     "An order that is out for delivery can't be cancelled or sent to a different address. Call the delivery "
     "partner from the order page and explain; any time lost because of a wrong address counts as a "
     "customer-side delay. If the order can't be handed over, refuse it and request a refund for the unopened "
     "items once it is marked delivered."),
    ("Can I order electronics and groceries in the same order?",
     "Yes. One order can mix categories. If something goes wrong, each item follows the rule of its own "
     "category, so the milk and the charger in the same bag have different windows and different remedies."),
    ("Do I have to return the whole order to get a refund for one item?",
     "No. Requests are raised item by item. The approval limit is counted per order, though: refunds of up to "
     "₹500 on one order can be approved by a support agent or the automated assistant, and anything above that "
     "goes to the Customer Care Lead."),
    ("how do i change my phone number",
     "Go to Account › Profile, enter the new number and confirm it with the OTP sent to that number. Your "
     "orders, Plus membership and QuickBasket Cash stay with the account."),
    ("Can I reorder something I bought last week?",
     "Yes. Open the old order under Orders and tap Reorder. The basket is filled with the same items at "
     "today's prices, and anything the store doesn't have in stock right now is left out."),
    ("What are household essentials, and which return rule do they follow?",
     "Things like detergent, cleaning supplies, kitchen rolls and stationery. They have no category rule of "
     "their own, so the general rule applies: they can be returned within 7 days of delivery if they are "
     "unused and in their original packaging."),
]
DELIVERY += [
    ("The partner left my order at the lobby. Is that allowed?",
     "In some apartment complexes the residents' association doesn't allow delivery partners beyond the lobby "
     "or the security desk, and the order is handed over there. If your complex allows doorstep delivery, "
     "mention it in the order notes."),
    ("Is anything charged on top of the delivery fee?",
     "A surcharge, where one applies, is shown as its own line on the bill before you pay. The one customers "
     "ask about most is the ₹35 late-night surcharge in Delhi NCR, on orders placed between 11 pm and 6 am "
     "from the 24-hour stores. A surcharge is separate from the delivery fee, so free delivery, including "
     "Plus free delivery, does not remove it."),
    ("My order was late and one item was spoiled. Do I raise one request or two?",
     "One. Late-delivery compensation is worked out automatically, so there is nothing to raise for the "
     "delay. For the spoiled item, raise a request from the order page with a photo, inside the window for "
     "that item's category."),
]
RETURNS_HEAD += [
    ("Does the 7-day rule apply to fruit and vegetables too?",
     "No. The 7-day rule is the general rule, and category rules always take priority over it. Fresh fruits "
     "and vegetables must be reported within 24 hours of delivery and are not returnable."),
    ("What kind of photo do you need?",
     "A clear photo of the item that shows the problem, taken after delivery. For dairy and bakery, include "
     "the best-before date on the pack. For frozen food and meat, the photo has to show the packaging and "
     "the temperature label. Photos are required for damaged or spoiled items in every category."),
    ("My refund is for ₹1,249. Why is it taking longer than my last one?",
     "Refunds above ₹500 per order can't be approved by a support agent or the automated assistant. They go "
     "to the Customer Care Lead, a human, who reviews the photo evidence before deciding. The refund timeline "
     "for your payment method starts once the refund is approved."),
    ("The 24-hour window ended at 2 am, when chat was closed. Can I report it in the morning?",
     "No. A window is not extended because chat is closed. The order page accepts requests at any hour, so "
     "raise the request there before the window ends. Support chat is open from 7:00 am to midnight."),
    ("Support said my item is not eligible. Can I ask someone else to look at it?",
     "Yes. Tell Support you are unhappy with the decision and the conversation is handed to a human agent. "
     "The agent reviews the request again, but under the same Customer Policy: nobody in Support can approve "
     "an outcome the policy doesn't allow."),
    ("can you make an exception just this once",
     "Support, human or automated, can't promise or approve something the Customer Policy does not allow, "
     "such as a refund outside a category window. If you think the rule was applied wrongly to your order, "
     "ask for a human agent to review it."),
]
PAY_HEAD += [
    ("My UPI app shows the payment as pending. Has my order been placed?",
     "Not yet. An order is placed only when the payment is confirmed, and it then appears under Orders. If a "
     "pending payment fails after the money was debited, your bank reverses it automatically within 3–5 "
     "business days."),
    ("I was charged twice for one order.",
     "Check Orders first. If only one order is listed, the second debit is a failed payment that your bank "
     "reverses automatically within 3–5 business days. If it hasn't come back after 5 business days, chat "
     "with Support and share the UPI reference number or the last four digits of the card."),
    ("How do I know my refund was approved?",
     "The order page shows the request as approved, with the date and the amount, and the app sends a "
     "notification. The timeline for your payment method is counted from that date."),
]
COD_CANCEL += [
    ("I'm in Hinjewadi Phase 1. Can I pay cash?",
     "Yes. The restriction applies only to addresses in Hinjewadi Phase 3. In Phases 1 and 2, and in the rest "
     "of Pune, cash on delivery is available on orders up to ₹3,000."),
    ("i placed the order two minutes ago, can i cancel for free",
     "Only if no delivery partner has been assigned yet. The fee depends on the stage of the order, not on "
     "how many minutes have passed, and a partner is often assigned quickly. The order page shows the "
     "current stage and whether the ₹25 fee applies before you confirm the cancellation."),
]
PLUS += [
    ("Monthly or yearly: what is the difference?",
     "Only the price and the billing period. The benefits are identical. Twelve months on the monthly plan "
     "cost ₹1,788, against ₹1,299 for the yearly plan, so the yearly plan is ₹489 cheaper over a year."),
    ("I'm a Plus member and my order was 25 minutes late. Do I get the ₹50?",
     "No. For an order that is 16 to 30 minutes late, Plus members get the delivery fee refunded, like "
     "everyone else. The extra ₹50 QuickBasket Cash for Plus members applies only when the order is more "
     "than 30 minutes late."),
    ("My basket was ₹230 but a coupon brought it down to ₹180. Why did I pay for delivery with Plus?",
     "Plus free delivery applies to orders above ₹199, and the order value is counted after discounts. At "
     "₹180 the order is below the threshold, so the normal delivery fee for your city applies."),
    ("Can I swap my Plus benefits for cash?",
     "No. Plus benefits can't be exchanged for money or for QuickBasket Cash, and unused free deliveries "
     "don't carry any value."),
    ("What happens to Plus if my account is suspended?",
     "If an account is suspended for misuse, the Plus membership is cancelled and the current period is not "
     "refunded."),
]
WALLET += [
    ("Is late-delivery compensation the same as Refund Cash?",
     "No. Late-delivery compensation is Compensation Cash, which expires 180 days after it is credited. "
     "Refund Cash comes from refunds you took as QuickBasket Cash and from cash-on-delivery refunds, and it "
     "never expires."),
    ("How do I stop QuickBasket Cash being used on an order?",
     "QuickBasket Cash is applied automatically at checkout. Switch off the QuickBasket Cash toggle in the "
     "bill summary before you pay, and the order is charged fully to your other payment method."),
    ("i haven't ordered for months, is my refund money in the wallet still there",
     "Yes, if it is Refund Cash: that never expires, however long you go without ordering. Compensation Cash "
     "and Promotional Cash do expire, 180 days and 90 days after they were credited."),
]
OFFERS += [
    ("Can I use FIRST100 on a ₹250 order?",
     "No. FIRST100 needs a first order of ₹299 or more. Add items to reach ₹299 and the ₹100 discount appears "
     "in the bill summary."),
    ("How much cashback did DIWALI10 give on different order values?",
     "10% of the order value, capped at ₹200, on orders of ₹999 or more. So a ₹1,500 order earned ₹150, a "
     "₹2,500 order earned the maximum of ₹200, and a ₹900 order earned nothing because it was below ₹999."),
    ("I bought an item at 10% off for ₹360 instead of ₹400. What is refunded if I return it?",
     "₹360, the amount you actually paid. The ₹40 discount is not paid out."),
]
SAFETY += [
    ("Support chat is closed. How do I report a problem at 1 am?",
     "Use the order page. Return, refund and missing-item requests can be raised there at any hour, and the "
     "time you raise the request is what counts for the category window. Chat reopens at 7:00 am."),
    ("What information should I keep ready before I chat with Support?",
     "The order ID (format QB-12345), a photo if an item is damaged or spoiled, and the app signed in to the "
     "account that placed the order. With those three things most requests are settled in one conversation."),
]

SUMMARY = {
    "Ordering and account": [
        "Every request needs the order ID (format QB-12345) and must come from the account that placed the order.",
        "Support confirms the order is yours before discussing it.",
        "An order can't be edited after it is placed; cancel and reorder instead.",
        "Prices include GST; the invoice is under Orders › Invoice."],
    "Delivery and tracking": [
        "The promised delivery time shown at checkout is the one that counts.",
        "Delivery fees depend on the city and on the order value after discounts.",
        "Partners wait up to 7 minutes at a gate; waiting for entry is a customer-side delay.",
        "Out for delivery means it can't be cancelled, only refused at the door."],
    "Late deliveries": [
        "Up to 15 minutes late: no compensation.",
        "16 to 30 minutes late: delivery fee refunded.",
        "More than 30 minutes late: delivery fee refunded plus ₹50 QuickBasket Cash, for every customer.",
        "Credited automatically as QuickBasket Cash within 2 hours of delivery; never a bank refund.",
        "Customer-caused delays and declared weather or traffic advisories are excluded."],
    "Returns and refunds by category": [
        "General rule: 7 days, unused, original packaging. Category rules take priority.",
        "Fresh produce and dairy, bakery & eggs: report within 24 hours. Frozen & meat: within 12 hours.",
        "Packaged food, personal care and baby care: 7 days, unopened or seal unbroken.",
        "Refunds up to ₹500 per order: support agent or automated assistant. Above ₹500: Customer Care Lead.",
        "One refund per order, at most three refunds in any 30-day period, and none before delivery."],
    "Electronics and accessories": [
        "Return window: 7 days from the delivery time shown in the app.",
        "Replacement first; a refund only if no replacement is in stock.",
        "The item must be unused, with its box and all accessories.",
        "After 7 days the manufacturer's warranty applies."],
    "Payments and refund timelines": [
        "UPI refunds: 2–4 business days. Card refunds: 5–7 business days.",
        "QuickBasket Cash refunds are instant, and you can choose QuickBasket Cash for any refund.",
        "Cash on delivery: instant as QuickBasket Cash; bank refund on request in 5–7 business days.",
        "A failed payment is reversed by your bank in 3–5 business days; it is not a refund."],
    "Cash on delivery and cancellations": [
        "Cash on delivery: orders up to ₹3,000; not for gift cards, Plus or Hinjewadi Phase 3.",
        "Cancelling is free until a delivery partner is assigned, then ₹25 until pickup.",
        "Out for delivery: no cancellation; refuse at the door and request a refund for unopened items."],
    "QuickBasket Plus": [
        "₹149 per month or ₹1,299 per year.",
        "Free delivery on orders above ₹199, counted after discounts.",
        "More than 30 minutes late: Plus members get ₹50 QuickBasket Cash on top of the delivery fee refund.",
        "Full refund if cancelled within 48 hours with no free delivery used; no refund of the current period after that."],
    "QuickBasket Cash and gift cards": [
        "Refund Cash never expires; Compensation Cash lasts 180 days; Promotional Cash lasts 90 days.",
        "Promotional Cash pays for at most 50% of an order.",
        "QuickBasket Cash can't be transferred or withdrawn, except a cash-on-delivery refund on request.",
        "Gift cards: ₹250 to ₹10,000, valid 12 months, never refunded or exchanged."],
    "Offers and promo codes": [
        "One offer per order, shown as its own line on the bill before you pay.",
        "Refunds are the amount actually paid after the discount.",
        "Cashback is Promotional Cash and is reversed if the order that earned it is refunded.",
        "Free gifts are not returnable or refunded."],
    "Cities and coverage": [
        "We deliver in Hyderabad, Bengaluru, Chennai, Pune, Mumbai and Delhi NCR.",
        "Kochi and Jaipur: launch planned for January 2027; no orders and no fees announced yet.",
        "Delivery fees and store hours differ by city; a few local rules differ too."],
    "Safety, privacy and talking to a human": [
        "Support chat: 7:00 am to midnight, every day, in the app.",
        "Unhappy with a decision? The conversation is handed to a human agent.",
        "The automated assistant never promises what the Customer Policy doesn't allow.",
        "QuickBasket never asks for your UPI PIN, card PIN, CVV or bank OTP."],
}

GLOSSARY = [
    ("Order ID", "The reference of an order, in the format QB-12345. Needed for every request."),
    ("Promised delivery time", "The time shown at checkout when you place the order. Lateness is measured against it."),
    ("Delivery time shown in the app", "The moment the order was marked delivered. Every return or report window "
     "is counted from it."),
    ("Category rules", "The return and report rules that apply to a category of items. They take priority over "
     "the general 7-day rule."),
    ("Customer-side delay", "Time lost because of a wrong address, the customer not being reachable or waiting "
     "for entry at a gated community. It is excluded when lateness is worked out."),
    ("Declared advisory", "A weather or traffic advisory that QuickBasket declares for a city, shown as a banner "
     "in the app."),
    ("QuickBasket Cash", "The wallet in the app. It holds Refund Cash, Compensation Cash and Promotional Cash."),
    ("Business days", "Bank working days. Weekends and public holidays are not counted."),
    ("Customer Care Lead", "The human who decides refund requests that a support agent or the automated "
     "assistant is not allowed to approve."),
    ("Superseded policy", "An older version of the Customer Policy, kept only for orders placed while it was in force."),
]


# ------------------------------------------------------------------ worked examples (generated)
def cancel_examples(rng):
    out = []
    for m, t in [("UPI", "2–4 business days"), ("card", "5–7 business days"), ("cash on delivery", None)]:
        for assigned in (False, True):
            v = pick(rng, [260, 340, 480, 615, 790, 1150])
            stage = ("after a delivery partner was assigned but before pickup" if assigned
                     else "before any delivery partner was assigned")
            if t:
                q = pick(rng, [f"I paid ₹{v:,} by {m} and cancelled {stage}. How much comes back, and when?",
                               f"cancelled a ₹{v:,} {m} order {stage}. what refund will i get"])
                a = (f"₹{v - 25:,}. A ₹25 fee applies once a delivery partner has been assigned, and on a prepaid order "
                     f"it is deducted from the amount returned. The ₹{v - 25:,} goes back to your {m} "
                     f"{'account ' if m == 'UPI' else ''}in {t}." if assigned else
                     f"The full ₹{v:,}. Cancelling before a delivery partner is assigned is free, and the amount goes "
                     f"back to your {m} {'account ' if m == 'UPI' else ''}in {t}. You can also take it as "
                     "QuickBasket Cash, which is instant.")
            else:
                q = pick(rng, [f"I chose cash on delivery for a ₹{v:,} order and cancelled {stage}. Do I owe anything?",
                               f"cod order of ₹{v:,} cancelled {stage}, any charges?"])
                a = ("Yes, ₹25. You had not paid anything, so there is no refund, but the ₹25 cancellation fee is "
                     "added to your next order and shown on that bill." if assigned else
                     "No. Nothing had been paid, and cancelling before a delivery partner is assigned is free.")
            out.append((q, a))
    return out


def approval_examples(rng):
    out = []
    for amt in [120, 480, 500, 501, 899, 1249]:
        q = pick(rng, [f"Who approves a refund of ₹{amt:,} on one order?", f"my refund is ₹{amt:,}, can the assistant approve it",
                       f"Can chat support approve a ₹{amt:,} refund straight away?"])
        if amt <= 500:
            a = (f"A support agent or the automated assistant can approve it, because ₹{amt} is within the ₹500 "
                 "limit per order. They first confirm that the order is yours, that it has been delivered and that "
                 "the item is eligible under its category rules.")
        else:
            a = (f"The Customer Care Lead, a human. ₹{amt:,} is above the ₹500 limit per order, so a support agent or "
                 "the automated assistant can't approve it. The Customer Care Lead makes the same checks and also "
                 "reviews the photo evidence.")
        out.append((q, a))
    return out


def plus_city_examples(rng):
    out = []
    for c in CITIES:
        n, mid = c["name"], rupees(c["fee_mid"])
        k = -(-149 // mid)
        q = pick(rng, [f"Is Plus worth it in {n}?", f"How many orders a month before Plus pays for itself in {n}?",
                       f"should i take plus, i live in {n}"])
        a = (f"It depends on how often you order. Without Plus, an order from ₹199 to {c['free_from']} in {n} pays a "
             f"{c['fee_mid']} delivery fee, and orders above {c['free_from']} are delivered free anyway. At ₹149 per "
             f"month, the monthly plan pays for itself from {k} such orders in a month, before counting Plus prices "
             "and the extra late-delivery compensation.")
        out.append((q, a))
    return out


def promo_cash_examples(rng):
    out = []
    for i, (cash, order) in enumerate([(300, 400), (150, 800), (500, 240), (90, 150)]):
        used = min(cash, order // 2)
        q = [f"I have ₹{cash} of cashback and my order is ₹{order}. How much of it can I use?",
             f"₹{cash} promotional cash in wallet, order of ₹{order}, how much gets applied",
             f"My wallet shows ₹{cash} Promotional Cash. How much comes off a ₹{order} order?"][(i + rng.randrange(3)) % 3]
        a = (f"₹{used}. Promotional Cash can pay for at most 50% of an order, which is ₹{order // 2} on a ₹{order} "
             "order" + (f", so ₹{cash - used} stays in the wallet until its expiry date." if used < cash else
                        ", and your balance is within that limit, so all of it is used."))
        out.append((q, a))
    return out


GIFT_VALUES = [(200, "No. The smallest gift card is ₹250."),
               (275, "No. Gift card values go up in steps of ₹50, so you can buy ₹250 or ₹300, but not ₹275."),
               (5000, "Yes. Any value from ₹250 to ₹10,000 in steps of ₹50 is available, and ₹5,000 is one of them."),
               (12000, "No. The largest single gift card is ₹10,000. You can buy more than one card.")]
STAGES = [
    ("Placed", "The store has the order and is packing it. No delivery partner has been assigned yet, so you can "
               "still cancel free of charge."),
    ("Delivery partner assigned", "A partner is on the way to the store or waiting for the order. You can still "
                                  "cancel until pickup, but a ₹25 fee applies."),
    ("Picked up", "The partner has collected the order and is on the way to you; this is the same as out for "
                  "delivery. The order can't be cancelled now, though you can refuse it at the door."),
    ("Delivered", "The order has been handed over, and the delivery time shown here starts every return or "
                  "report window. It can't be cancelled; raise a return or refund request if something is wrong."),
]


def render_section(n, title, reviewed, intro, qas):
    lines = [f"## {n}. {title}", "", f"*Last reviewed: {reviewed}*", "", intro, "", "In short:", ""]
    lines += [f"- {b}" for b in SUMMARY[title]] + [""]
    for q, a in qas:
        lines += [f"**{q}**", "", a, ""]
    return lines


def build(ctx, out_dir):
    rng = ctx.rng("faq")
    cat_qs = category_questions(rng)
    pay_qs = payment_questions(rng)
    city_qs = city_questions(rng)
    prod_qs = product_questions(rng)
    late_qs = late_examples(rng)
    stage_qs = [(pick(rng, [f"My order status says \"{st}\". What does that mean?",
                            f"what does \"{st}\" mean on the order page"]), a) for st, a in STAGES]
    gift_qs = [(pick(rng, [f"Can I buy a gift card for ₹{v:,}?", f"is a ₹{v:,} gift card available"]), a)
               for v, a in GIFT_VALUES]

    sections = [
        ("Ordering and account", "8 October 2026",
         "How ordering works, what you need for a request, and how your account is used.", ORDERING),
        ("Delivery and tracking", "15 October 2026",
         "Following an order from the store to your door, and what happens at gates, offices and in bad weather.",
         DELIVERY[:3] + stage_qs + DELIVERY[3:]),
        ("Late deliveries", STALE,
         "What we do when an order arrives after the promised delivery time.", LATE[:8] + late_qs + LATE[8:]),
        ("Returns and refunds by category", "6 October 2026",
         "The general rule first, then fresh produce, dairy, frozen food, packaged food, personal care and baby "
         "care in turn. Electronics have their own section below.", RETURNS_HEAD[:5] + cat_qs + RETURNS_HEAD[5:6] + approval_examples(rng) + RETURNS_HEAD[6:]),
        ("Electronics and accessories", STALE,
         "Returns, replacements and warranties for chargers, cables, earphones, power banks, wearables and other "
         "electronics sold on QuickBasket.", ELECTRONICS[:9] + prod_qs + ELECTRONICS[9:]),
        ("Payments and refund timelines", "12 October 2026",
         "How to pay, and how long money takes to come back for each payment method.", PAY_HEAD[:4] + pay_qs + PAY_HEAD[4:]),
        ("Cash on delivery and cancellations", "2 November 2026",
         "When you can pay cash, and when and how an order can be cancelled.",
         COD_CANCEL[:12] + cancel_examples(rng) + COD_CANCEL[12:]),
        ("QuickBasket Plus", "5 October 2026",
         "Price, benefits, renewal and cancellation of the Plus membership.", PLUS + plus_city_examples(rng)),
        ("QuickBasket Cash and gift cards", "20 October 2026",
         "The wallet in the app and how gift cards work.", WALLET[:3] + promo_cash_examples(rng) + WALLET[3:9] + gift_qs + WALLET[9:]),
        ("Offers and promo codes", "10 November 2026",
         "The rules that are common to all offers, plus the two codes customers ask about most.", OFFERS),
        ("Cities and coverage", "3 November 2026",
         "Where we deliver, what delivery costs in each city, store hours and the local rules that differ.",
         CITY_HEAD + city_qs + CITY_TAIL),
        ("Safety, privacy and talking to a human", "28 October 2026",
         "Reaching Support, what the automated assistant can and can't do, and keeping your account safe.", SAFETY),
    ]

    total = sum(len(s[3]) for s in sections)
    lines = ["# QuickBasket Customer FAQ", "",
             "*Fictional company for training use. All content synthetic.*", "",
             f"Answers to the {total} questions customers ask us most, in {len(sections)} sections. Each section "
             "shows the date it was last reviewed. The rules themselves are set by the QuickBasket Customer "
             "Policy; this FAQ explains them in everyday language.", "",
             "**Sections**", ""]
    lines += [f"{i}. {s[0]}" for i, s in enumerate(sections, 1)]
    lines.append("")
    for i, (title, reviewed, intro, qas) in enumerate(sections, 1):
        lines += render_section(i, title, reviewed, intro, qas)
    lines += ["## Words used in this FAQ", ""] + [f"- **{t}:** {d}" for t, d in GLOSSARY] + [""]
    lines += ["---", "", "Still stuck? Chat with QuickBasket Support in the app, 7:00 am to midnight, every day."]
    write_md(f"{out_dir}/{FILE}", "\n".join(lines))

    kind = f"stale FAQ section (last reviewed {STALE})"
    ctx.conflict("Electronics return window", FILE, "5. Electronics and accessories",
                 "Electronics can be returned within 7 days; manufacturer warranty applies after 7 days",
                 "3 days; manufacturer warranty after 3 days (Section 3)", kind)
    ctx.conflict("Late compensation for non-Plus customers (more than 30 minutes)", FILE, "3. Late deliveries",
                 "More than 30 minutes late: delivery fee refunded plus ₹50 QuickBasket Cash for every customer",
                 "Delivery fee refunded only; the ₹50 is for Plus members (Section 5)", kind)
    ctx.exception("Order changes after placing", FILE, "1. Ordering and account",
                  "No minimum order value; address and items can't be changed after an order is placed (cancel and reorder)",
                  "Not in the Customer Policy; consistent with the cancellation rules")
    ctx.exception("Whole-order cancellation only", FILE, "7. Cash on delivery and cancellations",
                  "A single item can't be cancelled from an order; an offer can't be added after the order is placed",
                  "Not in the Customer Policy")
    return [dict(file=FILE, title="Customer FAQ", kind="FAQ", fmt="Markdown")]
