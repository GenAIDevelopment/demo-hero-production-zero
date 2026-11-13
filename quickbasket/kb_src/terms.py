"""Plus membership terms (PDF), gift card and QuickBasket Cash terms (PDF), payments detail (Markdown)."""
from .render import md_table, write_md, write_pdf

FOOT = " · Fictional company for training use. All content synthetic."


def _plus_extra(rng):
    from .promo_detail import ITEMS
    rows = []
    for cat in ("Packaged food & beverages", "Dairy, bakery & eggs", "Personal care & beauty", "Baby care"):
        for item in rng.sample(ITEMS[cat], 5):
            price = rng.choice([45, 60, 85, 99, 120, 149, 180, 210, 249, 299, 340])
            rows.append([item, cat, f"₹{price}", f"₹{price - max(3, round(price * rng.choice([4, 5, 6, 8]) / 100))}"])
    fee_rows = []
    for city, mid_fee in (("Hyderabad", 19), ("Bengaluru", 19), ("Delhi NCR", 19), ("Chennai", 15), ("Pune", 15), ("Mumbai", 25)):
        for n in (4, 8, 12):
            saved = n * mid_fee
            fee_rows.append([city, f"{n} orders of ₹300", f"₹{mid_fee} each", f"₹{saved}",
                             "Yes" if saved > 149 else "No, unless you also use member prices"])
    return [
        ("h", "9. Member prices: examples"),
        ("p", "Member prices change often. These examples show the kind of saving; the price in the app on the day "
              "of the order is the one that applies."),
        ("table", ["Item", "Category", "Regular price", "Plus price"], rows, [62, 52, 30, 30]),
        ("p", "If an item bought at a Plus price is refunded, the refund is the Plus price actually paid."),
        ("h", "10. Does Plus pay for itself? Examples"),
        ("p", "Free delivery saves the delivery fee on orders above ₹199. The table uses each city's delivery fee for "
              "an order of ₹300 and compares a month's saving with the ₹149 monthly price."),
        ("table", ["City", "Orders in a month", "Delivery fee without Plus", "Saved with Plus", "More than ₹149?"],
         fee_rows, [28, 36, 40, 32, 38]),
        ("h", "11. Common questions"),
        ("p", "**Do I get free delivery on a ₹150 order?** No. Free delivery is for orders above ₹199. A ₹150 order "
              "pays the normal delivery fee for your city."),
        ("p", "**My order was 25 minutes late. What do I get as a Plus member?** The same as everyone: the delivery "
              "fee is refunded as QuickBasket Cash. If your delivery was free, there is no fee to refund."),
        ("p", "**My order was 40 minutes late.** Plus members get the delivery fee refunded plus ₹50 QuickBasket Cash "
              "when an order is more than 30 minutes late, unless the delay was caused by the customer or a declared "
              "weather or traffic advisory."),
        ("p", "**I bought Plus yesterday and used one free delivery. Can I still get a refund?** No. The 48-hour "
              "refund is only available if no free delivery has been used."),
        ("p", "**I bought Plus three days ago and haven't used it.** The 48 hours have passed, so the current period "
              "isn't refunded. You can cancel so it doesn't renew."),
        ("p", "**Can I pay for Plus with QuickBasket Cash or a gift card?** No. Plus is paid by UPI autopay, credit "
              "card or debit card."),
        ("p", "**Does Plus remove the Delhi NCR late-night surcharge?** No. The ₹35 surcharge is separate from the "
              "delivery fee and applies to everyone."),
        ("p", "**I joined at ₹129. Why am I paying ₹149?** The price changed on 1 June 2026. Members who joined "
              "earlier moved to ₹149 at their first renewal after that date."),
        ("p", "**Can my family use my Plus?** Plus covers one account. Anyone ordering from that account, to any "
              "saved address, gets the benefits; sharing the account between households isn't allowed."),
        ("p", "**Does Plus work in every city?** Yes, in every city where QuickBasket delivers."),
        ("p", "**How do I switch from monthly to yearly?** Choose the yearly plan under Account › QuickBasket Plus. "
              "It starts when your current month ends."),
    ]


