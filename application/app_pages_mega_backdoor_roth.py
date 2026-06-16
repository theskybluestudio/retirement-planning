#!/usr/bin/env python3
from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from app_i18n import section, tooltip
from app_state import render_shared_assumptions_panel
from app_ui import format_currency, format_dataframe, money_input, render_explainer, render_header, render_note


LIMITS_BY_YEAR = {
    2024: {
        "elective_deferral": 23_000.0,
        "annual_additions": 69_000.0,
        "catch_up_50": 7_500.0,
        "catch_up_60_63": 7_500.0,
        "compensation_cap": 345_000.0,
    },
    2025: {
        "elective_deferral": 23_500.0,
        "annual_additions": 70_000.0,
        "catch_up_50": 7_500.0,
        "catch_up_60_63": 7_500.0,
        "compensation_cap": 350_000.0,
    },
    2026: {
        "elective_deferral": 24_500.0,
        "annual_additions": 72_000.0,
        "catch_up_50": 8_000.0,
        "catch_up_60_63": 11_250.0,
        "compensation_cap": 360_000.0,
    },
}


def _current_supported_year() -> int:
    year = date.today().year
    return year if year in LIMITS_BY_YEAR else max(LIMITS_BY_YEAR)


def _default_catch_up_limit(age: int, year: int) -> float:
    limits = LIMITS_BY_YEAR[year]
    if 60 <= age <= 63:
        return limits["catch_up_60_63"]
    if age >= 50:
        return limits["catch_up_50"]
    return 0.0


