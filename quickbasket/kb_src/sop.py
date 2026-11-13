"""Delivery Partner Standard Operating Procedure (PDF). Internal operations manual, fictional and synthetic.

No planted conflicts: everything here agrees with Customer Policy v4.2 and the city addenda. Operational
rules that can change the answer to a customer question are registered with ctx.exception(...).
The customer-facing numbers (return windows, refund timelines, compensation amounts) are deliberately not
restated; the SOP points to the Customer Policy instead.
"""
from .common import pick
from .render import write_pdf

FILE = "12_delivery_partner_sop.pdf"
HEADER = ("QuickBasket Delivery Partner SOP v2.3 · Effective 1 October 2026 · Internal · "
          "Fictional company for training use. All content synthetic.")

QB_SIDE = "QuickBasket-side (compensation applies under Section 5)"
CUST = "Customer-side (no compensation)"
ADV = "Advisory (no compensation)"


# ----------------------------------------------------------------------------------------------- chapter 1
def ch1():
    return [
        ("title", "Delivery Partner Standard Operating Procedure",
         "SOP v2.3 · Effective 1 October 2026 · For delivery partners and store staff · Internal document"),
        ("small", "Fictional company for training use. All content synthetic."),
        ("h", "1. Purpose, who this is for, and how it fits with the Customer Policy"),
        ("h3", "1.1 What this document is"),
        ("p", "This is the working manual for everyone who moves a QuickBasket order from a store shelf to a "
              "customer's door. It tells you what to do, in what order, and what to record in the partner app. "
              "It is written for delivery partners, so \"you\" means the partner on the road. Store staff "
              "(pickers, packers, the cash desk and the Store Shift Lead) use the same document, because most "
              "problems on the road start or end at the store counter."),
        ("p", "Version 2.3 takes effect on 1 October 2026, the same day as Customer Policy v4.2. It replaces "
              "SOP v2.2. If you still have a printed copy of an older SOP, hand it to your Store Shift Lead."),
        ("h3", "1.2 Who must follow it"),
        ("table", ["Role", "What this SOP covers for you"], [
            ["Delivery partner (two-wheeler, e-bike or bicycle)", "Everything from shift start to cash deposit: "
             "pickup, cold chain, riding, handover, reason codes, incidents."],
            ["Picker and packer", "Chapters 3 and 4: sealing bags, category checks, cold items packed last."],
            ["Store Shift Lead", "Chapters 3, 4, 8, 9 and 13: disputes at the counter, returned orders, cash "
             "deposit, incident reports."],
            ["Store cash desk", "Chapter 9: change float, cash deposit and receipts."],
            ["City Operations", "Chapters 10 and 11: reviewing delay reason codes and declaring advisories."],
            ["Partner Help (in-app chat)", "Any chapter: the first place a partner asks when the SOP does not "
             "answer the question."]], [52, 122]),
        ("h3", "1.3 How this SOP relates to the Customer Policy"),
        ("p", "Customers are promised things in one place only: the **Customer Policy v4.2** (effective "
              "1 October 2026), together with the city addenda and the published terms for Plus, offers, gift "
              "cards and QuickBasket Cash. **This SOP never changes what customers are promised.** It only "
              "describes how we work so that those promises are kept."),
        ("ul", [
            "If this SOP and the Customer Policy ever seem to disagree about what a customer gets, the Customer "
            "Policy is right and this SOP is wrong. Tell Partner Help so the SOP can be corrected.",
            "The times and limits in this SOP (for example the wait at a gate, the wait at a door, the time a "
            "frozen item may be out of the freezer) are **operations rules for partners and stores**. They are "
            "not return windows, refund timelines or compensation amounts. Those are in the Customer Policy.",
            "You are not expected to know the Customer Policy by heart, and you must not quote it to customers. "
            "When a customer asks what they will get, the answer is always: \"Please raise it from the order "
            "page or chat with Support in the app. Support will decide under the Customer Policy.\"",
            "Nothing a partner or a store employee says at the door or at the counter changes the Customer "
            "Policy. A partner cannot grant, promise or refuse a refund, a replacement or late-delivery "
            "compensation."]),
        ("h3", "1.4 Words used in this SOP"),
        ("table", ["When the SOP says", "It means"], [
            ["Must / never", "A rule. Breaking it is a compliance issue and is reviewed by City Operations."],
            ["Should", "The normal way of working. Use judgement if the situation is unusual, and note why in the app."],
            ["The app / the partner app", "The QuickBasket Partner app on your phone."],
            ["The customer's app / the order page", "What the customer sees. You never ask to hold the customer's phone."],
            ["Support", "QuickBasket Support for customers (in-app chat, 7:00 am to midnight, every day)."],
            ["Partner Help", "In-app chat for partners, staffed during all store hours in your city."],
            ["City Operations", "The city control desk. The only team that declares weather and traffic advisories."]],
         [52, 122]),
        ("h3", "1.5 The five rules that matter most"),
        ("ol", [
            "**Safety first.** No order is worth an accident. If it is unsafe to ride, stop and tell Partner Help.",
            "**No OTP, no handover.** The only exception is a contactless leave-at-door delivery that the "
            "customer selected in their app (Chapter 6).",
            "**Record what really happened.** Reason codes, photos and timers must match the facts. A wrong "
            "reason code can take away compensation a customer is owed, or give compensation that is not owed.",
            "**Never promise money.** Refunds, replacements and compensation are decided by Support or credited "
            "automatically under the Customer Policy. You do not say what the customer will get.",
            "**Respect privacy.** Use masked calling only. Never keep a customer's number or a photo of a customer."]),
    ]


# ----------------------------------------------------------------------------------------------- chapter 2
def ch2():
    return [
        ("h", "2. Shift start"),
        ("p", "A good shift starts ten minutes before your first order. The checks below take about that long. "
              "The app will not assign orders until the shift-start checklist is complete."),
        ("h3", "2.1 App login"),
        ("ol", [
            "Open the partner app and log in with your own partner ID. Never log in on someone else's ID and "
            "never let anyone else ride on yours.",
            "Complete the selfie check. Remove your helmet and mask for the photo. If the selfie check fails "
            "twice, go to the Store Shift Lead, who can verify you in person.",
            "Allow location and notifications. The app needs location while you are on shift to route you and "
            "to record arrival at a gate or a door. Location is switched off when you end the shift.",
            "Check that your phone battery is above 40% and that you have a working charger or power bank. An "
            "order cannot be completed if your phone dies before the OTP is entered.",
            "Read the banner at the top of the home screen. If City Operations has declared a weather or "
            "traffic advisory for your city or zone, it is shown there (Chapter 11).",
            "Tap **Start shift** and choose your home store. You can be assigned orders only from stores in your zone."]),
        ("h3", "2.2 Vehicle check"),
        ("table", ["Check", "What to look for", "If it fails"], [
            ["Brakes", "Both brakes bite firmly; no spongy lever", "Do not start. Fix first, then tell the Shift Lead."],
            ["Tyres", "No visible cuts; pressure looks normal; tread present", "Fix before the shift. A puncture on "
             "the road is a QuickBasket-side delay (code D-205), not the customer's problem."],
            ["Lights and horn", "Headlight, tail light, indicators and horn all work", "Do not ride after dark without lights."],
            ["Fuel or battery", "Enough for at least four hours of riding", "Refuel or swap the battery before the first order."],
            ["Mirrors", "Both mirrors fitted and adjusted", "Fit or adjust before leaving."],
            ["Documents", "Driving licence, registration, insurance and pollution certificate (digital copies are fine)",
             "You cannot go on shift without valid documents. Bicycle partners need only their partner ID."],
            ["Phone mount", "Phone fixed in the mount, screen visible without holding it", "No mount, no riding with navigation."],
            ["Helmet", "Strap intact; visor clean", "No helmet, no shift. This has no exceptions."]], [30, 78, 66]),
        ("h3", "2.3 Delivery bag check"),
        ("ul", [
            "Use only the QuickBasket insulated delivery bag issued to you. Personal backpacks are not allowed for orders.",
            "Open the bag and smell it. A bag that smells of spilled milk, fish or detergent is not fit for food. "
            "Wipe it with the sanitiser spray at the store counter and let it dry before loading.",
            "Check both zips and the Velcro flap of the cold compartment. A cold compartment that does not close "
            "is not a cold compartment (Chapter 4).",
            "Collect two frozen gel packs from the store freezer for the cold compartment. Swap them for fresh "
            "ones whenever they feel soft, and at least once in the middle of a long shift.",
            "Carry the bag's rain cover and two spare paper carry bags. You do not carry seal tape: only the "
            "store seals bags."]),
        ("h3", "2.4 Hygiene and appearance"),
        ("ul", [
            "Wash or sanitise your hands before you touch the first order of the shift and after every refuelling stop.",
            "Wear the QuickBasket jacket or T-shirt and carry your partner ID card where it can be seen. Gate "
            "security in most gated communities will ask for it.",
            "Do not ride if you have a fever, a stomach illness or an open wound on your hands. Tell the Shift "
            "Lead and mark yourself unavailable. You are not penalised for a sick day reported before the shift.",
            "No smoking, chewing tobacco or eating while you are carrying an order.",
            "Never open a sealed bag, taste, smell or handle the items inside it."]),
        ("h3", "2.5 Change float for cash orders"),
        ("p", "If you accept cash-on-delivery orders, collect the ₹500 change float in small notes and coins from "
              "the store cash desk and confirm it in the app. The float is the store's money and is returned "
              "with your cash deposit at shift end (Chapter 9). Partners working in Hinjewadi Phase 3 (Pune) do "
              "not carry a float for that zone because cash on delivery is not offered there."),
    ]


# ----------------------------------------------------------------------------------------------- chapter 3
CATEGORY_CARRY = [
    ["Fresh fruits & vegetables", "Top of the main compartment, never under heavy items. Leafy vegetables and "
     "soft fruit (bananas, tomatoes, papaya) go last and on top.",
     "Bag is not wet or leaking. Nothing visibly crushed through the bag. Loose produce is in a tied inner bag."],
    ["Dairy, bakery & eggs", "Milk, curd, paneer and butter in the cold compartment. Eggs in the egg tray "
     "sleeve, flat, on top. Bread and cakes on top of the main compartment, never squeezed.",
     "Egg tray is taped shut. Milk pouches are not leaking. Chilled items feel cold to the touch through the bag."],
    ["Frozen & meat", "Cold compartment only, between the two gel packs. Raw meat and fish in their own sealed "
     "inner bag, never touching other food.",
     "Packs are hard-frozen (frozen items) or cold (fresh meat). The temperature label on each pack shows the "
     "safe colour. Inner bag is sealed. See Chapter 4."],
    ["Packaged food & beverages", "Main compartment, heavy items (atta, rice, oil, bottles) at the bottom. "
     "Glass bottles upright with a cardboard divider.",
     "No leaking oil or dented cans visible. Bottle caps are tight. Bag weight matches the label on the bag."],
    ["Personal care & beauty", "Main compartment, in a separate bag from food. Liquids (shampoo, handwash) upright.",
     "Separate bag from food items. No leaks. Manufacturer seals are not your job to inspect; do not open boxes."],
    ["Electronics & accessories", "In the padded sleeve, inside the main compartment, away from liquids and "
     "cold items. Never strapped to the outside of the bag.",
     "The box is in a tamper-evident security pouch with a serial sticker. Pouch number matches the app. "
     "Box is not dented or wet."],
    ["Baby care", "Main compartment, in a separate bag from detergents and personal care liquids. Diaper packs "
     "can ride on top.",
     "Formula and baby food tins are not dented. Separate bag. Seal tape intact."],
    ["Gift cards & QuickBasket Plus", "Nothing to carry. Gift cards and Plus are digital and are delivered in "
     "the customer's app.",
     "If a customer asks you about a gift card or Plus, direct them to Support in their app. Cash on delivery "
     "is not offered for either."],
]


def ch3():
    return [
        ("h", "3. Picking up at the store"),
        ("p", "Most wrong-item and missing-item complaints can be traced to thirty seconds at the pickup "
              "counter. Take those thirty seconds. Time spent verifying an order at the counter is never held "
              "against you."),
        ("h3", "3.1 Arriving at the store"),
        ("ol", [
            "When the app assigns an order, tap **Accept** and ride to the store shown. Do not wait outside a "
            "different store hoping to be reassigned.",
            "Park in the partner bay, not in front of the customer entrance or the shutter.",
            "Tap **Reached store**. This starts the store's handover clock, which is how a store delay is "
            "separated from a partner delay later (Chapter 10).",
            "Wait at the partner counter. Do not go into the picking aisles or the cold room."]),
        ("h3", "3.2 Order verification"),
        ("p", "Every order leaves the store in one or more sealed bags. Each bag has a label with the order ID "
              "(format QB-12345), the bag number (for example 1 of 3) and the customer's first name and "
              "locality. The full address and the phone number are never printed on the bag."),
        ("ol", [
            "Read the order ID on the app screen aloud to the packer. The packer reads the ID on the bag label back.",
            "Scan the QR code on **every** bag. The app shows a green tick per bag and tells you how many bags the "
            "order has. Do not leave until all bags show a tick.",
            "Check the bag count. If the app says 3 bags and you have 2, the order is not ready. Do not accept "
            "\"the third one is small, we will send it with the next rider\".",
            "Check that each bag is sealed with QuickBasket seal tape and that the tape is not cut or re-stuck. "
            "If a seal is broken, hand the bag back. The store re-checks and re-seals it (delay code D-108).",
            "If you are carrying more than one order, keep each order's bags together and put the order that "
            "will be delivered first on top. The app shows the delivery sequence.",
            "Tap **Picked up**. From this moment the order shows as out for delivery in the customer's app, and "
            "the customer can no longer cancel it."]),
        ("h3", "3.3 Sealed bags"),
        ("ul", [
            "Only store staff seal bags. You never open, re-pack or re-seal a bag, even if a customer asks you "
            "to remove an item at the door.",
            "A sealed bag protects you. If a customer says an item is missing and the seal was intact at "
            "handover, the question goes to the store's packing record, not to you.",
            "If a bag tears on the road, do not move items into another bag yourself unless items would "
            "otherwise fall out. If you must, take a photo first, use a spare paper carry bag, and tell Partner "
            "Help. Tell the customer at the door that the bag tore on the way."]),
        ("h3", "3.4 Item checks by category"),
        ("p", "You do not check individual items against the bill; the packer does that. You check how each "
              "category is packed and how you carry it. The eight categories are the same ones used in "
              "Section 3 of the Customer Policy."),
        ("table", ["Category", "How to carry it", "What to check at the counter"], CATEGORY_CARRY, [34, 70, 70]),
        ("h3", "3.5 When something is wrong at the counter"),
        ("table", ["What you see", "What you do", "Delay code if it makes the order late"], [
            ["Order not packed when you arrive", "Wait at the counter. Do not leave for another order unless the "
             "app reassigns you.", "D-101 Store packing delay"],
            ["Packer says an item is out of stock", "The store calls the customer through the store console. You "
             "do not call the customer about substitutions.", "D-102 Stock-out found at packing"],
            ["Bag label shows a different order ID", "Hand it back. Never take a bag whose label does not match your app.",
             "D-104 Wrong bag handed over"],
            ["Frozen or chilled items not ready", "Wait. Cold items are packed last on purpose (Chapter 4).",
             "D-105 Cold items not ready"],
            ["Seal broken or bag leaking", "Hand it back for re-check and re-seal.", "D-108 Bag re-packed at store"],
            ["Bag feels far lighter or heavier than the weight on its label", "Ask the packer to re-weigh it in front of you.",
             "D-110 Weight or quality recheck"],
            ["Label printer or billing system down", "The Shift Lead writes the order ID by hand and signs the bag. "
             "Scan is replaced by a manual confirm from the Shift Lead's console.", "D-106 Billing or label printer fault"]],
         [52, 76, 46]),
        ("p", "The store selects the store-side reason code at the counter, in front of you. If you disagree "
              "with the code chosen, do not argue at the counter. Add a note in the app; City Operations "
              "reviews disputed codes the same day."),
    ]


