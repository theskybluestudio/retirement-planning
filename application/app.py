#!/usr/bin/env python3
from __future__ import annotations

import streamlit as st

from app_i18n import section
from app_pages_assumptions import render_page as render_assumptions
from app_pages_home import render_page as render_home
from app_pages_irmaa import render_page as render_irmaa
from app_pages_retirement_readiness import render_page as render_readiness
from app_pages_rmd_strategy import render_page as render_rmd_strategy
from app_pages_safe_withdrawal import render_page as render_safe_withdrawal
from app_pages_savings_rate import render_page as render_savings_rate
from app_pages_sequence_risk import render_page as render_sequence_risk
from app_pages_social_security import render_page as render_social_security
from app_pages_spending_smile import render_page as render_spending_smile
from app_pages_withdrawal_order import render_page as render_withdrawal_order
from app_shell import setup_page


def build_navigation() -> list[st.Page]:
    lang = st.session_state.get("language", "en")
    assumptions = section("assumptions")
    rmd = section("rmd")
    readiness = section("readiness")
    social_security = section("social_security")
    irmaa = section("irmaa")
    sequence = section("sequence")
    safe_withdrawal = section("safe_withdrawal")
    withdrawal_order = section("withdrawal_order")
    spending_smile = section("spending_smile")
    savings_rate = section("savings_rate")

    return [
        st.Page(render_home, title="Home" if lang == "en" else "首页", url_path="home", default=True),
        st.Page(render_assumptions, title=assumptions["title"], url_path="shared-assumptions"),
        st.Page(render_rmd_strategy, title=rmd["title"], url_path="rmd-roth-conversion-strategy"),
        st.Page(render_readiness, title=readiness["title"], url_path="retirement-readiness"),
        st.Page(render_social_security, title=social_security["title"], url_path="social-security-optimizer"),
        st.Page(render_irmaa, title=irmaa["title"], url_path="medicare-irmaa"),
        st.Page(render_sequence_risk, title=sequence["title"], url_path="sequence-risk-visualizer"),
        st.Page(render_safe_withdrawal, title=safe_withdrawal["title"], url_path="safe-withdrawal-guardrails"),
        st.Page(render_withdrawal_order, title=withdrawal_order["title"], url_path="withdrawal-order"),
        st.Page(render_spending_smile, title=spending_smile["title"], url_path="spending-smile-planner"),
        st.Page(render_savings_rate, title=savings_rate["title"], url_path="savings-rate-catch-up"),
    ]



def main() -> None:
    setup_page("Retirement Planning Suite")
    navigation = st.navigation(build_navigation())
    navigation.run()


if __name__ == "__main__":
    main()
