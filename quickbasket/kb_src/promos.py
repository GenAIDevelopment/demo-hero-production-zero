"""Promo terms and conditions: 24 campaigns, 12 expired and 12 active on 14 November 2026. PDF.
Bank and brand names are fictional."""
from . import promo_detail
from .common import pick
from .render import write_pdf

ALL = "All QuickBasket cities"
C = [  # name, code, start, end, status, offer, min order, max benefit, cities, payment, specific clauses
    dict(name="Summer Coolers", code="COOL15", start="1 April 2026", end="31 May 2026", expired=True,
         offer="15% off ice creams, juices and soft drinks", min="₹299", cap="₹90", cities=ALL, pay="Any",
         spec=["Applies only to items tagged 'Summer Coolers' in the app at the time of the order.",
               "Frozen items in this offer follow the Frozen & meat rules of the Customer Policy: report problems "
               "within 12 hours, with a photo of the packaging and the temperature label."]),
    dict(name="Back to School", code="SCHOOL20", start="1 June 2026", end="30 June 2026", expired=True,
         offer="20% off stationery and lunch boxes", min="₹399", cap="₹150", cities=ALL, pay="Any",
         spec=["Limited to five units of any single item per order.",
               "Stationery bought under this offer can be returned within 7 days if unused and in its original packaging."]),
    dict(name="Cricket Final Night", code="SIXER", start="14 June 2026", end="14 June 2026", expired=True,
         offer="Flat ₹75 off snacks and beverages from 6 pm to 11 pm", min="₹449", cap="₹75", cities=ALL, pay="Any",
         spec=["Valid only for orders placed between 6:00 pm and 11:00 pm on the day of the final.",
               "Promised delivery times may be longer during the match; late-delivery compensation still follows "
               "Section 5 of the Customer Policy."]),
    dict(name="Monsoon Munchies", code="RAINY15", start="1 July 2026", end="31 August 2026", expired=True,
         offer="15% off snacks, tea and instant noodles", min="₹299", cap="₹75", cities=ALL, pay="Any",
         spec=["Not valid during declared weather advisories when deliveries in the locality are paused.",
               "Discount applies to eligible items only; other items in the same order are charged at full price."]),
    dict(name="Freedom Sale", code="FREEDOM100", start="13 August 2026", end="16 August 2026", expired=True,
         offer="Flat ₹100 off", min="₹799", cap="₹100", cities=ALL, pay="Any",
         spec=["One use per account during the sale.",
               "Not valid on electronics priced above ₹2,999."]),
    dict(name="Onam Sadya Specials", code="ONAM10", start="25 August 2026", end="5 September 2026", expired=True,
         offer="10% off banana leaves, rice, coconut and sadya essentials", min="₹499", cap="₹120",
         cities="Bengaluru and Chennai", pay="Any",
         spec=["Fresh items in this offer (banana leaves, vegetables) follow the Fresh fruits & vegetables rules: "
               "report within 24 hours, photo required.",
               "Not available in Kochi, where QuickBasket does not deliver yet."]),
    dict(name="Modak Fest", code="MODAK", start="27 August 2026", end="6 September 2026", expired=True,
         offer="Free box of 6 modaks on sweets orders of ₹499 or more", min="₹499 (sweets)", cap="One free box",
         cities="Mumbai, Pune and Hyderabad", pay="Any",
         spec=["The free box is added automatically while stocks last.",
               "Free items are not returnable and are not refunded. If the whole order is returned, the free box "
               "is not charged back."]),
    dict(name="Navratri Fasting Essentials", code="VRAT12", start="2 October 2026", end="11 October 2026",
         expired=True, offer="12% off sabudana, kuttu atta, rock salt and fasting snacks", min="₹349", cap="₹100",
         cities=ALL, pay="Any",
         spec=["Packaged items bought under this offer follow the Packaged food & beverages rules: returnable "
               "within 7 days if unopened and before expiry."]),
    dict(name="Durga Puja Delights", code="PUJO", start="9 October 2026", end="13 October 2026", expired=True,
         offer="₹60 off sweets and festive snacks", min="₹399", cap="₹60", cities=ALL, pay="Any",
         spec=["Valid once per account per day during the campaign."]),
    dict(name="Diwali Dhamaka", code="DIWALI10", start="25 October 2026", end="5 November 2026", expired=True,
         offer="10% cashback as QuickBasket Cash", min="₹999", cap="₹200", cities=ALL, pay="Any",
         spec=["Cashback is credited as QuickBasket Cash within 48 hours of delivery.",
               "Cashback is promotional QuickBasket Cash: it expires 90 days after it is credited.",
               "**If the order is refunded, in full or in part, the cashback is reversed** (for a partial refund, "
               "in proportion to the refunded amount). If the cashback has already been spent, the reversed "
               "amount is deducted from the refund.",
               "The campaign ended on 5 November 2026. Orders placed after that date don't earn this cashback, "
               "even if the code is still saved in the app."]),
    dict(name="Dhanteras Electronics Deal", code="DHAN300", start="31 October 2026", end="2 November 2026",
         expired=True, offer="Extra ₹300 off electronics", min="₹2,999 (electronics)", cap="₹300", cities=ALL,
         pay="Deccan Pay Bank credit cards only",
         spec=["Electronics bought under this offer follow the normal electronics rules: 3 days, replacement "
               "first, refund only if no replacement stock.",
               "If the order is refunded, the refund is the amount actually paid, after the ₹300 discount."]),
    dict(name="Plus Trial Spring", code="PLUSTRY", start="1 March 2026", end="31 March 2026", expired=True,
         offer="First month of QuickBasket Plus for ₹1", min="None", cap="One month", cities=ALL, pay="UPI autopay or card",
         spec=["After the trial month, Plus renews at the regular price unless cancelled.",
               "Only for accounts that have never had Plus."]),
    dict(name="First Order", code="FIRST100", start="1 January 2026", end="31 March 2027", expired=False,
         offer="Flat ₹100 off your first order", min="₹299", cap="₹100", cities=ALL, pay="Any",
         spec=["Only for an account's first delivered order. One use per account, device and UPI ID.",
               "If the first order is cancelled before a delivery partner is assigned, the code becomes usable again "
               "within 24 hours.",
               "Can't be combined with the waitlist launch offer in new cities."]),
    dict(name="Refer and Earn", code="(personal referral link)", start="1 January 2026", end="Until further notice",
         expired=False, offer="₹100 QuickBasket Cash each for you and your friend", min="Friend's first order of ₹299",
         cap="₹1,000 per month for the referrer", cities=ALL, pay="Any",
         spec=["Both rewards are credited after the friend's first order is delivered and not cancelled.",
               "If the friend's first order is refunded in full, both rewards are reversed.",
               "Referral QuickBasket Cash is promotional: it expires 90 days after it is credited."]),
    dict(name="Wedding Season Bulk Saver", code="SHAADI8", start="10 November 2026", end="28 February 2027",
         expired=False, offer="8% off large orders", min="₹2,499", cap="₹400", cities=ALL, pay="Any",
         spec=["Excludes electronics, gift cards and QuickBasket Plus.",
               "Large orders may be split into two deliveries; the promised time applies to the last delivery."]),
    dict(name="Cricket Nights", code="(automatic)", start="1 November 2026", end="31 December 2026", expired=False,
         offer="Free delivery from 7 pm to 11 pm on international match days", min="₹149", cap="One delivery fee",
         cities=ALL, pay="Any",
         spec=["Match days are listed on the offer banner in the app.",
               "Removes the delivery fee only; the Delhi NCR late-night surcharge (after 11 pm) is not covered."]),
    dict(name="Children's Day Treats", code="BACHPAN", start="12 November 2026", end="16 November 2026",
         expired=False, offer="₹50 off chocolates, juices and baby snacks", min="₹349", cap="₹50", cities=ALL, pay="Any",
         spec=["Baby food bought under this offer is not returnable, as in the Baby care rules of the Customer Policy."]),
    dict(name="Konkan Card Tuesdays", code="KONKAN10", start="1 September 2026", end="31 December 2026",
         expired=False, offer="10% instant discount every Tuesday", min="₹699", cap="₹150", cities=ALL,
         pay="Konkan Card credit and debit cards only",
         spec=["Once per card per Tuesday.",
               "For card refunds, the refund lands in 5–7 business days, as in Section 4 of the Customer Policy."]),
    dict(name="TrustLine No-Cost EMI", code="(automatic at checkout)", start="1 October 2026", end="31 March 2027",
         expired=False, offer="No-cost EMI for 3 or 6 months on electronics", min="₹3,000 (electronics)",
         cap="Interest waived", cities=ALL, pay="TrustLine Bank credit cards only",
         spec=["If the order is replaced, the EMI continues unchanged. If it is refunded, TrustLine Bank cancels the "
               "EMI plan and reverses the amount; the bank may take up to two billing cycles.",
               "Electronics follow the normal rules: 3 days, replacement first."]),
    dict(name="Winter Wellness", code="WINTER15", start="1 November 2026", end="31 January 2027", expired=False,
         offer="15% off personal care and wellness", min="₹499", cap="₹120", cities=ALL, pay="Any",
         spec=["Opened personal care items can be returned only if damaged on arrival, as in the Customer Policy."]),
    dict(name="Plus Trial Winter", code="PLUS49", start="1 November 2026", end="30 November 2026", expired=False,
         offer="First month of QuickBasket Plus for ₹49", min="None", cap="One month", cities=ALL,
         pay="UPI autopay or card",
         spec=["Only for accounts that have never had Plus.",
               "The trial follows the normal Plus cancellation rules (Customer Policy, Section 6): cancel within 48 "
               "hours for a full refund of the ₹49 if no free delivery has been used.",
               "After the trial month, Plus renews at ₹149 per month unless cancelled."]),
    dict(name="Free Gift Mondays", code="(automatic)", start="2 November 2026", end="28 December 2026",
         expired=False, offer="Free 1 kg pack of atta on orders of ₹999 or more on Mondays", min="₹999", cap="One pack",
         cities=ALL, pay="Any",
         spec=["**The free gift is not returnable and is not refunded.** Returning it does not change the refund "
               "for the rest of the order.",
               "If returns take the order below ₹999, the free gift is not charged back."]),
    dict(name="Weekend Free Delivery", code="(automatic)", start="7 November 2026", end="27 December 2026",
         expired=False, offer="Free delivery on Saturdays and Sundays", min="₹149", cap="One delivery fee",
         cities=ALL, pay="Any",
         spec=["If an order with free delivery arrives late, there is no delivery fee to refund. Late compensation "
               "for Plus members (₹50 for more than 30 minutes) still applies."]),
    dict(name="Fresh Friday", code="(automatic)", start="1 January 2026", end="Until further notice", expired=False,
         offer="20% off fruits and vegetables every Friday", min="₹249", cap="₹60", cities=ALL, pay="Any",
         spec=["Discounted fruits and vegetables follow the normal rules: report problems within 24 hours with a photo.",
               "A refund for a discounted item is the discounted price actually paid."]),
]

