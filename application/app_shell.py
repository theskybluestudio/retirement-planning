#!/usr/bin/env python3
from __future__ import annotations

import streamlit as st
import st_cookie

from app_i18n import init_i18n, render_language_switch
from app_state import init_session_state
from app_ui import inject_css



def setup_page(page_title: str) -> None:
    st.set_page_config(page_title=page_title, layout="wide")
    init_session_state()
    st_cookie.apply()
    init_i18n()
    inject_css()
    render_language_switch()
