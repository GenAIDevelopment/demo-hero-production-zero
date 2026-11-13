"""City addenda (one Markdown document, six cities) and the "coming soon" page. Fictional company;
localities are real place names, stores and fees are invented."""
from .common import pick
from .render import md_table, write_md

CITIES = [
    dict(name="Hyderabad", since="March 2023", first=True, prefix="HYD",
         localities=["Gachibowli", "Madhapur", "HITEC City", "Kondapur", "Kukatpally", "Miyapur", "Banjara Hills",
                     "Jubilee Hills", "Begumpet", "Secunderabad", "Ameerpet", "Manikonda", "Nanakramguda", "Kokapet",
                     "Narsingi", "Tolichowki", "Mehdipatnam", "Himayatnagar", "Abids", "Dilsukhnagar", "LB Nagar",
                     "Uppal", "Habsiguda", "Tarnaka", "Malkajgiri", "Kompally", "Bachupally", "Nizampet",
                     "Chandanagar", "Lingampally", "Attapur", "Kothapet"],
         hours="6:00 am to 1:00 am", fee_small="₹35", fee_mid="₹19", free_from="₹499",
         weather="Heavy-rain advisories (mostly July to October). Waterlogging-prone underpasses are avoided automatically.",
         local=[
             ("Gated communities", "Many large communities in Gachibowli, Kondapur, Kokapet and Narsingi require an "
              "entry OTP at the gate. Delivery partners wait up to 7 minutes at the gate for entry. Time spent waiting "
              "for gate entry counts as a customer-side delay under Section 5 of the Customer Policy."),
             ("Old City", "Parts of Abids and the area around Charminar are served by bicycle partners during evening "
              "peak hours. Promised delivery times shown at checkout already include this."),
             ("Tech parks", "Inside HITEC City and Nanakramguda office campuses, orders are handed over at the "
              "reception or the visitor desk, not at individual desks."),
         ],
         faq=[("Why does my promised time change in the evening?", "Between 7 pm and 10 pm the app recalculates "
               "promised times every few minutes based on traffic on the Outer Ring Road and inner-city roads. "
               "The time shown when you place the order is the one used for late-delivery compensation."),
              ("Can I order from Secunderabad if my office is in Gachibowli?", "Orders are served by the store that "
               "covers the delivery address, so you can order to any serviceable address in the city.")]),
    dict(name="Bengaluru", since="August 2023", prefix="BLR",
         localities=["Koramangala", "Indiranagar", "HSR Layout", "BTM Layout", "Jayanagar", "JP Nagar", "Whitefield",
                     "Marathahalli", "Bellandur", "Sarjapur Road", "Electronic City", "Hebbal", "Yelahanka",
                     "Malleshwaram", "Rajajinagar", "Basavanagudi", "Banashankari", "Hennur", "Kalyan Nagar",
                     "Frazer Town", "Domlur", "Ulsoor", "MG Road", "Bannerghatta Road", "Kengeri", "Vijayanagar",
                     "RT Nagar", "Sahakar Nagar", "KR Puram", "Brookefield"],
         hours="6:00 am to 1:00 am", fee_small="₹35", fee_mid="₹19", free_from="₹499",
         weather="Heavy-rain advisories (May to October). Some low-lying roads near Bellandur and Silk Board are "
                 "paused during declared advisories.",
         local=[
             ("QB Tech Hub same-day swaps", "Three Bengaluru stores are QB Tech Hubs: Koramangala (BLR-01), Whitefield "
              "(BLR-04) and HSR Layout (BLR-03). For electronics bought from these stores, an approved replacement "
              "inside the 3-day window is delivered the same day if the request is approved before 6 pm. This "
              "changes only how fast the replacement arrives; the 3-day window and the other electronics rules in "
              "the Customer Policy stay the same."),
             ("Apartment towers", "In large apartment complexes on Sarjapur Road and in Whitefield, partners come "
              "to the flat door if the association allows it, otherwise to the lobby."),
             ("Tech parks", "In Electronic City and the Outer Ring Road tech parks, deliveries go to the security "
              "desk of the building named in the address."),
         ],
         faq=[("Is same-day replacement available for all electronics?", "Only for electronics bought from the three "
               "QB Tech Hub stores, and only when the replacement is approved before 6 pm within the 3-day window."),
              ("Why can't I see some items in Yelahanka?", "Each store carries a slightly different range. The app only "
               "shows items the store covering your address has in stock.")]),
    dict(name="Chennai", since="January 2024", prefix="CHN",
         localities=["T. Nagar", "Adyar", "Velachery", "Anna Nagar", "Mylapore", "Nungambakkam", "Besant Nagar",
                     "Thiruvanmiyur", "Perungudi", "Sholinganallur", "Porur", "Vadapalani", "Kodambakkam", "Guindy",
                     "Tambaram", "Chromepet", "Pallavaram", "Medavakkam", "Ashok Nagar", "KK Nagar", "Royapettah",
                     "Egmore", "Kilpauk", "Perambur", "Ambattur", "Mogappair", "Valasaravakkam", "Alwarpet"],
         hours="6:00 am to midnight", fee_small="₹30", fee_mid="₹15", free_from="₹449",
         weather="Cyclone and heavy-rain advisories (mainly October to December, the northeast monsoon).",
         local=[
             ("Cyclone advisory: longer reporting window", "When QuickBasket declares a cyclone or heavy-rain advisory "
              "for Chennai, the reporting window for Fresh fruits & vegetables, Dairy, bakery & eggs, and Frozen & "
              "meat is extended to 48 hours for orders delivered during the advisory. All other conditions (photo, "
              "not returnable, refund or replacement only) stay the same. Late-delivery compensation does not apply "
              "during a declared advisory, as in Section 5 of the Customer Policy."),
             ("Coastal roads", "During high-tide warnings, East Coast Road and Besant Nagar beach-side lanes may be "
              "served by a different store, which can change the promised time."),
             ("OMR offices", "On the Old Mahabalipuram Road (Perungudi to Sholinganallur) offices, orders are handed "
              "over at the building reception."),
         ],
         faq=[("Is the 48-hour window available all year?", "No. It applies only to orders delivered while a cyclone or "
               "heavy-rain advisory is declared for Chennai. At other times the normal windows in the Customer Policy "
               "apply: 24 hours for fresh produce and dairy, 12 hours for frozen food and meat."),
              ("How do I know an advisory is active?", "A banner appears at the top of the app and on the order page "
               "while an advisory is declared for your city.")]),
    dict(name="Pune", since="May 2024", prefix="PUN",
         localities=["Kothrud", "Baner", "Aundh", "Hinjewadi", "Wakad", "Pimple Saudagar", "Viman Nagar",
                     "Kalyani Nagar", "Koregaon Park", "Kharadi", "Hadapsar", "Magarpatta", "Wanowrie", "Kondhwa",
                     "NIBM Road", "Camp", "Shivajinagar", "Deccan", "Karve Nagar", "Warje", "Bavdhan", "Pashan",
                     "Balewadi", "Yerawada", "Sinhagad Road", "Katraj", "Bibwewadi", "Undri"],
         hours="6:30 am to midnight", fee_small="₹30", fee_mid="₹15", free_from="₹449",
         weather="Monsoon advisories (June to September), especially for the ghat-side areas near Warje and Bavdhan.",
         local=[
             ("Hinjewadi Phase 3: no cash on delivery", "Cash on delivery is not available for addresses in Hinjewadi "
              "Phase 3, because partners cannot carry cash into the IT-park security zone. UPI, cards and "
              "QuickBasket Cash work as usual."),
             ("Hinjewadi Phases 1 and 2", "Deliveries go to the main gate reception of the campus named in the address."),
             ("Housing societies", "Most societies in Baner, Wakad and Kharadi need the customer to approve the partner "
              "on the society's visitor app. Waiting for approval counts as a customer-side delay."),
         ],
         faq=[("Why can't I choose cash on delivery?", "If your address is in Hinjewadi Phase 3, cash on delivery isn't "
               "offered. Everywhere else in Pune it is available for orders up to the normal cash-on-delivery limit."),
              ("Do you deliver to Pimpri and Chinchwad?", "Pimple Saudagar and Wakad are covered. Other parts of "
               "Pimpri-Chinchwad are not serviceable yet.")]),
    dict(name="Mumbai", since="October 2024", prefix="MUM",
         localities=["Andheri West", "Andheri East", "Bandra West", "Khar", "Santacruz", "Juhu", "Vile Parle",
                     "Goregaon", "Malad", "Kandivali", "Borivali", "Powai", "Ghatkopar", "Chembur", "Kurla", "Dadar",
                     "Worli", "Lower Parel", "Prabhadevi", "Colaba", "Fort", "Matunga", "Sion", "Mulund", "Bhandup",
                     "Vikhroli", "Thane West", "Vashi", "Kharghar", "Nerul"],
         hours="6:00 am to 1:00 am", fee_small="₹39", fee_mid="₹25", free_from="₹549",
         weather="Monsoon advisories (June to September), including red-alert days.",
         local=[
             ("Red-alert days", "On days the city is under a red alert for heavy rain, deliveries to low-lying "
              "localities (parts of Kurla, Sion, Andheri East and Dahisar side lanes) may be paused. The app shows "
              "the pause before checkout, so no order is accepted that can't be delivered. Late-delivery "
              "compensation does not apply during a declared advisory."),
             ("Old buildings without lifts", "In older buildings in Dadar, Matunga and Fort without lifts, heavy "
              "orders (over 15 kg) are delivered to the ground floor unless the customer asks for doorstep delivery "
              "in the order notes."),
             ("Navi Mumbai and Thane", "Vashi, Nerul, Kharghar and Thane West are served by their own stores, so the "
              "range can differ from the main city stores."),
         ],
         faq=[("Why is the delivery fee higher in Mumbai?", "Mumbai fees reflect longer travel times and higher store "
               "costs. Plus members still get free delivery on orders above ₹199."),
              ("Will my order be accepted on a red-alert day?", "Only if your locality isn't paused. If it is, the app "
               "tells you before you pay.")]),
    dict(name="Delhi NCR", since="February 2026", prefix="DEL",
         localities=["Connaught Place", "Karol Bagh", "Rajouri Garden", "Janakpuri", "Dwarka", "Vasant Kunj", "Saket",
                     "Hauz Khas", "Greater Kailash", "Lajpat Nagar", "Defence Colony", "Mayur Vihar", "Preet Vihar",
                     "Rohini", "Pitampura", "Model Town", "Noida Sector 18", "Noida Sector 62", "Noida Sector 137",
                     "Greater Noida West", "Gurugram DLF Phase 1", "Gurugram DLF Phase 4", "Gurugram Sohna Road",
                     "Gurugram Golf Course Road", "Gurugram Sector 56", "Indirapuram", "Vaishali", "Faridabad Sector 15"],
         hours="24 hours at four stores (DEL-01, DEL-03, DEL-06, DEL-08); 6:00 am to 1:00 am elsewhere",
         fee_small="₹35", fee_mid="₹19", free_from="₹499",
         weather="Fog advisories (December to January) and air-quality advisories when partners' outdoor work is limited.",
         local=[
             ("Late-night surcharge", "Orders placed between 11:00 pm and 6:00 am from the four 24-hour stores carry a "
              "late-night surcharge of ₹35. It applies to all customers, including QuickBasket Plus members, and is "
              "shown before payment. It is separate from the delivery fee, so Plus free delivery does not remove it."),
             ("Fog advisories", "During declared fog advisories, promised delivery times are extended and late-delivery "
              "compensation does not apply, as in Section 5 of the Customer Policy."),
             ("Gurugram and Noida towers", "Large residential towers in Gurugram and Noida usually require gate entry "
              "through the society's visitor app; waiting for entry counts as a customer-side delay."),
         ],
         faq=[("Do Plus members pay the late-night surcharge?", "Yes. The ₹35 late-night surcharge applies to everyone. "
               "Plus free delivery covers the delivery fee only."),
              ("Which stores are open all night?", "DEL-01 Connaught Place, DEL-03 Saket, DEL-06 Gurugram DLF Phase 4 "
               "and DEL-08 Noida Sector 18.")]),
]

