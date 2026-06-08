#!/usr/bin/env python3
from __future__ import annotations

import streamlit as st

from app_i18n import section
from app_ui import format_currency, render_explainer, render_header, render_note



def future_value(balance: float, contribution: float, rate: float, years: int) -> float:
    total = balance
    for _ in range(years):
        total = total * (1 + rate) + contribution
    return total



def required_contribution(target: float, current_savings: float, rate: float, years: int) -> float:
    if years <= 0:
        return max(0.0, target - current_savings)
    grown_current = current_savings * ((1 + rate) ** years)
    annuity_factor = sum((1 + rate) ** power for power in range(years))
    needed = max(0.0, target - grown_current)
    return needed / annuity_factor if annuity_factor else needed / years



def render_page() -> None:
    zh = st.session_state.get("language", "en") == "zh"
    common = section("common")
    assumptions = section("assumptions")
    labels = section("savings_rate")
    render_header(labels["title"], labels["subtitle"])
    render_explainer(common["about_tool"], labels["about_body"])

    with st.expander(common["shared_inputs"], expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.number_input(assumptions["current_age"], min_value=18, max_value=80, key="current_age")
            st.number_input(assumptions["retirement_age"], min_value=25, max_value=80, key="retirement_age")
        with c2:
            st.number_input(assumptions["traditional_balance"], min_value=0.0, step=10_000.0, key="traditional_balance")
            st.number_input(assumptions["roth_balance"], min_value=0.0, step=10_000.0, key="roth_balance")
            st.number_input(assumptions["taxable_balance"], min_value=0.0, step=10_000.0, key="taxable_balance")
        with c3:
            st.number_input(assumptions["annual_contribution"], min_value=0.0, step=1_000.0, key="annual_contribution")
            st.number_input(assumptions["annual_return"], min_value=0.0, max_value=0.20, step=0.005, format="%.3f", key="annual_return")

    with st.sidebar:
        st.divider()
        st.header(common["page_specific_inputs"])
        target_portfolio = st.number_input(labels["target_portfolio"], min_value=0.0, step=50_000.0, key="save_target_portfolio")

    current_age = int(st.session_state.current_age)
    retirement_age = int(st.session_state.retirement_age)
    current_savings = float(st.session_state.traditional_balance) + float(st.session_state.roth_balance) + float(st.session_state.taxable_balance)
    current_annual_savings = float(st.session_state.annual_contribution)
    annual_return = float(st.session_state.annual_return)

    years = max(0, int(retirement_age - current_age))
    projected = future_value(float(current_savings), float(current_annual_savings), float(annual_return), years)
    needed = required_contribution(float(target_portfolio), float(current_savings), float(annual_return), years)
    gap = needed - float(current_annual_savings)
    extra_year_projection = future_value(float(current_savings), float(current_annual_savings), float(annual_return), years + 3)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(labels["projected_portfolio"], format_currency(projected))
    c2.metric(labels["required_annual_savings"], format_currency(needed))
    c3.metric(labels["savings_gap"], format_currency(gap))
    c4.metric(labels["retire_later"], format_currency(extra_year_projection))

    render_note(
        f"To target {format_currency(target_portfolio)} by age {retirement_age}, this model estimates annual savings of about {format_currency(needed)}."
        if not zh
        else f"若想在 {retirement_age} 岁前达到 {format_currency(target_portfolio)} 的目标资产，这个模型估算每年大约需要储蓄 {format_currency(needed)}。"
    )
    st.caption(
        f"Using shared assumptions: age {current_age}, retire at {retirement_age}, current portfolio {format_currency(current_savings)}, annual savings {format_currency(current_annual_savings)}, return {annual_return:.1%}."
        if not zh
        else f"使用共享假设：当前年龄 {current_age}，退休年龄 {retirement_age}，当前资产 {format_currency(current_savings)}，年度储蓄 {format_currency(current_annual_savings)}，收益率 {annual_return:.1%}。"
    )

    if gap <= 0:
        st.success("在这个简化模型中，当前储蓄速度足以达到目标。" if zh else "Current savings pace is enough to hit the target in this simplified model.")
    else:
        monthly_gap = gap / 12
        st.warning(
            f"当前储蓄每年大约少了 {format_currency(gap)}，即每月约少 {format_currency(monthly_gap)}。" if zh else f"Current savings fall short by about {format_currency(gap)} per year, or roughly {format_currency(monthly_gap)}/month."
        )

    st.subheader(labels["tradeoff_ideas"])
    if zh:
        st.markdown(
            f"- 保持每年储蓄 **{format_currency(current_annual_savings)}**，并推迟退休\n"
            f"- 将年度储蓄提高到接近 **{format_currency(needed)}**\n"
            f"- 如果支出假设过高，可下调目标资产"
        )
    else:
        st.markdown(
            f"- Keep saving **{format_currency(current_annual_savings)}** and retire later\n"
            f"- Raise annual savings toward **{format_currency(needed)}**\n"
            f"- Reduce the target portfolio if spending assumptions are too high"
        )
    st.caption(labels["caption"])
