#!/usr/bin/env python3
from __future__ import annotations

import pandas as pd
import streamlit as st

from app_i18n import section, tooltip
from app_state import render_shared_assumptions_panel
from app_ui import format_currency, format_dataframe, render_explainer, render_header, render_note


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
    zh = st.session_state.get("language", "en") == "zh"
    common = section("common")
    assumptions = section("assumptions")
    labels = section("social_security")
    render_header(labels["title"], labels["subtitle"])
    render_explainer(common["about_tool"], labels["about_body"])

    render_shared_assumptions_panel(common, assumptions)

    with st.sidebar:
        st.divider()
        st.header(common["page_specific_inputs"])
        longevity_age = st.number_input(labels["longevity_age"], min_value=70, max_value=100, key="ss_longevity_age", help=tooltip("social_security", "longevity_age"))
        selected_claim_age = st.slider(labels["highlight_age"], min_value=62, max_value=70, value=67, key="ss_selected_claim_age")

    fra_annual_benefit = float(st.session_state.social_security_fra_benefit)

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
    selected_row = df.loc[df["claim_age"] == selected_claim_age].iloc[0]
    age_62_lifetime = df.loc[df["claim_age"] == 62, "lifetime_benefit"].iloc[0]
    age_70_lifetime = df.loc[df["claim_age"] == 70, "lifetime_benefit"].iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(labels["best_age"], f"{int(best_row['claim_age'])}")
    c2.metric(labels["best_lifetime"], format_currency(best_row["lifetime_benefit"]))
    c3.metric((f"Benefit at {selected_claim_age}" if not zh else f"{selected_claim_age} 岁收益"), f"{format_currency(selected_row['annual_benefit'])}/yr")
    c4.metric(("Age 70 vs 62" if not zh else "70 岁 vs 62 岁"), format_currency(age_70_lifetime - age_62_lifetime))

    render_note(
        f"Claiming at age {selected_claim_age} produces about {format_currency(selected_row['annual_benefit'])} per year in this simplified model, with lifetime benefits of {format_currency(selected_row['lifetime_benefit'])} if benefits are collected through age {longevity_age}."
        if not zh
        else f"在这个简化模型中，若 {selected_claim_age} 岁领取，每年大约可获得 {format_currency(selected_row['annual_benefit'])}，若领取至 {longevity_age} 岁，终身收益约为 {format_currency(selected_row['lifetime_benefit'])}。"
    )
    st.caption(
        f"Using shared assumptions: Social Security benefit at FRA {format_currency(fra_annual_benefit)} and current planned claim age {int(st.session_state.social_security_claim_age)}."
        if not zh
        else f"使用共享假设：FRA 时社保收入 {format_currency(fra_annual_benefit)}，当前计划领取年龄 {int(st.session_state.social_security_claim_age)}。"
    )

    chart_col, detail_col = st.columns([1.3, 1.0])
    with chart_col:
        st.subheader(labels["annual_vs_lifetime"])
        chart_df = df.set_index("claim_age")[["annual_benefit", "lifetime_benefit"]]
        st.line_chart(chart_df)
    with detail_col:
        st.subheader(labels["quick_read"])
        if age_70_lifetime > age_62_lifetime:
            st.info("In this longevity scenario, delaying to 70 beats claiming at 62 on lifetime dollars." if not zh else "在这个寿命情景下，延迟到 70 岁领取在终身总额上优于 62 岁领取。")
        else:
            st.info("In this longevity scenario, earlier claiming wins on lifetime dollars." if not zh else "在这个寿命情景下，更早领取在终身总额上更有利。")
        st.write(f"Selected claim age: **{selected_claim_age}**" if not zh else f"选定领取年龄：**{selected_claim_age}**")
        st.write(f"Years collected: **{int(selected_row['years_collected'])}**" if not zh else f"领取年数：**{int(selected_row['years_collected'])}**")

    st.subheader(labels["comparison"])
    st.dataframe(format_dataframe(df, currency_columns=["annual_benefit", "lifetime_benefit"], integer_columns=["claim_age", "years_collected"]), width="stretch")
    st.caption(labels["caption"])
