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

st.set_page_config(
    page_title="InsureFlow — Insurance Analytics & AI",
    page_icon="🛡️",
    layout="wide",
)

PRODUCTS = {
    "Home": {
        "name": "Smart Home Basic",
        "subtitle": "Home + belongings",
        "description": "Core protection for renters and apartment owners, including belongings, liability, accidental damage and travel cover.",
    },
    "Car": {
        "name": "Flexible Car Standard",
        "subtitle": "Vehicle protection",
        "description": "Flexible motor cover for everyday drivers with traffic liability and optional damage protection.",
    },
    "Pet": {
        "name": "Digital Pet Care",
        "subtitle": "Veterinary care",
        "description": "Pet insurance for dogs and cats with veterinary-care protection and digital-first support.",
    },
    "Accident": {
        "name": "Everyday Accident",
        "subtitle": "Personal accident protection",
        "description": "Extra financial protection for unexpected accidents in everyday life.",
    },
}

# Illustrative portfolio metrics so the public demo can show an analytics layer
# without requiring access to production databases or cloud credentials.
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

    if priority in PRODUCTS:
        categories.append(priority)
        reasons.append(f"Your main protection goal is {priority.lower()} coverage.")

    if home_status != "None" and "Home" not in categories:
        categories.append("Home")
        reasons.append(
            f"You selected {home_status.lower()} housing, so home and belongings protection is relevant."
        )

    if owns_car and "Car" not in categories:
        categories.append("Car")
        reasons.append("You own a car, so vehicle and liability protection is relevant.")

    if owns_pet and "Pet" not in categories:
        categories.append("Pet")
        reasons.append("You own a pet, so veterinary-cost protection may be useful.")

    if not categories:
        categories.append("Accident")
        reasons.append("Accident cover provides a simple baseline protection option to compare.")

    return categories[:3], reasons[:3]


st.title("🛡️ InsureFlow")
st.caption("AI-native insurance analytics & recommendation platform · Portfolio demo")

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
st.header("AI insurance recommendation")
st.write(
    "Create a customer profile to generate an explainable insurance-product shortlist. "
    "The full repository also contains the production-style Google ADK/Gemini, SQL/RAG, "
    "FastAPI and GCP-ready implementation."
)

with st.form("recommendation_form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.slider("Age", 18, 75, 29)
        household = st.selectbox("Household", ["Single", "Couple", "Family"])
    with c2:
        home_status = st.selectbox("Housing", ["Renter", "Homeowner", "None"])
        priority = st.selectbox("Main protection goal", ["Home", "Car", "Pet", "Accident"])
    with c3:
        owns_car = st.checkbox("Owns a car")
        owns_pet = st.checkbox("Owns a dog or cat")

    submitted = st.form_submit_button("Generate recommendation", type="primary")

categories, reasons = build_recommendations(
    age, household, home_status, owns_car, owns_pet, priority
)

if submitted:
    st.success("Recommendation generated")

st.subheader("Recommendation summary")
st.write(f"**Profile:** age {age} · {household.lower()} · {home_status.lower()} housing")
for reason in reasons:
    st.write(f"• {reason}")

product_columns = st.columns(len(categories))
for column, category in zip(product_columns, categories):
    product = PRODUCTS[category]
    with column:
        with st.container(border=True):
            st.markdown(f"### {product['name']}")
            st.caption(f"{category} · {product['subtitle']}")
            st.write(product["description"])
            st.markdown(f"**Recommended category:** {category}")

st.info(
    "Demo recommendations and dashboard metrics are illustrative portfolio data, "
    "not insurance or financial advice."
)

with st.expander("Project architecture"):
    st.code(
        """Streamlit portfolio dashboard
        │
        ├── Analytics / KPI demonstration
        └── Recommendation demonstration

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