# ----------------------------------------------------------------------------------------------- chapter 4
def ch4():
    return [
        ("h", "4. Cold chain: frozen, meat and dairy"),
        ("p", "Cold chain means the item stays cold from our freezer or chiller to the customer's hands, with "
              "no warm gap in between. Food that has warmed up and cooled again can look fine and still be "
              "unsafe. The numbers in this chapter are **operations limits for stores and partners**. They are "
              "not customer windows; what a customer can report and by when is in Section 3 of the Customer Policy."),
        ("h3", "4.1 Operations limits"),
        ("table", ["Item type", "Where it is kept in the store", "Limit from store cold storage to sealed cold compartment",
                   "Limit from leaving cold storage to handover", "If the limit is passed"], [
            ["Frozen food (ice cream, frozen vegetables, frozen snacks)", "Freezer", "5 minutes", "45 minutes",
             "Do not hand over the frozen items. Mark \"Cold chain break\" and follow 4.5."],
            ["Raw meat, poultry and fish (fresh or frozen)", "Meat chiller or freezer", "5 minutes", "45 minutes",
             "Do not hand over the meat items. Mark \"Cold chain break\" and follow 4.5."],
            ["Dairy (milk, curd, paneer, butter, cheese)", "Chiller", "10 minutes", "90 minutes",
             "Do not hand over the dairy items. Mark \"Cold chain break\" and follow 4.5."],
            ["Eggs and bakery", "Shelf or bakery rack", "No cold limit", "No cold limit",
             "Carry flat and on top. Not a cold-chain item."]], [38, 26, 34, 30, 46]),
        ("p", "The partner app runs a **cold clock** for every order that contains frozen, meat or dairy items. "
              "It starts when the packer scans the cold items out of the freezer or chiller and it is shown on "
              "your delivery screen as minutes remaining. It turns amber with 10 minutes left and red at zero."),
        ("h3", "4.2 Insulated bag rules"),
        ("ul", [
            "Cold items travel only in the cold compartment of the insulated bag, between two frozen gel packs.",
            "The cold compartment is closed with both the zip and the flap, every time, even for a two-minute ride.",
            "Nothing warm goes in the cold compartment. QuickBasket does not deliver hot food, so there is "
            "never a reason to carry anything hot in the delivery bag.",
            "Raw meat and fish stay inside their own sealed inner bag. If the inner bag leaks, the cold "
            "compartment is wiped with sanitiser before the next order.",
            "Do not open the cold compartment at a gate or in a lift lobby \"to save time\". Open it at the door, "
            "at the moment of handover.",
            "Do not leave the delivery bag in direct sun on a parked vehicle. Take it with you if you leave the vehicle.",
            "Gel packs are returned to the store freezer at shift end. A gel pack that has split is thrown away at the store."]),
        ("h3", "4.3 The temperature label"),
        ("p", "Every frozen and meat pack carries a QuickBasket temperature label: a small round sticker on the "
              "pack. It is **blue** while the pack has stayed cold. It turns **pink, then red** if the pack has "
              "been warm for too long, and it does not turn back. Dairy items do not carry the label."),
        ("ol", [
            "At the counter, the packer shows you that the label on each frozen or meat pack is blue before "
            "sealing the inner bag. If you were not shown, ask.",
            "At the door, if the customer opens the bag in front of you and a label is pink or red, treat it as "
            "a damaged item (Chapter 7): photo in the partner app, mark the item, and ask the customer to raise "
            "it from their order page.",
            "Tell customers, if they ask, that the label is on the pack and that Support may ask for a photo of "
            "the packaging and the label. Do not tell them what Support will decide."]),
        ("h3", "4.4 Sequence for cold orders"),
        ("ol", [
            "Dry and ambient bags are packed and sealed first and wait at the counter.",
            "When you tap **Reached store**, the packer brings the cold items from the freezer or chiller. "
            "This is why cold items are sometimes \"not ready\" when the rest of the order is.",
            "Cold items go straight into your cold compartment, within the limit in 4.1. You close it.",
            "Deliver cold orders first if you are carrying more than one order and the app's sequence allows "
            "it. If the app's sequence puts a cold order second, follow the app; it has already checked the cold clock.",
            "At the door, hand over the cold bag first and say \"this bag has frozen or chilled items\", so "
            "the customer can put it away."]),
        ("h3", "4.5 Cold chain break"),
        ("p", "A cold chain break is any of: the cold clock reaching zero before handover, a temperature label "
              "that is pink or red, a cold compartment that was left open, or gel packs that have fully melted."),
        ("ol", [
            "Do not hand over the affected cold items, even if the customer says they do not mind.",
            "In the app, open the order, choose **Report item issue › Cold chain break** and select the items. "
            "Take a photo of the items and the cold clock screen.",
            "Hand over the rest of the order as normal, with OTP. The customer's order page will show the cold "
            "items as not delivered.",
            "Tell the customer: \"These items were not kept cold enough, so I cannot hand them over. It is "
            "recorded on your order. Support will sort it out under the Customer Policy.\" Do not say what the "
            "customer will receive.",
            "On a cash order, collect the amount the app shows after you have marked the items. The app "
            "recalculates the amount to collect.",
            "Return the affected items to the store in the cold compartment. The Shift Lead scans them in. "
            "They are never put back on sale by a partner's decision."]),
        ("p", "A cold chain break is always recorded as a QuickBasket-side issue. It is never the customer's fault."),
    ]


# ----------------------------------------------------------------------------------------------- chapter 5
def ch5():
    return [
        ("h", "5. On the road"),
        ("h3", "5.1 Routing"),
        ("ul", [
            "Follow the route in the partner app. It already avoids roads that City Operations has paused "
            "(for example waterlogged underpasses during a declared advisory).",
            "If you know a road is blocked and the app does not, take the safe alternative and tap **Report "
            "road problem**. This helps the next partner and is recorded against the order.",
            "Do not take wrong-side shortcuts, footpaths or closed service lanes to save time.",
            "When you carry more than one order, deliver in the sequence the app shows. If an earlier drop takes "
            "long, the delay to the later order is QuickBasket-side (code D-209), not the later customer's fault.",
            "If the map pin and the written address clearly point to different places, stop and use masked "
            "calling to ask the customer which is right, before riding to either."]),
        ("h3", "5.2 Road safety"),
        ("table", ["Rule", "Detail"], [
            ["Helmet", "Strapped, for every trip, including the short ride back to the store. Bicycle partners too."],
            ["Speed", "Within the posted limit. The promised delivery time is the company's promise, not a "
                      "target for you to chase by speeding."],
            ["Signals", "Stop at red lights and stop lines. Jumping a signal is a compliance issue even when no one is hurt."],
            ["One-ways", "Never ride against traffic, even for a short stretch."],
            ["Load", "The delivery bag is worn on the back or fixed in the carrier. Nothing hangs from the handlebar."],
            ["Passengers", "No pillion rider while you are on shift."],
            ["Alcohol and drugs", "Zero tolerance. A partner found riding under the influence is taken off the platform."],
            ["Tiredness", "Take the break the app offers after every four hours on shift. Tired riding causes accidents."]],
         [34, 140]),
        ("h3", "5.3 No phone while riding"),
        ("p", "This rule has no exceptions."),
        ("ul", [
            "The phone stays in the mount while the vehicle is moving. You do not hold it, type on it or read "
            "messages on it while riding.",
            "Navigation is by voice prompts and glances at the mounted screen.",
            "To call a customer, to accept a new order, to select a reason code or to chat with Partner Help: "
            "pull over, stop, put a foot down, then use the phone.",
            "Earphones: one ear only, for navigation prompts, and only where local traffic rules allow it.",
            "If a customer calls you through masked calling while you are riding, let it ring. Call back when you have stopped."]),
        ("h3", "5.4 Rain"),
        ("p", "Rain is part of the job in every QuickBasket city. Rain by itself is **not** an advisory and does "
              "not change what the customer is promised."),
        ("ul", [
            "Put the rain cover on the delivery bag before you leave the store, not after the first shower.",
            "Slow down. Painted lines, metal covers and the first ten minutes of rain on a dry road are the most slippery.",
            "Do not ride through water when you cannot see the road surface. Open drains and potholes hide under it. "
            "Take another route or wait, and tell Partner Help.",
            "If you have to stop and shelter, tap **Sheltering: rain** in the app so the customer sees an updated "
            "arrival time. If the order is late as a result and no advisory is declared, the code is D-402 "
            "(rain, no advisory), which is QuickBasket-side.",
            "Only City Operations can declare a weather advisory (Chapter 11). You cannot declare one, and you "
            "must not tell a customer that \"there is an advisory\" unless the banner is showing in the app.",
            "Paper bags fail when wet. At the door, hand bags over from inside the rain cover and support them "
            "from below."]),
        ("h3", "5.5 Parking and entering buildings"),
        ("ul", [
            "Park where the building or the security guard asks you to. Lock the vehicle and take the delivery bag with you.",
            "Do not leave a bag with orders for other customers unattended on the vehicle.",
            "Use the service lift where a building has one and asks delivery staff to use it.",
            "Walking time inside a large complex after you have been let in is part of the delivery. It is not "
            "gate waiting time and is not a customer-side delay (code D-210 if it makes the order late)."]),
    ]


