#!/usr/bin/env python3
from __future__ import annotations

import pandas as pd
import streamlit as st

from app_i18n import section
from app_state import get_total_portfolio
from app_ui import format_currency, render_explainer, render_header, render_note



def simulate_path(start_balance: float, annual_withdrawal: float, returns: list[float]) -> list[dict[str, float]]:
    balance = start_balance
    rows = []
    for year, rate in enumerate(returns, start=1):
        start_year = balance
        balance = max(0.0, balance - annual_withdrawal)
        balance *= 1 + rate
        rows.append(
            {
                "year": year,
                "start_balance": start_year,
                "return": rate,
                "end_balance": balance,
            }
        )
    return rows



def render_page() -> None:
    zh = st.session_state.get("language", "en") == "zh"
    common = section("common")
    labels = section("sequence")
    render_header(labels["title"], labels["subtitle"])
    render_explainer(common["about_tool"], labels["about_body"])

    start_balance = get_total_portfolio()
    annual_withdrawal = float(st.session_state.annual_retirement_spending)

    bad_early = [-0.18, -0.12, -0.08, 0.08, 0.10, 0.11, 0.12, 0.09, 0.08, 0.10]
    bad_late = [0.08, 0.10, 0.11, 0.12, 0.09, 0.08, 0.10, -0.18, -0.12, -0.08]

    early_df = pd.DataFrame(simulate_path(start_balance, annual_withdrawal, bad_early))
    late_df = pd.DataFrame(simulate_path(start_balance, annual_withdrawal, bad_late))
    end_early = early_df["end_balance"].iloc[-1]
    end_late = late_df["end_balance"].iloc[-1]

    c1, c2, c3 = st.columns(3)
    c1.metric(labels["bad_early"], format_currency(end_early))
    c2.metric(labels["bad_late"], format_currency(end_late))
    c3.metric(labels["difference"], format_currency(end_late - end_early))

    render_note(
        f"Both paths use the same return set. The only difference is order. In this case, bad early returns leave the portfolio with {format_currency(end_late - end_early)} less by year 10."
        if not zh
        else f"两条路径使用相同的收益集合，唯一差别是顺序。在这个例子中，坏收益先发生会让投资组合到第 10 年时少 {format_currency(end_late - end_early)}。"
    )
    st.caption(
        f"Using shared assumptions: total investable portfolio {format_currency(start_balance)} and annual retirement spending {format_currency(annual_withdrawal)} as the withdrawal level."
        if not zh
        else f"使用共享假设：总投资资产 {format_currency(start_balance)}，以及年度退休支出 {format_currency(annual_withdrawal)} 作为提款水平。"
    )

    comparison = pd.DataFrame(
        {
            "year": early_df["year"],
            "bad_early": early_df["end_balance"],
            "bad_late": late_df["end_balance"],
        }
    ).set_index("year")

    st.subheader(labels["paths"])
    st.line_chart(comparison)

    st.subheader(labels["details"])
    detail = pd.DataFrame(
        {
            "year": early_df["year"],
            "bad_early_return": early_df["return"],
            "bad_early_end_balance": early_df["end_balance"],
            "bad_late_return": late_df["return"],
            "bad_late_end_balance": late_df["end_balance"],
        }
    )
    st.dataframe(detail, use_container_width=True)

    st.caption(labels["caption"])
