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
    export_assumptions,
    get_total_portfolio,
    import_assumptions,
    reset_assumptions,
    validate_assumptions,
)
from app_ui import format_currency, render_explainer, render_header, render_note



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
                labels["annual_return"]: f"{float(values['annual_return']) * 100:.1f}%",
                labels["inflation"]: f"{float(values['inflation']) * 100:.1f}%",
                labels["ss_claim_age"]: int(values["social_security_claim_age"]),
                labels["target_bracket"] if "target_bracket" in labels else ("Target bracket" if not zh else "目标税档"): str(values["rmd_target_bracket"]),
                labels["withdrawal_rate"] if "withdrawal_rate" in labels else ("Withdrawal rate" if not zh else "提款率"): f"{float(values['readiness_withdrawal_rate']) * 100:.1f}%",
            }
        )

    st.subheader(labels["scenario_comparison"])
    st.dataframe(pd.DataFrame(comparison_rows), use_container_width=True, hide_index=True)

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
    with left:
        st.subheader(labels["personal"])
        st.number_input(labels["current_age"], min_value=18, max_value=80, key="current_age")
        st.number_input(labels["retirement_age"], min_value=25, max_value=80, key="retirement_age")
        st.number_input(labels["life_expectancy"], min_value=70, max_value=105, key="life_expectancy")
        st.selectbox(labels["filing_status"], options=["mfj", "single"], key="filing_status")

        st.subheader(labels["accounts"])
        st.number_input(labels["traditional_balance"], min_value=0.0, step=10_000.0, key="traditional_balance")
        st.number_input(labels["roth_balance"], min_value=0.0, step=10_000.0, key="roth_balance")
        st.number_input(labels["taxable_balance"], min_value=0.0, step=10_000.0, key="taxable_balance")
        st.checkbox(labels["has_roth_ira"], key="has_roth_ira")
        st.checkbox(labels["has_taxable_brokerage"], key="has_taxable_brokerage")

    with right:
        st.subheader(labels["cash_flow"])
        st.number_input(labels["annual_contribution"], min_value=0.0, step=1_000.0, key="annual_contribution")
        st.number_input(labels["annual_retirement_spending"], min_value=0.0, step=5_000.0, key="annual_retirement_spending")
        st.number_input(labels["annual_ss_benefit"], min_value=0.0, step=1_000.0, key="annual_social_security_benefit")
        st.number_input(labels["annual_ss_benefit_fra"], min_value=0.0, step=1_000.0, key="social_security_fra_benefit")
        st.number_input(labels["ss_claim_age"], min_value=62, max_value=75, key="social_security_claim_age")
        st.number_input(labels["annual_pension_income"], min_value=0.0, step=1_000.0, key="annual_pension_income")
        st.number_input(labels["annual_other_income"], min_value=0.0, step=1_000.0, key="annual_other_income")

        st.subheader(labels["market_tax"])
        st.number_input(labels["annual_return"], min_value=0.0, max_value=0.20, step=0.005, format="%.3f", key="annual_return")
        st.number_input(labels["inflation"], min_value=0.0, max_value=0.10, step=0.005, format="%.3f", key="inflation")
        st.number_input(labels["state_tax_rate"], min_value=0.0, max_value=0.20, step=0.005, format="%.3f", key="state_tax_rate")

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
