"""Electronics warranty and brand directory (PDF). All brands and service partners are fictional."""
from .common import CITY_NAMES, pick
from .render import write_pdf

BRANDS = ["Voltix", "Sonara", "Kalpa Audio", "Nimbus Tech", "Zapcell", "Orbit Wear", "Tarang", "Pulsewave",
          "Lumina Home", "Kavach Cases", "Dhwani", "Aerobeat", "Gridline", "Chargewell", "Raftaar", "Nova Bands",
          "Tez Charge", "Mitra Smart", "Saaz Sound", "Bijli Power", "Prakash LED", "Hexa Cell", "Ripple Audio",
          "Vyom Wear", "Kosmo Fit", "Fluxa", "Ampere One", "Neela Tech", "Jugnu Lights", "Taal Audio", "Tvara",
          "Pixelon", "Corecharge", "Bolt and Bit", "Sutra Cables", "Veda Wear", "Ozone Grooming", "Trimly",
          "Shakti Power", "Kaveri Smart", "Monsoon Audio", "Dakshin Tech", "Hilltop Mobile", "Tara Home",
          "Indus Wired", "Sangam Sound", "Prism Plug", "Yatra Gear"]
PRODUCTS = [
    ("True wireless earbuds", [6, 12], "Battery and charging case covered; ear tips are not."),
    ("Over-ear headphones", [12], "Covers drivers, battery and Bluetooth; cushions are consumables."),
    ("Chargers and adapters", [6, 12], "Covers the adapter; physical damage from drops isn't covered."),
    ("USB cables", [6], "Replacement only; frayed or bent connectors aren't covered."),
    ("Power banks", [6, 12], "Covers battery capacity falling below 70% of rated capacity."),
    ("Smartwatches", [12], "Covers display, battery and sensors; straps are not covered."),
    ("Fitness bands", [6, 12], "Covers battery and sensors; water damage covered only up to the stated rating."),
    ("Bluetooth speakers", [12, 18], "Covers speaker drivers and battery."),
    ("Phone cases and screen guards", [0], "No warranty; only the 3-day QuickBasket window applies."),
    ("Trimmers and grooming devices", [12, 24], "Covers motor and battery; blades are consumables."),
    ("Smart plugs and LED bulbs", [12, 24], "Covers electronics; bulbs covered against early failure."),
    ("Keyboards, mice and webcams", [6, 12], "Covers electronics and switches."),
    ("Memory cards and pen drives", [12, 24], "Replacement of the card only; lost data is never covered."),
    ("Extension boards", [12], "Covers sockets, switch and surge protection."),
]
PARTNERS = ["ServeRight Repairs", "FixPoint Electronics", "CareHub Service", "QuickServe Care", "Brand-run service centre"]
CLAIMS = ["Book pickup on the partner's website with the invoice", "Walk in to a listed service centre with the invoice",
          "Call the brand helpline, then courier the product", "Book in the brand's app; doorstep pickup in most cities",
          "Chat with QuickBasket Support for a warranty referral"]

PARTNER_STEPS = {
    "ServeRight Repairs": [
        "Book a pickup on the ServeRight website with the QuickBasket invoice number and the product's serial number.",
        "Pack the product with its accessories. The original box helps but is not required.",
        "A courier collects it within 2 working days. You get a job number by SMS.",
        "ServeRight inspects the product and tells you whether the fault is covered. Covered repairs are free.",
        "The repaired or replaced product is delivered back. Keep the job sheet: the repair itself is covered for 90 days."],
    "FixPoint Electronics": [
        "Walk in to a FixPoint centre in your city with the product and the invoice (a phone copy is fine).",
        "The front desk checks the serial number against the invoice and logs the fault.",
        "Small faults are fixed while you wait. For others you get a collection date.",
        "If the product can't be repaired, FixPoint asks the brand to approve a replacement; this adds a few days.",
        "Collect the product with the job sheet, or pay a courier fee to have it sent home."],
    "CareHub Service": [
        "Raise a ticket in the brand's app or by email with the invoice and a photo or short video of the fault.",
        "CareHub replies with a ticket number and, in most cities, a doorstep pickup slot.",
        "Hand over the product only to a pickup agent who shows the ticket number.",
        "CareHub repairs or replaces the product as the brand decides.",
        "The product comes back by courier with a service report."],
    "QuickServe Care": [
        "Call the brand's helpline or use its chat; they register the complaint and pass it to QuickServe Care.",
        "QuickServe Care sends a prepaid courier label by email.",
        "Pack the product well and hand it to the courier. Remove memory cards and SIM cards first.",
        "QuickServe Care inspects, then repairs or replaces under the brand's warranty.",
        "The product is couriered back. Damage in transit must be reported to QuickServe Care within 48 hours of receiving it."],
    "Brand-run service centre": [
        "Find the nearest centre on the brand's own website.",
        "Take the product, the invoice and a government ID.",
        "The centre gives a written estimate of time. Warranty repairs are free; out-of-warranty repairs are quoted first.",
        "Collect the product when the centre messages you."],
}

