#!/usr/bin/env python3
from __future__ import annotations

import pandas as pd
import streamlit as st


CLAIMING_FACTORS = {
    62: 0.70,
    63: 0.75,
    64: 0.80,
    65: 0.8667,
    66: 0.9333,
    67: 1.00,
    68: 1.08,
    69: 1.16,
    70: 1.24,
}



def render_page() -> None:
    st.title("Social Security Optimizer")
    st.caption("Compare claiming ages using a simple benefit and lifetime-value model.")

    with st.sidebar:
        st.header("Claiming inputs")
        fra_age = st.selectbox("Full retirement age", options=[66, 67], index=1, key="ss_fra_age")
        fra_annual_benefit = st.number_input("Annual benefit at FRA", min_value=0.0, value=36_000.0, step=1_000.0, key="ss_fra_annual_benefit")
        longevity_age = st.number_input("Longevity age for comparison", min_value=70, max_value=100, value=90, key="ss_longevity_age")

    rows = []
    for age in range(62, 71):
        factor = CLAIMING_FACTORS[age]
        annual_benefit = fra_annual_benefit * factor
        years_collected = max(0, longevity_age - age + 1)
        lifetime_benefit = annual_benefit * years_collected
        rows.append(
            {
                "claim_age": age,
                "annual_benefit": annual_benefit,
                "years_collected": years_collected,
                "lifetime_benefit": lifetime_benefit,
            }
        )

    df = pd.DataFrame(rows)
    best_row = df.loc[df["lifetime_benefit"].idxmax()]

    c1, c2, c3 = st.columns(3)
    c1.metric("Best claim age in this model", f"{int(best_row['claim_age'])}")
    c2.metric("Annual benefit then", f"${best_row['annual_benefit']:,.0f}")
    c3.metric("Lifetime benefit", f"${best_row['lifetime_benefit']:,.0f}")

    st.subheader("Claiming comparison")
    st.dataframe(df, use_container_width=True)

    chart_df = df.set_index("claim_age")[["annual_benefit", "lifetime_benefit"]]
    st.subheader("Annual vs lifetime benefits")
    st.line_chart(chart_df)

    age_62 = df.loc[df["claim_age"] == 62, "lifetime_benefit"].iloc[0]
    age_70 = df.loc[df["claim_age"] == 70, "lifetime_benefit"].iloc[0]
    if age_70 > age_62:
        st.info("In this longevity scenario, delaying to 70 beats claiming at 62 on lifetime dollars.")
    else:
        st.info("In this longevity scenario, earlier claiming wins on lifetime dollars.")

    st.caption("This MVP uses simplified claiming factors and ignores taxation, COLA details, spousal benefits, and discount rates.")
