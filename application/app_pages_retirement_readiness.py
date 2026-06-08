#!/usr/bin/env python3
from __future__ import annotations

import pandas as pd
import streamlit as st

from app_i18n import section
from app_state import get_total_portfolio
from app_ui import format_currency, render_explainer, render_header, render_note



def render_page() -> None:
    zh = st.session_state.get("language", "en") == "zh"
    common = section("common")
    labels = section("readiness")
    render_header(labels["title"], labels["subtitle"])
    render_explainer(common["about_tool"], labels["about_body"])

    with st.expander(common["shared_inputs"], expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.number_input(labels["current_age"], min_value=18, max_value=80, key="current_age")
            st.number_input(labels["retirement_age"], min_value=25, max_value=80, key="retirement_age")
        with c2:
            st.number_input(labels["traditional_balance"], min_value=0.0, step=10_000.0, key="traditional_balance")
            st.number_input(labels["roth_balance"], min_value=0.0, step=10_000.0, key="roth_balance")
            st.number_input(labels["taxable_balance"], min_value=0.0, step=10_000.0, key="taxable_balance")
        with c3:
            st.number_input(labels["annual_contribution"], min_value=0.0, step=1_000.0, key="annual_contribution")
            st.number_input(labels["annual_return"], min_value=0.0, max_value=0.20, step=0.005, format="%.3f", key="annual_return")
            st.number_input(labels["inflation"], min_value=0.0, max_value=0.10, step=0.005, format="%.3f", key="inflation")
            st.number_input(labels["annual_retirement_spending"], min_value=0.0, step=5_000.0, key="annual_retirement_spending")
            st.number_input(labels["annual_ss_benefit"], min_value=0.0, step=1_000.0, key="annual_social_security_benefit")
            st.number_input(labels["annual_pension_income"], min_value=0.0, step=1_000.0, key="annual_pension_income")

    with st.sidebar:
        st.divider()
        st.header(common["page_specific_inputs"])
        withdrawal_rate = st.number_input(labels["withdrawal_rate"], min_value=0.01, max_value=0.10, step=0.005, format="%.3f", key="readiness_withdrawal_rate")

    current_age = int(st.session_state.current_age)
    retirement_age = int(st.session_state.retirement_age)
    current_savings = get_total_portfolio()
    annual_contribution = float(st.session_state.annual_contribution)
    annual_return = float(st.session_state.annual_return)
    inflation = float(st.session_state.inflation)
    annual_spending = float(st.session_state.annual_retirement_spending)
    annual_social_security = float(st.session_state.annual_social_security_benefit)
    annual_pension = float(st.session_state.annual_pension_income)

    years_to_retirement = max(0, int(retirement_age - current_age))
    nominal_balance = float(current_savings)
    real_balance = float(current_savings)
    rows = []
    for year in range(years_to_retirement + 1):
        age = current_age + year
        rows.append({"age": age, "nominal_balance": nominal_balance, "real_balance": real_balance})
        nominal_balance = nominal_balance * (1 + annual_return) + annual_contribution
        real_balance = real_balance * ((1 + annual_return) / (1 + inflation)) + annual_contribution

    final_nominal = rows[-1]["nominal_balance"] if rows else float(current_savings)
    final_real = rows[-1]["real_balance"] if rows else float(current_savings)
    portfolio_income = final_nominal * withdrawal_rate
    fixed_income = annual_social_security + annual_pension
    total_income = portfolio_income + fixed_income
    gap = total_income - annual_spending
    replacement_ratio = total_income / annual_spending if annual_spending else 0.0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(labels["nest_egg"], format_currency(final_nominal))
    c2.metric(labels["real_nest_egg"], format_currency(final_real))
    c3.metric(labels["total_income"], f"{format_currency(total_income)}/yr")
    c4.metric(labels["funding_ratio"], f"{replacement_ratio:.0%}")

    render_note(
        f"Portfolio income at a {withdrawal_rate:.1%} withdrawal rate is {format_currency(portfolio_income)} per year. That creates a {'surplus' if gap >= 0 else 'gap'} of {format_currency(abs(gap))} relative to the target spending level."
        if not zh
        else f"按 {withdrawal_rate:.1%} 的提款率计算，资产收入约为每年 {format_currency(portfolio_income)}。相对于目标支出，这形成了 {format_currency(abs(gap))} 的{'盈余' if gap >= 0 else '缺口'}。"
    )
    st.caption(
        f"Using shared assumptions: total current portfolio {format_currency(current_savings)}, annual contribution {format_currency(annual_contribution)}, annual return {annual_return:.1%}, inflation {inflation:.1%}."
        if not zh
        else f"使用共享假设：当前总资产 {format_currency(current_savings)}，年度投入 {format_currency(annual_contribution)}，年化收益率 {annual_return:.1%}，通胀率 {inflation:.1%}。"
    )

    projection_df = pd.DataFrame(rows).set_index("age")
    chart_col, detail_col = st.columns([1.35, 1.0])
    with chart_col:
        st.subheader(labels["growth"])
        st.line_chart(projection_df)
    with detail_col:
        st.subheader(labels["interpretation"])
        if gap >= 0:
            st.success(labels["covers"])
        else:
            extra_monthly = abs(gap) / 12
            st.warning(
                f"This plan shows an annual shortfall of {format_currency(abs(gap))}. Roughly {format_currency(extra_monthly)}/month needs to come from higher savings, later retirement, lower spending, or more guaranteed income."
                if not zh
                else f"这个方案显示每年存在 {format_currency(abs(gap))} 的缺口。大约每月需要额外 {format_currency(extra_monthly)}，可以通过更多储蓄、更晚退休、更低支出或更多固定收入来弥补。"
            )
        years_text = "year" if years_to_retirement == 1 else "years"
        if zh:
            st.write(f"在这个情景中，距离退休还有 **{years_to_retirement} 年**。")
            st.write(f"固定收入来源每年贡献 **{format_currency(fixed_income)}**。")
        else:
            st.write(f"There are **{years_to_retirement} {years_text}** until retirement in this scenario.")
            st.write(f"Fixed income sources contribute **{format_currency(fixed_income)}** per year.")

    st.subheader(labels["table"])
    st.dataframe(projection_df.reset_index(), use_container_width=True)
    st.caption(labels["caption"])