PRODUCT_NOTES = {
    "True wireless earbuds": "Most earbud faults that show up in the first week are pairing problems, which a reset "
        "usually fixes (place both buds in the case, hold the case button for 10 seconds). A bud that won't charge, a "
        "cracked case or one side much quieter than the other are warranty faults. Lost single buds are not covered.",
    "Over-ear headphones": "Ear cushions and headbands wear out with use and are sold separately. Noise-cancelling "
        "faults (humming, one-sided cancellation) are covered. Keep the original box: some brands ask for it for pickup.",
    "Chargers and adapters": "Use the charger only at the voltage printed on it. A charger that gets hot to touch, "
        "smells of burning or charges slower than its rating is faulty; stop using it and raise a claim. Bent pins "
        "or a cracked body from a fall are physical damage and aren't covered.",
    "USB cables": "Cables are covered for internal faults (no data, no charge) but not for wear at the connector, "
        "which is the most common reason cables stop working.",
    "Power banks": "A power bank is faulty if it can no longer deliver about 70% of its rated capacity, swells, or "
        "gets very hot while charging. Never use a swollen power bank; keep it away from heat and raise a claim. "
        "Power banks can't be sent by air courier, so claims are handled by road pickup or walk-in.",
    "Smartwatches": "Display, battery, buttons and sensors are covered. Straps are consumables. Water damage is "
        "covered only within the water rating printed on the box, and not for hot water, saunas or sea water.",
    "Fitness bands": "Step and heart-rate readings vary between devices; a difference compared with another device is "
        "not a fault. A band that won't sync, charge or turn on is.",
    "Bluetooth speakers": "Distortion at low volume, a battery that lasts less than half its rated time, or a "
        "speaker that won't pair are covered faults. Damage from liquids is covered only for speakers with a water "
        "rating, and only within it.",
    "Phone cases and screen guards": "These have no manufacturer warranty. Problems must be reported within the "
        "QuickBasket 3-day window for accessories.",
    "Trimmers and grooming devices": "Blades and combs are consumables. Motor faults, battery faults and charging "
        "faults are covered. For hygiene reasons, an opened trimmer can't be returned to QuickBasket unless it is "
        "faulty; within 3 days a faulty one is replaced first.",
    "Smart plugs and LED bulbs": "Smart plugs are covered for the relay and Wi-Fi module. LED bulbs are covered for "
        "early failure (not lighting, flickering) within the warranty period. Bulbs broken in use are not covered.",
    "Keyboards, mice and webcams": "Double-clicking mice, stuck keys and webcams that drop out are covered. Worn-off "
        "key labels are not.",
    "Memory cards and pen drives": "A card that becomes read-only, isn't detected or loses capacity is replaced. "
        "Brands never cover lost data, so back up anything important.",
    "Extension boards": "Covered for loose sockets, a faulty switch and failed surge protection. Overloading beyond "
        "the rated wattage voids the warranty.",
}