GENERAL = [  # (topic, [phrasings])
    ("one_offer", ["Only one offer can be applied to an order, unless the offer says otherwise.",
                   "Offers can't be combined. If more than one could apply, the app applies the one with the higher benefit.",
                   "This offer can't be used together with any other code or automatic offer."]),
    ("refund_paid", ["Returns and refunds follow the Customer Policy v4.2. Any refund is the amount actually paid, after the discount.",
                     "If an item is refunded, the refund is the price you paid after this offer, not the original price.",
                     "Refund amounts are always based on what was paid, after discounts, under the Customer Policy."]),
    ("no_gift", ["Not valid on gift cards or QuickBasket Plus purchases.",
                 "Gift cards and QuickBasket Plus memberships are excluded.",
                 "The offer does not apply to gift card or Plus purchases."]),
    ("cities", ["Valid only in cities where QuickBasket delivers today.",
                "Available only for delivery addresses QuickBasket serves; not in Kochi or Jaipur before launch.",
                "Only orders to serviceable addresses qualify."]),
    ("withdraw", ["QuickBasket may change or end this offer early with notice in the app. Orders already placed keep the benefit.",
                  "We may withdraw the offer at any time; this doesn't affect orders placed before the change.",
                  "The offer can be ended early. Orders placed before that keep the benefit shown at checkout."]),
    ("abuse", ["Accounts that misuse offers (for example several accounts on one device) may lose the benefit and be reviewed.",
               "Misuse, including fake accounts or repeated refund requests to keep offer benefits, may lead to the benefit being withdrawn.",
               "If we see offer misuse, the benefit can be withdrawn and the account reviewed by the Customer Care team."]),
    ("cancel", ["If an order is cancelled free of charge before a delivery partner is assigned, the offer is restored within 24 hours.",
                "Cancelling before a partner is assigned restores the offer to your account within a day.",
                "A cancelled order doesn't use up the offer if it is cancelled before a delivery partner is assigned."]),
    ("min", ["The minimum order value is calculated after other discounts and before delivery fees.",
             "Minimum order value: item total after discounts, excluding delivery fees, surcharges and tips.",
             "Delivery fees, tips and surcharges don't count towards the minimum order value."]),
    ("tax", ["Prices include GST. The discount is applied before GST is shown on the invoice.",
             "The invoice shows the discount as a separate line; GST is included in prices.",
             "All prices shown include taxes."]),
    ("disputes", ["Questions or disputes about this offer go to QuickBasket Support in the app; unresolved disputes are handed to a human agent.",
                  "If you disagree with how an offer was applied, chat with Support. A human agent reviews disputes.",
                  "Disputes are handled by QuickBasket Support and escalated to a human agent if needed."]),
    ("stock", ["Offer items are subject to stock at the store that serves your address.",
               "Availability depends on the store covering your address.",
               "If an offer item is out of stock, the offer can't be substituted with another item."]),
    ("late", ["Late-delivery compensation follows Section 5 of the Customer Policy and isn't changed by this offer.",
              "This offer doesn't change late-delivery compensation, which is credited as QuickBasket Cash under Section 5.",
              "Delivery promises and compensation for late orders are unchanged by this offer."]),
    ("account", ["One account per person. The offer is linked to the account that places the order.",
                 "The benefit belongs to the account that placed the order and can't be transferred.",
                 "Offers can't be transferred between accounts."]),
    ("display", ["The benefit is shown on the checkout screen before payment. If it isn't shown, it hasn't been applied.",
                 "Check the bill summary before paying: an applied offer appears as its own line.",
                 "If the offer line isn't on the bill at checkout, the offer was not applied to that order."]),
    ("law", ["These terms are governed by the laws of India. Fictional company: these terms exist for training only.",
             "Governed by Indian law. QuickBasket is a fictional company used for training.",
             "Indian law applies. This is a fictional company for training use."]),
]


