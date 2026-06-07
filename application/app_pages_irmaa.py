#!/usr/bin/env python3
from __future__ import annotations

import pandas as pd
import streamlit as st

from app_i18n import section
from app_ui import format_currency, render_header, render_note
from roth_conversion_engine import IRMAA_2026



def render_page() -> None:
    zh = st.session_state.get("language", "en") == "zh"
    common = section("common")
    labels = section("irmaa")
    render_header(labels["title"], labels["subtitle"])

    with st.sidebar:
        st.header(common["page_specific_inputs"])
        extra_income = st.number_input(labels["extra_income"], min_value=0.0, value=25_000.0, step=1_000.0, key="irmaa_extra_income")

    filing_status = str(st.session_state.filing_status)
    base_magi = (
        float(st.session_state.annual_other_income)
        + float(st.session_state.annual_pension_income)
        + float(st.session_state.annual_social_security_benefit)
    )

    total_magi = base_magi + extra_income
    thresholds = IRMAA_2026[filing_status]

    surcharge = 0.0
    current_ceiling = thresholds[-1][0]
    next_threshold = None
    for threshold, annual_surcharge in thresholds:
        if total_magi <= threshold:
            surcharge = annual_surcharge
            current_ceiling = threshold
            next_threshold = threshold
            break

    prior_threshold = 0.0
    for threshold, annual_surcharge in thresholds:
        if total_magi > threshold:
            prior_threshold = threshold
            continue
        break

    room_to_ceiling = max(0.0, current_ceiling - total_magi)
    table = pd.DataFrame(
        [{"magi_threshold": threshold, "annual_irmaa_surcharge": surcharge_value} for threshold, surcharge_value in thresholds]
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(labels["total_magi"], format_currency(total_magi))
    c2.metric(labels["annual_surcharge"], format_currency(surcharge))
    c3.metric(labels["room"], format_currency(room_to_ceiling))
    c4.metric(labels["modeled_extra"], format_currency(extra_income))

    render_note(
        f"With {format_currency(base_magi)} of base MAGI and {format_currency(extra_income)} of extra income, the modeled MAGI is {format_currency(total_magi)}. That lands in a tier with an annual IRMAA surcharge of {format_currency(surcharge)}."
        if not zh
        else f"在基础 MAGI 为 {format_currency(base_magi)}、额外收入为 {format_currency(extra_income)} 的情况下，模型中的总 MAGI 为 {format_currency(total_magi)}，对应的年度 IRMAA 附加费为 {format_currency(surcharge)}。"
    )
    st.caption(
        f"Using shared assumptions: filing status {filing_status.upper()}, annual other income {format_currency(float(st.session_state.annual_other_income))}, pension {format_currency(float(st.session_state.annual_pension_income))}, and Social Security {format_currency(float(st.session_state.annual_social_security_benefit))} to build the base MAGI."
        if not zh
        else f"使用共享假设：报税身份 {filing_status.upper()}，年度其他收入 {format_currency(float(st.session_state.annual_other_income))}，养老金 {format_currency(float(st.session_state.annual_pension_income))}，以及社保收入 {format_currency(float(st.session_state.annual_social_security_benefit))} 来构造基础 MAGI。"
    )

    chart_col, detail_col = st.columns([1.2, 1.0])
    with chart_col:
        st.subheader(labels["thresholds"])
        st.dataframe(table, use_container_width=True)
    with detail_col:
        st.subheader(labels["quick_read"])
        if extra_income > 0:
            st.info("Useful for Roth conversions, capital gains, bonus income, or large one-year distributions." if not zh else "适合用于模拟 Roth 转换、资本利得、奖金收入或大额一次性分配。")
        st.write(f"Current tier floor: **{format_currency(prior_threshold)}**" if not zh else f"当前档位下限：**{format_currency(prior_threshold)}**")
        st.write(f"Current tier ceiling: **{format_currency(current_ceiling)}**" if not zh else f"当前档位上限：**{format_currency(current_ceiling)}**")
        if next_threshold is not None:
            st.write(f"Remaining headroom: **{format_currency(room_to_ceiling)}**" if not zh else f"剩余空间：**{format_currency(room_to_ceiling)}**")

    st.caption(labels["caption"])
