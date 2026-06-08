#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st

from app_i18n import section, t
from app_state import (
    PAGE_DEFAULTS,
    SCENARIO_PRESETS,
    SHARED_DEFAULTS,
    apply_preset,
    commit_shared_widget,
    export_assumptions,
    get_total_portfolio,
    import_assumptions,
    prime_shared_widget,
    reset_assumptions,
    shared_widget_key,
    validate_assumptions,
)
from app_ui import format_currency, format_dataframe, format_percent, money_input, percent_input, render_explainer, render_header, render_note



def render_page() -> None:
    labels = section("assumptions")
    preset_labels = section("presets")
    zh = st.session_state.get("language", "en") == "zh"
    render_header(
        labels["title"],
        labels["subtitle"],
    )
    render_explainer(section("common")["about_tool"], labels["about_body"])

    st.subheader(labels["scenario_presets"])
    preset_cols = st.columns(len(SCENARIO_PRESETS))
    for col, preset_name in zip(preset_cols, SCENARIO_PRESETS.keys()):
        with col:
            label = {
                "Base": preset_labels["base"],
                "Conservative": preset_labels["conservative"],
                "Aggressive": preset_labels["aggressive"],
                "Early Retirement": preset_labels["early_retirement"],
            }.get(preset_name, preset_name)
            if st.button(label, use_container_width=True):
                apply_preset(preset_name)
                st.rerun()

    comparison_rows = []
    for preset_name, overrides in SCENARIO_PRESETS.items():
        values = (SHARED_DEFAULTS | PAGE_DEFAULTS | overrides)
        comparison_rows.append(
            {
                "scenario": {
                    "Base": preset_labels["base"],
                    "Conservative": preset_labels["conservative"],
                    "Aggressive": preset_labels["aggressive"],
                    "Early Retirement": preset_labels["early_retirement"],
                }.get(preset_name, preset_name),
                labels["retirement_age"]: int(values["retirement_age"]),
                labels["annual_contribution"]: format_currency(float(values["annual_contribution"])),
                labels["planned_spending"]: format_currency(float(values["annual_retirement_spending"])),
                labels["annual_return"]: format_percent(float(values["annual_return"])),
                labels["inflation"]: format_percent(float(values["inflation"])),
                labels["ss_claim_age"]: int(values["social_security_claim_age"]),
                labels["target_bracket"] if "target_bracket" in labels else ("Target bracket" if not zh else "目标税档"): str(values["rmd_target_bracket"]),
                labels["withdrawal_rate"] if "withdrawal_rate" in labels else ("Withdrawal rate" if not zh else "提款率"): format_percent(float(values["readiness_withdrawal_rate"])),
            }
        )

    st.subheader(labels["scenario_comparison"])
    comparison_df = pd.DataFrame(comparison_rows)
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)

    action_col, download_col = st.columns([1.0, 1.4])
    with action_col:
        if st.button(labels["reset_defaults"], use_container_width=True):
            reset_assumptions()
            st.rerun()
    with download_col:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        st.download_button(
            labels["download_json"],
            data=export_assumptions(),
            file_name=f"retirement-assumptions-{timestamp}.json",
            mime="application/json",
            use_container_width=True,
        )

    uploaded = st.file_uploader(labels["load_json"], type=["json"])
    if uploaded is not None:
        try:
            import_assumptions(uploaded.getvalue().decode("utf-8"))
            st.success(labels["loaded_json_success"])
            st.rerun()
        except Exception as exc:
            st.error(f"{labels['load_json_error']} {exc}")

    left, right = st.columns(2)
    shared_keys = [
        "current_age", "retirement_age", "life_expectancy", "filing_status",
        "traditional_balance", "roth_balance", "taxable_balance", "has_roth_ira", "has_taxable_brokerage",
        "annual_contribution", "annual_retirement_spending", "annual_social_security_benefit", "social_security_fra_benefit",
        "social_security_claim_age", "annual_pension_income", "annual_other_income", "annual_return", "inflation", "state_tax_rate",
    ]
    for key in shared_keys:
        prime_shared_widget(key)

    with left:
        st.subheader(labels["personal"])
        st.number_input(labels["current_age"], min_value=18, max_value=80, key=shared_widget_key("current_age"), on_change=commit_shared_widget, args=("current_age",))
        st.number_input(labels["retirement_age"], min_value=25, max_value=80, key=shared_widget_key("retirement_age"), on_change=commit_shared_widget, args=("retirement_age",))
        st.number_input(labels["life_expectancy"], min_value=70, max_value=105, key=shared_widget_key("life_expectancy"), on_change=commit_shared_widget, args=("life_expectancy",))
        st.selectbox(labels["filing_status"], options=["mfj", "single"], key=shared_widget_key("filing_status"), on_change=commit_shared_widget, args=("filing_status",))

        st.subheader(labels["accounts"])
        money_input(labels["traditional_balance"], min_value=0.0, key=shared_widget_key("traditional_balance"), on_change=commit_shared_widget, args=("traditional_balance",))
        money_input(labels["roth_balance"], min_value=0.0, key=shared_widget_key("roth_balance"), on_change=commit_shared_widget, args=("roth_balance",))
        money_input(labels["taxable_balance"], min_value=0.0, key=shared_widget_key("taxable_balance"), on_change=commit_shared_widget, args=("taxable_balance",))
        st.checkbox(labels["has_roth_ira"], key=shared_widget_key("has_roth_ira"), on_change=commit_shared_widget, args=("has_roth_ira",))
        st.checkbox(labels["has_taxable_brokerage"], key=shared_widget_key("has_taxable_brokerage"), on_change=commit_shared_widget, args=("has_taxable_brokerage",))

    with right:
        st.subheader(labels["cash_flow"])
        money_input(labels["annual_contribution"], min_value=0.0, key=shared_widget_key("annual_contribution"), on_change=commit_shared_widget, args=("annual_contribution",))
        money_input(labels["annual_retirement_spending"], min_value=0.0, key=shared_widget_key("annual_retirement_spending"), on_change=commit_shared_widget, args=("annual_retirement_spending",))
        money_input(labels["annual_ss_benefit"], min_value=0.0, key=shared_widget_key("annual_social_security_benefit"), on_change=commit_shared_widget, args=("annual_social_security_benefit",))
        money_input(labels["annual_ss_benefit_fra"], min_value=0.0, key=shared_widget_key("social_security_fra_benefit"), on_change=commit_shared_widget, args=("social_security_fra_benefit",))
        st.number_input(labels["ss_claim_age"], min_value=62, max_value=75, key=shared_widget_key("social_security_claim_age"), on_change=commit_shared_widget, args=("social_security_claim_age",))
        money_input(labels["annual_pension_income"], min_value=0.0, key=shared_widget_key("annual_pension_income"), on_change=commit_shared_widget, args=("annual_pension_income",))
        money_input(labels["annual_other_income"], min_value=0.0, key=shared_widget_key("annual_other_income"), on_change=commit_shared_widget, args=("annual_other_income",))

        st.subheader(labels["market_tax"])
        percent_input(labels["annual_return"], min_value=0.0, max_value=0.20, key=shared_widget_key("annual_return"), on_change=commit_shared_widget, args=("annual_return",))
        percent_input(labels["inflation"], min_value=0.0, max_value=0.10, key=shared_widget_key("inflation"), on_change=commit_shared_widget, args=("inflation",))
        percent_input(labels["state_tax_rate"], min_value=0.0, max_value=0.20, key=shared_widget_key("state_tax_rate"), on_change=commit_shared_widget, args=("state_tax_rate",))

    errors, warnings = validate_assumptions()
    if errors:
        for message in errors:
            st.error(message)
    if warnings:
        for message in warnings:
            st.warning(message)
    if not errors and not warnings:
        st.success(labels["consistent"])

    c1, c2, c3 = st.columns(3)
    c1.metric(labels["total_portfolio"], format_currency(get_total_portfolio()))
    c2.metric(labels["planned_spending"], format_currency(float(st.session_state.annual_retirement_spending)))
    c3.metric(labels["annual_contribution"], format_currency(float(st.session_state.annual_contribution)))

    render_note(labels["note"])
