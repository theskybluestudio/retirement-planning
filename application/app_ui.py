#!/usr/bin/env python3
from __future__ import annotations

import streamlit as st


ACCENT = "#0f766e"


PAGE_GROUPS = {
    "Core planners": [
        "Home",
        "RMD / Roth Conversion Strategy",
        "Retirement Readiness",
        "Social Security Optimizer",
        "Medicare IRMAA",
        "Sequence Risk Visualizer",
    ],
    "Income & withdrawals": [
        "Safe Withdrawal Guardrails",
        "Withdrawal Order",
        "Spending Smile Planner",
        "Savings Rate / Catch-Up",
    ],
    "Reference": ["Roadmap"],
}


def inject_css() -> None:
    st.markdown(
        f"""
        <style>
        .block-container {{
            padding-top: 1.25rem;
            padding-bottom: 2rem;
        }}
        .mesh-hero {{
            padding: 1.1rem 1.25rem;
            border: 1px solid rgba(15, 118, 110, 0.18);
            border-radius: 16px;
            background: linear-gradient(135deg, rgba(15,118,110,0.10), rgba(14,165,233,0.05));
            margin-bottom: 1rem;
        }}
        .mesh-hero h1 {{
            margin: 0 0 0.35rem 0;
            font-size: 2rem;
        }}
        .mesh-hero p {{
            margin: 0;
            color: rgba(250,250,250,0.82);
        }}
        .mesh-note {{
            border-left: 4px solid {ACCENT};
            padding: 0.85rem 1rem;
            background: rgba(15,118,110,0.06);
            border-radius: 10px;
            margin: 0.75rem 0 1rem 0;
        }}
        .mesh-small {{
            color: rgba(250,250,250,0.70);
            font-size: 0.92rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )



def render_header(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="mesh-hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )



def render_note(text: str) -> None:
    st.markdown(f'<div class="mesh-note">{text}</div>', unsafe_allow_html=True)



def render_explainer(label: str, body: str, *, expanded: bool = False) -> None:
    with st.expander(label, expanded=expanded):
        st.markdown(body)



def format_currency(value: float) -> str:
    return f"${value:,.0f}"