def build(ctx, out_dir):
    rng = ctx.rng("promos")
    blocks = [("title", "QuickBasket Offers: Terms and Conditions",
               f"All campaigns from 1 January 2026 · Status as of 14 November 2026 · {len(C)} campaigns"),
              ("p", "This document collects the terms and conditions of every QuickBasket offer run since 1 January "
                    "2026. Expired campaigns are kept for customers asking about past orders. Offers never change "
                    "the Customer Policy v4.2: windows, refund timelines and approval limits stay the same unless a "
                    "campaign says so explicitly."),
              ("table", ["Campaign", "Code", "Valid", "Status"],
               [[c["name"], c["code"], f"{c['start']} – {c['end']}", "Expired" if c["expired"] else "Active"] for c in C],
               [52, 40, 58, 24]),
              ]
    for i, c in enumerate(C, 1):
        status = "EXPIRED" if c["expired"] else "ACTIVE"
        blocks += [("h", f"{i}. {c['name']} ({status})"),
                   ("table", ["Item", "Details"], [
                       ["Offer", c["offer"]], ["Code", c["code"]], ["Valid", f"{c['start']} to {c['end']}"],
                       ["Minimum order", c["min"]], ["Maximum benefit", c["cap"]], ["Cities", c["cities"]],
                       ["Payment method", c["pay"]]], [40, 134]),
                   ("h3", "Terms specific to this offer")]
        blocks.append(("ol", c["spec"]))
        calc, cats = promo_detail.DETAIL[c["name"]]
        blocks += [("h3", pick(rng, ["How to use it", "How to get this offer", "Steps"])),
                   ("ol", pick(rng, promo_detail.STEPS))]
        blocks += promo_detail.examples(calc, rng)
        blocks += promo_detail.items(cats, rng)
        blocks.append(("h3", pick(rng, ["General terms", "Standard terms", "Other terms"])))
        topics = GENERAL[:]
        rng.shuffle(topics)
        chosen = topics[:rng.randint(10, 13)]
        blocks.append(("ol", [pick(rng, phr) for _, phr in chosen]))
    f = "07_promo_terms.pdf"
    write_pdf(f"{out_dir}/{f}", "QuickBasket Offers: Terms and Conditions · Fictional company for training use. "
                                "All content synthetic.", blocks)
    ctx.exception("Diwali cashback reversal", f, "10. Diwali Dhamaka",
                  "Cashback reversed if the order is refunded (in proportion for partial refunds); deducted from the refund if already spent",
                  "A refund on a Diwali order is smaller than the item price")
    ctx.exception("Free gifts", f, "Modak Fest, Free Gift Mondays",
                  "Free gift items are not returnable and not refunded", "Adds a rule the Customer Policy doesn't have")
    ctx.exception("Plus trial cancellation", f, "21. Plus Trial Winter",
                  "₹49 trial follows the 48-hour Plus cancellation rule", "Consistent with Section 6; confirms the trial fee is refundable within 48 hours")
    ctx.exception("Promotional QuickBasket Cash expiry", f, "Diwali Dhamaka, Refer and Earn",
                  "Cashback and referral QuickBasket Cash expire 90 days after credit", "The Customer Policy says nothing about expiry")
    return [dict(file=f, title="Promo terms and conditions (24 campaigns)", kind="Offer T&Cs", fmt="PDF")]