def _gift_extra():
    return [
        ("h", "Part D. Buying and sending a gift card"),
        ("ol", ["Open Account › Gift cards › Buy a gift card.",
                "Choose a value from ₹250 to ₹10,000 (in steps of ₹50) and a design.",
                "Enter the recipient's name and mobile number or email, and an optional message.",
                "Pay by UPI or card. Gift cards can't be bought with QuickBasket Cash, another gift card or cash on delivery.",
                "The recipient gets the code straight away, or on a date you choose (up to 30 days ahead)."]),
        ("h", "Part E. More questions"),
        ("p", "**I sent a gift card to the wrong number.** If the code hasn't been redeemed, Support can cancel it and "
              "send a new code to the right person. This is a reissue, not a refund."),
        ("p", "**Can I return a gift card I don't want?** No. Gift cards can't be refunded or exchanged."),
        ("p", "**Can I use two gift cards on one order?** Yes. Add both under Account › Gift cards; balances are "
              "used in the order they expire."),
        ("p", "**My order cost less than my gift card.** The rest stays on the card until it expires."),
        ("p", "**My order cost more than my gift card.** Pay the rest by UPI, card, QuickBasket Cash or cash on delivery."),
        ("p", "**Can a gift card be used in a city that isn't live yet?** No. It can be used only for delivery "
              "addresses QuickBasket serves. Kochi and Jaipur are planned for January 2027."),
        ("p", "**Why did my Promotional Cash pay for only half my order?** Promotional Cash can pay for at most 50% "
              "of an order. Refund Cash and Compensation Cash have no such limit."),
        ("p", "**Which QuickBasket Cash is used first?** The balance that expires soonest: usually Promotional Cash, "
              "then Compensation Cash, then Refund Cash."),
        ("p", "**My late-delivery ₹50 disappeared.** Compensation Cash expires 180 days after it is credited. The "
              "wallet shows each credit's expiry date."),
    ]


PAY_ERRORS = [
    ("Payment declined by bank", "The bank refused the payment.", "Try another method, or ask your bank. Nothing is charged."),
    ("UPI request timed out", "The UPI request wasn't approved within 5 minutes.", "Place the order again and approve the request in your UPI app."),
    ("Money debited, order not placed", "The payment went through after the order timed out.", "Wait: the bank reverses it automatically in 3–5 business days."),
    ("Card not supported", "The card type isn't accepted.", "Use another card or UPI. Net banking and pay-later aren't accepted."),
    ("Incorrect CVV or OTP", "Card details were entered wrongly.", "Re-enter the details. Three wrong tries block the card for the order; use another method."),
    ("UPI daily limit reached", "Your bank's daily UPI limit is used up.", "Use a card, or split the order."),
    ("Cash on delivery not available", "The order is above ₹3,000, includes a gift card or Plus, or the address is in Hinjewadi Phase 3.", "Pay by UPI or card."),
    ("Gift card expired", "The gift card passed its 12-month validity.", "Expired cards can't be used or extended."),
    ("QuickBasket Cash limit", "Promotional Cash can cover at most 50% of an order.", "Pay the rest another way."),
    ("Saved card removed", "The bank's card token expired.", "Add the card again under Account › Payments."),
    ("Duplicate payment", "Two payments were made for one order.", "The extra payment is reversed automatically in 3–5 business days."),
    ("Autopay failed (Plus)", "A Plus renewal payment failed.", "We retry for 3 days. Update the payment method under Account › QuickBasket Plus."),
]


