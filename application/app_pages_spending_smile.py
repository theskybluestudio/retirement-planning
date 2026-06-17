#!/usr/bin/env python3
from __future__ import annotations

import pandas as pd
import streamlit as st

from app_i18n import section, tooltip
from app_state import render_shared_assumptions_panel
from app_ui import format_currency, format_dataframe, money_input, render_explainer, render_header, render_note



def render_page() -> None:
    zh = st.session_state.get("language", "en") == "zh"
    common = section("common")
    assumptions = section("assumptions")
    labels = section("spending_smile")
    render_header(labels["title"], labels["subtitle"])
    render_explainer(common["about_tool"], labels["about_body"])

    render_shared_assumptions_panel(common, assumptions)

    with st.sidebar:
        st.divider()
        st.header(common["page_specific_inputs"])
        go_go_years = st.number_input(labels["go_go_years"], min_value=1, max_value=20, value=10, key="smile_go_go_years", help=tooltip("spending_smile", "go_go_years"))
        go_go_multiplier = st.number_input(labels["go_go_multiplier"], min_value=0.5, max_value=2.0, value=1.15, step=0.05, key="smile_go_go_multiplier", help=tooltip("spending_smile", "go_go_multiplier"))
        slow_go_years = st.number_input(labels["slow_go_years"], min_value=1, max_value=20, value=10, key="smile_slow_go_years", help=tooltip("spending_smile", "slow_go_years"))
        slow_go_multiplier = st.number_input(labels["slow_go_multiplier"], min_value=0.5, max_value=2.0, value=0.95, step=0.05, key="smile_slow_go_multiplier", help=tooltip("spending_smile", "slow_go_multiplier"))
        no_go_years = st.number_input(labels["no_go_years"], min_value=1, max_value=20, value=10, key="smile_no_go_years", help=tooltip("spending_smile", "no_go_years"))
        no_go_multiplier = st.number_input(labels["no_go_multiplier"], min_value=0.5, max_value=2.0, value=0.80, step=0.05, key="smile_no_go_multiplier", help=tooltip("spending_smile", "no_go_multiplier"))
        healthcare_step_up = money_input(labels["healthcare_step_up"], min_value=0.0, value=15_000.0, key="smile_healthcare_step_up", help=tooltip("spending_smile", "healthcare_step_up"))

    retirement_age = int(st.session_state.retirement_age)
    base_spending = float(st.session_state.annual_retirement_spending)

    phases = [
        ("Go-go", int(go_go_years), float(go_go_multiplier), 0.0),
        ("Slow-go", int(slow_go_years), float(slow_go_multiplier), 0.0),
        ("No-go", int(no_go_years), float(no_go_multiplier), float(healthcare_step_up)),
    ]

    rows = []
    current_age = int(retirement_age)
    for phase_name, years, multiplier, extra in phases:
        for _ in range(years):
            rows.append(
                {
                    "age": current_age,
                    "phase": phase_name,
                    "annual_spending": base_spending * multiplier + extra,
                }
            )
            current_age += 1

    df = pd.DataFrame(rows)
    flat_total = len(df) * float(base_spending)
    phase_total = df["annual_spending"].sum()

    c1, c2, c3 = st.columns(3)
    c1.metric(labels["years_modeled"], f"{len(df)}")
    c2.metric(labels["flat_total"], format_currency(flat_total))
    c3.metric(labels["phase_total"], format_currency(phase_total))

    render_note(
        f"This spending path differs from a flat plan by {format_currency(phase_total - flat_total)} over the modeled retirement horizon."
        if not zh
        else f"在所建模的退休期间内，这条分阶段支出路径与固定支出方案相比相差 {format_currency(phase_total - flat_total)}。"
    )
    st.caption(
        f"Using shared assumptions: retirement age {retirement_age} and base annual spending {format_currency(base_spending)}."
        if not zh
        else f"使用共享假设：退休年龄 {retirement_age}，基础年度支出 {format_currency(base_spending)}。"
    )

    left, right = st.columns([1.25, 1.0])
    with left:
        st.subheader(labels["spending_by_age"])
        st.line_chart(df.set_index("age")[["annual_spending"]])
    with right:
        st.subheader(labels["phase_averages"])
        phase_summary = df.groupby("phase", as_index=True)["annual_spending"].mean().to_frame()
        st.bar_chart(phase_summary)

    st.subheader(labels["detailed_schedule"])
    st.dataframe(format_dataframe(df, currency_columns=["annual_spending"]), width="stretch")
    st.caption(labels["caption"])