# ----------------------------------------------------------------------------------------------- chapter 6
def ch6():
    return [
        ("h", "6. Handover"),
        ("p", "Handover is the moment the order becomes the customer's. It is also the moment that fixes the "
              "**delivered time** in the app, which every customer window in the Customer Policy is counted "
              "from and which decides whether the delivery was late. Get it right."),
        ("h3", "6.1 OTP handover (the normal case)"),
        ("p", "Every order has a 4-digit handover OTP. It is shown to the customer on the order page in their "
              "app from the moment the order is picked up. It is never shown to you."),
        ("ol", [
            "Tap **Arrived** when you are at the door (or at the reception or gate where the handover will "
            "happen). This starts the door timer.",
            "Greet the customer and say the order is from QuickBasket. Say the first name on the order: "
            "\"Order for Priya?\"",
            "Ask: \"Please read me the 4-digit OTP on your order page.\" The customer reads it; you type it "
            "into the partner app.",
            "When the app shows the green **OTP verified** screen, hand over the bags, cold bag first.",
            "On a cash-on-delivery order, collect the cash before you hand over the bags (Chapter 9).",
            "The app marks the order delivered at the moment the OTP is verified. That time is the delivered "
            "time the customer sees."]),
        ("ul", [
            "**Never hand over without the OTP.** Not to a customer who says \"I'm in a hurry\", not to a "
            "regular customer you recognise, not to a security guard who says the customer told him to collect it.",
            "Never ask the customer to tell you the OTP on a call before you arrive, and never type an OTP "
            "before you are at the handover point. Entering the OTP early marks the order delivered early, "
            "which is a false record.",
            "Never ask to see or hold the customer's phone. The customer reads the OTP out or shows the screen.",
            "The customer does not have to sign anything, show ID or share any other code. If someone asks you "
            "for \"the QuickBasket code\" from **your** phone, refuse: there isn't one.",
            "Three wrong OTP attempts lock the screen for two minutes. Ask the customer to refresh their order "
            "page and read the OTP again. If it still fails, see 6.7."]),
        ("h3", "6.2 Contactless leave-at-door (the only exception to OTP)"),
        ("p", "A customer can choose **Leave at door** for an order in their app. When they have, your handover "
              "screen shows a blue \"Leave at door\" badge and any note the customer wrote (for example "
              "\"hang on the door handle\")."),
        ("ol", [
            "Check for the badge. No badge means OTP handover, whatever a note, a neighbour or a guard says.",
            "Place the bags at the door of the address in the app, off the floor if possible, out of the rain "
            "and out of direct sun. Do not block the door.",
            "Ring the bell or knock once.",
            "Take the handover photo in the partner app. It must show the bags and the door or the flat number. "
            "It must not show any person.",
            "The app marks the order delivered when the photo is uploaded. That is the delivered time.",
            "Leave. You do not wait for the door to open."]),
        ("ul", [
            "Leave-at-door must be selected **by the customer, in their app**. If a customer asks for it on a "
            "call, say: \"Please switch on Leave at door on your order page.\" Proceed when the badge appears on your screen.",
            "Leave-at-door is not offered on cash-on-delivery orders, because cash has to be collected. If a "
            "cash customer asks you to leave the order, you cannot.",
            "Leave-at-door is not offered for an electronics replacement where you have to collect the old item (Chapter 12).",
            "If the door is inside a gated community and you are not let in, leave-at-door does not mean "
            "\"leave at the gate\". Follow 6.5.",
            "Cold items can be left at the door when the customer has chosen it. Put the cold bag in the "
            "shade and mention \"frozen items\" in the handover note."]),
        ("h3", "6.3 Handing over to someone else at the address"),
        ("p", "The OTP is the proof, not the face. You may hand over to any person **at the delivery address** "
              "who gives you the correct OTP: a family member, a flatmate, domestic staff, a colleague."),
        ("table", ["Who is at the door", "Can you hand over?", "Notes"], [
            ["The customer", "Yes, with OTP", "Normal case."],
            ["Family member, flatmate or staff at the same address", "Yes, with OTP", "They get the OTP from the customer. You wait while they do, within the door timer."],
            ["Someone at the address who does not have the OTP", "No", "Offer to wait while they call the customer. Use masked calling yourself (6.6)."],
            ["A neighbour in the same building", "Only if the customer asks you to on a masked call and the neighbour gives the correct OTP",
             "Add the note \"handed to neighbour, flat number\" in the app. Never choose a neighbour yourself."],
            ["Security guard at the gate or lobby", "Only with the correct OTP", "A guard's word that \"madam said to leave it here\" is not enough."],
            ["Someone who meets you on the road or in the parking area and says the order is theirs", "No",
             "Hand over at the address in the app, or at its gate or reception. OTP alone on the street is not enough."],
            ["A different building, street or locality", "No", "That is a change of address, which partners cannot make (6.8)."]],
         [56, 50, 68]),
        ("h3", "6.4 Office buildings and receptions"),
        ("ul", [
            "In tech parks and office campuses, orders are handed over at the reception, visitor desk or "
            "security desk of the building named in the address, not at individual desks or floors.",
            "Tap **Arrived** at the reception and use masked calling to tell the customer you are there.",
            "The customer, or a colleague they send, comes to the reception and gives the OTP.",
            "The reception staff are not the customer. Do not leave an order with the reception unless the "
            "person at the desk gives you the correct OTP, or the order has the Leave at door badge and the "
            "customer's note says to leave it at reception.",
            "If the campus does not let delivery partners past the main gate, the main gate reception is the "
            "handover point. This is normal in Hinjewadi Phases 1 and 2 (Pune) and several Hyderabad, "
            "Bengaluru and Chennai campuses."]),
        ("h3", "6.5 Gated communities"),
        ("p", "Most large housing societies and apartment complexes control entry with a gate OTP, an intercom "
              "call or an approval on the society's visitor app. Only the customer can give that approval."),
        ("ol", [
            "At the gate, tell security the flat number and that it is a QuickBasket delivery. Show your partner ID if asked.",
            "Tap **At gate: waiting for entry**. This starts the gate timer and records the delay as \"gate "
            "entry delay\". Do it as soon as you are stopped, not later from memory.",
            "Use masked calling once to tell the customer you are at the gate and need entry approved.",
            "**Wait up to 7 minutes at the gate.** The app shows the timer.",
            "When you are let in, tap **Entered**. The gate timer stops. Ride or walk to the door and do a normal OTP handover.",
            "If you are not let in within 7 minutes, call the customer again and offer handover at the gate: "
            "the customer comes to the gate and gives the OTP there.",
            "If the customer cannot be reached on that second call, the order is treated as not reachable: mark "
            "**Customer not reachable** and return to the store (6.6 and Chapter 8). You do not wait a further "
            "five minutes; the gate wait has already been longer."]),
        ("ul", [
            "Time recorded on the gate timer is a **customer-side delay** under Section 5 of the Customer "
            "Policy. It is taken out when lateness is worked out (Chapter 10). This is why the timer must be "
            "started and stopped honestly.",
            "The gate timer measures waiting for **entry**. A queue at the lift, a long walk to Tower 9 or a "
            "search for parking after you are inside is not gate time.",
            "Do not give security your phone to \"talk to the customer\", and do not ask security for the "
            "customer's intercom or phone number.",
            "If security wants to keep your ID card or your vehicle key, refuse politely and offer to sign the "
            "visitor register. If entry is refused for that reason, treat it as entry not given."]),
        ("h3", "6.6 Customer not reachable"),
        ("p", "You are at the door, you have rung the bell or knocked, and nobody answers; or you are at an "
              "address you cannot find and the customer does not pick up."),
        ("ol", [
            "Tap **Arrived**. The door timer starts.",
            "Ring the bell or knock. Wait a moment. Do it once more.",
            "**Call the customer through masked calling.** Let it ring fully.",
            "Wait about two minutes, then **call a second time.** The app also sends the customer a "
            "notification that you are at the door.",
            "**Wait 5 minutes at the door** in total, counted on the door timer from when you tapped Arrived.",
            "If the customer answers or opens the door at any point, do a normal OTP handover.",
            "If the 5 minutes pass with two unanswered calls logged, tap **Customer not reachable**. The app "
            "will let you select it only when both calls and the full wait are on record.",
            "Do not leave the order at the door, with a neighbour or with security. Take it back to the store (Chapter 8)."]),
        ("ul", [
            "Not reachable is a customer-side delay. The app records it with code D-504 (calls not answered) or "
            "D-505 (nobody at the door).",
            "You do not tell the customer, by call or note, what will happen to the order or to their money. "
            "Support contacts the customer and decides under the Customer Policy.",
            "If the customer calls back after you have left, do not turn around on your own decision. Tell them "
            "to chat with Support in the app; Support will tell you through the app if the order is to be re-attempted.",
            "If you have a cold order for the next customer in your bag, the 5-minute wait still applies. The "
            "app has already allowed for it in the cold clock."]),
        ("h3", "6.7 OTP problems"),
        ("table", ["Problem", "What you do"], [
            ["Customer cannot find the OTP", "It is on the order page, under the delivery status. Ask them to open "
             "the QuickBasket app, tap Orders, and tap the live order."],
            ["Customer's phone is switched off or has no internet", "They can log in on another phone or ask the "
             "person who placed the order. Wait within the door timer. No OTP, no handover."],
            ["OTP is rejected three times", "Ask the customer to refresh the order page. Wait for the two-minute lock to clear and try once more."],
            ["The OTP screen on your app does not open or keeps failing", "Chat with Partner Help. Partner Help can "
             "confirm the handover from their side after the customer confirms in the customer's app. You never "
             "complete an order by any other route. Delay code D-304."],
            ["The order was placed by someone who is not at the address (for example for a parent)",
             "The person who placed the order sends the OTP to the person at the door. You wait within the door timer."],
            ["Customer refuses to share the OTP but wants the order", "Explain once that the OTP is the handover "
             "proof and protects their order. If they still refuse, treat it as a refused delivery (Chapter 8)."]],
         [62, 112]),
        ("h3", "6.8 Address changes"),
        ("p", "Partners cannot change a delivery address. Small corrections inside the same premises are fine: "
              "the other tower gate of the same society, the back entrance of the same building, the reception "
              "instead of the fourth floor. Anything else is a different address."),
        ("ul", [
            "If the customer asks you to bring the order to a different building, street or locality, say: "
            "\"I can deliver only to the address on the order. Please chat with Support in the app.\"",
            "If the address or pin entered by the customer was wrong and you lost time finding the right "
            "place within the same premises or lane, record it with the wrong-address codes (D-501 or D-502).",
            "If the app's map sent you to the wrong place although the customer's written address was correct "
            "and complete, that is our error: code D-303, QuickBasket-side."]),
        ("h3", "6.9 At the door: manners"),
        ("ul", [
            "Stand back from the door after ringing. Do not step inside a home, even when invited to put the bags in the kitchen.",
            "Heavy orders: carry them to the door. In older buildings without lifts in Mumbai, see the city note in Chapter 12.",
            "Do not ask for a tip or a rating. Customers can tip in the app; a tip goes fully to you.",
            "Do not comment on what the customer ordered.",
            "If the customer is rude, stay calm, complete or stop the handover as the rules say, and report it afterwards (Chapter 13)."]),
    ]


# ----------------------------------------------------------------------------------------------- chapters 7-9
def ch7():
    return [
        ("h", "7. Damaged or wrong items at the doorstep"),
        ("p", "Sometimes the customer opens the bag while you are still there and finds a broken bottle, a "
              "crushed pack, a pink temperature label or an item they did not order. Your job is to **record** "
              "it accurately. Deciding what the customer gets is Support's job, under the Customer Policy."),
        ("h3", "7.1 What you do"),
        ("ol", [
            "Complete the handover first if you have not already: OTP, and cash on a cash order. The customer "
            "raises their request after the order is marked delivered.",
            "Stay calm and say: \"I'm sorry about that. Let me record it on the order.\"",
            "In the partner app, open the order and tap **Report item issue**.",
            "Choose the issue: Damaged, Leaking, Spoiled or warm, Wrong item, Missing item, or Seal broken.",
            "Select the item from the list. If you cannot tell which line it is, choose \"Not sure\" and describe it in the note.",
            "Take a photo of the item and the bag it came in. Photograph the item only: no faces, no interior of the home.",
            "Tell the customer: \"It is recorded on your order. Please raise the request from your order page "
            "or chat with Support in the app. Support will decide under the Customer Policy.\"",
            "Tap **Submit**. Your report is attached to the order, where Support can see it."]),
        ("h3", "7.2 What you never do"),
        ("ul", [
            "**Never promise a refund or a replacement**, or say how long one will take or how much it will be. "
            "\"You will definitely get your money back\" is a promise you cannot keep for them.",
            "Never tell the customer they are **not** eligible either. You do not know the category rules well "
            "enough, and it is not your decision.",
            "Never raise the request for the customer from their phone. Requests can only be raised by the "
            "account that placed the order.",
            "Never offer to bring a replacement \"on my next trip\", to pay the customer yourself, or to settle it in cash.",
            "Never accept blame or assign blame (\"the store always does this\"). Record facts.",
            "Never take a photo with your own camera app. Use the partner app only, so that the photo is "
            "attached to the order and not stored on your phone."]),
        ("h3", "7.3 Should you take the item back?"),
        ("table", ["Situation", "What happens to the item"], [
            ["Damaged, leaking or spoiled food item", "It stays with the customer unless they ask you to take it away. "
             "If you take it, put it in a spare bag, mark \"Item returned with partner\" and hand it to the Shift Lead."],
            ["Wrong item (not what was ordered), unopened", "Ask if the customer wants to keep it for now. If not, "
             "take it back sealed, mark \"Item returned with partner\"."],
            ["Electronics box dented or security pouch torn", "The customer decides whether to keep it. Photograph "
             "the pouch and the box before anything is opened."],
            ["Frozen or meat item with a pink or red temperature label", "Treat as a cold chain break: take it "
             "back in the cold compartment (4.5)."],
            ["Customer wants to hand back an item simply because they changed their mind", "You cannot take a "
             "single item back at the door. See Chapter 8."]], [70, 104]),
        ("p", "Your report helps the customer; it does not replace the customer's own request. If the customer "
              "does not raise a request in their app, nothing further happens. Support decides every request "
              "under the Customer Policy, including its category rules and photo requirements."),
        ("h3", "7.4 If the customer blames you"),
        ("p", "If the bag seals were intact at handover, say so in the report note (\"seals intact at "
              "handover\"). If a bag was damaged on the road, for example in a fall or in heavy rain, say that "
              "too. An honest note is never held against you; a missing note is."),
    ]


def ch8():
    return [
        ("h", "8. Refused deliveries and returns to store"),
        ("h3", "8.1 When a customer refuses the order"),
        ("p", "Once an order is out for delivery it can no longer be cancelled in the app. A customer who no "
              "longer wants it can refuse it at the door. That is their right under Section 7 of the Customer "
              "Policy, and you do not argue with it."),
        ("ol", [
            "Ask once, politely, whether they are refusing the whole order. Do not ask for a reason; if they "
            "give one, note it.",
            "In the app, tap **Order refused at door** and choose the closest reason from the list.",
            "Do not ask for the OTP. Do not collect any cash on a cash order.",
            "Do not open the bags. Refused orders go back sealed.",
            "Say: \"I have recorded that you refused the order. For anything about a refund, please use the "
            "order page or chat with Support in the app.\" Do not say whether, when or how much will be refunded.",
            "Take the order back to the store (8.3)."]),
        ("h3", "8.2 No part-acceptance at the door"),
        ("p", "A customer either accepts the whole order with the OTP, or refuses the whole order. You cannot "
              "open a sealed bag to take one item out, and you cannot hand over two bags out of three."),
        ("ul", [
            "If the customer wants most of the order but not one item, they accept the order and then raise a "
            "request for that item from the order page. Support decides it under the Customer Policy.",
            "The two exceptions are both decided by QuickBasket, not by the customer: items you hold back for a "
            "cold chain break (4.5), and a damaged or wrong item that the customer asks you to take away after "
            "you have reported it (7.3).",
            "On a cash order, the amount to collect is always the amount on your app screen. You never work out "
            "a reduced amount yourself."]),
        ("h3", "8.3 Returning an order to the store"),
        ("p", "An order comes back to the store when it was refused, when the customer was not reachable, when "
              "entry was not given and gate handover failed, or when Partner Help tells you to bring it back."),
        ("ol", [
            "Finish any other deliveries in your sequence first, unless the returned order has cold items and "
            "the cold clock is amber or red. In that case go to the store first and tell Partner Help.",
            "Ride back to the store the order came from, not to the nearest store.",
            "At the partner counter, tap **Returned to store** and hand the sealed bags to the Shift Lead.",
            "The Shift Lead scans each bag in and checks the seals in front of you. The app shows you a return receipt.",
            "Cold items are checked against the cold clock and the temperature labels by the Shift Lead, who "
            "decides whether they go back into stock. This is never the partner's decision.",
            "If any seal is broken or a bag is missing, the Shift Lead records it and you add your note before you leave."]),
        ("table", ["Why the order came back", "What you record", "What you tell the customer"], [
            ["Refused at the door", "Order refused at door + reason", "\"It is recorded. Please use the order page or Support chat.\""],
            ["Customer not reachable (door)", "Customer not reachable (D-504 or D-505)", "Nothing. Support contacts them."],
            ["Gate entry not given and gate handover failed", "Gate entry delay, then Customer not reachable (D-506 or D-507, then D-504)",
             "Nothing further. Support contacts them."],
            ["Address cannot be found and customer does not answer", "Wrong address (D-501 or D-502), then Customer not reachable",
             "Nothing. Support contacts them."],
            ["Customer refuses to share the OTP", "Order refused at door: OTP not shared", "\"Without the OTP I cannot hand over. Support can help in the app.\""],
            ["Partner Help instruction (for example store recall of an item)", "Returned on instruction", "What Partner Help tells you to say, nothing more."]],
         [58, 60, 56]),
        ("p", "What happens next to the order, to any payment already made and to any refund is decided by "
              "Support under the Customer Policy. Partners and store staff do not tell the customer the outcome, "
              "and a returned order is never re-sent because a partner or a store decided to on their own."),
    ]


