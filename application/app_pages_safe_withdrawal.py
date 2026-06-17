#!/usr/bin/env python3
from __future__ import annotations

import pandas as pd
import streamlit as st

from app_i18n import section, tooltip
from app_state import get_total_portfolio, render_shared_assumptions_panel
from app_ui import format_currency, format_dataframe, format_percent, percent_input, render_explainer, render_header, render_note


RETURNS = [-0.15, -0.08, 0.18, 0.12, 0.07, 0.11, -0.04, 0.09, 0.06, 0.08, 0.05, 0.07, -0.10, 0.14, 0.09]



def simulate_fixed(balance: float, withdrawal: float) -> list[dict[str, float]]:
    rows = []
    for year, rate in enumerate(RETURNS, start=1):
        start_balance = balance
        actual_withdrawal = min(balance, withdrawal)
        balance = max(0.0, balance - actual_withdrawal)
        balance *= 1 + rate
        rows.append({"year": year, "strategy": "Fixed", "start_balance": start_balance, "withdrawal": actual_withdrawal, "return": rate, "end_balance": balance})
    return rows



def simulate_guardrails(balance: float, initial_withdrawal: float, floor_rate: float, ceiling_rate: float) -> list[dict[str, float]]:
    rows = []
    withdrawal = initial_withdrawal
    for year, rate in enumerate(RETURNS, start=1):
        start_balance = balance
        withdrawal_rate = withdrawal / start_balance if start_balance else 0.0
        if withdrawal_rate > ceiling_rate:
            withdrawal *= 0.90
        elif withdrawal_rate < floor_rate:
            withdrawal *= 1.08
        actual_withdrawal = min(balance, withdrawal)
        balance = max(0.0, balance - actual_withdrawal)
        balance *= 1 + rate
        rows.append({"year": year, "strategy": "Guardrails", "start_balance": start_balance, "withdrawal": actual_withdrawal, "return": rate, "end_balance": balance})
    return rows



def render_page() -> None:
    zh = st.session_state.get("language", "en") == "zh"
    common = section("common")
    assumptions = section("assumptions")
    labels = section("safe_withdrawal")
    render_header(labels["title"], labels["subtitle"])
    render_explainer(common["about_tool"], labels["about_body"])

    render_shared_assumptions_panel(common, assumptions)

    with st.sidebar:
        st.divider()
        st.header(common["page_specific_inputs"])
        floor_rate = percent_input(labels["lower_guardrail"], min_value=0.01, max_value=0.10, key="guard_floor_rate", help=tooltip("safe_withdrawal", "lower_guardrail"))
        ceiling_rate = percent_input(labels["upper_guardrail"], min_value=0.02, max_value=0.15, key="guard_ceiling_rate", help=tooltip("safe_withdrawal", "upper_guardrail"))

    start_balance = get_total_portfolio()
    initial_withdrawal = float(st.session_state.annual_retirement_spending)

    fixed_rows = simulate_fixed(float(start_balance), float(initial_withdrawal))
    guard_rows = simulate_guardrails(float(start_balance), float(initial_withdrawal), float(floor_rate), float(ceiling_rate))
    fixed_df = pd.DataFrame(fixed_rows)
    guard_df = pd.DataFrame(guard_rows)

    fixed_end = fixed_df["end_balance"].iloc[-1]
    guard_end = guard_df["end_balance"].iloc[-1]
    fixed_total = fixed_df["withdrawal"].sum()
    guard_total = guard_df["withdrawal"].sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(labels["fixed_end"], format_currency(fixed_end))
    c2.metric(labels["guardrails_end"], format_currency(guard_end))
    c3.metric(labels["fixed_withdrawals"], format_currency(fixed_total))
    c4.metric(labels["guardrail_withdrawals"], format_currency(guard_total))

    render_note(
        f"The guardrail path ends with {format_currency(guard_end - fixed_end)} more portfolio value in this return sequence while paying out {format_currency(guard_total - fixed_total)} {'more' if guard_total >= fixed_total else 'less'} over the full period."
        if not zh
        else f"在这条收益路径下，护栏策略最终比固定策略多保留 {format_currency(guard_end - fixed_end)} 资产，同时整个期间的提款总额{'更高' if guard_total >= fixed_total else '更低'} {format_currency(abs(guard_total - fixed_total))}。"
    )
    st.caption(
        f"Using shared assumptions: total investable portfolio {format_currency(start_balance)} and annual retirement spending {format_currency(initial_withdrawal)} as the starting withdrawal."
        if not zh
        else f"使用共享假设：总投资资产 {format_currency(start_balance)}，并以年度退休支出 {format_currency(initial_withdrawal)} 作为起始提款额。"
    )

    balances = pd.DataFrame({
        "year": fixed_df["year"],
        "fixed": fixed_df["end_balance"],
        "guardrails": guard_df["end_balance"],
    }).set_index("year")
    withdrawals = pd.DataFrame({
        "year": fixed_df["year"],
        "fixed": fixed_df["withdrawal"],
        "guardrails": guard_df["withdrawal"],
    }).set_index("year")

    left, right = st.columns(2)
    with left:
        st.subheader(labels["ending_path"])
        st.line_chart(balances)
    with right:
        st.subheader(labels["withdrawal_path"])
        st.line_chart(withdrawals)

    detail = fixed_df.merge(guard_df, on="year", suffixes=("_fixed", "_guardrails"))
    st.subheader(labels["scenario_detail"])
    st.dataframe(format_dataframe(detail, currency_columns=["start_balance_fixed", "withdrawal_fixed", "end_balance_fixed", "start_balance_guardrails", "withdrawal_guardrails", "end_balance_guardrails"]), width="stretch")
    st.caption(labels["caption"])
