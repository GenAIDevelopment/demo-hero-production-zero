"""Shared facts and the conflict registry for the QuickBasket knowledge base (fictional, synthetic).

Every rule in the knowledge base comes from the facts below, which are the Customer Policy v4.2 (the
source of truth). A document may only disagree with v4.2 through Ctx.conflict(...), which records it in
kb/conflicts.md. Legitimate additions that change an answer (a city exception, a launch date, a promo
rule) are recorded with Ctx.exception(...).
"""
import random

DEMO_TODAY = "14 November 2026"

# Customer Policy v4.2: the values every other document must agree with.
V42 = dict(
    version="4.2", effective="1 October 2026",
    cities=["Hyderabad", "Bengaluru", "Chennai", "Pune", "Mumbai", "Delhi NCR"],
    general_window="7 days",
    fruit_window="24 hours", dairy_window="24 hours", frozen_window="12 hours",
    packaged_window="7 days", personal_window="7 days", electronics_window="3 days", baby_window="7 days",
    upi="2–4 business days", card="5–7 business days", cod_bank="5–7 business days",
    late_16_30="Delivery fee refunded", late_over30_all="Delivery fee refunded",
    late_over30_plus="Delivery fee refunded plus ₹50 QuickBasket Cash", plus_bonus="₹50",
    plus_month="₹149", plus_year="₹1,299", plus_free_above="₹199", plus_cancel_hours="48 hours",
    cancel_fee="₹25", approval_limit="₹500", max_refunds_30d="three",
    has_plus=True,
)

CITY_NAMES = V42["cities"]


class Ctx:
    """Build context: deterministic randomness per document, plus the conflict registry."""

    def __init__(self, seed=42):
        self.seed = seed
        self.conflicts = []    # disagreements with v4.2
        self.exceptions = []   # legitimate additions that change an answer

    def rng(self, name):
        return random.Random(f"{self.seed}:{name}")

    def conflict(self, topic, doc, where, says, v42_says, kind):
        self.conflicts.append(dict(topic=topic, doc=doc, where=where, says=says, v42=v42_says, kind=kind))

    def exception(self, topic, doc, where, says, effect):
        self.exceptions.append(dict(topic=topic, doc=doc, where=where, says=says, effect=effect))


def pick(rng, options):
    return options[rng.randrange(len(options))]
