#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import streamlit as st

from app_i18n import section
from app_ui import render_header, render_icon_link_button, render_note


REPO_URL = "https://github.com/theskybluestudio/retirement-planning"
ISSUES_URL = f"{REPO_URL}/issues"
PAYPAL_URL = "https://www.paypal.com/donate/?hosted_button_id=N8E2PJ3ET7Q6N"
PAYPAL_ICON = Path(__file__).parent / "assets" / "paypal.svg"


def render_page() -> None:
    labels = section("feedback")
    render_header(labels["title"], labels["subtitle"])

    st.subheader(labels["github_section"])
    st.markdown(labels["body"])
    render_note(labels["note"])
    st.markdown(f"- [{labels['repo_link']}]({REPO_URL})")
    st.markdown(f"- [{labels['issues_link']}]({ISSUES_URL})")

    st.markdown("---")
    st.subheader(labels["support_section"])
    st.markdown(labels["support_body"])
    render_icon_link_button(labels["paypal_link"], PAYPAL_URL, str(PAYPAL_ICON))

