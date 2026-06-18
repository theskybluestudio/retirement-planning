#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import base64
import html

import streamlit as st


ACCENT = "#0f766e"
ASSETS_DIR = Path(__file__).parent / "assets"


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
            padding-bottom: 5.5rem;
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
        .mesh-link-button {{
            display: inline-flex;
            align-items: center;
            gap: 0.55rem;
            padding: 0.7rem 1rem;
            border-radius: 999px;
            background: linear-gradient(135deg, #0070ba, #003087);
            color: white !important;
            text-decoration: none !important;
            font-weight: 600;
            border: 1px solid rgba(255,255,255,0.10);
            box-shadow: 0 6px 18px rgba(0,48,135,0.22);
            margin: 0.35rem 0 0.5rem 0;
        }}
        .mesh-link-button:hover {{
            filter: brightness(1.05);
            text-decoration: none !important;
        }}
        .mesh-link-button img {{
            width: 20px;
            height: 20px;
            display: block;
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



def render_icon_link_button(label: str, url: str, icon_path: str, *, css_class: str = "mesh-link-button") -> None:
    icon_bytes = Path(icon_path).read_bytes()
    icon_b64 = base64.b64encode(icon_bytes).decode("ascii")
    st.markdown(
        f'<a class="{css_class}" href="{url}" target="_blank" rel="noopener noreferrer"><img src="data:image/svg+xml;base64,{icon_b64}" alt="">{label}</a>',
        unsafe_allow_html=True,
    )



def render_explainer(label: str, body: str, *, expanded: bool = False) -> None:
    with st.expander(label, expanded=expanded):
        st.markdown(body)



def render_global_footer(text: str) -> None:
    st.markdown(
        f"""
        <div class="mesh-global-footer">{html.escape(text)}</div>
        <style>
        .mesh-global-footer {{
            position: fixed;
            left: 0;
            right: 0;
            bottom: 0;
            z-index: 999;
            padding: 0.7rem 1rem 0.85rem 1rem;
            text-align: center;
            font-size: 0.84rem;
            color: rgba(250,250,250,0.78);
            background: rgba(10, 14, 20, 0.92);
            border-top: 1px solid rgba(255,255,255,0.08);
            backdrop-filter: blur(8px);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )



def _money_text_key(key: str) -> str:
    return f"{key}__money_text"


def _parse_money_text(value: str) -> float:
    cleaned = value.replace("$", "").replace(",", "").strip()
    if cleaned in {"", ".", "-", "-."}:
        return 0.0
    return float(cleaned)


def _percent_text_key(key: str) -> str:
    return f"{key}__percent_text"


def _parse_percent_text(value: str) -> float:
    cleaned = value.replace("%", "").replace(",", "").strip()
    if cleaned in {"", ".", "-", "-."}:
        return 0.0
    return float(cleaned) / 100.0


def money_input(
    label: str,
    *,
    key: str,
    min_value: float = 0.0,
    value: float | None = None,
    help: str | None = None,
    on_change=None,
    args: tuple = (),
) -> float:
    numeric_value = float(st.session_state.get(key, value if value is not None else min_value))
    text_key = _money_text_key(key)
    st.session_state[text_key] = f"{numeric_value:,.0f}"

    def _handle_change() -> None:
        try:
            parsed = max(min_value, _parse_money_text(st.session_state[text_key]))
        except ValueError:
            parsed = numeric_value
        st.session_state[key] = float(parsed)
        st.session_state[text_key] = f"{parsed:,.0f}"
        if on_change is not None:
            on_change(*args)

    st.text_input(label, key=text_key, on_change=_handle_change, help=help)
    return float(st.session_state.get(key, numeric_value))


def percent_input(
    label: str,
    *,
    key: str,
    min_value: float = 0.0,
    max_value: float | None = None,
    value: float | None = None,
    help: str | None = None,
    on_change=None,
    args: tuple = (),
) -> float:
    numeric_value = float(st.session_state.get(key, value if value is not None else min_value))
    text_key = _percent_text_key(key)
    st.session_state[text_key] = f"{numeric_value * 100:,.2f}%"

    def _handle_change() -> None:
        try:
            parsed = _parse_percent_text(st.session_state[text_key])
        except ValueError:
            parsed = numeric_value
        parsed = max(min_value, parsed)
        if max_value is not None:
            parsed = min(max_value, parsed)
        st.session_state[key] = float(parsed)
        st.session_state[text_key] = f"{parsed * 100:,.2f}%"
        if on_change is not None:
            on_change(*args)

    st.text_input(label, key=text_key, on_change=_handle_change, help=help)
    return float(st.session_state.get(key, numeric_value))


def format_percent(value: float) -> str:
    return f"{float(value) * 100:.2f}%"


def format_dataframe(
    df,
    *,
    currency_columns: list[str] | None = None,
    percent_columns: list[str] | None = None,
    integer_columns: list[str] | None = None,
):
    formatted = df.copy()
    for column in currency_columns or []:
        if column in formatted.columns:
            formatted[column] = formatted[column].map(format_currency)
    for column in percent_columns or []:
        if column in formatted.columns:
            formatted[column] = formatted[column].map(format_percent)
    for column in integer_columns or []:
        if column in formatted.columns:
            formatted[column] = formatted[column].map(lambda value: f"{int(value):,}")
    return formatted


def format_currency(value: float) -> str:
    return f"${value:,.0f}"
