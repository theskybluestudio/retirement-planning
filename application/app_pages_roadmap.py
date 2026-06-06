#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import streamlit as st


ROADMAP_PATH = Path(__file__).resolve().parents[1] / "ROADMAP.md"



def render_page() -> None:
    st.title("Roadmap")
    st.caption("Planned calculators and build order for the retirement planning suite.")

    if ROADMAP_PATH.exists():
        st.markdown(ROADMAP_PATH.read_text())
    else:
        st.warning("ROADMAP.md was not found.")