def plus_terms(ctx, out_dir):
    f = "08_plus_membership_terms.pdf"
    blocks = [
        ("title", "QuickBasket Plus: Membership Terms", "Current terms effective 1 June 2026 · Last reviewed 1 October 2026"),
        ("p", "QuickBasket Plus is a paid membership that makes regular ordering cheaper and faster. These terms "
              "explain what Plus includes, how billing works and how to cancel. They sit alongside the Customer "
              "Policy v4.2; where both mention Plus, they say the same thing."),
        ("h", "1. Price and billing"),
        ("table", ["Plan", "Price", "Billing"], [
            ["Monthly", "₹149 per month", "Charged on the same date each month"],
            ["Yearly", "₹1,299 per year", "Charged once a year; works out to about ₹108 per month"]], [40, 50, 84]),
        ("ul", ["Prices include GST.",
                "Plus renews automatically at the end of each period until you cancel. We send a reminder 3 days "
                "before a yearly renewal.",
                "You can pay by UPI autopay, credit card or debit card. QuickBasket Cash and gift cards can't be used "
                "to pay for Plus.",
                "If a renewal payment fails, we retry for 3 days. Benefits pause if all retries fail and restart as "
                "soon as a payment succeeds."]),
        ("h", "2. What you get"),
        ("table", ["Benefit", "Details"], [
            ["Free delivery", "On every order above ₹199 (order value after discounts). Orders of ₹199 or less pay "
                              "the normal delivery fee for the city."],
            ["Extra late-delivery compensation", "If an order is more than 30 minutes late, Plus members get the "
             "delivery fee refunded plus ₹50 QuickBasket Cash (Customer Policy, Section 5). For 16 to 30 minutes "
             "late, Plus members get the delivery fee refunded, like everyone else."],
            ["Member prices", "Selected items carry a lower Plus price, shown with the Plus badge."],
            ["Early access", "Plus members can shop sale campaigns 2 hours before everyone else."],
            ["Priority chat", "Plus chats are answered first in the support queue."]], [52, 122]),
        ("h", "3. What free delivery doesn't cover"),
        ("ul", ["Surcharges that are separate from the delivery fee, such as the Delhi NCR late-night surcharge "
                "(11 pm to 6 am).", "Orders of ₹199 or less.", "Gift card purchases, which are delivered digitally."]),
        ("h", "4. Cancelling Plus"),
        ("p", "You can cancel Plus any time from Account › QuickBasket Plus › Cancel membership."),
        ("table", ["When you cancel", "What happens"], [
            ["Within 48 hours of purchase, and no free delivery used yet", "Full refund of the membership fee to the original payment method."],
            ["Within 48 hours, but a free delivery has already been used", "No refund. Plus stays active until the end of the current period."],
            ["After 48 hours", "No refund for the current period. Plus stays active until it ends and does not renew."]],
         [70, 104]),
        ("p", "These rules are the same for monthly and yearly plans, and for trial offers unless the offer's terms "
              "say otherwise. Plus is not returnable in any other way (Customer Policy, Section 3)."),
        ("h", "5. Using Plus fairly"),
        ("ul", ["One membership covers one QuickBasket account. Sharing an account between households isn't allowed.",
                "Plus benefits can't be exchanged for cash or QuickBasket Cash.",
                "If an account is suspended for misuse, Plus is cancelled without a refund for the current period."]),
        ("h", "6. Changes to these terms"),
        ("p", "We give at least 30 days' notice in the app before changing Plus prices or benefits. A price change "
              "applies from your next renewal after the notice period."),
        ("h", "7. Previous terms (for reference)"),
        ("p", "**Terms effective 1 January 2026 to 31 May 2026 (superseded on 1 June 2026):** Plus cost ₹129 per "
              "month or ₹1,199 per year and included free delivery on orders above ₹249. Members who joined before "
              "1 June 2026 moved to the current price at their first renewal after that date."),
        ("h", "8. Questions"),
        ("p", "Chat with QuickBasket Support in the app, or write to plus@quickbasket.example."),
    ]
    blocks += _plus_extra(ctx.rng("plus"))
    write_pdf(f"{out_dir}/{f}", "QuickBasket Plus: Membership Terms" + FOOT, blocks)
    for topic, says, v42 in [("Plus monthly price", "₹129 per month (previous terms, Jan–May 2026)", "₹149 per month (Section 6)"),
                             ("Plus yearly price", "₹1,199 per year (previous terms)", "₹1,299 per year (Section 6)"),
                             ("Plus free-delivery threshold", "Free delivery above ₹249 (previous terms)", "Above ₹199 (Section 6)")]:
        ctx.conflict(topic, f, "7. Previous terms", says, v42, "superseded terms section (dated)")
    return dict(file=f, title="QuickBasket Plus membership terms", kind="Membership T&Cs", fmt="PDF")


