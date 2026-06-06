#!/usr/bin/env python3
from __future__ import annotations

import pandas as pd
import streamlit as st

from roth_conversion_engine import IRMAA_2026



def render_page() -> None:
    st.title("Medicare IRMAA")
    st.caption("Check whether income events push modified AGI into a higher IRMAA tier.")

    with st.sidebar:
        st.header("IRMAA inputs")
        filing_status = st.selectbox("Filing status", options=["mfj", "single"], index=0, key="irmaa_filing_status")
        base_magi = st.number_input("Base MAGI", min_value=0.0, value=180_000.0, step=1_000.0, key="irmaa_base_magi")
        extra_income = st.number_input("Extra income event", min_value=0.0, value=25_000.0, step=1_000.0, key="irmaa_extra_income")

    total_magi = base_magi + extra_income
    thresholds = IRMAA_2026[filing_status]

    surcharge = 0.0
    current_threshold = thresholds[-1][0]
    room_to_next = 0.0
    for idx, (threshold, annual_surcharge) in enumerate(thresholds):
        if total_magi <= threshold:
            surcharge = annual_surcharge
            current_threshold = threshold
            if idx > 0:
                room_to_next = max(0.0, threshold - total_magi)
            else:
                room_to_next = max(0.0, threshold - total_magi)
            break

    table = pd.DataFrame(
        [{"magi_threshold": threshold, "annual_irmaa_surcharge": surcharge_value} for threshold, surcharge_value in thresholds]
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Total MAGI", f"${total_magi:,.0f}")
    c2.metric("Annual IRMAA surcharge", f"${surcharge:,.0f}")
    c3.metric("Room to current tier ceiling", f"${room_to_next:,.0f}")

    st.subheader("2026 thresholds")
    st.dataframe(table, use_container_width=True)

    if extra_income > 0:
        st.info("Useful for modeling Roth conversions, capital gains, bonus income, or large one-year distributions.")

    st.caption("This page uses the same 2026 threshold table as the conversion model. Real Medicare billing uses lookback rules and other details.")