def build(ctx, out_dir):
    rng = ctx.rng("warranty")
    rows = []
    for i, brand in enumerate(BRANDS):
        prods = sorted({p[0] for p in rng.sample(PRODUCTS, rng.randint(1, 3))})
        months = max(pick(rng, next(p for p in PRODUCTS if p[0] == prods[0])[1]), 0)
        rows.append([brand, ", ".join(prods), f"{months} months" if months else "No warranty",
                     PARTNERS[i % len(PARTNERS)], pick(rng, CLAIMS)])
    centres = []
    for city in CITY_NAMES:
        for p in PARTNERS[:4]:
            centres.append([city, p, pick(rng, ["Pickup and walk-in", "Walk-in only", "Pickup only"]),
                            pick(rng, ["Mon–Sat, 10 am–7 pm", "Every day, 10 am–8 pm", "Mon–Sat, 9:30 am–6:30 pm"]),
                            pick(rng, ["5–7 working days", "7–10 working days", "3–5 working days"])])
    blocks = [
        ("title", "Electronics Warranty and Brand Directory", "For electronics and accessories sold on QuickBasket · Updated 1 October 2026"),
        ("h", "1. QuickBasket's window first, then the manufacturer's warranty"),
        ("table", ["When the problem is reported", "Who handles it", "What you get"], [
            ["Within 3 days of delivery", "QuickBasket (Customer Policy, Section 3)",
             "A replacement first; a refund only if no replacement is in stock. The item must be unused, with all "
             "accessories and the box."],
            ["After 3 days", "The manufacturer, under its warranty",
             "Repair or replacement as the brand decides, by the service partner listed below."]], [50, 50, 74]),
        ("p", "The warranty period starts on the delivery date shown in the app, and the GST invoice under Orders › "
              "Invoice works as proof of purchase for every brand below. QuickBasket doesn't repair products itself "
              "and doesn't extend manufacturer warranties."),
        ("p", "In Bengaluru, electronics bought from the three QB Tech Hub stores can get a same-day replacement "
              "within the 3-day window (see the City Addenda). This doesn't change the window."),
        ("h", "2. Brand directory"),
        ("table", ["Brand", "Products", "Warranty", "Service partner", "How to claim"], rows, [26, 44, 20, 32, 52]),
        ("h", "3. Service centres by city"),
        ("table", ["City", "Service partner", "Service type", "Hours", "Typical turnaround"], centres, [24, 40, 34, 40, 36]),
        ("p", "Brand-run service centres are listed on each brand's own website. Kochi and Jaipur have no listed "
              "service centres yet; customers there can use courier claims once QuickBasket launches."),
        ("h", "4. Brand support contacts"),
        ("p", "Use these for warranty questions after the 3-day QuickBasket window. Addresses are examples for a "
              "fictional company; none of them is a real mailbox."),
        ("table", ["Brand", "Support email", "Support hours", "Languages", "What the brand asks for"],
         [[b, "care@" + b.lower().replace(" ", "") + ".example",
           pick(rng, ["Mon–Sat, 10 am–7 pm", "Every day, 9 am–9 pm", "Mon–Fri, 10 am–6 pm"]),
           pick(rng, ["English, Hindi", "English, Hindi, Telugu, Tamil", "English, Hindi, Kannada, Marathi"]),
           pick(rng, ["Invoice and a photo of the fault", "Invoice, serial number and a short video",
                      "Invoice and the original box", "Invoice and serial number"])] for b in BRANDS], [26, 46, 34, 34, 34]),
        ("h", "5. How a claim works with each service partner"),
    ]
    for partner, steps in PARTNER_STEPS.items():
        blocks += [("h3", partner), ("ol", steps)]
    blocks += [
        ("h", "6. Product notes"),
    ]
    for name, months, cover in PRODUCTS:
        blocks += [("h3", name),
                   ("p", f"Usual warranty: {' or '.join(str(m) + ' months' for m in months) if months != [0] else 'none'}. "
                         f"{cover} {PRODUCT_NOTES[name]}")]
    blocks += [
        ("h", "7. What warranties don't cover"),
        ("ul", ["Physical damage: drops, cracks, bent pins, crushed cables.",
                "Liquid damage beyond the product's water rating.",
                "Damage from using the wrong charger or voltage.",
                "Consumables: ear tips, cushions, straps, blades, filters.",
                "Products opened or repaired by someone other than the brand's service partner.",
                "Lost data on memory cards, pen drives or devices."]),
        ("h", "8. How QuickBasket Support helps after 3 days"),
        ("ol", ["Confirm the order belongs to the customer and find the delivery date.",
                "Share the GST invoice and the service partner's details from this directory.",
                "If the brand refuses a valid claim, the customer can ask for escalation; a human agent follows up "
                "with the brand. QuickBasket doesn't issue refunds for products outside the 3-day window."]),
    ]
    f = "10_electronics_warranty_directory.pdf"
    write_pdf(f"{out_dir}/{f}", "Electronics Warranty and Brand Directory · Fictional company for training use. "
                                "All content synthetic.", blocks)
    return [dict(file=f, title="Electronics warranty and brand directory", kind="Directory", fmt="PDF")]