def ch9():
    return [
        ("h", "9. Cash on delivery (COD)"),
        ("h3", "9.1 Where and when COD is offered"),
        ("table", ["Rule", "Detail"], [
            ["Order value", "Cash on delivery is offered on orders up to ₹3,000. You will never be assigned a cash order above ₹3,000."],
            ["Not offered for", "Gift cards and QuickBasket Plus (both digital). Addresses in **Hinjewadi Phase 3, Pune**: "
             "no cash on delivery, because partners cannot carry cash into the IT-park security zone."],
            ["Everywhere else", "Offered in all six cities, at every store, during all store hours."],
            ["How you know", "A cash order shows a yellow **COLLECT CASH** bar with the amount, from assignment to handover."]],
         [36, 138]),
        ("p", "If a customer in Hinjewadi Phase 3 says they chose cash, they are mistaken: the app does not offer "
              "it for that zone. Check your screen. If there is no COLLECT CASH bar, the order is prepaid and "
              "you collect nothing."),
        ("h3", "9.2 Collecting cash"),
        ("ol", [
            "Before you ask for the OTP, tell the customer the amount on your screen: \"The amount to pay is ₹842.\"",
            "Collect cash for exactly that amount. Count it in front of the customer.",
            "Give change from your change float. Count the change into the customer's hand.",
            "Tap **Cash collected** and enter the amount received. Then ask for the OTP and hand over.",
            "The customer's bill is in their app under Orders › Invoice. You do not carry or write paper receipts."]),
        ("ul", [
            "**Cash only, into your hand, for a cash order.** Never accept a UPI transfer to your personal "
            "number, a transfer to anyone else's account, a cheque, or a promise to pay later. A customer who "
            "does not have the cash can refuse the order (Chapter 8); the payment method cannot be changed "
            "after an order is placed.",
            "Never collect more than the amount shown, and never collect any amount on a prepaid order. There "
            "are no \"handling\", \"stairs\", \"rain\" or \"late night\" charges collected by partners. "
            "Anything the customer owes is already in the amount on your screen.",
            "Do not round the amount up or down. If the bill is ₹842, the customer pays ₹842.",
            "A cash tip is the customer's choice. Do not ask for one, and do not keep change as a tip unless "
            "the customer clearly says so.",
            "If you think a note is fake or badly torn, ask politely for another note. If there is no other "
            "note, the order cannot be handed over; record it as refused: payment not made.",
            "If the amount on your screen looks wrong to the customer, do not negotiate. The customer can "
            "accept and raise it with Support afterwards, or refuse the order."]),
        ("h3", "9.3 Change"),
        ("ul", [
            "Start every shift with the ₹500 change float in small notes and coins (2.5).",
            "If you run out of change, ask the customer if they have the exact amount. If not, you may give "
            "change from the cash you have already collected on earlier orders.",
            "If neither works, chat with Partner Help before leaving the door. Do not leave owing the customer "
            "change, and do not ask the customer to \"adjust it next time\".",
            "Top up small notes at the store cash desk whenever you pass the store."]),
        ("h3", "9.4 Cash in hand and daily deposit"),
        ("table", ["Rule", "Detail"], [
            ["Cash-in-hand limit", "₹6,000 of collected cash (not counting the float). When you reach it, the app "
             "stops assigning cash orders to you until you deposit. Prepaid orders continue."],
            ["When to deposit", "At the end of every shift, the same day, at the cash desk of your home store. "
             "Also any time you pass the store with more than ₹3,000 in hand."],
            ["How", "The cash desk counts the cash in front of you and enters it. You confirm the amount in the "
             "app and receive a digital deposit receipt. Return the ₹500 float at the same time."],
            ["Mismatch", "If the counted amount differs from the app's total, the Shift Lead records the "
             "difference with you present. Shortfalls that are not explained are recovered from your next payout."],
            ["Never", "Never take collected cash home overnight, deposit it with another partner, or hand it to "
             "store staff away from the cash desk."]], [36, 138]),
        ("h3", "9.5 Cash and safety"),
        ("ul", [
            "Keep cash in the inner zip pocket of your jacket or waist pouch, not in the delivery bag and not in the vehicle.",
            "Do not count your day's cash in public.",
            "If someone tries to rob you, give up the cash. Do not resist. Get to a safe place, press SOS in the "
            "app and report it (Chapter 13). You are not charged for cash lost in a reported robbery that is "
            "confirmed by a police complaint."]),
        ("h3", "9.6 What partners say about COD refunds"),
        ("p", "Nothing. If a cash customer asks how they would get money back for an item, the answer is the "
              "same as for every other question about money: \"Please raise it from the order page or chat with "
              "Support in the app.\" You never return cash at the door for an item, on any order."),
    ]


# ----------------------------------------------------------------------------------------------- chapter 10
DELAY_CODES = [
    # store
    ("D-101", "Store packing delay", "The order was not packed and sealed when the partner reached the store, or picking started late.", "QB"),
    ("D-102", "Stock-out found at packing", "An item shown as in stock was not on the shelf; time was lost finding it, substituting it or calling the customer.", "QB"),
    ("D-103", "Picker or packer shortage", "Too few store staff on the floor for the number of orders in the queue.", "QB"),
    ("D-104", "Wrong bag handed over", "The partner was given another order's bag and had to return or wait for the swap.", "QB"),
    ("D-105", "Cold items not ready", "Frozen, meat or dairy items were brought out late, or the cold room queue held the order.", "QB"),
    ("D-106", "Billing or label printer fault", "The bill or bag label could not be printed at the store.", "QB"),
    ("D-107", "Store opened late", "The store was not open or not ready to dispatch at its published opening time.", "QB"),
    ("D-108", "Bag re-packed at store", "A seal was broken or a bag was leaking at the counter and the order was re-checked and re-sealed.", "QB"),
    ("D-109", "Held for batching", "The store or the system held the order to send it with another order on the same trip.", "QB"),
    ("D-110", "Weight or quality recheck", "Fresh produce or a weighed item was re-weighed or re-checked before dispatch.", "QB"),
    # partner and vehicle
    ("D-201", "No partner available", "No delivery partner could be assigned for some time after the order was packed.", "QB"),
    ("D-202", "Partner reached store late", "The assigned partner took longer than the app's estimate to reach the store.", "QB"),
    ("D-203", "Partner route error", "The partner took a wrong turn or went to the wrong building although the address and pin were correct.", "QB"),
    ("D-204", "Vehicle breakdown", "The partner's vehicle stopped working during the trip (engine, chain, electrical fault).", "QB"),
    ("D-205", "Puncture", "A tyre puncture during the trip.", "QB"),
    ("D-206", "Fuel or battery ran out", "The vehicle ran out of fuel or charge during the trip.", "QB"),
    ("D-207", "Partner accident or fall", "The partner was in an accident or fell. Safety comes first; the order is reassigned if needed.", "QB"),
    ("D-208", "Order reassigned", "The order was moved to a second partner after pickup or after the first partner was assigned.", "QB"),
    ("D-209", "Earlier drop took longer", "On a multi-order trip, an earlier delivery overran, for any reason, and made this order late.", "QB"),
    ("D-210", "Long walk or parking inside premises", "After entry was given: distance from parking to the tower, internal security checks, finding the block.", "QB"),
    ("D-211", "Lift not working or stairs", "The lift was out of order or not available to delivery staff and the partner climbed the stairs.", "QB"),
    # systems
    ("D-301", "Partner app outage", "The partner app was down, slow or logged the partner out during the trip.", "QB"),
    ("D-302", "Order or payment system outage", "A QuickBasket system fault held the order before dispatch.", "QB"),
    ("D-303", "Map or pin error by QuickBasket", "The customer's written address was correct and complete, but the app's map led to the wrong place.", "QB"),
    ("D-304", "OTP screen fault", "The handover OTP could not be entered or verified because of a fault on our side.", "QB"),
    ("D-305", "Masked calling failure", "Calls through the app would not connect because of a fault on our side, so the customer could not be told the partner had arrived.", "QB"),
    ("D-306", "Store system outage", "The store console or inventory system was down and orders could not be released.", "QB"),
    # road and other
    ("D-401", "Traffic, no advisory", "Ordinary congestion, peak-hour traffic or a jam, with no traffic advisory declared by City Operations.", "QB"),
    ("D-402", "Rain, no advisory", "Rain or waterlogging slowed or stopped the partner, with no weather advisory declared by City Operations.", "QB"),
    ("D-403", "Road closed or diverted, no advisory", "A procession, festival crowd, road work or diversion, with no traffic advisory declared.", "QB"),
    ("D-404", "Police or document check", "The partner was stopped for a routine check.", "QB"),
    ("D-405", "Other or unknown", "None of the codes fits, or the cause is not known. Reviewed by City Operations within one working day.", "QB"),
    # customer-side
    ("D-501", "Wrong address: written address", "The address typed by the customer was wrong or incomplete (no flat number, wrong tower, wrong street).", "CUST"),
    ("D-502", "Wrong address: pin location", "The customer placed the map pin somewhere other than the real delivery point.", "CUST"),
    ("D-503", "Wrong address: asked to deliver elsewhere", "The customer asked, on a call or at the door, for the order to go to a different entrance or point within the premises.", "CUST"),
    ("D-504", "Not reachable: calls not answered", "The customer did not answer two masked calls and the partner needed them to find the address, get entry or hand over.", "CUST"),
    ("D-505", "Not reachable: nobody at the door", "The partner waited at the door on the door timer and nobody came.", "CUST"),
    ("D-506", "Gate entry: waiting for approval", "Time on the gate timer waiting for the customer's gate OTP, intercom reply or visitor-app approval.", "CUST"),
    ("D-507", "Gate entry: customer asked to come to the gate", "Security did not allow entry and the partner waited for the customer to come to the gate.", "CUST"),
    # advisory
    ("D-601", "Declared weather advisory", "A weather advisory declared by City Operations was in force for the zone (banner showing in the app).", "ADV"),
    ("D-602", "Declared traffic advisory", "A traffic advisory declared by City Operations was in force for the zone (banner showing in the app).", "ADV"),
    ("D-603", "Zone paused under a declared advisory", "Deliveries to the locality were paused by City Operations under a declared advisory after the order was accepted.", "ADV"),
]
SIDE_LABEL = {"QB": QB_SIDE, "CUST": CUST, "ADV": ADV}
SIDE_SHORT = {"QB": "QuickBasket-side", "CUST": "customer-side", "ADV": "advisory"}

# (promised, delivered-minus-promised minutes, [(code, customer-side minutes or None)], advisory in force?)
LATE_EXAMPLES = [
    ("7:40 pm", 12, [("D-101", None)], False),
    ("8:05 am", 22, [("D-401", None)], False),
    ("9:15 pm", 34, [("D-204", None)], False),
    ("6:50 pm", 26, [("D-506", 6)], False),
    ("1:10 pm", 19, [("D-506", 7)], False),
    ("10:30 am", 41, [("D-102", None), ("D-506", 5)], False),
    ("11:20 pm", 33, [("D-101", None), ("D-505", 5)], False),
    ("7:05 pm", 28, [("D-402", None)], False),
    ("7:05 pm", 28, [("D-601", None)], True),
    ("3:45 pm", 17, [("D-502", 9)], False),
    ("8:30 pm", 48, [("D-301", None), ("D-209", None)], False),
    ("12:15 pm", 9, [("D-507", 7)], False),
    ("5:55 pm", 31, [("D-303", None)], False),
    ("9:40 am", 36, [("D-201", None), ("D-504", 4)], False),
]


def _add_minutes(clock, minutes):
    t, ap = clock.split(" ")
    h, m = [int(x) for x in t.split(":")]
    h24 = (h % 12) + (12 if ap == "pm" else 0)
    total = (h24 * 60 + m + minutes) % (24 * 60)
    h24, m = divmod(total, 60)
    ap = "am" if h24 < 12 else "pm"
    h = h24 % 12 or 12
    return f"{h}:{m:02d} {ap}"


def _bracket(mins):
    if mins <= 15:
        return "Up to 15 minutes"
    if mins <= 30:
        return "16 to 30 minutes"
    return "More than 30 minutes"


def _late_rows(rng):
    names = {c: n for c, n, _, _ in DELAY_CODES}
    rows = []
    for promised, late, codes, advisory in LATE_EXAMPLES:
        delivered = _add_minutes(promised, late)
        cust = sum(m for _, m in codes if m)
        code_txt = "; ".join(f"{c} {names[c]}" + (f" ({m} min on the timer)" if m else "") for c, m in codes)
        if advisory:
            result = pick(rng, ["Declared advisory in force: Section 5 excludes the order. Nothing is credited.",
                                "Advisory banner was showing: excluded under Section 5. No compensation row applies."])
        else:
            counted = late - cust
            row = _bracket(counted)
            if cust:
                result = pick(rng, [
                    f"{late} minutes after the promised time, less {cust} customer-side minutes = {counted} counted. Row: \"{row}\".",
                    f"{late} − {cust} = {counted} minutes counted. The system uses the \"{row}\" row of Section 5."])
            else:
                result = pick(rng, [f"All {late} minutes are QuickBasket-side. Row: \"{row}\".",
                                    f"No customer-side time. {late} minutes counted; the \"{row}\" row of Section 5 applies."])
        rows.append([promised, delivered, code_txt, result])
    return rows


