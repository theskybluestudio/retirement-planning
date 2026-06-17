#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime

import streamlit as st

from app_i18n import section
from app_state import (
    export_assumptions,
    get_total_portfolio,
    import_assumptions,
    render_shared_assumptions_panel,
    reset_assumptions,
    validate_assumptions,
)
from app_ui import format_currency, render_explainer, render_header, render_note



def render_page() -> None:
    labels = section("assumptions")
    render_header(
        labels["title"],
        labels["subtitle"],
    )
    render_explainer(section("common")["about_tool"], labels["about_body"])

    action_col, download_col = st.columns([1.0, 1.4])
    with action_col:
        if st.button(labels["reset_defaults"], width="stretch"):
            reset_assumptions()
            st.rerun()
    with download_col:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        st.download_button(
            labels["download_json"],
            data=export_assumptions(),
            file_name=f"retirement-assumptions-{timestamp}.json",
            mime="application/json",
            width="stretch",
        )

    uploaded = st.file_uploader(labels["load_json"], type=["json"])
    if uploaded is not None:
        try:
            import_assumptions(uploaded.getvalue().decode("utf-8"))
            st.success(labels["loaded_json_success"])
            st.rerun()
        except Exception as exc:
            st.error(f"{labels['load_json_error']} {exc}")

    render_shared_assumptions_panel({"shared_inputs": labels["title"]}, labels, expanded=True)

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
