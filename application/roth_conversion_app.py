#!/usr/bin/env python3
from __future__ import annotations

import streamlit as st

from app_pages_rmd_strategy import render_page


if __name__ == "__main__":
    st.set_page_config(page_title="RMD / Roth Conversion Strategy", layout="wide")
    render_page()