def ch10(rng):
    code_rows = [[c, n, d, SIDE_LABEL[s]] for c, n, d, s in DELAY_CODES]
    n_qb = sum(1 for x in DELAY_CODES if x[3] == "QB")
    n_c = sum(1 for x in DELAY_CODES if x[3] == "CUST")
    n_a = sum(1 for x in DELAY_CODES if x[3] == "ADV")
    return [
        ("h", "10. Late deliveries and delay reason codes"),
        ("h3", "10.1 How lateness is measured"),
        ("p", "Every order shows the customer a **promised delivery time at checkout**. That time is fixed when "
              "the order is placed. It is the only time that counts for lateness, even if the estimated arrival "
              "shown on the tracking screen moves later."),
        ("p", "The **delivered time** is the time the app marks the order delivered: the moment the handover OTP "
              "is verified, or, for a leave-at-door order, the moment the handover photo is uploaded."),
        ("p", "**Lateness = delivered time in the app minus promised time at checkout.** The system works it out. "
              "Nobody types it in, and nobody can edit either time: not you, not the store, not Support."),
        ("ul", [
            "If the delivery was late, the app asks you for a **delay reason code** before you can close the "
            "order. The store adds its own code at the counter if the delay started there. An order can carry more than one code.",
            "Minutes recorded on the **gate timer** and the **door timer** for customer-side reasons, and time "
            "lost to a wrong address that the app has on record, are customer-side minutes. They are taken out "
            "of the lateness before Section 5 of the Customer Policy is applied. Only the remaining minutes count.",
            "If a **declared advisory** was in force for the zone, Section 5 excludes the order. This is applied "
            "by the system from the advisory's start and end times, not from what a partner selects.",
            "Everything else counts in full. A late order with only QuickBasket-side codes is a late order."]),
        ("h3", "10.2 What you say to the customer about a late delivery"),
        ("p", "Apologise, briefly and sincerely: \"Sorry for the delay.\" That is all."),
        ("ul", [
            "**Never tell a customer what compensation they will get**, whether they will get any, or that they "
            "will get none. Compensation for late delivery is credited automatically under Section 5 of the "
            "Customer Policy; nobody at the door decides it.",
            "Do not tell the customer which reason code you are selecting, and do not let a customer talk you "
            "into a code (\"just say it was the store\").",
            "Do not blame the store, the traffic police, the app or the customer.",
            "If the customer asks, say: \"If anything is due for the delay, it is added automatically. You can "
            "see it in your app or ask Support in chat.\""]),
        ("h3", "10.3 The two kinds of delay"),
        ("table", ["Kind", "What it covers", "Effect under Section 5 of the Customer Policy"], [
            ["Customer-side", "Exactly three things: **wrong address**, **customer not reachable**, **gated community entry**.",
             "Excluded. These minutes do not count towards lateness."],
            ["Advisory", "A weather or traffic advisory **declared by City Operations** and shown as a banner in the app.",
             "Excluded while the advisory is in force."],
            ["QuickBasket-side", "**Everything else**: store delay, partner delay, vehicle breakdown, app outage, "
             "stock-out found at packing, ordinary traffic, rain without a declared advisory, and any cause not listed above.",
             "Counts. Compensation applies as set out in Section 5 and is credited automatically."]], [30, 84, 60]),
        ("p", "When in doubt, a delay is QuickBasket-side. A customer-side code is used only when the app has "
              "the record to support it: the gate timer, the door timer, two logged masked calls, or an address "
              "correction. The app will not let you select a customer-side code without that record, and City "
              "Operations reviews customer-side codes every day."),
        ("h3", "10.4 Delay reason codes"),
        ("p", f"There are {len(DELAY_CODES)} codes: {n_qb} QuickBasket-side, {n_c} customer-side and {n_a} "
              "advisory. D-1xx codes are store causes, D-2xx partner and vehicle causes, D-3xx system causes, "
              "D-4xx road and other causes, D-5xx customer-side causes, and D-6xx declared advisories."),
        ("table", ["Code", "Name", "Description", "Counts as"], code_rows, [14, 38, 74, 48]),
        ("h3", "10.5 Choosing the right code"),
        ("ol", [
            "Choose the code for what actually caused the delay, not for what is easiest to explain.",
            "If two things happened, select both. The app records the minutes for each from its own timers "
            "where it has them.",
            "D-5xx codes appear in your list only if the matching timer or call record exists for the order.",
            "D-6xx codes appear only while City Operations has an advisory in force for the zone. If you see "
            "heavy rain and no banner, the code is D-402.",
            "If nothing fits, choose D-405 and write one line. Do not pick a customer-side code because "
            "nothing else fits.",
            "A code can be corrected only by City Operations, after review. Ask through Partner Help the same day."]),
        ("table", ["Tempting mistake", "Why it is wrong", "Correct code"], [
            ["Selecting gate entry delay because the society is large and the walk was long", "Walking after entry is not waiting for entry", "D-210"],
            ["Selecting not reachable when you called once and left", "The rule is two calls and the full door wait", "Go back to 6.6; no customer-side code"],
            ["Selecting weather advisory because it was raining hard", "Only City Operations declares an advisory", "D-402"],
            ["Selecting wrong address when the app's map was wrong but the typed address was right", "That is our map error", "D-303"],
            ["Selecting traffic advisory for an ordinary evening jam", "A jam is not an advisory", "D-401"],
            ["Selecting customer not reachable when masked calling was down", "The customer could not have answered", "D-305"],
            ["Selecting store delay for your own late arrival at the store", "The store clock starts when you tap Reached store", "D-202"]],
         [70, 62, 42]),
        ("h3", "10.6 Worked examples"),
        ("p", "These examples show how the system counts minutes. The rows named in the last column are the "
              "rows of the late-delivery table in Section 5 of the Customer Policy. What each row gives the "
              "customer is in the Customer Policy, not here, and is never discussed at the door."),
        ("table", ["Promised at checkout", "Delivered in the app", "Codes on the order", "How the system counts it"],
         _late_rows(rng), [24, 24, 62, 64]),
        ("h3", "10.7 Misuse of reason codes"),
        ("p", "Selecting a customer-side or advisory code that is not true takes away something the customer is "
              "owed. Starting a gate timer when you are not at a gate, tapping Arrived from the road, or entering "
              "an OTP before the handover are false records. Each is a serious compliance issue and can end "
              "your access to the platform. Honest QuickBasket-side codes are never held against a partner "
              "when the cause was outside the partner's control."),
    ]


# ----------------------------------------------------------------------------------------------- chapter 11
ADVISORY_CITIES = [
    ["Hyderabad", "Heavy-rain advisories", "Mostly July to October",
     "The app routes around waterlogging-prone underpasses automatically. Do not override it."],
    ["Bengaluru", "Heavy-rain advisories", "May to October",
     "Some low-lying roads near Bellandur and Silk Board are paused during declared advisories."],
    ["Chennai", "Cyclone and heavy-rain advisories", "Mainly October to December (northeast monsoon)",
     "Customers get a longer reporting window for fresh, dairy and frozen or meat items on orders delivered "
     "during the advisory (see the Chennai city addendum). Do not explain it at the door; point to Support."],
    ["Pune", "Monsoon advisories", "June to September",
     "Take extra care on the ghat-side areas near Warje and Bavdhan."],
    ["Mumbai", "Monsoon advisories, including red-alert days", "June to September",
     "On red-alert days, deliveries to low-lying localities (parts of Kurla, Sion, Andheri East and Dahisar "
     "side lanes) may be paused. The customer's app shows the pause before checkout."],
    ["Delhi NCR", "Fog advisories; air-quality advisories", "Fog: December to January. Air quality: when declared",
     "During fog advisories promised times are extended. During air-quality advisories partners' outdoor work is limited."],
]


def ch11():
    return [
        ("h", "11. Weather and traffic advisories"),
        ("h3", "11.1 Who declares an advisory"),
        ("p", "**Only QuickBasket City Operations declares an advisory.** A delivery partner cannot. A store "
              "cannot. A Store Shift Lead cannot. Support cannot. A news report, a government alert, a message "
              "in a partner group or a flooded road in front of you is not a QuickBasket advisory until City "
              "Operations declares one."),
        ("p", "This matters to customers. Under Section 5 of the Customer Policy, late-delivery compensation "
              "does not apply during a declared weather or traffic advisory. So an advisory must be a formal, "
              "recorded decision with a start time, an end time and a zone, not an opinion at the door."),
        ("h3", "11.2 How you know one is in force"),
        ("ul", [
            "A declared advisory is shown as a **banner** at the top of the partner app and at the top of the "
            "customer's app and order page, for the city or the zones it covers.",
            "The banner names the type (weather or traffic), the zones and the time it was declared. It "
            "disappears when City Operations ends the advisory.",
            "If there is no banner, there is no advisory. Use the ordinary codes (D-401, D-402, D-403).",
            "An advisory can cover a whole city or only some zones. An order outside the zones named in the "
            "banner is not covered by it."]),
        ("h3", "11.3 What changes for you during an advisory"),
        ("ol", [
            "Promised delivery times shown to customers at checkout are extended by the system. You do not need to ride faster.",
            "Some roads or localities may be paused. The app will not route you through a paused road or "
            "assign you an order for a paused locality.",
            "The D-601, D-602 and D-603 codes become available for orders in the covered zones.",
            "Safety rules get stricter, not looser: no riding through standing water, no riding in fog without "
            "working lights, and stop if you cannot see the road.",
            "If you feel it is unsafe to continue, stop somewhere safe and tell Partner Help. You are not "
            "penalised for stopping during a declared advisory."]),
        ("h3", "11.4 What you say to customers"),
        ("ul", [
            "You may say: \"There is an advisory showing in the app for this area today, so deliveries are slower.\" "
            "Say it only if the banner is showing.",
            "Do not say \"so you will not get compensation\" or anything else about compensation.",
            "Do not tell a customer there is an advisory when there is none, to excuse a late delivery. "
            "The customer can see for themselves whether the banner is in their app."]),
        ("h3", "11.5 Asking for an advisory"),
        ("p", "If conditions are dangerous and no banner is showing, report it: tap **Report road problem** or "
              "chat with Partner Help with your location and one line on what you see. Shift Leads pass the "
              "same information to City Operations from the store console. City Operations decides, using "
              "reports from several partners and stores and official alerts. Until it decides, there is no advisory."),
        ("h3", "11.6 City notes on advisories"),
        ("table", ["City", "Advisories you will see", "Usual season", "What to know"], ADVISORY_CITIES, [22, 36, 36, 80]),
        ("p", "In every city the rule is the same: the advisory exists when City Operations declares it and "
              "the banner shows, and it ends when the banner goes."),
    ]


# ----------------------------------------------------------------------------------------------- chapter 12
CITY_NOTES = [
    dict(city="Hyderabad", hours="6:00 am to 1:00 am", notes=[
        "**Gated communities.** Many large communities in Gachibowli, Kondapur, Kokapet and Narsingi need an "
        "entry OTP at the gate. Start the gate timer and wait up to 7 minutes (6.5).",
        "**Old City.** Parts of Abids and the area around Charminar are served by bicycle partners during "
        "evening peak hours. If you are on a motorbike and are assigned there in the evening, park outside "
        "the narrow lanes and walk.",
        "**Tech parks.** Inside HITEC City and Nanakramguda office campuses, hand over at the reception or the "
        "visitor desk, not at individual desks.",
        "**Rain.** Heavy-rain advisories are most common from July to October. Underpasses that flood are "
        "avoided by the app's routing."]),
    dict(city="Bengaluru", hours="6:00 am to 1:00 am", notes=[
        "**QB Tech Hub same-day swaps.** Koramangala (BLR-01), HSR Layout (BLR-03) and Whitefield (BLR-04) are "
        "QB Tech Hub stores. When Support approves an electronics replacement before 6 pm, inside the "
        "customer's electronics window, for an item bought from one of these stores, the replacement is "
        "delivered the same day. You deliver the new item and collect the old one. Follow the swap steps below.",
        "**Apartment towers.** In large complexes on Sarjapur Road and in Whitefield, go to the flat door if the "
        "association allows it, otherwise hand over in the lobby.",
        "**Tech parks.** In Electronic City and the Outer Ring Road tech parks, deliveries go to the security "
        "desk of the building named in the address.",
        "**Rain.** Heavy-rain advisories run from May to October. Low-lying roads near Bellandur and Silk Board "
        "may be paused during declared advisories."]),
    dict(city="Chennai", hours="6:00 am to midnight", notes=[
        "**Cyclone and heavy-rain advisories.** Mainly October to December. During a declared advisory, work "
        "to the stricter safety rules in Chapter 11.",
        "**Coastal roads.** During high-tide warnings, East Coast Road and the Besant Nagar beach-side lanes may "
        "be served by a different store. Check which store your order is from before you ride.",
        "**OMR offices.** On Old Mahabalipuram Road, from Perungudi to Sholinganallur, hand over at the building reception.",
        "**Heat.** In summer afternoons, cold orders are sent with a third gel pack. Ask the packer if it is missing."]),
    dict(city="Pune", hours="6:30 am to midnight", notes=[
        "**Hinjewadi Phase 3: no cash on delivery.** You will never see a COLLECT CASH bar for a Phase 3 "
        "address. Do not carry order cash into the IT-park security zone, and never collect cash from a Phase 3 customer.",
        "**Hinjewadi Phases 1 and 2.** Deliver to the main gate reception of the campus named in the address.",
        "**Housing societies.** Most societies in Baner, Wakad and Kharadi need the customer to approve you on "
        "the society's visitor app. Start the gate timer; waiting for approval is a customer-side delay.",
        "**Monsoon.** Advisories are most likely from June to September. Ride with extra care on the ghat-side "
        "areas near Warje and Bavdhan."]),
    dict(city="Mumbai", hours="6:00 am to 1:00 am", notes=[
        "**Red-alert days.** When the city is under a red alert for heavy rain and City Operations has "
        "declared an advisory, deliveries to low-lying localities (parts of Kurla, Sion, Andheri East and "
        "Dahisar side lanes) may be paused. You will not be assigned orders for a paused locality.",
        "**Old buildings without lifts.** In older buildings in Dadar, Matunga and Fort without lifts, heavy "
        "orders (over 15 kg) are delivered to the ground floor unless the customer asked for doorstep delivery "
        "in the order notes. Check the notes before you call the customer down.",
        "**Navi Mumbai and Thane.** Vashi, Nerul, Kharghar and Thane West are served by their own stores. You "
        "will not be sent across the creek from a main city store.",
        "**Local trains and bridges.** Do not carry orders on trains or cross railway tracks on foot to save time."]),
    dict(city="Delhi NCR", hours="24 hours at DEL-01 Connaught Place, DEL-03 Saket, DEL-06 Gurugram DLF Phase 4 "
                               "and DEL-08 Noida Sector 18; 6:00 am to 1:00 am at other stores", notes=[
        "**24-hour stores.** The four 24-hour stores run a night shift from 11:00 pm to 6:00 am. Night-shift "
        "partners must have working lights and a reflective jacket, and collect them at the store if missing.",
        "**Late-night surcharge.** Customers who order from the 24-hour stores between 11:00 pm and 6:00 am pay "
        "a late-night surcharge in their bill. It is already included in the amount on your screen. You never "
        "collect it separately and you never explain or waive it; questions go to Support.",
        "**Fog.** During declared fog advisories (December to January) promised times are extended. Ride with "
        "the headlight on low beam and stop if you cannot see the road.",
        "**Air quality.** When City Operations declares an air-quality advisory, outdoor work is limited: "
        "shifts are shortened and masks are issued at the store.",
        "**Gurugram and Noida towers.** Large residential towers usually need gate entry through the society's "
        "visitor app. Start the gate timer; waiting for entry is a customer-side delay."]),
]


