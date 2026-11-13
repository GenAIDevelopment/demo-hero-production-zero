"""Per-campaign detail for the promo terms, generated from data: steps, worked examples (computed, so
the arithmetic is always right) and sample eligible items with the return rule for their category."""
from .common import pick

CAT_RULE = {  # return rule per category: copied from Customer Policy v4.2, Section 3
    "Fresh fruits & vegetables": "Report within 24 hours; refund or replacement only; photo required",
    "Dairy, bakery & eggs": "Report within 24 hours; refund or replacement only",
    "Frozen & meat": "Report within 12 hours; refund only; photo of packaging and temperature label",
    "Packaged food & beverages": "Return or refund within 7 days; unopened, before expiry",
    "Personal care & beauty": "Return or refund within 7 days; seal unbroken",
    "Electronics & accessories": "3 days; replacement first, refund if no replacement stock",
    "Baby care": "7 days; seal unbroken; formula and food not returnable",
    "Household & stationery": "Return within 7 days; unused, original packaging",
}
ITEMS = {
    "Fresh fruits & vegetables": ["Bananas (6 pieces)", "Tomatoes 500 g", "Onions 1 kg", "Coriander bunch", "Apples 4 pieces",
                                  "Banana leaves (pack of 5)", "Coconut (1 piece)", "Lemons 250 g", "Potatoes 1 kg", "Spinach bunch"],
    "Dairy, bakery & eggs": ["Toned milk 1 L", "Curd 400 g", "Paneer 200 g", "Brown bread 400 g", "Eggs (pack of 6)",
                             "Butter 100 g", "Kaju katli 250 g", "Gulab jamun (pack of 6)", "Modak (box of 6)", "Rasgulla 500 g"],
    "Frozen & meat": ["Vanilla ice cream tub 700 ml", "Mango ice cream bar (pack of 4)", "Frozen green peas 500 g",
                      "Chicken curry cut 500 g", "Frozen parathas (pack of 5)", "Kulfi sticks (pack of 6)"],
    "Packaged food & beverages": ["Masala chips 150 g", "Instant noodles (pack of 4)", "Assam tea 250 g", "Orange juice 1 L",
                                  "Cola 750 ml", "Basmati rice 1 kg", "Sabudana 500 g", "Kuttu atta 500 g", "Rock salt 200 g",
                                  "Roasted peanuts 200 g", "Milk chocolate bar 100 g", "Whole wheat atta 5 kg",
                                  "Toor dal 1 kg", "Sunflower oil 1 L", "Mixed fruit juice (pack of 6)", "Namkeen mix 400 g"],
    "Personal care & beauty": ["Moisturising lotion 200 ml", "Lip balm", "Herbal shampoo 340 ml", "Hand cream 75 g",
                               "Face wash 100 ml", "Body wash 250 ml", "Sunscreen SPF 50 50 g", "Hair oil 200 ml"],
    "Electronics & accessories": ["True wireless earbuds", "20 W fast charger", "10,000 mAh power bank", "USB-C cable 1 m",
                                  "Bluetooth speaker", "Smartwatch", "Fitness band", "LED smart bulb (pack of 2)"],
    "Baby care": ["Baby wipes (pack of 72)", "Diapers M (pack of 30)", "Baby lotion 200 ml", "Fruit puree pouch (baby food)",
                  "Baby cereal 300 g (baby food)", "Baby shampoo 200 ml"],
    "Household & stationery": ["Notebooks (pack of 6)", "Ball pens (pack of 10)", "Steel lunch box", "Water bottle 750 ml",
                               "Pencil box", "Sketch pens (pack of 12)", "Paper plates (pack of 50)", "Diyas (pack of 12)"],
}
# campaign name -> (calc, categories)
# calc: ("pct", %, cap, min) | ("flat", amount, min) | ("cashback", %, cap, min) | None
DETAIL = {
    "Summer Coolers": (("pct", 15, 90, 299), ["Frozen & meat", "Packaged food & beverages"]),
    "Back to School": (("pct", 20, 150, 399), ["Household & stationery"]),
    "Cricket Final Night": (("flat", 75, 449), ["Packaged food & beverages"]),
    "Monsoon Munchies": (("pct", 15, 75, 299), ["Packaged food & beverages"]),
    "Freedom Sale": (("flat", 100, 799), ["Packaged food & beverages", "Personal care & beauty", "Household & stationery"]),
    "Onam Sadya Specials": (("pct", 10, 120, 499), ["Fresh fruits & vegetables", "Packaged food & beverages"]),
    "Modak Fest": (None, ["Dairy, bakery & eggs"]),
    "Navratri Fasting Essentials": (("pct", 12, 100, 349), ["Packaged food & beverages"]),
    "Durga Puja Delights": (("flat", 60, 399), ["Dairy, bakery & eggs", "Packaged food & beverages"]),
    "Diwali Dhamaka": (("cashback", 10, 200, 999), ["Dairy, bakery & eggs", "Packaged food & beverages", "Household & stationery"]),
    "Dhanteras Electronics Deal": (("flat", 300, 2999), ["Electronics & accessories"]),
    "Plus Trial Spring": (None, []),
    "First Order": (("flat", 100, 299), ["Fresh fruits & vegetables", "Dairy, bakery & eggs", "Packaged food & beverages"]),
    "Refer and Earn": (None, []),
    "Wedding Season Bulk Saver": (("pct", 8, 400, 2499), ["Packaged food & beverages", "Household & stationery", "Dairy, bakery & eggs"]),
    "Cricket Nights": (None, ["Packaged food & beverages"]),
    "Children's Day Treats": (("flat", 50, 349), ["Packaged food & beverages", "Baby care"]),
    "Konkan Card Tuesdays": (("pct", 10, 150, 699), ["Packaged food & beverages", "Personal care & beauty"]),
    "TrustLine No-Cost EMI": (None, ["Electronics & accessories"]),
    "Winter Wellness": (("pct", 15, 120, 499), ["Personal care & beauty"]),
    "Plus Trial Winter": (None, []),
    "Free Gift Mondays": (None, ["Packaged food & beverages"]),
    "Weekend Free Delivery": (None, []),
    "Fresh Friday": (("pct", 20, 60, 249), ["Fresh fruits & vegetables"]),
}
STEPS = [
    ["Add eligible items to your basket.", "On the bill screen, tap **Offers** and choose this offer, or type the code.",
     "Check that the offer shows as its own line on the bill before you pay."],
    ["Fill your basket until it reaches the minimum order value.", "Open **Offers** at checkout and apply the code.",
     "Confirm the saving on the bill summary, then pay."],
    ["Shop as usual.", "At checkout, enter the code in the **Promo code** box (automatic offers apply by themselves).",
     "Look for the offer line on the bill. If it isn't there, the offer hasn't been applied."],
]


