#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import streamlit as st

from app_i18n import section
from app_ui import render_header


ROADMAP_PATH = Path(__file__).resolve().parents[1] / "ROADMAP.md"
ROADMAP_ZH_PATH = Path(__file__).resolve().parents[1] / "ROADMAP.zh.md"



def render_page() -> None:
    zh = st.session_state.get("language", "en") == "zh"
    labels = section("roadmap_page")
    render_header(labels["title"], labels["subtitle"])

    target_path = ROADMAP_ZH_PATH if zh and ROADMAP_ZH_PATH.exists() else ROADMAP_PATH
    if target_path.exists():
        st.markdown(target_path.read_text())
    else:
        st.warning(labels["missing"])