def ch12(rng):
    b = [("h", "12. City notes for partners"),
         ("p", "The rules in this SOP are the same in all six cities: Hyderabad, Bengaluru, Chennai, Pune, Mumbai "
               "and Delhi NCR. The notes below add local detail. What customers are promised in each city is in "
               "the city addenda to the Customer Policy, not here. Kochi and Jaipur are not live: there are no "
               "stores, no orders and no partner shifts there yet.")]
    for n, c in enumerate(CITY_NOTES, 1):
        opener = pick(rng, ["Store hours", "Stores are open", "Dispatch hours"])
        b += [("h3", f"12.{n} {c['city']}"),
              ("p", f"{opener}: {c['hours']}. Your shift can only start and end inside these hours."),
              ("ul", c["notes"])]
    b += [
        ("h3", "12.7 Bengaluru: QB Tech Hub swap steps"),
        ("p", "A swap is a delivery and a collection in one visit. It exists only in Bengaluru, only from the "
              "three QB Tech Hub stores, and only after Support has approved the replacement. You never decide "
              "whether a customer is eligible; the swap task appears in your app when it has been approved."),
        ("ol", [
            "At the store, collect the replacement in its security pouch. Scan the pouch. The app shows \"Swap: collect old item\".",
            "At the door, ask for the OTP as usual. Leave-at-door is not offered on a swap.",
            "Ask the customer for the old item with its box and all accessories. Check them against the "
            "checklist on your screen (for example: handset, charger, cable, manual, box).",
            "Do not test the old item or judge whether it is faulty. If something on the checklist is missing, "
            "tick \"missing\" for that line and take a photo of what was handed over. Do not refuse the swap "
            "yourself; chat with Partner Help, who will tell you whether to proceed.",
            "Put the old item in the return pouch, seal it in front of the customer and scan it.",
            "Hand over the replacement. Enter the OTP.",
            "Return the old item to the Tech Hub store the same shift and get a return receipt."]),
        ("table", ["City", "Local point", "Chapter"], [
            ["Hyderabad", "Gate OTPs in Gachibowli, Kondapur, Kokapet, Narsingi; reception handover in tech parks", "6.4, 6.5"],
            ["Bengaluru", "QB Tech Hub swaps from BLR-01, BLR-03, BLR-04", "12.7"],
            ["Chennai", "Cyclone and heavy-rain advisories; OMR receptions", "11, 6.4"],
            ["Pune", "No cash on delivery in Hinjewadi Phase 3; main gate reception in Phases 1 and 2", "9.1, 6.4"],
            ["Mumbai", "Red-alert pauses; ground-floor delivery of heavy orders in old buildings without lifts", "11, 12.5"],
            ["Delhi NCR", "Four 24-hour stores; night shift; fog and air-quality advisories", "12.6, 11"]], [26, 118, 30]),
    ]
    return b


# ----------------------------------------------------------------------------------------------- chapters 13-14
def ch13():
    return [
        ("h", "13. Customer conduct, abuse, safety incidents and accidents"),
        ("p", "You are entitled to be treated with respect, and so is the customer. Most deliveries are polite "
              "and take under a minute. This chapter is for the few that are not."),
        ("h3", "13.1 Your conduct"),
        ("ul", [
            "Be polite, brief and factual. Do not argue, raise your voice or use abusive language, even in reply.",
            "Do not enter homes. Do not accept food, drink or gifts beyond a glass of water.",
            "Do not contact a customer after the delivery for any reason. No calls, no messages, no social media.",
            "Do not ask personal questions and do not comment on a customer's home, family or order.",
            "Never threaten to cancel, delay or withhold an order."]),
        ("h3", "13.2 Abuse or threats from a customer or anyone at the address"),
        ("ol", [
            "Do not respond in kind. Step back from the door.",
            "If the handover can be completed safely (OTP given), complete it and leave.",
            "If it cannot, say: \"I am not able to complete this delivery. Support will contact you.\" Leave with the order.",
            "Once you are away from the address, tap **Report incident › Abuse or threat** and describe what "
            "was said or done, in plain words. Do not record audio or video of the customer.",
            "If you took the order away, return it to the store (Chapter 8) and tell the Shift Lead.",
            "Partner Help calls you back through the app. The customer's side is handled by a human Support agent."]),
        ("h3", "13.3 If you feel unsafe"),
        ("ul", [
            "Leave. You never have to stay at an address where you feel in danger, and you never have to enter "
            "a dark stairwell, a locked compound or a flat to complete an order.",
            "Press the **SOS** button in the app. It shares your live location with City Operations and opens a "
            "priority line to Partner Help. If you are in immediate danger, call the emergency services first.",
            "Animals: if a dog is loose at the gate or door, do not go in. Use masked calling and ask the "
            "customer to come out or to tie it up. Waiting for this is recorded on the door timer.",
            "Harassment of any kind, including sexual harassment, is reported the same way and is followed up "
            "by the Partner Safety team, not by the store."]),
        ("h3", "13.4 Accidents"),
        ("ol", [
            "Stop. Get yourself off the road. Your safety comes before the vehicle, the order and the time.",
            "If you or anyone else is hurt, call the emergency services. Then press SOS in the app.",
            "Do not continue the delivery if you are hurt, shaken or the vehicle is damaged. Tell Partner Help; "
            "the order is reassigned (code D-207 or D-208).",
            "If you can do so safely, take photos of the scene and the vehicles in the partner app's incident form.",
            "Do not admit fault, sign anything or hand over money at the scene. Exchange names and vehicle numbers.",
            "Tell your Shift Lead the same day. Fill in the accident report in the app within one day of the "
            "accident. This is needed for the partner accident insurance claim."]),
        ("h3", "13.5 What to report, and to whom"),
        ("table", ["What happened", "Report to", "How", "When"], [
            ["Accident, injury, fall", "Partner Help and Shift Lead", "SOS, then Report incident › Accident", "Immediately; written report within one day"],
            ["Abuse, threat or harassment by a customer", "Partner Help (passed to Partner Safety)", "Report incident › Abuse or threat", "As soon as you are away from the address"],
            ["Robbery or theft of cash, order or vehicle", "Partner Help, Shift Lead and the police", "SOS, then Report incident › Theft", "Immediately"],
            ["Damaged, wrong or missing item at the door", "Recorded on the order for Support", "Report item issue", "At the door"],
            ["Cold chain break", "Recorded on the order; Shift Lead on return", "Report item issue › Cold chain break", "Before handover"],
            ["Unsafe road, flooding, blocked route", "City Operations", "Report road problem", "When stopped safely"],
            ["Cash shortfall or mismatch", "Store cash desk and Shift Lead", "At deposit", "Same shift"],
            ["Customer asks you to break a rule (no OTP, cash for a prepaid order, different address)", "Partner Help", "In-app chat", "Before you act"],
            ["Another partner or store employee breaking this SOP", "City Operations", "Report incident › Compliance, or conduct@quickbasket.example", "Any time; can be anonymous"],
            ["Suspected fraud (fake OTP requests, someone posing as QuickBasket staff)", "Partner Help", "In-app chat", "Immediately"]],
         [50, 40, 48, 36]),
        ("p", "Written follow-up, where the app is not enough: partnerhelp@quickbasket.example for anything "
              "about shifts, payouts and this SOP; partnersafety@quickbasket.example for safety incidents."),
        ("h3", "13.6 People pretending to be QuickBasket"),
        ("p", "QuickBasket staff never ask you for a customer's OTP, your app password or your payout details "
              "by call or message. If someone does, it is fraud. Do not share anything; report it in Partner "
              "Help chat."),
    ]


def ch14():
    return [
        ("h", "14. Privacy"),
        ("p", "Customers trust you with their address and with the fact of what they ordered. That information "
              "is for one purpose: completing this delivery. When the delivery ends, your use of it ends."),
        ("h3", "14.1 Masked calling"),
        ("ul", [
            "All calls between you and a customer go through **masked calling** in the partner app. You tap the "
            "call button on the order; the customer sees a QuickBasket number, and you never see theirs.",
            "Masked calling works only while the order is live. It stops when the order is delivered, refused or returned.",
            "Calls made through the app are logged (time and whether answered). That log is what proves the two "
            "calls in the not-reachable rule.",
            "If masked calling does not connect, do not look for another way to reach the customer. Chat with "
            "Partner Help and record D-305 if the order becomes late."]),
        ("h3", "14.2 Never keep customer phone numbers"),
        ("ul", [
            "If a customer calls you directly or gives you their number, do not save it. Do not write it on a "
            "bag, in a notebook or in your phone.",
            "Do not give customers your personal number, and do not agree to \"call me directly next time\".",
            "Do not message customers on any chat app, before or after the delivery.",
            "Do not ask security guards or neighbours for a customer's number."]),
        ("h3", "14.3 Never keep photos of customers"),
        ("ul", [
            "Take photos only inside the partner app, and only the photos this SOP asks for: the leave-at-door "
            "handover photo, item issue photos, incident photos.",
            "Photos must not show a customer's face, children, or the inside of a home. If a person walks into "
            "the frame, retake the photo.",
            "Photos taken in the partner app are stored with the order, not in your phone's gallery. Do not "
            "screenshot them.",
            "Never photograph or film a customer, even during an argument. Report it instead (Chapter 13)."]),
        ("h3", "14.4 Addresses, orders and screens"),
        ("ul", [
            "Do not screenshot or share order screens, addresses, customer names or order contents, in partner "
            "groups or anywhere else.",
            "Do not talk about what a customer ordered: not to neighbours, not to security, not to other partners.",
            "Bag labels show only the order ID, the bag number, a first name and a locality. Do not write "
            "anything else on a bag.",
            "If a third person at the gate or the door asks whose order it is or what is in it, say only "
            "\"a QuickBasket delivery for this address\".",
            "Do not visit a customer's address again for any reason other than a new assigned order."]),
        ("h3", "14.5 Your own data"),
        ("p", "The customer sees your first name, your photo, your vehicle type and your live location while "
              "their order is on the way, and nothing after it is completed. Your location is recorded only "
              "while you are on shift. Questions about your data: privacy@quickbasket.example."),
        ("h3", "14.6 If you make a mistake"),
        ("p", "If you saved a number, took a photo outside the app or shared a screen by mistake, delete it and "
              "tell Partner Help the same day. Mistakes reported early are treated as mistakes. Hidden ones are "
              "treated as breaches."),
    ]


# ----------------------------------------------------------------------------------------------- chapter 15
OPENERS = ["What do I do if {q}?", "{Q}. What now?", "Situation: {q}.", "What should I do when {q}?",
           "{Q}. What is the right way to handle it?", "How do I handle it when {q}?"]
CLOSERS = [
    "If you are unsure at any step, stop and chat with Partner Help before you act.",
    "Do not tell the customer what they will get. Support decides under the Customer Policy.",
    "Record it in the app at the time it happens, not from memory at the end of the shift.",
    "When in doubt, choose the safer option and add a note to the order.",
    "Nothing you say at the door changes what the Customer Policy gives the customer.",
    "Partner Help is in the app for exactly this kind of situation.",
]

