#!/usr/bin/env python3
from __future__ import annotations

import pandas as pd
import streamlit as st

from app_i18n import section
from app_ui import format_currency, render_explainer, render_header, render_note


TAX_RATE = 0.22
CAPITAL_GAINS_RATE = 0.15



def simulate_strategy(name: str, annual_spending: float, taxable: float, traditional: float, roth: float, order: list[str]) -> dict[str, float]:
    remaining_need = annual_spending
    taxes = 0.0
    withdrawn = {"taxable": 0.0, "traditional": 0.0, "roth": 0.0}
    balances = {"taxable": taxable, "traditional": traditional, "roth": roth}

    for bucket in order:
        if remaining_need <= 0:
            break
        available = balances[bucket]
        draw = min(available, remaining_need)
        balances[bucket] -= draw
        withdrawn[bucket] += draw
        if bucket == "traditional":
            taxes += draw * TAX_RATE
        elif bucket == "taxable":
            taxes += draw * CAPITAL_GAINS_RATE * 0.35
        remaining_need -= draw

    return {
        "strategy": name,
        "taxable_draw": withdrawn["taxable"],
        "traditional_draw": withdrawn["traditional"],
        "roth_draw": withdrawn["roth"],
        "estimated_tax": taxes,
        "ending_taxable": balances["taxable"],
        "ending_traditional": balances["traditional"],
        "ending_roth": balances["roth"],
        "unfunded_need": remaining_need,
    }



def render_page() -> None:
    zh = st.session_state.get("language", "en") == "zh"
    common = section("common")
    assumptions = section("assumptions")
    labels = section("withdrawal_order")
    render_header(labels["title"], labels["subtitle"])
    render_explainer(common["about_tool"], labels["about_body"])

    with st.expander(common["shared_inputs"], expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            st.number_input(assumptions["taxable_balance"], min_value=0.0, step=10_000.0, key="taxable_balance")
            st.number_input(assumptions["traditional_balance"], min_value=0.0, step=10_000.0, key="traditional_balance")
        with c2:
            st.number_input(assumptions["roth_balance"], min_value=0.0, step=10_000.0, key="roth_balance")
            st.number_input(assumptions["annual_retirement_spending"], min_value=0.0, step=5_000.0, key="annual_retirement_spending")

    with st.sidebar:
        st.divider()
        st.header(common["using_shared_assumptions"])
        st.caption(common["update_shared_assumptions"])

    annual_spending = float(st.session_state.annual_retirement_spending)
    taxable = float(st.session_state.taxable_balance)
    traditional = float(st.session_state.traditional_balance)
    roth = float(st.session_state.roth_balance)

    strategies = [
        simulate_strategy("Taxable → Traditional → Roth", annual_spending, taxable, traditional, roth, ["taxable", "traditional", "roth"]),
        simulate_strategy("Traditional → Taxable → Roth", annual_spending, taxable, traditional, roth, ["traditional", "taxable", "roth"]),
        simulate_strategy("Taxable → Roth → Traditional", annual_spending, taxable, traditional, roth, ["taxable", "roth", "traditional"]),
    ]
    df = pd.DataFrame(strategies)
    best = df.loc[df["estimated_tax"].idxmin()]

    c1, c2, c3 = st.columns(3)
    c1.metric(labels["lowest_tax"], best["strategy"])
    c2.metric(labels["tax_cost"], format_currency(best["estimated_tax"]))
    c3.metric(labels["unfunded_need"], format_currency(best["unfunded_need"]))

    render_note(
        f"In this simple one-year comparison, **{best['strategy']}** produces the lowest estimated tax bill at {format_currency(best['estimated_tax'])}."
        if not zh
        else f"在这个简单的一年期对比中，**{best['strategy']}** 的估算税负最低，为 {format_currency(best['estimated_tax'])}。"
    )
    st.caption(
        f"Using shared assumptions: spending need {format_currency(annual_spending)}, taxable {format_currency(taxable)}, traditional {format_currency(traditional)}, Roth {format_currency(roth)}."
        if not zh
        else f"使用共享假设：支出需求 {format_currency(annual_spending)}，应税账户 {format_currency(taxable)}，traditional {format_currency(traditional)}，Roth {format_currency(roth)}。"
    )

    st.subheader(labels["strategy_comparison"])
    st.dataframe(df, use_container_width=True)

    tax_chart = df.set_index("strategy")[["estimated_tax"]]
    balance_chart = df.set_index("strategy")[["ending_taxable", "ending_traditional", "ending_roth"]]
    left, right = st.columns(2)
    with left:
        st.subheader(labels["estimated_taxes"])
        st.bar_chart(tax_chart)
    with right:
        st.subheader(labels["balances_after_year"])
        st.bar_chart(balance_chart)

    st.caption(labels["caption"])