NOTES = ["Gate OTP needed in most communities", "Lift access usually allowed", "Narrow lanes: two-wheeler only",
         "Office campuses: reception handover", "Heavy evening traffic", "Society visitor app approval",
         "Serviced by bicycle partners at peak", "Ground-floor handover in older buildings", "Fast lane: under 12 minutes",
         "Parking for partners at the main gate only", "Large housing societies", "Mixed residential and market area"]
ETAS = ["10–14 min", "12–16 min", "12–18 min", "14–20 min", "15–22 min", "16–24 min"]

INTROS = [
    "This addendum adds {city}-specific details to the Customer Policy v4.2. Where it states an exception, the "
    "exception applies in {city} only; everything else follows the Customer Policy.",
    "These notes cover how QuickBasket works in {city}: where we deliver, which store serves you, what delivery "
    "costs and the local rules. They add to the Customer Policy v4.2 and apply only in {city}.",
    "Use this page for anything specific to {city}. The Customer Policy v4.2 still applies in full; the rules "
    "below are local additions, and any exception is limited to {city}.",
]
FEE_LINES = [
    "Delivery fees depend on the order value after discounts:",
    "What you pay for delivery in {city} depends on the order total (after any discount):",
    "The delivery fee is set by the order value, after offers are applied:",
]