def render_page() -> None:
    zh = st.session_state.get("language", "en") == "zh"
    common = section("common")
    assumptions = section("assumptions")
    labels = section("mega_backdoor")
    render_header(labels["title"], labels["subtitle"])
    render_explainer(common["about_tool"], labels["about_body"])

    render_shared_assumptions_panel(common, assumptions)

    default_year = int(st.session_state.get("mega_tax_year", _current_supported_year()))
    age = int(st.session_state.current_age)

    with st.sidebar:
        st.divider()
        st.header(common["page_specific_inputs"])
        tax_year = st.selectbox(labels["tax_year"], options=sorted(LIMITS_BY_YEAR.keys()), index=sorted(LIMITS_BY_YEAR.keys()).index(default_year), key="mega_tax_year", help=tooltip("mega_backdoor", "tax_year"))
        limits = LIMITS_BY_YEAR[int(tax_year)]
        default_catch_up = _default_catch_up_limit(age, int(tax_year))
        st.session_state["mega_catch_up_limit"] = default_catch_up
        compensation = money_input(labels["eligible_compensation"], min_value=0.0, value=float(st.session_state.get("mega_compensation", 200_000.0)), key="mega_compensation", help=tooltip("mega_backdoor", "eligible_compensation"))
        employee_deferrals = money_input(labels["employee_deferrals"], min_value=0.0, value=float(st.session_state.get("mega_employee_deferrals", st.session_state.annual_contribution)), key="mega_employee_deferrals", help=tooltip("mega_backdoor", "employee_deferrals"))
        employer_contributions = money_input(labels["employer_contributions"], min_value=0.0, value=float(st.session_state.get("mega_employer_contributions", 0.0)), key="mega_employer_contributions", help=tooltip("mega_backdoor", "employer_contributions"))
        after_tax_already = money_input(labels["after_tax_already"], min_value=0.0, value=float(st.session_state.get("mega_after_tax_already", 0.0)), key="mega_after_tax_already", help=tooltip("mega_backdoor", "after_tax_already"))
        catch_up_limit = money_input(labels["catch_up_limit"], min_value=0.0, value=default_catch_up, key="mega_catch_up_limit", help=tooltip("mega_backdoor", "catch_up_limit"))
        plan_after_tax_cap = money_input(labels["plan_after_tax_cap"], min_value=0.0, value=float(st.session_state.get("mega_plan_after_tax_cap", 0.0)), key="mega_plan_after_tax_cap", help=tooltip("mega_backdoor", "plan_after_tax_cap"))
        allows_after_tax = st.checkbox(labels["allows_after_tax"], value=bool(st.session_state.get("mega_allows_after_tax", True)), key="mega_allows_after_tax", help=tooltip("mega_backdoor", "allows_after_tax"))
        allows_conversion = st.checkbox(labels["allows_conversion"], value=bool(st.session_state.get("mega_allows_conversion", True)), key="mega_allows_conversion", help=tooltip("mega_backdoor", "allows_conversion"))

    compensation_used = min(float(compensation), float(limits["compensation_cap"]))
    annual_additions_cap = min(float(limits["annual_additions"]), compensation_used)
    counted_deferrals = min(float(employee_deferrals), float(limits["elective_deferral"]))
    catch_up_used = min(max(0.0, float(employee_deferrals) - counted_deferrals), float(catch_up_limit))
    excess_deferrals = max(0.0, float(employee_deferrals) - counted_deferrals - catch_up_used)
    raw_mega_room = max(0.0, annual_additions_cap - counted_deferrals - float(employer_contributions))
    remaining_mega_room = max(0.0, raw_mega_room - float(after_tax_already))
    if float(plan_after_tax_cap) > 0:
        remaining_mega_room = min(remaining_mega_room, max(0.0, float(plan_after_tax_cap) - float(after_tax_already)))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(labels["available_after_tax"], format_currency(remaining_mega_room))
    c2.metric(labels["annual_additions_cap"], format_currency(annual_additions_cap))
    c3.metric(labels["counted_deferrals"], format_currency(counted_deferrals))
    c4.metric(labels["employer_total"], format_currency(employer_contributions))

    note_text = (
        f"Based on {tax_year} limits, this estimate leaves about {format_currency(remaining_mega_room)} of remaining after-tax 401(k) room for a Mega Backdoor Roth, after counting {format_currency(counted_deferrals)} of employee deferrals, {format_currency(employer_contributions)} of employer contributions, and {format_currency(after_tax_already)} already contributed after-tax."
        if not zh
        else f"按 {tax_year} 年规则估算，在计入员工递延 {format_currency(counted_deferrals)}、雇主供款 {format_currency(employer_contributions)} 和已完成税后供款 {format_currency(after_tax_already)} 后，当前大约还剩 {format_currency(remaining_mega_room)} 的税后 401(k) 空间可用于 Mega Backdoor Roth。"
    )
    render_note(note_text)
    st.caption(
        f"The 415(c) annual-additions cap is limited to the lesser of plan compensation and the IRS dollar limit. Catch-up contributions are tracked separately and do not reduce the Mega Backdoor room under this simplified estimate."
        if not zh
        else "415(c) 年度总供款上限取“合格薪酬”和 IRS 金额上限中的较小值。这个简化模型会把 catch-up 单独处理，不把它算进 Mega Backdoor Roth 的可用空间。"
    )

    detail = pd.DataFrame(
        [
            {"item": labels["detail_comp_cap"], "amount": compensation_used},
            {"item": labels["detail_annual_additions_limit"], "amount": float(limits["annual_additions"])},
            {"item": labels["detail_effective_415c_limit"], "amount": annual_additions_cap},
            {"item": labels["detail_elective_limit"], "amount": float(limits["elective_deferral"])},
            {"item": labels["detail_counted_deferrals"], "amount": counted_deferrals},
            {"item": labels["detail_employer_contributions"], "amount": float(employer_contributions)},
            {"item": labels["detail_raw_room"], "amount": raw_mega_room},
            {"item": labels["detail_after_tax_already"], "amount": float(after_tax_already)},
            {"item": labels["detail_remaining_room"], "amount": remaining_mega_room},
        ]
    )

    left, right = st.columns([1.2, 1.0])
    with left:
        st.subheader(labels["calculation_breakdown"])
        st.dataframe(format_dataframe(detail, currency_columns=["amount"]), use_container_width=True, hide_index=True)
    with right:
        st.subheader(labels["quick_checks"])
        st.write(f"{labels['catch_up_used']}: **{format_currency(catch_up_used)}**")
        st.write(f"{labels['compensation_cap']}: **{format_currency(limits['compensation_cap'])}**")
        if excess_deferrals > 0:
            st.warning(
                f"Employee deferrals exceed the elective-deferral plus catch-up limits by about {format_currency(excess_deferrals)}."
                if not zh
                else f"员工递延供款超过 elective deferral 加 catch-up 上限，超出约 {format_currency(excess_deferrals)}。"
            )
        if not allows_after_tax:
            st.error(labels["after_tax_not_available"])
        elif not allows_conversion:
            st.info(labels["conversion_not_available"])
        else:
            st.success(labels["looks_executable"])

    st.caption(labels["caption"])