SCENARIOS = [
    dict(q="the customer says \"I'm driving, just leave it with the guard\"", steps=[
        "Check your handover screen for the Leave at door badge. A request on a call is not enough.",
        "Say: \"I can leave it only if you switch on Leave at door on your order page, or if the guard gives me the OTP.\"",
        "If the guard reads you the correct OTP, hand over to the guard at the gate of the delivery address and note \"handed to security with OTP\".",
        "If neither happens, follow the not-reachable steps: two masked calls, 5 minutes on the door timer, then return to the store."],
        ref="6.2, 6.3, 6.6"),
    dict(q="the customer opens the door but cannot find the OTP", steps=[
        "Ask them to open the QuickBasket app, tap Orders and tap the live order. The 4-digit OTP is under the delivery status.",
        "Wait while they look. The door timer is running; that is fine.",
        "If the order was placed by someone else, ask them to get the OTP from that person.",
        "If no OTP can be given, do not hand over. Record \"Order refused at door: OTP not shared\" and return the order to the store."],
        ref="6.1, 6.7, 8.3"),
    dict(q="the society gate will not let me in and the customer is not answering", steps=[
        "Tap **At gate: waiting for entry** as soon as you are stopped.",
        "Make one masked call to tell the customer you are at the gate.",
        "Wait up to 7 minutes on the gate timer.",
        "Call a second time and offer handover at the gate.",
        "If the second call is not answered, tap **Customer not reachable** and take the order back to the store."],
        ref="6.5, 6.6"),
    dict(q="the customer finds a broken bottle in the bag while I am still at the door", steps=[
        "Say you are sorry and that you will record it on the order.",
        "Tap **Report item issue › Damaged**, select the item and take a photo of the item and its bag in the partner app.",
        "Tell the customer to raise the request from their order page or in Support chat.",
        "Do not promise a refund or a replacement, and do not say how long anything will take.",
        "If the customer does not want to keep the broken item, take it away in a spare bag and mark \"Item returned with partner\"."],
        ref="7.1, 7.3"),
    dict(q="the customer says one item is not what they ordered", steps=[
        "Complete the handover with OTP if it is not already done.",
        "Tap **Report item issue › Wrong item** and photograph the item.",
        "Ask whether they want to keep the item for now. If not, take it back sealed and mark \"Item returned with partner\".",
        "Tell them to raise it in their app. Support decides what happens."],
        ref="7.1, 7.3"),
    dict(q="the customer wants to keep the groceries but send one item back because they changed their mind", steps=[
        "Explain that you cannot open a sealed bag or take a single item back at the door.",
        "The customer can accept the whole order and raise a request for that item from the order page, or refuse the whole order.",
        "Do not say whether the item can be returned. That depends on its category under the Customer Policy and is for Support to decide.",
        "Record nothing extra unless the customer refuses the whole order."],
        ref="8.2"),
    dict(q="the customer refuses the whole order at the door", steps=[
        "Ask once whether they are refusing the whole order.",
        "Tap **Order refused at door** and pick the closest reason.",
        "Do not ask for the OTP and do not collect cash.",
        "Tell them that anything about a refund is handled from the order page or by Support in chat.",
        "Return the sealed bags to the store and get the return receipt."],
        ref="8.1, 8.3"),
    dict(q="a cash customer offers to pay by UPI to my own number", steps=[
        "Decline politely. A cash order is paid in cash; you never take money into a personal account.",
        "Explain that the payment method cannot be changed after the order is placed.",
        "If the customer has no cash, they can refuse the order. Record \"Order refused at door: payment not made\".",
        "Return the order to the store."],
        ref="9.2"),
    dict(q="I do not have enough change for a ₹2,000 note", steps=[
        "Ask if the customer has a smaller note or the exact amount.",
        "Use change from cash you collected on earlier orders if you have it.",
        "If you still cannot make change, chat with Partner Help before leaving the door.",
        "Never leave owing change, and never keep the difference as a tip unless the customer clearly offers it."],
        ref="9.3"),
    dict(q="an order for a Hinjewadi Phase 3 address shows no amount to collect but the customer wants to pay cash", steps=[
        "Check your screen: no COLLECT CASH bar means the order is prepaid.",
        "Tell the customer the order is already paid and that cash on delivery is not offered in Hinjewadi Phase 3.",
        "Do not accept any cash.",
        "Do the normal OTP handover at the handover point for the campus."],
        ref="9.1, 12.4"),
    dict(q="it is raining heavily, I am going to be late, and there is no advisory banner in the app", steps=[
        "Ride safely. Shelter if you must, and tap **Sheltering: rain** so the customer sees an updated arrival time.",
        "Do not tell the customer there is an advisory. There is none until City Operations declares it.",
        "If conditions are dangerous, tap **Report road problem** so City Operations knows.",
        "When you close the order, select D-402 Rain, no advisory. It is a QuickBasket-side delay.",
        "Apologise for the delay at the door and say nothing about compensation."],
        ref="5.4, 10, 11"),
    dict(q="the customer asks \"you are 40 minutes late, what do I get?\"", steps=[
        "Apologise for the delay.",
        "Say: \"If anything is due for the delay, it is added automatically. You can see it in your app or ask Support in chat.\"",
        "Do not name an amount, do not say whether they will or will not get something, and do not mention reason codes.",
        "Select the true delay reason code when you close the order."],
        ref="10.2"),
    dict(q="my bike gets a puncture on the way to the customer", steps=[
        "Stop somewhere safe, off the road.",
        "Tap **Vehicle problem › Puncture** in the app. The customer sees an updated arrival time.",
        "If the repair will take more than a few minutes, chat with Partner Help. The order may be reassigned to another partner.",
        "If the order has cold items, watch the cold clock and tell Partner Help the minutes remaining.",
        "The delay code is D-205. It is QuickBasket-side, whatever the customer was told."],
        ref="2.2, 10.4"),
    dict(q="the partner app freezes just as I reach the door", steps=[
        "Close and reopen the app once. Check that you have network.",
        "If the OTP screen will not open, do not hand over on trust.",
        "Chat with Partner Help (or ask the customer to open Support chat if your app is fully down). Partner Help can confirm the handover from their side after the customer confirms in the customer's app.",
        "When the app is back, select D-301 or D-304 if the order was late."],
        ref="6.7, 10.4"),
    dict(q="the cold clock turns red before I reach the customer", steps=[
        "Do not hand over the frozen, meat or dairy items covered by the clock.",
        "Tap **Report item issue › Cold chain break**, select the items and take the photos.",
        "Hand over the rest of the order with OTP. On a cash order, collect the recalculated amount on your screen.",
        "Tell the customer the items were not kept cold enough and that it is recorded on the order.",
        "Take the cold items back to the store in the cold compartment."],
        ref="4.5"),
    dict(q="the customer points to a pink temperature label on a pack of chicken", steps=[
        "Treat it as a cold chain break for that pack.",
        "Photograph the pack and the label in the partner app and mark the item.",
        "Take the pack back in the cold compartment.",
        "Tell the customer to raise it from the order page. Support may ask them for a photo of the packaging and the label, so suggest they take one before you take the pack."],
        ref="4.3, 4.5, 7.3"),
    dict(q="the store hands me two bags but the app says the order has three", steps=[
        "Do not tap Picked up.",
        "Tell the packer the bag count does not match and wait for the third bag.",
        "Scan all three bags and check each seal.",
        "If the wait makes the order late, the store selects D-101 or D-104 at the counter."],
        ref="3.2, 3.5"),
    dict(q="the map pin takes me to the wrong lane", steps=[
        "Stop and compare the written address with where you are.",
        "Use masked calling to ask the customer for a landmark.",
        "If the customer's written address was wrong or incomplete, or they placed the pin wrongly, record D-501 or D-502.",
        "If the written address was right and the app's map was wrong, record D-303. That one is QuickBasket-side.",
        "If the customer does not answer two calls and you cannot find the address, mark Customer not reachable and return the order."],
        ref="6.8, 10.4"),
    dict(q="the customer calls and asks me to bring the order to their office in another locality instead", steps=[
        "Say that you can deliver only to the address on the order.",
        "Ask them to chat with Support in the app.",
        "Go to the address on the order and follow the normal handover or not-reachable steps there.",
        "Do not ride to the new address, even if it is close and even if the customer offers to pay you."],
        ref="6.8"),
    dict(q="a neighbour offers to take the order because the customer is out", steps=[
        "Do not hand over on the neighbour's word.",
        "Call the customer through masked calling.",
        "If the customer asks you to give it to that neighbour and the neighbour reads you the correct OTP, hand over and note the flat number.",
        "If the customer does not answer, complete the two calls and the 5-minute wait, then return the order."],
        ref="6.3, 6.6"),
    dict(q="the office reception says \"leave it here, we will pass it on\"", steps=[
        "Check for the Leave at door badge and a customer note naming the reception.",
        "If there is no badge, call the customer through masked calling and ask them, or a colleague with the OTP, to come to the reception.",
        "Hand over only against the correct OTP.",
        "If nobody comes, follow the not-reachable steps."],
        ref="6.4"),
    dict(q="the order has the Leave at door badge but it is a cash order", steps=[
        "This should not happen: leave-at-door is not offered on cash orders.",
        "Do not leave the order. Ring the bell and collect cash and OTP as normal.",
        "If nobody answers, follow the not-reachable steps.",
        "Tell Partner Help afterwards so the fault can be looked at."],
        ref="6.2, 9.2"),
    dict(q="the customer is abusive at the door", steps=[
        "Stay calm and step back. Do not reply in kind.",
        "If they give the OTP and it is safe, complete the handover and leave.",
        "If not, say that you cannot complete the delivery and that Support will contact them, then leave with the order.",
        "Away from the address, tap **Report incident › Abuse or threat**.",
        "Return the order to the store if you still have it."],
        ref="13.2"),
    dict(q="there is a loose dog at the gate of the house", steps=[
        "Do not enter.",
        "Tap Arrived and call the customer through masked calling. Ask them to come out or tie up the dog.",
        "Wait on the door timer. Make the second call if the first is not answered.",
        "If nobody comes within the 5-minute wait, mark Customer not reachable and return the order."],
        ref="13.3, 6.6"),
    dict(q="I am in a minor accident and the bags fall on the road", steps=[
        "Get yourself to safety first. Check whether you are hurt.",
        "Press SOS or chat with Partner Help.",
        "Photograph the bags in the incident form. Do not re-pack items into the bags and carry on as if nothing happened.",
        "Partner Help decides whether the order continues, is reassigned or goes back to the store.",
        "If you do deliver, tell the customer the bags fell and add the note to the order."],
        ref="13.4, 3.3"),
    dict(q="a customer on a Bengaluru swap hands me the old phone without its charger", steps=[
        "Tick \"missing\" against the charger on the checklist.",
        "Photograph what was handed over.",
        "Chat with Partner Help before you hand over the replacement. They tell you whether to proceed.",
        "Do not tell the customer the swap is refused or approved on your own judgement."],
        ref="12.7"),
    dict(q="the customer says the ice cream is soft and asks me to take it back and bring another", steps=[
        "Check the cold clock on your screen. If it is red, follow the cold chain break steps.",
        "If it is not red, tap **Report item issue › Spoiled or warm**, photograph the item and mark it.",
        "Do not promise to bring another one. You cannot.",
        "Tell them to raise it from the order page; Support decides."],
        ref="4.5, 7.1, 7.2"),
    dict(q="security at a gated community wants to keep my partner ID card until I come out", steps=[
        "Offer to show the card and sign the visitor register instead.",
        "If they insist on keeping the card or your keys, do not hand them over.",
        "Call the customer and offer handover at the gate.",
        "The time waiting at the gate is on the gate timer, up to 7 minutes."],
        ref="6.5"),
    dict(q="the customer gave the OTP on a call while I was still two streets away", steps=[
        "Do not enter it.",
        "Ride to the door, tap Arrived, and ask the person at the door to read the OTP again.",
        "Enter the OTP only at the handover point, at the moment of handover."],
        ref="6.1, 10.7"),
    dict(q="I reach the door and the customer says they already cancelled the order", steps=[
        "Check your app. If the order is still live, it has not been cancelled; an order that is out for delivery cannot be cancelled in the app.",
        "Tell the customer they can accept the order or refuse it at the door.",
        "If they refuse, record **Order refused at door** and return the order.",
        "Do not discuss fees or refunds. Point them to Support."],
        ref="8.1"),
    dict(q="the customer in a Mumbai building without a lift asks me to carry a 20 kg order to the fourth floor", steps=[
        "Check the order notes. If the customer asked for doorstep delivery in the notes, carry it up, in two trips if needed.",
        "If there is no such note, heavy orders in these buildings are handed over on the ground floor.",
        "Explain politely and ask the customer to come down with the OTP.",
        "If the stairs make the order late, the code is D-211, not a customer-side code."],
        ref="12.5, 10.4"),
    dict(q="a customer asks whether there is a weather advisory today because the delivery is late", steps=[
        "Look at the banner in your app.",
        "If a banner is showing for the zone, you may say so.",
        "If there is no banner, say \"No, there is no advisory in the app right now.\"",
        "Either way, say nothing about compensation."],
        ref="11.2, 11.4"),
    dict(q="someone calls me saying they are from QuickBasket and asks for the customer's OTP", steps=[
        "Do not share anything. QuickBasket staff never ask for an OTP by call.",
        "End the call.",
        "Report it in Partner Help chat straight away."],
        ref="13.6"),
]


def ch15(rng):
    b = [("h", "15. Scenarios: \"What do I do if...\""),
         ("p", f"These {len(SCENARIOS)} short scenarios come from real questions partners ask Partner Help. Each "
               "one applies the chapters above; none of them adds a new rule. The chapter reference at the end "
               "of each scenario tells you where the rule is written.")]
    order = list(range(len(SCENARIOS)))
    rng.shuffle(order)
    for n, i in enumerate(order, 1):
        s = SCENARIOS[i]
        q = s["q"]
        title = pick(rng, OPENERS).format(q=q, Q=q[0].upper() + q[1:])
        b.append(("h3", f"15.{n} {title}"))
        b.append(("ol", s["steps"]))
        tail = pick(rng, ["See", "Rule:", "Where it is written:", "Reference:"]) + f" {s['ref']}."
        if rng.random() < 0.45:
            tail += " " + pick(rng, CLOSERS)
        b.append(("small", tail))
    return b