HOLIDAYS = [("Sunday 15 November 2026", "Normal hours"), ("Friday 25 December 2026", None),
            ("Thursday 31 December 2026", "Normal hours; expect longer promised times after 8 pm"),
            ("Friday 1 January 2027", None), ("Thursday 14 January 2027", None), ("Tuesday 26 January 2027", None)]
HOLIDAY_HOURS = ["Normal hours", "Opens at 8:00 am, normal closing time", "Normal opening time, closes at 10:00 pm",
                 "Normal hours; fresh produce range may be smaller"]
PEAKS = [("6:00 am to 9:00 am", "Morning milk and bread rush", ["12–16 min", "12–18 min", "14–18 min"]),
         ("9:00 am to 5:00 pm", "Quiet hours", ["10–14 min", "10–15 min", "12–15 min"]),
         ("5:00 pm to 7:00 pm", "Evening build-up", ["14–20 min", "15–20 min", "15–22 min"]),
         ("7:00 pm to 10:00 pm", "Evening peak", ["18–26 min", "18–28 min", "20–28 min"]),
         ("After 10:00 pm", "Late evening", ["12–18 min", "14–18 min", "14–20 min"])]
SERVICES = ["Fresh produce, dairy, frozen", "Full range including electronics", "Groceries and household only",
            "Full range; electronics by next-slot transfer", "Full range including baby care and personal care"]


