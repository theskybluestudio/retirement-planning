#!/usr/bin/env python3
from __future__ import annotations

import pandas as pd
import streamlit as st



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
    st.title("Sequence of Returns Risk")
    st.caption("Same average return, different order — very different retirement outcomes.")

    with st.sidebar:
        st.header("Sequence inputs")
        start_balance = st.number_input("Starting portfolio", min_value=0.0, value=1_500_000.0, step=10_000.0, key="seq_start_balance")
        annual_withdrawal = st.number_input("Annual withdrawal", min_value=0.0, value=60_000.0, step=1_000.0, key="seq_annual_withdrawal")

    bad_early = [-0.18, -0.12, -0.08, 0.08, 0.10, 0.11, 0.12, 0.09, 0.08, 0.10]
    bad_late = [0.08, 0.10, 0.11, 0.12, 0.09, 0.08, 0.10, -0.18, -0.12, -0.08]

    early_df = pd.DataFrame(simulate_path(start_balance, annual_withdrawal, bad_early))
    late_df = pd.DataFrame(simulate_path(start_balance, annual_withdrawal, bad_late))

    c1, c2 = st.columns(2)
    c1.metric("Ending balance: bad early", f"${early_df['end_balance'].iloc[-1]:,.0f}")
    c2.metric("Ending balance: bad late", f"${late_df['end_balance'].iloc[-1]:,.0f}")

    comparison = pd.DataFrame(
        {
            "year": early_df["year"],
            "bad_early": early_df["end_balance"],
            "bad_late": late_df["end_balance"],
        }
    ).set_index("year")

    st.subheader("Portfolio paths")
    st.line_chart(comparison)

    st.subheader("Scenario details")
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

    st.caption("These two scenarios use the same return set in a different order. That order alone can materially change outcomes once withdrawals begin.")