def gift_terms(ctx, out_dir):
    f = "09_gift_cards_and_qb_cash.pdf"
    blocks = [
        ("title", "Gift Cards and QuickBasket Cash", "Terms effective 1 October 2026"),
        ("h", "Part A. QuickBasket gift cards"),
        ("table", ["Topic", "Rule"], [
            ["Values", "₹250 to ₹10,000, in steps of ₹50."],
            ["Validity", "12 months from the date of purchase. The expiry date is shown on the card."],
            ["How to use", "Add the code under Account › Gift cards. The balance is used before other payment methods."],
            ["Refunds and exchanges", "Gift cards cannot be refunded or exchanged (Customer Policy, Section 3)."],
            ["Partial use", "Any unused balance stays on the card until it expires."],
            ["What you can't buy", "Other gift cards and QuickBasket Plus."],
            ["Lost codes", "An unredeemed code can be reissued once if the purchaser shows the purchase receipt. "
                           "Redeemed codes can't be reissued."],
            ["Orders paid by gift card", "If an order paid with a gift card is refunded, the refund goes back to the "
                                         "gift card balance, or to QuickBasket Cash if the card has expired."]], [42, 132]),
        ("h", "Part B. QuickBasket Cash"),
        ("p", "QuickBasket Cash is the wallet inside the app. It is used automatically at checkout unless you switch "
              "it off for an order. There are three kinds, shown separately in the wallet:"),
        ("table", ["Kind", "Where it comes from", "Expiry", "Limits"], [
            ["Refund Cash", "Refunds you chose to take as QuickBasket Cash, and cash-on-delivery refunds",
             "Never expires", "Can pay for up to 100% of an order"],
            ["Compensation Cash", "Late-delivery compensation (delivery fee refunds and the Plus ₹50)",
             "180 days after it is credited", "Can pay for up to 100% of an order"],
            ["Promotional Cash", "Cashback offers and referral rewards", "90 days after it is credited",
             "Can pay for up to 50% of an order"]], [32, 66, 36, 40]),
        ("ul", ["QuickBasket Cash can't be transferred to another account or withdrawn to a bank account. The only "
                "exception is a cash-on-delivery refund, which can be sent to a bank account on request in 5–7 "
                "business days (Customer Policy, Section 4).",
                "When QuickBasket Cash is used on an order that is later refunded, the refund returns to the same "
                "kind of QuickBasket Cash it came from, with its original expiry date.",
                "Promotional Cash from an offer is reversed if the order that earned it is refunded (see the offer's terms).",
                "QuickBasket Cash can't be used to buy gift cards or QuickBasket Plus."]),
        ("h", "Part C. Questions customers ask"),
        ("p", "**My compensation didn't show up.** Late-delivery compensation is credited automatically within "
              "2 hours of delivery. If it's missing after that, chat with Support with the order ID."),
        ("p", "**Can I get my QuickBasket Cash back in my bank?** No, except for cash-on-delivery refunds, which can "
              "be sent to a bank account on request."),
        ("p", "**My gift card expired yesterday. Can you extend it?** No. Expired gift cards can't be extended or refunded."),
    ]
    blocks += _gift_extra()
    write_pdf(f"{out_dir}/{f}", "Gift Cards and QuickBasket Cash" + FOOT, blocks)
    ctx.exception("QuickBasket Cash expiry", f, "Part B", "Refund Cash never expires; Compensation Cash 180 days; Promotional Cash 90 days, max 50% of an order",
                  "The Customer Policy says nothing about expiry or limits")
    return dict(file=f, title="Gift card and QuickBasket Cash terms", kind="Wallet T&Cs", fmt="PDF")


