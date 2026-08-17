"""Standalone Streamlit portfolio dashboard.

Run locally:
    streamlit run streamlit_app.py

This lightweight demo is intentionally self-contained so it can be deployed
directly to Streamlit Community Cloud. The production-style ADK/FastAPI/SQL/RAG
application remains in the rest of the repository.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from real_world_recommendations import products_for_need


st.set_page_config(
    page_title="InsureFlow — Insurance Analytics & AI",
    page_icon="🛡️",
    layout="wide",
)


# -------------------------------------------------------------------
# DEMO INSURANCE CATEGORIES
# -------------------------------------------------------------------

PRODUCTS = {
    "Home": {
        "name": "Home Insurance",
        "subtitle": "Home + belongings",
        "description": (
            "Protection for your home, belongings, liability and other "
            "household-related risks."
        ),
    },
    "Car": {
        "name": "Car Insurance",
        "subtitle": "Vehicle protection",
        "description": (
            "Vehicle protection covering risks such as traffic liability, "
            "damage and roadside incidents depending on coverage level."
        ),
    },
    "Pet": {
        "name": "Pet Insurance",
        "subtitle": "Veterinary care",
        "description": (
            "Insurance for dogs and cats that can provide financial protection "
            "for veterinary treatment and related care."
        ),
    },
    "Accident": {
        "name": "Accident Insurance",
        "subtitle": "Personal accident protection",
        "description": (
            "Additional financial protection following unexpected personal "
            "accidents and injuries."
        ),
    },
}


# -------------------------------------------------------------------
# ILLUSTRATIVE ANALYTICS DATA
# -------------------------------------------------------------------

METRICS = {
    "Active policies": "12,450",
    "Claims (30d)": "843",
    "Avg. premium": "€31.20",
    "Renewal rate": "87.4%",
}


CLAIMS = pd.DataFrame(
    {
        "Product": ["Home", "Car", "Pet", "Accident"],
        "Claims": [286, 241, 189, 127],
    }
)


RISK = pd.DataFrame(
    {
        "Risk band": ["Low", "Medium", "High"],
        "Policies": [7110, 4030, 1310],
    }
)


# -------------------------------------------------------------------
# RECOMMENDATION LOGIC
# -------------------------------------------------------------------

def build_recommendations(
    age: int,
    household: str,
    home_status: str,
    owns_car: bool,
    owns_pet: bool,
    priority: str,
):
    categories: list[str] = []
    reasons: list[str] = []

    # Respect the customer's main stated protection goal.
    if priority in PRODUCTS:
        categories.append(priority)
        reasons.append(
            f"Your main protection goal is {priority.lower()} coverage."
        )

    # Housing determines whether home protection is relevant.
    if home_status != "None" and "Home" not in categories:
        categories.append("Home")
        reasons.append(
            f"You selected {home_status.lower()} housing, so home and "
            "belongings protection is relevant."
        )

    # Only recommend car insurance when the customer owns a car.
    if owns_car and "Car" not in categories:
        categories.append("Car")
        reasons.append(
            "You own a car, so vehicle and liability protection is relevant."
        )

    # Only recommend pet insurance when the customer owns a dog or cat.
    if owns_pet and "Pet" not in categories:
        categories.append("Pet")
        reasons.append(
            "You own a pet, so veterinary-cost protection may be useful."
        )

    # Accident insurance works as an additional personal-protection option.
    if (
        priority == "Accident"
        and "Accident" not in categories
    ):
        categories.append("Accident")
        reasons.append(
            "You selected personal accident protection as a priority."
        )

    if not categories:
        categories.append("Accident")
        reasons.append(
            "Accident cover provides a baseline personal-protection option "
            "to consider."
        )

    return categories[:4], reasons[:4]


# -------------------------------------------------------------------
# PAGE HEADER
# -------------------------------------------------------------------

st.title("🛡️ InsureFlow")
st.caption(
    "AI-native insurance analytics & recommendation platform · Portfolio demo"
)


# -------------------------------------------------------------------
# ANALYTICS
# -------------------------------------------------------------------

m1, m2, m3, m4 = st.columns(4)

m1.metric("Active policies", METRICS["Active policies"])
m2.metric("Claims · 30 days", METRICS["Claims (30d)"])
m3.metric("Average premium", METRICS["Avg. premium"])
m4.metric("Renewal rate", METRICS["Renewal rate"])


st.divider()


left, right = st.columns(2)

with left:
    st.subheader("Claims by product")
    st.bar_chart(CLAIMS.set_index("Product"))

with right:
    st.subheader("Portfolio risk distribution")
    st.bar_chart(RISK.set_index("Risk band"))


st.divider()


# -------------------------------------------------------------------
# CUSTOMER QUESTIONNAIRE
# -------------------------------------------------------------------

st.header("AI insurance recommendation")

st.write(
    "Create a customer profile to generate an explainable insurance-product "
    "shortlist. InsureFlow then connects the recommended coverage categories "
    "with relevant real-world Swedish insurance products."
)


with st.form("recommendation_form"):

    c1, c2, c3 = st.columns(3)

    with c1:
        age = st.slider(
            "Age",
            18,
            75,
            29,
        )

        household = st.selectbox(
            "Household",
            [
                "Single",
                "Couple",
                "Family",
            ],
        )

    with c2:
        home_status = st.selectbox(
            "Housing",
            [
                "Renter",
                "Homeowner",
                "None",
            ],
        )

        priority = st.selectbox(
            "Main protection goal",
            [
                "Home",
                "Car",
                "Pet",
                "Accident",
            ],
        )

    with c3:
        owns_car = st.checkbox(
            "Owns a car"
        )

        owns_pet = st.checkbox(
            "Owns a dog or cat"
        )

    submitted = st.form_submit_button(
        "Generate recommendation",
        type="primary",
    )


# -------------------------------------------------------------------
# GENERATE RESULTS ONLY AFTER SUBMISSION
# -------------------------------------------------------------------

if submitted:

    categories, reasons = build_recommendations(
        age,
        household,
        home_status,
        owns_car,
        owns_pet,
        priority,
    )

    st.success("Recommendation generated")


    # ---------------------------------------------------------------
    # CUSTOMER PROFILE
    # ---------------------------------------------------------------

    st.subheader("Recommendation summary")

    st.write(
        f"**Profile:** age {age} · "
        f"{household.lower()} · "
        f"{home_status.lower()} housing"
    )

    for reason in reasons:
        st.write(f"• {reason}")


    # ---------------------------------------------------------------
    # RECOMMENDED INSURANCE CATEGORIES
    # ---------------------------------------------------------------

    st.subheader("Recommended coverage")

    product_columns = st.columns(len(categories))

    for column, category in zip(
        product_columns,
        categories,
    ):

        product = PRODUCTS[category]

        with column:

            with st.container(border=True):

                st.markdown(
                    f"### {product['name']}"
                )

                st.caption(
                    f"{category} · "
                    f"{product['subtitle']}"
                )

                st.write(
                    product["description"]
                )

                st.markdown(
                    f"**Recommended category: {category}**"
                )


    # ---------------------------------------------------------------
    # REAL-WORLD INSURANCE OPTIONS
    # ---------------------------------------------------------------

    st.divider()

    st.header("Relevant real-world insurance options")

    st.write(
        "Based on the same profile above, InsureFlow retrieves relevant "
        "real-world products for each recommended insurance category."
    )

    st.caption(
        "These are relevant options rather than an objective ranking. "
        "Premiums, eligibility and final coverage depend on each insurer's "
        "current terms and individual assessment."
    )


    for category in categories:

        st.markdown(f"## {category} Insurance")

        # Explain why this category appears.
        if category == "Home":

            if home_status == "Renter":
                st.write(
                    "Because you rent your home, these products provide "
                    "relevant household and belongings protection."
                )

            elif home_status == "Homeowner":
                st.write(
                    "Because you own your home, these products provide "
                    "relevant protection for your home and belongings."
                )

            else:
                st.write(
                    "These are real-world home-insurance options "
                    "matching your selected protection goal."
                )

        elif category == "Car":

            if owns_car:
                st.write(
                    "Because you own a car, these providers offer relevant "
                    "vehicle and liability protection."
                )

            else:
                st.write(
                    "You selected car protection as your main goal. "
                    "These are real-world car-insurance options to explore."
                )

        elif category == "Pet":

            if owns_pet:
                st.write(
                    "Because you own a dog or cat, these products provide "
                    "relevant veterinary-care protection."
                )

            else:
                st.write(
                    "You selected pet protection as your main goal. "
                    "These are real-world pet-insurance options to explore."
                )

        elif category == "Accident":

            st.write(
                "These products provide personal accident protection "
                "and can complement your other insurance coverage."
            )


        real_products = products_for_need(
            category=category.lower(),
            housing=home_status,
            limit=3,
        )


        if not real_products:

            st.info(
                "No real-world products are currently stored "
                "for this category."
            )

            continue


        option_columns = st.columns(
            len(real_products)
        )


        for column, real_product in zip(
            option_columns,
            real_products,
        ):

            with column:

                with st.container(border=True):

                    st.markdown(
                        f"### {real_product.provider}"
                    )

                    st.markdown(
                        f"**{real_product.name}**"
                    )

                    for highlight in real_product.highlights:

                        st.write(
                            f"✓ {highlight}"
                        )

                    st.caption(
                        f"Source checked: "
                        f"{real_product.checked}"
                    )

                    st.link_button(
                        "View official product ↗",
                        real_product.source_url,
                        use_container_width=True,
                    )


    # ---------------------------------------------------------------
    # DISCLAIMER
    # ---------------------------------------------------------------

    st.warning(
        "Portfolio demonstration only. InsureFlow does not calculate "
        "binding insurance quotes or claim that one insurer is objectively "
        "better than another. Product terms, eligibility and pricing can "
        "change. Always verify current information directly with the insurer."
    )


# -------------------------------------------------------------------
# ARCHITECTURE
# -------------------------------------------------------------------

st.divider()


with st.expander("How InsureFlow works"):

    st.code(
        """Customer profile
        │
        ▼
Insurance needs analysis
        │
        ▼
Recommended coverage categories
        │
        ▼
Real-world product retrieval
        │
        ▼
Relevant insurer options + evidence
        │
        ▼
Explainable customer-facing result""",
        language="text",
    )


with st.expander("Project architecture"):

    st.code(
        """Streamlit portfolio dashboard
        │
        ├── Analytics / KPI demonstration
        ├── Customer profile
        ├── Recommendation engine
        └── Real-world insurance product retrieval

Full repository
        │
        ├── Google ADK / Gemini agent
        ├── SQL product tools
        ├── RAG / FAQ retrieval
        ├── FastAPI backend
        ├── Docker / Terraform
        └── GCP-ready infrastructure""",
        language="text",
    )


st.info(
    "Dashboard metrics are illustrative portfolio data. "
    "Real-world insurance product information is manually curated "
    "from official insurer sources."
)