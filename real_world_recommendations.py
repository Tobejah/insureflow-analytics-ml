"""Integrated real-world product suggestions for InsureFlow's existing questionnaire.

This module deliberately keeps product selection deterministic:
1) the existing questionnaire determines the user's insurance needs;
2) this module maps those needs to a curated real-world product catalogue;
3) the UI explains why each option is relevant and links to the official source.

It does NOT calculate premiums, underwrite risk, or claim an objectively "best" insurer.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ProductOption:
    provider: str
    name: str
    category: str
    housing: tuple[str, ...] = ()
    highlights: tuple[str, ...] = ()
    source_url: str = ""
    checked: str = "2026-08-17"


PRODUCTS = (
    # HOME
    ProductOption(
        "Hedvig", "Rental Insurance", "home", ("Rent",),
        ("Designed for tenants", "Covers belongings and people in the household", "No lock-in period"),
        "https://www.hedvig.com/se-en/insurances/home-insurance",
    ),
    ProductOption(
        "Hedvig", "Homeowner Insurance", "home", ("Own apartment",),
        ("Designed for owned apartments/condominiums", "Covers belongings and apartment-related damage", "No lock-in period"),
        "https://www.hedvig.com/se-en/insurances/home-insurance/homeowner",
    ),
    ProductOption(
        "Hedvig", "House Insurance", "home", ("Own house",),
        ("Combined home and house protection", "Full-value house protection", "Covers household belongings"),
        "https://www.hedvig.com/se-en/insurances/house-insurance",
    ),
    ProductOption(
        "If", "Home Insurance", "home", ("Rent", "Own apartment", "Own house"),
        ("Real-world home-insurance option", "Use the official source to verify the level that matches your housing"),
        "https://www.if.se/privat/forsakringar/hemforsakring",
    ),
    ProductOption(
        "Länsförsäkringar", "Home Insurance", "home", ("Rent", "Own apartment", "Own house"),
        ("Real-world home-insurance option", "Housing-specific terms should be verified with the regional insurer"),
        "https://www.lansforsakringar.se/privat/forsakring/hemforsakring/",
    ),

    # PET
    ProductOption(
        "Hedvig", "Pet Insurance", "pet",
        highlights=("Dog and cat insurance", "Digital-first claims/service", "Multiple coverage levels"),
        source_url="https://www.hedvig.com/se-en/insurances/pet-insurance",
    ),
    ProductOption(
        "Lassie", "Pet Insurance", "pet",
        highlights=("Dog and cat insurance", "Digital veterinary support", "Preventive-care features"),
        source_url="https://www.lassie.co/en/",
    ),
    ProductOption(
        "Agria", "Pet Insurance", "pet",
        highlights=("Established pet-insurance offering", "Veterinary-care protection", "Animal-health guidance"),
        source_url="https://www.agria.se/djurforsakring/",
    ),

    # CAR
    ProductOption(
        "Hedvig", "Car Insurance", "car",
        highlights=("Traffic, half and full-cover options", "24/7 roadside assistance on relevant cover", "No lock-in period"),
        source_url="https://www.hedvig.com/se-en/insurances/car-insurance",
    ),
    ProductOption(
        "If", "Car Insurance", "car",
        highlights=("Multiple car-cover levels", "Roadside and own-damage protection on relevant levels", "Optional enhanced cover"),
        source_url="https://www.if.se/privat/forsakringar/bilforsakring",
    ),
    ProductOption(
        "Länsförsäkringar", "Car Insurance", "car",
        highlights=("Traffic, half and full-cover options", "Full cover includes own-car damage", "Optional additional benefits"),
        source_url="https://www.lansforsakringar.se/privat/forsakring/bilforsakring/",
    ),

    # ACCIDENT
    ProductOption(
        "Hedvig", "Accident Insurance", "accident",
        highlights=("Personal accident protection", "Available as a standalone Hedvig insurance", "Verify current limits and terms"),
        source_url="https://www.hedvig.com/se-en/insurances/accident-insurance",
    ),
    ProductOption(
        "If", "Accident Insurance", "accident",
        highlights=("Personal accident insurance option", "Verify current benefits, limits and eligibility on the official page"),
        source_url="https://www.if.se/privat/forsakringar/personforsakring/olycksfallsforsakring",
    ),
    ProductOption(
        "Länsförsäkringar", "Accident Insurance", "accident",
        highlights=("Personal accident insurance option", "Verify current benefits and regional terms on the official page"),
        source_url="https://www.lansforsakringar.se/privat/forsakring/personforsakring/olycksfallsforsakring/",
    ),
)


def infer_needs(housing: str, household: str, has_car: bool, has_pet: bool, accident_cover: bool = True):
    """Use the EXISTING questionnaire answers to determine relevant categories."""
    needs = [
        {
            "category": "home",
            "title": "Home insurance",
            "reason": f"Your housing situation is '{housing}', so home protection is relevant for your belongings, liability and household.",
        }
    ]
    if has_car:
        needs.append({
            "category": "car",
            "title": "Car insurance",
            "reason": "You indicated that you own/use a car, so relevant car-cover options are included.",
        })
    if has_pet:
        needs.append({
            "category": "pet",
            "title": "Pet insurance",
            "reason": "You indicated that your household includes a pet, so veterinary-care protection is relevant.",
        })
    if accident_cover:
        needs.append({
            "category": "accident",
            "title": "Accident insurance",
            "reason": "Personal accident cover is shown as an optional additional protection rather than assumed to be mandatory.",
        })
    return needs


def products_for_need(category: str, housing: str, limit: int = 3):
    candidates = [p for p in PRODUCTS if p.category == category]
    if category == "home":
        exact = [p for p in candidates if not p.housing or housing in p.housing]
        candidates = exact or candidates
    return candidates[:limit]