def _hours_and_peaks(c, stores, rng):
    city = c["name"]
    L = ["### What each store carries", "",
         "Each store stocks a slightly different range. The app only shows what the store covering your address has.", "",
         md_table(["Store", "Range", "Cold storage", "Returns pickup from this store"],
                  [[s[0], "Full range including electronics" if "Tech Hub" in s[2] else pick(rng, SERVICES),
                    "Chilled and frozen", pick(rng, ["Yes", "Yes", "Yes, 8 am to 9 pm"])] for s in stores]), "",
         "### Busy times", "",
         pick(rng, ["Promised times are longer when more people are ordering. Typical promised times in {city}:",
                    "How long delivery usually takes in {city}, by time of day:",
                    "Typical promised delivery times in {city} through the day:"]).format(city=city), "",
         md_table(["Time of day", "What's happening", "Typical promised time"],
                  [[t, what, pick(rng, etas)] for t, what, etas in PEAKS]), "",
         "The promised time shown at checkout is the one that counts for late-delivery compensation, not these averages.", "",
         "### Planned changes to store hours", "",
         md_table(["Date", f"{city} stores"], [[d, h or pick(rng, HOLIDAY_HOURS)] for d, h in HOLIDAYS]), "",
         "On every other day, stores keep their normal hours.", ""]
    return L