def _rs(n):
    return f"₹{n:,}"


def examples(calc, rng):
    if calc is None:
        return []
    kind = calc[0]
    lead = pick(rng, ["For example", "Worked examples", "How the numbers work"])
    out = []
    if kind in ("pct", "cashback"):
        _, pct, cap, mn = calc
        word = "cashback" if kind == "cashback" else "discount"
        below = mn - pick(rng, [20, 49, 60])
        mid = mn + pick(rng, [50, 101, 150])
        high = int(cap * 100 / pct) + pick(rng, [300, 500, 800])
        out.append(f"An order of {_rs(below)} of eligible items is below the {_rs(mn)} minimum, so there is no {word}.")
        out.append(f"An order of {_rs(mid)} gets {pct}% = {_rs(round(mid * pct / 100))} {word}.")
        out.append(f"An order of {_rs(high)} would work out to {_rs(round(high * pct / 100))}, but the maximum is "
                   f"{_rs(cap)}, so the {word} is {_rs(cap)}.")
        if kind == "cashback":
            order, part = 1500, 500
            cb = round(order * pct / 100)
            out.append(f"Refund example: an order of {_rs(order)} earns {_rs(cb)} cashback. If items worth {_rs(part)} "
                       f"are later refunded, {_rs(round(cb * part / order))} of the cashback is reversed. If the whole "
                       f"order is refunded, all {_rs(cb)} is reversed.")
        else:
            paid = mid - round(mid * pct / 100)
            out.append(f"Refund example: if that {_rs(mid)} order is refunded in full, the refund is the {_rs(paid)} "
                       "actually paid, not the price before the discount.")
    elif kind == "flat":
        _, amt, mn = calc
        below = mn - pick(rng, [10, 30, 50])
        ok = mn + pick(rng, [1, 51, 120])
        out.append(f"An order of {_rs(below)} is below the {_rs(mn)} minimum, so the offer does not apply.")
        out.append(f"An order of {_rs(ok)} gets {_rs(amt)} off, so you pay {_rs(ok - amt)} plus any delivery fee.")
        out.append(f"Refund example: if that order is refunded in full, the refund is the {_rs(ok - amt)} actually paid.")
    return [("h3", lead), ("ul", out)]


def items(cats, rng):
    if not cats:
        return []
    rows = []
    for cat in cats:
        pool = ITEMS[cat]
        for item in rng.sample(pool, min(len(pool), 3 if len(cats) > 1 else 6)):
            rows.append([item, cat, CAT_RULE[cat]])
    title = pick(rng, ["Examples of items in this offer and the return rule that applies",
                       "Sample eligible items, with their return rules",
                       "What's included (examples) and how returns work for each"])
    return [("h3", title), ("table", ["Item", "Category", "Return rule (Customer Policy v4.2)"], rows, [56, 44, 74]),
            ("small", "The full list of eligible items is shown in the app. The offer never changes an item's return rule.")]
