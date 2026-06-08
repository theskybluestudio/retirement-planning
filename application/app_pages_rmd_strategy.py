#!/usr/bin/env python3
from __future__ import annotations

import pandas as pd
import streamlit as st

from app_i18n import section
from app_state import commit_shared_widget, prime_shared_widget, shared_widget_key
from app_ui import format_currency, format_dataframe, format_percent, money_input, percent_input, render_explainer, render_header, render_note
from roth_conversion_engine import PlanInputs, compare_strategies, result_rows



def render_page() -> None:
    zh = st.session_state.get("language", "en") == "zh"
    common = section("common")
    assumptions = section("assumptions")
    labels = section("rmd")
    render_header(labels["title"], labels["subtitle"])
    render_explainer(common["about_tool"], labels["about_body"])

    for key in [
        "current_age", "retirement_age", "life_expectancy", "traditional_balance", "roth_balance", "taxable_balance",
        "has_roth_ira", "has_taxable_brokerage", "annual_contribution", "annual_retirement_spending",
        "annual_social_security_benefit", "annual_pension_income", "annual_other_income", "annual_return",
        "state_tax_rate", "filing_status", "social_security_claim_age",
    ]:
        prime_shared_widget(key)

    with st.expander(common["shared_inputs"], expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.number_input(assumptions["current_age"], min_value=18, max_value=80, key=shared_widget_key("current_age"), on_change=commit_shared_widget, args=("current_age",))
            st.number_input(assumptions["retirement_age"], min_value=25, max_value=80, key=shared_widget_key("retirement_age"), on_change=commit_shared_widget, args=("retirement_age",))
            st.number_input(assumptions["life_expectancy"], min_value=70, max_value=105, key=shared_widget_key("life_expectancy"), on_change=commit_shared_widget, args=("life_expectancy",))
        with c2:
            money_input(assumptions["traditional_balance"], min_value=0.0, key=shared_widget_key("traditional_balance"), on_change=commit_shared_widget, args=("traditional_balance",))
            money_input(assumptions["roth_balance"], min_value=0.0, key=shared_widget_key("roth_balance"), on_change=commit_shared_widget, args=("roth_balance",))
            money_input(assumptions["taxable_balance"], min_value=0.0, key=shared_widget_key("taxable_balance"), on_change=commit_shared_widget, args=("taxable_balance",))
            st.checkbox(assumptions["has_roth_ira"], key=shared_widget_key("has_roth_ira"), on_change=commit_shared_widget, args=("has_roth_ira",))
            st.checkbox(assumptions["has_taxable_brokerage"], key=shared_widget_key("has_taxable_brokerage"), on_change=commit_shared_widget, args=("has_taxable_brokerage",))
        with c3:
            money_input(assumptions["annual_contribution"], min_value=0.0, key=shared_widget_key("annual_contribution"), on_change=commit_shared_widget, args=("annual_contribution",))
            money_input(assumptions["annual_retirement_spending"], min_value=0.0, key=shared_widget_key("annual_retirement_spending"), on_change=commit_shared_widget, args=("annual_retirement_spending",))
            money_input(assumptions["annual_ss_benefit"], min_value=0.0, key=shared_widget_key("annual_social_security_benefit"), on_change=commit_shared_widget, args=("annual_social_security_benefit",))
            money_input(assumptions["annual_pension_income"], min_value=0.0, key=shared_widget_key("annual_pension_income"), on_change=commit_shared_widget, args=("annual_pension_income",))
            money_input(assumptions["annual_other_income"], min_value=0.0, key=shared_widget_key("annual_other_income"), on_change=commit_shared_widget, args=("annual_other_income",))
            percent_input(assumptions["annual_return"], min_value=0.0, max_value=0.20, key=shared_widget_key("annual_return"), on_change=commit_shared_widget, args=("annual_return",))
            percent_input(assumptions["state_tax_rate"], min_value=0.0, max_value=0.20, key=shared_widget_key("state_tax_rate"), on_change=commit_shared_widget, args=("state_tax_rate",))
            st.selectbox(assumptions["filing_status"], options=["mfj", "single"], key=shared_widget_key("filing_status"), on_change=commit_shared_widget, args=("filing_status",))
            st.number_input(assumptions["ss_claim_age"], min_value=62, max_value=75, key=shared_widget_key("social_security_claim_age"), on_change=commit_shared_widget, args=("social_security_claim_age",))

    with st.sidebar:
        st.divider()
        st.header(common["page_specific_inputs"])
        target_bracket = st.selectbox(labels["target_bracket"], options=["12%", "22%", "24%", "32%"], key="rmd_target_bracket")
        use_aca_model = st.checkbox(labels["aca"], key="rmd_use_aca_model")
        use_irmaa_model = st.checkbox(labels["irmaa"], key="rmd_use_irmaa_model")

    current_age = int(st.session_state.current_age)
    retirement_age = int(st.session_state.retirement_age)
    current_401k_balance = float(st.session_state.traditional_balance)
    annual_contribution = float(st.session_state.annual_contribution)
    annual_retirement_spending = float(st.session_state.annual_retirement_spending)
    has_roth_ira = bool(st.session_state.has_roth_ira)
    has_taxable_brokerage = bool(st.session_state.has_taxable_brokerage)
    filing_status = str(st.session_state.filing_status)
    current_roth_balance = float(st.session_state.roth_balance)
    current_taxable_balance = float(st.session_state.taxable_balance)
    annual_other_income = float(st.session_state.annual_other_income)
    annual_pension_income = float(st.session_state.annual_pension_income)
    social_security_claim_age = int(st.session_state.social_security_claim_age)
    annual_social_security_benefit = float(st.session_state.annual_social_security_benefit)
    annual_return = float(st.session_state.annual_return)
    state_tax_rate = float(st.session_state.state_tax_rate)
    life_expectancy = int(st.session_state.life_expectancy)

    inputs = PlanInputs(
        current_age=current_age,
        retirement_age=retirement_age,
        current_401k_balance=current_401k_balance,
        annual_contribution=annual_contribution,
        has_roth_ira=has_roth_ira,
        has_taxable_brokerage=has_taxable_brokerage,
        annual_retirement_spending=annual_retirement_spending,
        filing_status=filing_status,
        current_roth_balance=current_roth_balance,
        current_taxable_balance=current_taxable_balance,
        annual_other_income=annual_other_income,
        annual_pension_income=annual_pension_income,
        social_security_claim_age=social_security_claim_age,
        annual_social_security_benefit=annual_social_security_benefit,
        annual_return=annual_return,
        state_tax_rate=state_tax_rate,
        target_bracket=target_bracket,
        use_aca_model=use_aca_model,
        use_irmaa_model=use_irmaa_model,
        life_expectancy=life_expectancy,
    )

    results = compare_strategies(inputs)
    conv = results["conversion"]
    base = results["no_conversion"]
    savings = base.total_cost_to_life_expectancy - conv.total_cost_to_life_expectancy

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(labels["rmd_conv"], format_currency(conv.estimated_rmd_at_75))
    c2.metric(labels["rmd_base"], format_currency(base.estimated_rmd_at_75))
    c3.metric(labels["savings"], format_currency(savings))
    c4.metric(labels["trad75"], format_currency(conv.traditional_balance_at_75))

    render_note(
        f"In this scenario, the conversion path changes the age-75 RMD by {format_currency(base.estimated_rmd_at_75 - conv.estimated_rmd_at_75)} and changes total modeled lifetime costs by {format_currency(savings)}."
        if not zh
        else f"在这个情景中，转换路径让 75 岁的 RMD 变化了 {format_currency(base.estimated_rmd_at_75 - conv.estimated_rmd_at_75)}，并让模型估算的终身总成本变化了 {format_currency(savings)}。"
    )
    st.caption(
        f"Using shared assumptions: age {current_age}, retire at {retirement_age}, {format_currency(current_401k_balance)} traditional, {format_currency(current_roth_balance)} Roth, {format_currency(current_taxable_balance)} taxable, and {format_percent(annual_return)} annual return."
        if not zh
        else f"使用共享假设：当前年龄 {current_age}，退休年龄 {retirement_age}，traditional {format_currency(current_401k_balance)}，Roth {format_currency(current_roth_balance)}，taxable {format_currency(current_taxable_balance)}，年化收益率 {format_percent(annual_return)}。"
    )

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

    conv_df = pd.DataFrame(result_rows(conv))
    overview_tab, path_tab, detail_tab = st.tabs([labels["overview"], labels["balance_path"], labels["annual_detail"]])

    with overview_tab:
        st.subheader(labels["strategy_comparison"])
        st.dataframe(format_dataframe(summary, currency_columns=["traditional_at_75", "roth_at_75", "taxable_at_75", "rmd_at_75", "federal_tax_total", "state_tax_total", "aca_drag_total", "irmaa_total", "total_cost"]), use_container_width=True)
        compare_rmd = pd.DataFrame(
            {
                "scenario": ["conversion", "no_conversion"],
                "rmd_at_75": [conv.estimated_rmd_at_75, base.estimated_rmd_at_75],
            }
        ).set_index("scenario")
        st.subheader(labels["rmd_age_75"])
        st.bar_chart(compare_rmd)

    with path_tab:
        chart_df = conv_df[["age", "recommended_conversion", "end_traditional", "end_roth", "end_taxable"]].set_index("age")
        st.subheader(labels["ladder_path"])
        st.line_chart(chart_df)

    with detail_tab:
        st.subheader(labels["annual_path"])
        detail_df = conv_df[
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
        ]
        st.dataframe(
            format_dataframe(
                detail_df,
                currency_columns=[
                    "start_traditional",
                    "start_taxable",
                    "start_roth",
                    "spending_need",
                    "recommended_conversion",
                    "gross_income",
                    "estimated_federal_tax",
                    "estimated_state_tax",
                    "aca_subsidy_loss",
                    "irmaa_surcharge",
                    "end_traditional",
                    "end_roth",
                    "end_taxable",
                ],
            ),
            use_container_width=True,
        )

    st.caption(labels["caption"])
