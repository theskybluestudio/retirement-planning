#!/usr/bin/env python3
from __future__ import annotations

import streamlit as st

from app_pages_home import render_page as render_home
from app_pages_irmaa import render_page as render_irmaa
from app_pages_retirement_readiness import render_page as render_readiness
from app_pages_rmd_strategy import render_page as render_rmd_strategy
from app_pages_roadmap import render_page as render_roadmap
from app_pages_sequence_risk import render_page as render_sequence_risk
from app_pages_social_security import render_page as render_social_security

PAGES = {
    "Home": render_home,
    "RMD / Roth Conversion Strategy": render_rmd_strategy,
    "Retirement Readiness": render_readiness,
    "Social Security Optimizer": render_social_security,
    "Medicare IRMAA": render_irmaa,
    "Sequence Risk Visualizer": render_sequence_risk,
    "Roadmap": render_roadmap,
}


def main() -> None:
    st.set_page_config(page_title="Retirement Planning Suite", layout="wide")

    with st.sidebar:
        st.title("Retirement Planning")
        st.caption("A multi-tool planning workspace")
        page_name = st.radio("Choose an app", list(PAGES.keys()))
        st.divider()
        st.caption("Educational planning tools only — not tax, legal, or investment advice.")

    PAGES[page_name]()


if __name__ == "__main__":
    main()