# ----------------------------------------------------------------------------------------------- chapter 16
GLOSSARY = [
    ("Advisory", "A weather or traffic advisory declared by City Operations for a city or zone, shown as a banner in the app. Nobody else can declare one."),
    ("Arrived", "The button you tap at the handover point. It starts the door timer."),
    ("Bag label", "The sticker on each sealed bag: order ID, bag number, first name, locality."),
    ("Banner", "The strip at the top of the partner app and the customer's app that shows a declared advisory."),
    ("Cash-in-hand limit", "₹6,000 of collected cash, after which cash orders are not assigned until you deposit."),
    ("Change float", "₹500 in small notes and coins issued by the store cash desk at shift start and returned at shift end."),
    ("City Operations", "The city control desk. Declares advisories, pauses roads and localities, reviews reason codes."),
    ("COD", "Cash on delivery. Offered on orders up to ₹3,000; not offered in Hinjewadi Phase 3 (Pune) or for gift cards and Plus."),
    ("Cold chain break", "Any point at which a frozen, meat or dairy item was not kept cold enough. The item is not handed over."),
    ("Cold clock", "The countdown in the partner app for orders with frozen, meat or dairy items."),
    ("Cold compartment", "The zipped, insulated section of the delivery bag that holds gel packs and cold items."),
    ("Customer Policy", "Customer Policy v4.2, effective 1 October 2026. The only place customer promises are written."),
    ("Customer-side delay", "A delay caused by a wrong address, the customer not being reachable, or gated community entry. Excluded under Section 5."),
    ("Delay reason code", "A D-code recorded on a late order to say why it was late."),
    ("Delivered time", "The time the app marks the order delivered: OTP verified, or leave-at-door photo uploaded."),
    ("Door timer", "The timer that runs from Arrived. Used for the 5-minute wait."),
    ("Gate entry delay", "The status recorded while the gate timer is running."),
    ("Gate timer", "The timer that runs from \"At gate: waiting for entry\" to \"Entered\". Used for the wait of up to 7 minutes."),
    ("Gel pack", "A frozen pack that keeps the cold compartment cold. Two per bag, from the store freezer."),
    ("Handover OTP", "The 4-digit code on the customer's order page. The customer reads it to you at handover."),
    ("Handover photo", "The photo taken in the partner app for a leave-at-door delivery. Shows bags and door, never a person."),
    ("Home store", "The store you start and end your shift at and deposit cash at."),
    ("Leave at door", "Contactless delivery chosen by the customer in their app. The only handover without an OTP."),
    ("Masked calling", "Calls through the app that hide the customer's number from you and yours from the customer."),
    ("Order ID", "The order number in the format QB-12345."),
    ("Order page", "The page for one order in the customer's app. Shows status, OTP and the option to raise a request."),
    ("Partner Help", "In-app chat support for partners."),
    ("Partner Safety", "The team that follows up safety incidents, harassment and accidents."),
    ("Promised time", "The delivery time shown to the customer at checkout. Lateness is measured against it."),
    ("QB Tech Hub", "The Bengaluru stores BLR-01, BLR-03 and BLR-04, which do same-day electronics replacement swaps."),
    ("QuickBasket-side delay", "Any delay that is not customer-side and not under a declared advisory. Counts under Section 5."),
    ("Report item issue", "The partner app form for damaged, wrong, missing, warm or leaking items."),
    ("Seal tape", "The QuickBasket tape the store uses to close each bag. Only stores apply it."),
    ("Security pouch", "The tamper-evident pouch for electronics, with a serial sticker that is scanned at pickup."),
    ("Shift Lead", "The Store Shift Lead: the person in charge of the store during a shift."),
    ("SOS", "The emergency button in the partner app."),
    ("Support", "QuickBasket Support for customers: in-app chat, 7:00 am to midnight, every day."),
    ("Swap", "A Bengaluru Tech Hub delivery in which you hand over a replacement and collect the old item."),
    ("Temperature label", "The round sticker on frozen and meat packs: blue when kept cold, pink then red when not."),
]


def ch16():
    return [
        ("h", "16. Quick reference and glossary"),
        ("h3", "16.1 Operations timers and limits"),
        ("p", "These are partner and store operating limits. None of them is a customer return window, a refund "
              "timeline or a compensation amount; for those, see the Customer Policy."),
        ("table", ["What", "Limit", "Chapter"], [
            ["Wait at a gate for entry", "Up to 7 minutes on the gate timer", "6.5"],
            ["Calls to a customer who does not answer", "Two masked calls", "6.6"],
            ["Wait at the door before marking not reachable", "5 minutes on the door timer", "6.6"],
            ["Wrong OTP attempts before the screen locks", "Three; lock lasts two minutes", "6.1"],
            ["Frozen and meat: cold storage to sealed cold compartment", "5 minutes", "4.1"],
            ["Frozen and meat: cold storage to handover", "45 minutes on the cold clock", "4.1"],
            ["Dairy: chiller to sealed cold compartment", "10 minutes", "4.1"],
            ["Dairy: chiller to handover", "90 minutes on the cold clock", "4.1"],
            ["Cash on delivery order value", "Up to ₹3,000", "9.1"],
            ["Change float", "₹500", "2.5, 9.3"],
            ["Cash-in-hand limit", "₹6,000", "9.4"],
            ["Cash deposit", "End of every shift, same day", "9.4"],
            ["Phone battery at shift start", "Above 40%", "2.1"],
            ["Rest break", "After every four hours on shift", "5.2"],
            ["Accident report", "Within one day", "13.4"]], [84, 62, 28]),
        ("h3", "16.2 Who decides what"),
        ("table", ["Question", "Who decides", "What the partner does"], [
            ["Does the customer get a refund or a replacement?", "Support, under the Customer Policy", "Records the issue with a photo. Promises nothing."],
            ["Does the customer get late-delivery compensation?", "Nobody at the door. It is credited automatically under Section 5", "Selects the true reason code. Says nothing about amounts."],
            ["Is there a weather or traffic advisory?", "City Operations only", "Reads the banner. Reports dangerous conditions."],
            ["Is a delay customer-side?", "The app's timers and call log, reviewed by City Operations", "Starts and stops timers honestly."],
            ["Can the order be handed over without OTP?", "Only the customer, by choosing Leave at door in their app", "Checks for the badge."],
            ["Can the address be changed?", "Support", "Delivers only to the address on the order."],
            ["Can a returned item go back into stock?", "Store Shift Lead", "Hands it over sealed and gets a receipt."],
            ["Is a cold item safe to hand over?", "The cold clock and the temperature label", "Does not hand over after a cold chain break."],
            ["Can an electronics swap go ahead with a part missing?", "Partner Help", "Records what is missing and asks."],
            ["Should the order be re-attempted after a failed delivery?", "Support, through the app", "Does not turn around on a customer's call."]],
         [58, 58, 58]),
        ("h3", "16.3 What to say"),
        ("table", ["When", "Say", "Never say"], [
            ["Asking for the OTP", "\"Please read me the 4-digit OTP on your order page.\"", "\"I'll enter it later.\""],
            ["Item damaged or wrong", "\"It is recorded on your order. Please raise it from your order page or chat with Support.\"", "\"You'll get a full refund.\""],
            ["Late delivery", "\"Sorry for the delay.\"", "\"You'll get your delivery fee back.\""],
            ["Asked about compensation", "\"If anything is due, it is added automatically. You can check in the app.\"", "Any amount, or \"you won't get anything\"."],
            ["Customer wants a different address", "\"I can deliver only to the address on the order. Please chat with Support.\"", "\"I'll drop it there for a tip.\""],
            ["Customer wants it left without OTP", "\"Please switch on Leave at door on your order page.\"", "\"Okay, just this once.\""],
            ["Cash customer has no cash", "\"The order is cash on delivery. You can refuse it if you prefer.\"", "\"Send it to my number.\""],
            ["Rain, no banner", "\"Sorry, the rain slowed me down.\"", "\"There's an advisory today.\""]], [40, 84, 50]),
        ("h3", "16.4 Where to get help"),
        ("table", ["Need", "Where"], [
            ["Anything during a live order", "Partner Help, in-app chat"],
            ["Emergency", "Emergency services first, then SOS in the app"],
            ["Disputes at the store counter, cash deposit", "Store Shift Lead"],
            ["Shifts, payouts, questions about this SOP", "partnerhelp@quickbasket.example"],
            ["Safety incidents and harassment", "partnersafety@quickbasket.example"],
            ["Reporting a breach of this SOP", "conduct@quickbasket.example"],
            ["Your personal data", "privacy@quickbasket.example"],
            ["A customer's question about refunds, returns, compensation, Plus, offers or gift cards",
             "Not you. The customer's order page or Support chat in the customer's app."]], [84, 90]),
        ("h3", "16.5 Glossary"),
        ("table", ["Term", "Meaning"], [[t, m] for t, m in GLOSSARY], [40, 134]),
        ("h3", "16.6 Document control"),
        ("table", ["Version", "Effective", "Main changes"], [
            ["2.3", "1 October 2026", "Aligned with Customer Policy v4.2. Delay code list reorganised into six families. "
             "Cold clock added to the partner app. Swap steps for Bengaluru QB Tech Hubs added."],
            ["2.2", "1 June 2026", "Superseded. Do not use."],
            ["2.1", "1 February 2026", "Superseded. Do not use."]], [20, 34, 120]),
        ("p", "Owner: QuickBasket City Operations and Partner Experience. Questions and corrections: "
              "partnerhelp@quickbasket.example. This SOP is an internal operations document. It does not create "
              "or change any promise made to customers; those are in the Customer Policy v4.2."),
    ]


# ----------------------------------------------------------------------------------------------- build
EXCEPTIONS = [
    ("Handover OTP", "6.1 OTP handover",
     "An order is handed over only when the customer (or someone at the address) reads the 4-digit OTP from the "
     "order page; the order is marked delivered at that moment. No OTP, no handover",
     "The Customer Policy does not mention the OTP; it explains why a partner refuses to hand over and what fixes the delivered time"),
    ("Leave at door (contactless)", "6.2 Contactless leave-at-door",
     "The only handover without OTP is Leave at door, selected by the customer in their app; proof is a photo in "
     "the partner app; delivered time is the photo upload time; not offered on cash-on-delivery orders or "
     "Bengaluru Tech Hub swaps; a request by call or by a guard is not enough",
     "Decides whether an order can be left unattended and when it counts as delivered"),
    ("Handover to someone else", "6.3 Handing over to someone else at the address",
     "Anyone at the delivery address with the correct OTP can receive the order; a neighbour only if the customer "
     "asks on a masked call and the neighbour gives the OTP; never on the street or at a different address",
     "Answers 'can someone else collect my order?'"),
    ("Gate entry wait", "6.5 Gated communities",
     "Partner waits up to 7 minutes at the gate on the gate timer (recorded as 'gate entry delay'), then offers "
     "handover at the gate; if the customer can't be reached the order returns to the store",
     "Gate waiting time is customer-side under Section 5; consistent with the city addenda"),
    ("Customer not reachable", "6.6 Customer not reachable",
     "Two masked calls and a 5-minute wait at the door, then the order is marked not reachable and returned to "
     "the store; it is never left at the door, with a neighbour or with security",
     "Not reachable is a customer-side delay; Support decides what happens to the order"),
    ("Partners cannot promise outcomes", "1.3, 7.2 and 10.2",
     "A partner or store employee cannot grant, promise or refuse a refund, replacement or compensation; the "
     "partner records the issue with a photo and the customer raises the request in the app",
     "Anything a partner said at the door does not change what the Customer Policy gives"),
    ("No part-acceptance at the door", "8.2 No part-acceptance at the door",
     "A customer accepts the whole order with the OTP or refuses the whole order; a partner cannot open a sealed "
     "bag or take back a single unwanted item at the door",
     "A customer who wants to send back one item accepts the order and raises a request under the category rules"),
    ("Cold chain break", "4.5 Cold chain break",
     "Frozen, meat or dairy items that were not kept cold (cold clock expired or temperature label pink/red) are "
     "not handed over; the rest of the order is delivered and the items show as not delivered",
     "Explains a partly delivered order; always QuickBasket-side"),
    ("Cash on delivery at the door", "9.2 Collecting cash",
     "Cash orders are paid in cash only, for exactly the amount on the partner's screen; no UPI to the partner, "
     "no extra charges collected by partners; no cash is ever returned at the door",
     "A cash customer without cash can only refuse the order; consistent with 'payment method can't be changed'"),
    ("How lateness is measured", "10.1 How lateness is measured",
     "Lateness = delivered time in the app (OTP verified or leave-at-door photo uploaded) minus the promised "
     "time at checkout; customer-side minutes recorded on the gate and door timers or for a wrong address are "
     "taken out before Section 5 is applied",
     "A late order with some customer-side waiting can fall into a lower row of the Section 5 table"),
    ("Delay reason classification", "10.3 and 10.4",
     "Customer-side is exactly wrong address, not reachable and gated community entry (codes D-501 to D-507); "
     "advisory is only a City Operations declared advisory (D-601 to D-603); everything else, including store "
     "delay, partner delay, breakdown, puncture, app outage, stock-out at packing, ordinary traffic and rain "
     "without a declared advisory, is QuickBasket-side and compensation applies under Section 5",
     "Decides whether late-delivery compensation applies"),
    ("Evidence for customer-side codes", "10.3 The two kinds of delay",
     "A customer-side code can be selected only when the app has the gate timer, door timer, two logged masked "
     "calls or an address correction on record; when in doubt a delay is QuickBasket-side",
     "A partner's word alone does not make a delay customer-side"),
    ("Who declares an advisory", "11.1 Who declares an advisory",
     "Only City Operations declares a weather or traffic advisory, for named zones with start and end times, "
     "shown as a banner in the app; a partner, store or Support cannot; no banner means no advisory",
     "Rain or traffic without a declared advisory does not remove late-delivery compensation"),
    ("Address changes by partners", "6.8 Address changes",
     "Partners deliver only to the address on the order; they cannot take an order to a different building, "
     "street or locality at the customer's request",
     "A customer who wants a different address must contact Support"),
]


def build(ctx, out_dir):
    rng = ctx.rng("sop")
    blocks = (ch1() + ch2() + ch3() + ch4() + ch5() + ch6() + ch7() + ch8() + ch9() + ch10(rng) + ch11()
              + ch12(rng) + ch13() + ch14() + ch15(rng) + ch16())
    write_pdf(f"{out_dir}/{FILE}", HEADER, blocks)
    for topic, where, says, effect in EXCEPTIONS:
        ctx.exception(topic, FILE, where, says, effect)
    return [dict(file=FILE, title="Delivery Partner Standard Operating Procedure v2.3",
                 kind="Internal operations manual (SOP)", fmt="PDF")]
