#!/usr/bin/env python3
from __future__ import annotations

import streamlit as st

from app_i18n import section
from app_ui import render_header, render_note


REPO_URL = "https://github.com/lurrnet/retirement-planning"
ISSUES_URL = f"{REPO_URL}/issues"


def render_page() -> None:
    labels = section("feedback")
    render_header(labels["title"], labels["subtitle"])

    st.markdown(labels["body"])
    render_note(labels["note"])

    st.markdown(f"- [{labels['repo_link']}]({REPO_URL})")
    st.markdown(f"- [{labels['issues_link']}]({ISSUES_URL})")