def _city_section(c, rng):
    city = c["name"]
    stores = []
    locs = c["localities"]
    n_stores = 6 if len(locs) >= 30 else 5
    for i in range(n_stores):
        hub = locs[(i * len(locs)) // n_stores]
        stores.append([f"{c['prefix']}-{i + 1:02d}", hub, pick(rng, ["Dark store", "Dark store", "Dark store and pickup point"]),
                       c["hours"] if "24 hours" not in c["hours"] else
                       ("24 hours" if i + 1 in (1, 3, 6, 8) else "6:00 am to 1:00 am")])
    if city == "Delhi NCR":
        stores = [[f"DEL-{i:02d}", h, "Dark store", "24 hours" if i in (1, 3, 6, 8) else "6:00 am to 1:00 am"]
                  for i, h in enumerate(["Connaught Place", "Rajouri Garden", "Saket", "Dwarka", "Rohini",
                                         "Gurugram DLF Phase 4", "Gurugram Sohna Road", "Noida Sector 18",
                                         "Noida Sector 62", "Indirapuram"], 1)]
    if city == "Bengaluru":
        stores[0][1], stores[2][1], stores[3][1] = "Koramangala", "HSR Layout", "Whitefield"
        for s in (stores[0], stores[2], stores[3]):
            s[2] = "Dark store, QB Tech Hub"
    rows = []
    for i, loc in enumerate(locs):
        store = stores[min(i * len(stores) // len(locs), len(stores) - 1)][0]
        rows.append([loc, store, pick(rng, ETAS), pick(rng, NOTES)])
    lines = [f"## {city}", "", pick(rng, INTROS).format(city=city), "",
             f"**Serving since:** {c['since']}{' (QuickBasket’s first city)' if c.get('first') else ''}  ",
             f"**Store hours:** {c['hours']}  ",
             f"**Customer support:** in-app chat, 7:00 am to midnight, every day", "",
             "### Stores", "", md_table(["Store", "Area", "Type", "Hours"], stores), "",
             "### Delivery fees", "", pick(rng, FEE_LINES).format(city=city), "",
             md_table(["Order value (after discounts)", "Delivery fee", "QuickBasket Plus members"], [
                 ["Below ₹199", c["fee_small"], c["fee_small"]],
                 [f"₹199 to {c['free_from']}", c["fee_mid"], "Free (orders above ₹199)"],
                 [f"Above {c['free_from']}", "Free", "Free"]]), "",
             "Fees are shown before payment. When a late-delivery refund of the delivery fee applies (Customer "
             "Policy, Section 5), it is the fee shown in this table for that order.", "",
             "### Local rules", ""]
    for title, text in c["local"]:
        lines += [f"**{title}.** {text}", ""]
    lines += _hours_and_peaks(c, stores, rng)
    lines += ["### Weather and traffic", "", c["weather"] + " Advisories are declared by QuickBasket City Operations "
              "and shown as a banner in the app. During a declared advisory, late-delivery compensation does not "
              "apply (Customer Policy, Section 5).", "",
              "### Where we deliver", "",
              f"{len(locs)} localities are serviceable in {city} today. Typical times are averages over the last "
              "four weeks; your promised time is always the one shown at checkout.", "",
              md_table(["Locality", "Served from", "Typical delivery time", "Notes"], rows), "",
              f"### Common questions in {city}", ""]
    for q, a in c["faq"]:
        lines += [f"**{q}**  ", a, ""]
    return "\n".join(lines)


def build(ctx, out_dir):
    rng = ctx.rng("cities")
    parts = ["# QuickBasket City Addenda", "",
             "*Fictional company for training use. All content synthetic. Last updated 5 November 2026.*", "",
             "QuickBasket operates in six cities. Each section below adds local details to the **Customer Policy "
             "v4.2** (effective 1 October 2026): stores, delivery fees, serviceable localities and local rules. "
             "The Customer Policy always applies; an exception written here applies only in that city.", ""]
    parts += [_city_section(c, rng) for c in CITIES]
    write_md(f"{out_dir}/05_city_addenda.md", "\n".join(parts))
    f = "05_city_addenda.md"
    ctx.exception("Chennai cyclone advisory", f, "Chennai › Local rules",
                  "Fresh, dairy and frozen/meat report window extended to 48 hours for orders delivered during a declared cyclone or heavy-rain advisory in Chennai",
                  "Changes the answer only in Chennai, only during an advisory")
    ctx.exception("Delhi NCR late-night surcharge", f, "Delhi NCR › Local rules",
                  "₹35 surcharge on orders placed 11 pm–6 am from the four 24-hour stores, for everyone including Plus",
                  "Plus free delivery doesn't remove it")
    ctx.exception("Bengaluru QB Tech Hub swaps", f, "Bengaluru › Local rules",
                  "Same-day replacement for electronics from BLR-01/03/04 if approved before 6 pm within the 3-day window",
                  "Speed only; the 3-day window is unchanged")
    ctx.exception("Pune Hinjewadi Phase 3", f, "Pune › Local rules", "No cash on delivery in Hinjewadi Phase 3",
                  "COD answer depends on the address")
    ctx.exception("Delivery fee amounts", f, "each city › Delivery fees",
                  "Fee slabs per city (e.g. Mumbai ₹39 below ₹199); not stated in the Customer Policy",
                  "Fee questions are answerable only from this document")
    soon = _coming_soon(rng)
    write_md(f"{out_dir}/06_coming_soon_cities.md", soon)
    ctx.exception("Kochi and Jaipur", "06_coming_soon_cities.md", "whole page",
                  "Planned launch January 2027, waitlist only, no orders and no fees announced yet",
                  "Changes INC-104's correct answer to 'not yet; launch planned January 2027; no fee to quote'")
    return [dict(file=f, title="City addenda (6 cities)", kind="City-specific rules", fmt="Markdown"),
            dict(file="06_coming_soon_cities.md", title="Coming soon: Kochi and Jaipur", kind="Launch notice",
                 fmt="Markdown")]


def _coming_soon(rng):
    return "\n".join([
        "# Coming soon: Kochi and Jaipur", "",
        "*Fictional company for training use. All content synthetic. Published 5 November 2026.*", "",
        "QuickBasket plans to launch in **Kochi** and **Jaipur** in **January 2027**. Dates are planned and may "
        "change. Until launch, customers in these cities **can't place orders**, and **no delivery fees have been "
        "announced**. Fees, store hours and the list of serviceable localities will be published on launch day.", "",
        "## Kochi (Kerala)", "",
        "- **Planned launch:** January 2027 (exact date to be announced)",
        "- **First localities planned:** Kakkanad, Edappally, Kaloor, Vyttila, Panampilly Nagar",
        "- **Stores planned:** two dark stores at launch (Kakkanad and Edappally)",
        "- **Delivery fees:** not announced yet",
        "- **Can I order now?** No. You can join the waitlist in the app.", "",
        "## Jaipur (Rajasthan)", "",
        "- **Planned launch:** January 2027 (exact date to be announced)",
        "- **First localities planned:** Malviya Nagar, Vaishali Nagar, C-Scheme, Mansarovar",
        "- **Stores planned:** two dark stores at launch",
        "- **Delivery fees:** not announced yet",
        "- **Can I order now?** No. You can join the waitlist in the app.", "",
        "## How the waitlist works", "",
        "1. Open the app, enter your Kochi or Jaipur address and tap **Join the waitlist**.",
        "2. We'll send one notification when your locality goes live. We don't send marketing messages from the waitlist.",
        "3. Waitlist members get **₹100 off their first order** in the new city, on orders of ₹299 or more, valid for "
        "30 days from launch. It can't be combined with the FIRST100 first-order code.",
        "4. Joining the waitlist doesn't create a QuickBasket account and doesn't cost anything.", "",
        "## Questions we get a lot", "",
        "**Do you deliver in Kochi today?**  ",
        "Not yet. Kochi is planned for January 2027. Until then, orders can't be placed to Kochi addresses.", "",
        "**What will delivery cost in Kochi or Jaipur?**  ",
        "We haven't announced fees yet. They'll be published on launch day. Fees in other cities are listed in the "
        "City Addenda, but they don't apply to Kochi or Jaipur.", "",
        "**Can I send a gift card to someone in Kochi?**  ",
        "Yes. Gift cards are digital and can be bought from any city, but they can only be used once QuickBasket "
        "delivers to the recipient's address.", "",
        "**Will QuickBasket Plus work in the new cities?**  ",
        "Yes. Plus benefits apply in every city where we deliver, from launch day.", "",
        "**Which other cities are next?**  ",
        "We're looking at more cities, including Coimbatore, Visakhapatnam and Ahmedabad, but there are **no "
        "dates** for them. If a city isn't listed in the City Addenda or on this page, we don't deliver there.", "",
        "**I'm moving to Jaipur. Will my account and QuickBasket Cash work there?**  ",
        "Yes. Your account, saved addresses and QuickBasket Cash work in every city we serve. Your Jaipur address "
        "becomes serviceable on launch day.",
    ])
