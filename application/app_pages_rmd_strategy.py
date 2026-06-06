#!/usr/bin/env python3
from __future__ import annotations

import pandas as pd
import streamlit as st

from roth_conversion_defaults import DEFAULTS
from roth_conversion_engine import PlanInputs, compare_strategies, result_rows



def render_page() -> None:
    st.title("RMD / Roth Conversion Strategy")
    st.caption("Estimate whether strategic Roth conversions can reduce future RMDs and lifetime tax drag.")

    with st.sidebar:
        st.header("RMD strategy inputs")
        current_age = st.number_input("Current age", min_value=18, max_value=90, value=int(DEFAULTS["current_age"]), key="rmd_current_age")
        retirement_age = st.number_input("Retirement age", min_value=18, max_value=75, value=int(DEFAULTS["retirement_age"]), key="rmd_retirement_age")
        current_401k_balance = st.number_input("Current 401(k) / traditional IRA balance", min_value=0.0, value=float(DEFAULTS["current_401k_balance"]), step=10_000.0, key="rmd_current_401k_balance")
        annual_contribution = st.number_input("Annual contribution before retirement", min_value=0.0, value=float(DEFAULTS["annual_contribution"]), step=1_000.0, key="rmd_annual_contribution")
        annual_retirement_spending = st.number_input("Annual retirement spending", min_value=0.0, value=float(DEFAULTS["annual_retirement_spending"]), step=5_000.0, key="rmd_annual_retirement_spending")
        has_roth_ira = st.checkbox("Already has Roth IRA", value=bool(DEFAULTS["has_roth_ira"]), key="rmd_has_roth_ira")
        has_taxable_brokerage = st.checkbox("Has taxable brokerage", value=bool(DEFAULTS["has_taxable_brokerage"]), key="rmd_has_taxable_brokerage")

        st.header("Advanced inputs")
        filing_status = st.selectbox("Filing status", options=["mfj", "single"], index=0 if DEFAULTS["filing_status"] == "mfj" else 1, key="rmd_filing_status")
        current_roth_balance = st.number_input("Current Roth balance", min_value=0.0, value=float(DEFAULTS["current_roth_balance"]), step=10_000.0, key="rmd_current_roth_balance")
        current_taxable_balance = st.number_input("Current taxable balance", min_value=0.0, value=float(DEFAULTS["current_taxable_balance"]), step=10_000.0, key="rmd_current_taxable_balance")
        annual_other_income = st.number_input("Annual other ordinary income", min_value=0.0, value=float(DEFAULTS["annual_other_income"]), step=1_000.0, key="rmd_annual_other_income")
        annual_pension_income = st.number_input("Annual pension income", min_value=0.0, value=float(DEFAULTS["annual_pension_income"]), step=1_000.0, key="rmd_annual_pension_income")
        social_security_claim_age = st.number_input("Social Security claim age", min_value=62, max_value=75, value=int(DEFAULTS["social_security_claim_age"]), key="rmd_social_security_claim_age")
        annual_social_security_benefit = st.number_input("Annual Social Security benefit", min_value=0.0, value=float(DEFAULTS["annual_social_security_benefit"]), step=1_000.0, key="rmd_annual_social_security_benefit")
        annual_return = st.number_input("Annual return", min_value=0.0, max_value=0.20, value=float(DEFAULTS["annual_return"]), step=0.005, format="%.3f", key="rmd_annual_return")
        state_tax_rate = st.number_input("State tax rate", min_value=0.0, max_value=0.20, value=float(DEFAULTS["state_tax_rate"]), step=0.005, format="%.3f", key="rmd_state_tax_rate")
        target_bracket = st.selectbox("Target conversion bracket ceiling", options=["12%", "22%", "24%", "32%"], index=["12%", "22%", "24%", "32%"].index(str(DEFAULTS["target_bracket"])), key="rmd_target_bracket")
        use_aca_model = st.checkbox("Estimate ACA drag before 65", value=bool(DEFAULTS["use_aca_model"]), key="rmd_use_aca_model")
        use_irmaa_model = st.checkbox("Estimate IRMAA after 65", value=bool(DEFAULTS["use_irmaa_model"]), key="rmd_use_irmaa_model")
        life_expectancy = st.number_input("Life expectancy for cost comparison", min_value=75, max_value=100, value=int(DEFAULTS["life_expectancy"]), key="rmd_life_expectancy")

    inputs = PlanInputs(
        current_age=int(current_age),
        retirement_age=int(retirement_age),
        current_401k_balance=float(current_401k_balance),
        annual_contribution=float(annual_contribution),
        has_roth_ira=bool(has_roth_ira),
        has_taxable_brokerage=bool(has_taxable_brokerage),
        annual_retirement_spending=float(annual_retirement_spending),
        filing_status=filing_status,
        current_roth_balance=float(current_roth_balance),
        current_taxable_balance=float(current_taxable_balance),
        annual_other_income=float(annual_other_income),
        annual_pension_income=float(annual_pension_income),
        social_security_claim_age=int(social_security_claim_age),
        annual_social_security_benefit=float(annual_social_security_benefit),
        annual_return=float(annual_return),
        state_tax_rate=float(state_tax_rate),
        target_bracket=target_bracket,
        use_aca_model=bool(use_aca_model),
        use_irmaa_model=bool(use_irmaa_model),
        life_expectancy=int(life_expectancy),
    )

    results = compare_strategies(inputs)
    conv = results["conversion"]
    base = results["no_conversion"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("RMD at 75 (conversion)", f"${conv.estimated_rmd_at_75:,.0f}")
    col2.metric("RMD at 75 (no conversion)", f"${base.estimated_rmd_at_75:,.0f}")
    col3.metric("Estimated total savings", f"${base.total_cost_to_life_expectancy - conv.total_cost_to_life_expectancy:,.0f}")
    col4.metric("Traditional balance at 75", f"${conv.traditional_balance_at_75:,.0f}")

    summary = pd.DataFrame(
        [
            {
                "scenario": "conversion",
                "traditional_at_75": conv.traditional_balance_at_75,
                "roth_at_75": conv.roth_balance_at_75,
                "taxable_at_75": conv.taxable_balance_at_75,
                "rmd_at_75": conv.estimated_rmd_at_75,
                "federal_tax_total": conv.total_federal_tax_to_life_expectancy,
                "state_tax_total": conv.total_state_tax_to_life_expectancy,
                "aca_drag_total": conv.total_aca_drag_to_life_expectancy,
                "irmaa_total": conv.total_irmaa_to_life_expectancy,
                "total_cost": conv.total_cost_to_life_expectancy,
            },
            {
                "scenario": "no_conversion",
                "traditional_at_75": base.traditional_balance_at_75,
                "roth_at_75": base.roth_balance_at_75,
                "taxable_at_75": base.taxable_balance_at_75,
                "rmd_at_75": base.estimated_rmd_at_75,
                "federal_tax_total": base.total_federal_tax_to_life_expectancy,
                "state_tax_total": base.total_state_tax_to_life_expectancy,
                "aca_drag_total": base.total_aca_drag_to_life_expectancy,
                "irmaa_total": base.total_irmaa_to_life_expectancy,
                "total_cost": base.total_cost_to_life_expectancy,
            },
        ]
    )

    st.subheader("Strategy comparison")
    st.dataframe(summary, use_container_width=True)

    conv_df = pd.DataFrame(result_rows(conv))
    st.subheader("Annual conversion path")
    st.dataframe(
        conv_df[
            [
                "age",
                "start_traditional",
                "start_taxable",
                "start_roth",
                "spending_need",
                "recommended_conversion",
                "gross_income",
                "effective_marginal_bracket",
                "estimated_federal_tax",
                "estimated_state_tax",
                "aca_subsidy_loss",
                "irmaa_surcharge",
                "end_traditional",
                "end_roth",
                "end_taxable",
            ]
        ],
        use_container_width=True,
    )

    chart_df = conv_df[["age", "recommended_conversion", "end_traditional", "end_roth", "end_taxable"]].set_index("age")
    st.subheader("Balance path")
    st.line_chart(chart_df)

    compare_rmd = pd.DataFrame(
        {
            "scenario": ["conversion", "no_conversion"],
            "rmd_at_75": [conv.estimated_rmd_at_75, base.estimated_rmd_at_75],
        }
    ).set_index("scenario")
    st.subheader("RMD at age 75")
    st.bar_chart(compare_rmd)

    st.caption("Planning approximation only. Verify actual tax execution with CPA or tax software.")
