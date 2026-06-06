#!/usr/bin/env python3
from __future__ import annotations

import streamlit as st


TOOLS = [
    ("RMD / Roth Conversion Strategy", "Compare conversion vs no-conversion paths and estimate future RMD impact."),
    ("Retirement Readiness", "Estimate whether projected savings and income cover retirement spending."),
    ("Social Security Optimizer", "Compare claiming ages and lifetime benefits with break-even views."),
    ("Medicare IRMAA", "See whether income events trigger IRMAA surcharges and how much room remains."),
    ("Sequence Risk Visualizer", "Show how early bad returns can change retirement outcomes even with the same average return."),
]



def render_page() -> None:
    st.title("Retirement Planning Suite")
    st.write(
        "Use the sidebar to move between focused retirement planning tools. "
        "The suite is set up so each calculator can grow independently while still feeling like one app."
    )

    col1, col2 = st.columns([1.2, 1.0])
    with col1:
        st.subheader("Included apps")
        for name, description in TOOLS:
            st.markdown(f"- **{name}** — {description}")

    with col2:
        st.subheader("Build direction")
        st.markdown(
            "- Shared sidebar navigation\n"
            "- One app per planning question\n"
            "- Room to add more calculators over time\n"
            "- Reusable assumptions and visuals later"
        )

    st.info(
        "Right now the most complete page is the RMD / Roth Conversion Strategy tool. "
        "The others are lightweight MVPs so the suite structure is in place."
    )
