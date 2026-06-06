#!/usr/bin/env python3
from __future__ import annotations

import pandas as pd
import streamlit as st



def render_page() -> None:
    st.title("Retirement Readiness")
    st.caption("A simple on-track calculator for projected retirement income versus spending.")

    with st.sidebar:
        st.header("Readiness inputs")
        current_age = st.number_input("Current age", min_value=18, max_value=80, value=45, key="ready_current_age")
        retirement_age = st.number_input("Retirement age", min_value=25, max_value=80, value=65, key="ready_retirement_age")
        current_savings = st.number_input("Current retirement savings", min_value=0.0, value=750_000.0, step=10_000.0, key="ready_current_savings")
        annual_contribution = st.number_input("Annual contribution", min_value=0.0, value=30_000.0, step=1_000.0, key="ready_annual_contribution")
        annual_return = st.number_input("Annual return", min_value=0.0, max_value=0.15, value=0.06, step=0.005, format="%.3f", key="ready_annual_return")
        withdrawal_rate = st.number_input("Withdrawal rate", min_value=0.01, max_value=0.10, value=0.04, step=0.005, format="%.3f", key="ready_withdrawal_rate")
        annual_spending = st.number_input("Target annual retirement spending", min_value=0.0, value=120_000.0, step=5_000.0, key="ready_annual_spending")
        annual_social_security = st.number_input("Annual Social Security", min_value=0.0, value=36_000.0, step=1_000.0, key="ready_annual_social_security")
        annual_pension = st.number_input("Annual pension / other fixed income", min_value=0.0, value=0.0, step=1_000.0, key="ready_annual_pension")

    years_to_retirement = max(0, int(retirement_age - current_age))
    balance = float(current_savings)
    rows = []
    for year in range(years_to_retirement + 1):
        age = current_age + year
        rows.append({"age": age, "projected_balance": balance})
        balance = balance * (1 + annual_return) + annual_contribution

    final_balance = rows[-1]["projected_balance"] if rows else float(current_savings)
    portfolio_income = final_balance * withdrawal_rate
    fixed_income = annual_social_security + annual_pension
    total_income = portfolio_income + fixed_income
    gap = total_income - annual_spending

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Projected nest egg", f"${final_balance:,.0f}")
    c2.metric("Portfolio income", f"${portfolio_income:,.0f}/yr")
    c3.metric("Total retirement income", f"${total_income:,.0f}/yr")
    c4.metric("Surplus / gap", f"${gap:,.0f}/yr")

    projection_df = pd.DataFrame(rows).set_index("age")
    st.subheader("Projected portfolio growth")
    st.line_chart(projection_df)

    st.subheader("Interpretation")
    if gap >= 0:
        st.success("On this simplified model, projected income covers target retirement spending.")
    else:
        extra_monthly = abs(gap) / 12
        st.warning(f"This plan shows an annual shortfall of ${abs(gap):,.0f}. Roughly ${extra_monthly:,.0f}/month needs to come from higher savings, later retirement, lower spending, or better guaranteed income.")

    st.caption("This MVP uses a deterministic projection. It does not yet model inflation, taxes, or market volatility.")