def payments(ctx, out_dir):
    f = "14_payments_cod_cancellations.md"
    text = "\n".join([
        "# Payments, Cash on Delivery and Cancellations", "",
        "*Fictional company for training use. All content synthetic. Last reviewed 2 October 2026.*", "",
        "This page explains how paying, cancelling and getting money back works in practice. The rules come from "
        "the Customer Policy v4.2 (Sections 4, 7 and 8); this page adds the practical details.", "",
        "## Ways to pay", "",
        md_table(["Method", "Available for", "Notes"], [
            ["UPI", "All orders", "Pay with any UPI app, or UPI autopay for Plus."],
            ["Credit or debit card", "All orders", "Saved cards are tokenised; we never store full card numbers."],
            ["QuickBasket Cash", "All orders", "Used first unless switched off. Promotional Cash covers at most 50% of an order."],
            ["Gift card balance", "All orders except Plus and gift cards", "Used before other methods."],
            ["Cash on delivery (COD)", "Orders up to ₹3,000", "Not available for gift cards, Plus, or addresses in Hinjewadi Phase 3 (Pune)."]]),
        "", "Net banking and pay-later services are not accepted.", "",
        "## Split payments", "",
        "An order can be paid partly with QuickBasket Cash or a gift card and partly with UPI, a card or cash on "
        "delivery. If the order is refunded, each part goes back to where it came from: the wallet part instantly, "
        "the UPI part in 2–4 business days, the card part in 5–7 business days.", "",
        "## Failed payments", "",
        "If money leaves your account but the order isn't placed, it is not a refund: your bank reverses the "
        "payment automatically, usually within 3–5 business days. If it hasn't come back after 5 business days, "
        "chat with Support and share the UPI reference number or the last four digits of the card.", "",
        "## Payment problems and what to do", "",
        md_table(["What the app shows", "What it means", "What to do"], [list(r) for r in PAY_ERRORS]), "",
        "## Refund timelines", "",
        "Once a refund is approved, the money goes back to the original payment method (Customer Policy, Section 4):", "",
        md_table(["Paid with", "Refund lands in"], [
            ["UPI", "2–4 business days, to the same UPI-linked bank account"],
            ["Credit or debit card", "5–7 business days, depending on the issuing bank"],
            ["QuickBasket Cash", "Instant"],
            ["Cash on delivery", "Instant, as QuickBasket Cash. Bank refund on request: 5–7 business days"]]),
        "", "Customers can choose to take any refund as QuickBasket Cash instead, which is instant.", "",
        "## Cancelling an order", "",
        md_table(["Order stage (shown in the app)", "Can I cancel?", "Fee"], [
            ["Placed, no delivery partner assigned yet", "Yes", "Free"],
            ["Delivery partner assigned, not picked up", "Yes", "₹25"],
            ["Picked up / out for delivery", "No", "–"],
            ["Delivered", "No (raise a return or refund request instead)", "–"]]),
        "", "If an order is out for delivery and you no longer want it, you can refuse it at the door. Once the "
        "order is marked delivered, you can request a refund for unopened items. Refunds are never issued for an "
        "order that hasn't been delivered yet.", "",
        "The ₹25 fee is deducted from the refund of a prepaid order. For cash-on-delivery orders, it is added to "
        "your next order and shown on the bill.", "",
        "## Tips for delivery partners", "",
        "- Tips are optional and go 100% to the delivery partner.",
        "- A tip is refunded in full if the order is cancelled before pickup.",
        "- Tips are not part of the order value for offers or free delivery.", "",
        "## Invoices and GST", "",
        "Every delivered order has a GST invoice under Orders › Invoice. Prices shown in the app include GST. "
        "Business customers can add a GSTIN under Account › Business details before ordering; it can't be added "
        "to an invoice afterwards.", "",
        "## Refund approvals (who decides)", "",
        "Support agents and the automated assistant can approve refunds of up to ₹500 per order, if the order "
        "belongs to the customer, is delivered and is eligible under the category rules. Above ₹500, the Customer "
        "Care Lead approves after reviewing photo evidence. An order that has already been refunded can't be "
        "refunded again, and a customer can hold at most three refunds in any 30-day period; further requests go "
        "to the Customer Care Lead (Customer Policy, Section 8).", "",
        "## Common questions", "",
        "**I cancelled after the partner was assigned. Why was I charged ₹25?**  ",
        "Cancelling is free only until a delivery partner is assigned. After that, a ₹25 fee applies until pickup.", "",
        "**Can I change the payment method after placing the order?**  ",
        "No. Cancel the order (free if no partner is assigned yet) and place it again.", "",
        "**I paid by UPI and chose QuickBasket Cash for my refund. Can I switch it to my bank?**  ",
        "No. Once a refund is credited as QuickBasket Cash, it stays in the wallet.", "",
        "**Is cash on delivery available for a ₹4,500 order?**  ",
        "No. Cash on delivery is available for orders up to ₹3,000.", "",
    ])
    write_md(f"{out_dir}/{f}", text)
    ctx.exception("Cash on delivery limit", f, "Ways to pay", "COD only for orders up to ₹3,000; not for gift cards, Plus or Hinjewadi Phase 3",
                  "Not in the Customer Policy")
    return dict(file=f, title="Payments, cash on delivery and cancellations", kind="Help page", fmt="Markdown")


def build(ctx, out_dir):
    return [plus_terms(ctx, out_dir), gift_terms(ctx, out_dir), payments(ctx, out_dir)]
