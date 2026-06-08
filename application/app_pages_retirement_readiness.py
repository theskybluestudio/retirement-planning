#!/usr/bin/env python3
from __future__ import annotations

import pandas as pd
import streamlit as st

from app_i18n import section
from app_state import commit_shared_widget, get_total_portfolio, prime_shared_widget, shared_widget_key
from app_ui import format_currency, format_dataframe, format_percent, money_input, percent_input, render_explainer, render_header, render_note



def render_page() -> None:
    zh = st.session_state.get("language", "en") == "zh"
    common = section("common")
    assumptions = section("assumptions")
    labels = section("readiness")
    render_header(labels["title"], labels["subtitle"])
    render_explainer(common["about_tool"], labels["about_body"])

    for key in [
        "current_age", "retirement_age", "traditional_balance", "roth_balance", "taxable_balance",
        "annual_contribution", "annual_return", "inflation", "annual_retirement_spending",
        "annual_social_security_benefit", "annual_pension_income",
    ]:
        prime_shared_widget(key)

    with st.expander(common["shared_inputs"], expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.number_input(assumptions["current_age"], min_value=18, max_value=80, key=shared_widget_key("current_age"), on_change=commit_shared_widget, args=("current_age",))
            st.number_input(assumptions["retirement_age"], min_value=25, max_value=80, key=shared_widget_key("retirement_age"), on_change=commit_shared_widget, args=("retirement_age",))
        with c2:
            money_input(assumptions["traditional_balance"], min_value=0.0, key=shared_widget_key("traditional_balance"), on_change=commit_shared_widget, args=("traditional_balance",))
            money_input(assumptions["roth_balance"], min_value=0.0, key=shared_widget_key("roth_balance"), on_change=commit_shared_widget, args=("roth_balance",))
            money_input(assumptions["taxable_balance"], min_value=0.0, key=shared_widget_key("taxable_balance"), on_change=commit_shared_widget, args=("taxable_balance",))
        with c3:
            money_input(assumptions["annual_contribution"], min_value=0.0, key=shared_widget_key("annual_contribution"), on_change=commit_shared_widget, args=("annual_contribution",))
            percent_input(assumptions["annual_return"], min_value=0.0, max_value=0.20, key=shared_widget_key("annual_return"), on_change=commit_shared_widget, args=("annual_return",))
            percent_input(assumptions["inflation"], min_value=0.0, max_value=0.10, key=shared_widget_key("inflation"), on_change=commit_shared_widget, args=("inflation",))
            money_input(assumptions["annual_retirement_spending"], min_value=0.0, key=shared_widget_key("annual_retirement_spending"), on_change=commit_shared_widget, args=("annual_retirement_spending",))
            money_input(assumptions["annual_ss_benefit"], min_value=0.0, key=shared_widget_key("annual_social_security_benefit"), on_change=commit_shared_widget, args=("annual_social_security_benefit",))
            money_input(assumptions["annual_pension_income"], min_value=0.0, key=shared_widget_key("annual_pension_income"), on_change=commit_shared_widget, args=("annual_pension_income",))

    with st.sidebar:
        st.divider()
        st.header(common["page_specific_inputs"])
        withdrawal_rate = percent_input(labels["withdrawal_rate"], min_value=0.01, max_value=0.10, key="readiness_withdrawal_rate")

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
    c4.metric(labels["funding_ratio"], format_percent(replacement_ratio))

    render_note(
        f"Portfolio income at a {format_percent(withdrawal_rate)} withdrawal rate is {format_currency(portfolio_income)} per year. That creates a {'surplus' if gap >= 0 else 'gap'} of {format_currency(abs(gap))} relative to the target spending level."
        if not zh
        else f"按 {format_percent(withdrawal_rate)} 的提款率计算，资产收入约为每年 {format_currency(portfolio_income)}。相对于目标支出，这形成了 {format_currency(abs(gap))} 的{'盈余' if gap >= 0 else '缺口'}。"
    )
    st.caption(
        f"Using shared assumptions: total current portfolio {format_currency(current_savings)}, annual contribution {format_currency(annual_contribution)}, annual return {format_percent(annual_return)}, inflation {format_percent(inflation)}."
        if not zh
        else f"使用共享假设：当前总资产 {format_currency(current_savings)}，年度投入 {format_currency(annual_contribution)}，年化收益率 {format_percent(annual_return)}，通胀率 {format_percent(inflation)}。"
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
    st.dataframe(format_dataframe(projection_df.reset_index(), currency_columns=["nominal_balance", "real_balance"]), use_container_width=True)
    st.caption(labels["caption"])
