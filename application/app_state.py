#!/usr/bin/env python3
from __future__ import annotations

import json

import streamlit as st

from app_ui import money_input, percent_input


SHARED_DEFAULTS = {
    "current_age": 50,
    "retirement_age": 60,
    "life_expectancy": 90,
    "filing_status": "mfj",
    "traditional_balance": 1_000_000.0,
    "roth_balance": 500_000.0,
    "taxable_balance": 500_000.0,
    "annual_contribution": 30_000.0,
    "annual_return": 0.06,
    "inflation": 0.025,
    "state_tax_rate": 0.0,
    "annual_retirement_spending": 120_000.0,
    "annual_social_security_benefit": 36_000.0,
    "social_security_claim_age": 67,
    "annual_pension_income": 0.0,
    "annual_other_income": 0.0,
    "has_roth_ira": True,
    "has_taxable_brokerage": True,
    "social_security_fra_benefit": 36_000.0,
}


CLAIMING_FACTORS = {
    62: 0.70,
    63: 0.75,
    64: 0.80,
    65: 0.8667,
    66: 0.9333,
    67: 1.00,
    68: 1.08,
    69: 1.16,
    70: 1.24,
}


PAGE_DEFAULTS = {
    "rmd_target_bracket": "24%",
    "rmd_use_aca_model": True,
    "rmd_use_irmaa_model": True,
    "readiness_withdrawal_rate": 0.04,
    "ss_longevity_age": 90,
    "ss_selected_claim_age": 67,
    "irmaa_extra_income": 25_000.0,
    "guard_floor_rate": 0.03,
    "guard_ceiling_rate": 0.05,
    "smile_go_go_years": 10,
    "smile_go_go_multiplier": 1.15,
    "smile_slow_go_years": 10,
    "smile_slow_go_multiplier": 0.95,
    "smile_no_go_years": 10,
    "smile_no_go_multiplier": 0.80,
    "smile_healthcare_step_up": 15_000.0,
    "save_target_portfolio": 2_500_000.0,
}


ALL_DEFAULTS = SHARED_DEFAULTS | PAGE_DEFAULTS



def _persist_key(key: str) -> str:
    return f"_persist_{key}"


def shared_widget_key(key: str) -> str:
    return f"_widget_{key}"


def prime_shared_widget(key: str) -> None:
    st.session_state[shared_widget_key(key)] = st.session_state.get(key, ALL_DEFAULTS[key])


def estimate_annual_social_security_benefit(fra_benefit: float, claim_age: int) -> float:
    factor = CLAIMING_FACTORS.get(int(claim_age))
    if factor is None:
        if claim_age < 62:
            factor = CLAIMING_FACTORS[62]
        elif claim_age > 70:
            factor = CLAIMING_FACTORS[70]
        else:
            factor = CLAIMING_FACTORS[67]
    return max(0.0, float(fra_benefit) * float(factor))


def sync_estimated_social_security_benefit() -> None:
    fra_benefit = float(st.session_state.get("social_security_fra_benefit", SHARED_DEFAULTS["social_security_fra_benefit"]))
    claim_age = int(st.session_state.get("social_security_claim_age", SHARED_DEFAULTS["social_security_claim_age"]))
    estimated = estimate_annual_social_security_benefit(fra_benefit, claim_age)
    st.session_state["annual_social_security_benefit"] = estimated
    st.session_state[_persist_key("annual_social_security_benefit")] = estimated
    st.session_state[shared_widget_key("annual_social_security_benefit")] = estimated


def commit_shared_widget(key: str) -> None:
    value = st.session_state[shared_widget_key(key)]
    st.session_state[key] = value
    st.session_state[_persist_key(key)] = value
    if key in {"social_security_fra_benefit", "social_security_claim_age"}:
        sync_estimated_social_security_benefit()



def _sync_persistent_defaults() -> None:
    for key, default in ALL_DEFAULTS.items():
        persist_key = _persist_key(key)
        if key in st.session_state:
            st.session_state[persist_key] = st.session_state[key]
        elif persist_key in st.session_state:
            st.session_state[key] = st.session_state[persist_key]
        else:
            st.session_state[key] = default
            st.session_state[persist_key] = default



def init_session_state() -> None:
    if not st.session_state.get("_initialized_defaults"):
        reset_assumptions()
        st.session_state._initialized_defaults = True
    _sync_persistent_defaults()
    sync_estimated_social_security_benefit()



def reset_assumptions() -> None:
    for key, value in ALL_DEFAULTS.items():
        st.session_state[key] = value
        st.session_state[_persist_key(key)] = value
        st.session_state[shared_widget_key(key)] = value
    sync_estimated_social_security_benefit()



def export_assumptions() -> str:
    payload = {key: st.session_state.get(key, default) for key, default in ALL_DEFAULTS.items()}
    return json.dumps(payload, indent=2, sort_keys=True)



def import_assumptions(json_text: str) -> None:
    data = json.loads(json_text)
    if not isinstance(data, dict):
        raise ValueError("Assumptions JSON must be an object.")

    for key, default in ALL_DEFAULTS.items():
        if key not in data:
            continue
        incoming = data[key]
        if isinstance(default, bool):
            st.session_state[key] = bool(incoming)
        elif isinstance(default, int) and not isinstance(default, bool):
            st.session_state[key] = int(incoming)
        elif isinstance(default, float):
            st.session_state[key] = float(incoming)
        else:
            st.session_state[key] = incoming
        st.session_state[_persist_key(key)] = st.session_state[key]
        st.session_state[shared_widget_key(key)] = st.session_state[key]
    sync_estimated_social_security_benefit()



def render_shared_assumptions_panel(common_labels: dict, assumptions_labels: dict, *, expanded: bool = False) -> None:
    shared_keys = [
        "current_age", "retirement_age", "life_expectancy", "filing_status",
        "traditional_balance", "roth_balance", "taxable_balance",
        "annual_contribution", "annual_retirement_spending", "annual_social_security_benefit", "social_security_fra_benefit",
        "social_security_claim_age", "annual_pension_income", "annual_other_income", "annual_return", "inflation", "state_tax_rate",
    ]
    for key in shared_keys:
        prime_shared_widget(key)

    with st.expander(common_labels["shared_inputs"], expanded=expanded):
        left, right = st.columns(2)
        with left:
            st.subheader(assumptions_labels["personal"])
            st.number_input(assumptions_labels["current_age"], min_value=18, max_value=80, key=shared_widget_key("current_age"), on_change=commit_shared_widget, args=("current_age",))
            st.number_input(assumptions_labels["retirement_age"], min_value=25, max_value=80, key=shared_widget_key("retirement_age"), on_change=commit_shared_widget, args=("retirement_age",))
            st.number_input(assumptions_labels["life_expectancy"], min_value=70, max_value=105, key=shared_widget_key("life_expectancy"), on_change=commit_shared_widget, args=("life_expectancy",))
            st.selectbox(assumptions_labels["filing_status"], options=["mfj", "single"], key=shared_widget_key("filing_status"), on_change=commit_shared_widget, args=("filing_status",))

            st.subheader(assumptions_labels["accounts"])
            money_input(assumptions_labels["traditional_balance"], min_value=0.0, key=shared_widget_key("traditional_balance"), on_change=commit_shared_widget, args=("traditional_balance",))
            money_input(assumptions_labels["roth_balance"], min_value=0.0, key=shared_widget_key("roth_balance"), on_change=commit_shared_widget, args=("roth_balance",))
            money_input(assumptions_labels["taxable_balance"], min_value=0.0, key=shared_widget_key("taxable_balance"), on_change=commit_shared_widget, args=("taxable_balance",))

        with right:
            st.subheader(assumptions_labels["cash_flow"])
            money_input(assumptions_labels["annual_contribution"], min_value=0.0, key=shared_widget_key("annual_contribution"), on_change=commit_shared_widget, args=("annual_contribution",))
            money_input(assumptions_labels["annual_retirement_spending"], min_value=0.0, key=shared_widget_key("annual_retirement_spending"), on_change=commit_shared_widget, args=("annual_retirement_spending",))
            money_input(assumptions_labels["annual_ss_benefit_fra"], min_value=0.0, key=shared_widget_key("social_security_fra_benefit"), on_change=commit_shared_widget, args=("social_security_fra_benefit",))
            st.number_input(assumptions_labels["ss_claim_age"], min_value=62, max_value=75, key=shared_widget_key("social_security_claim_age"), on_change=commit_shared_widget, args=("social_security_claim_age",))
            sync_estimated_social_security_benefit()
            st.text_input(assumptions_labels["annual_ss_benefit"], value=f"{st.session_state.annual_social_security_benefit:,.0f}", disabled=True)
            money_input(assumptions_labels["annual_pension_income"], min_value=0.0, key=shared_widget_key("annual_pension_income"), on_change=commit_shared_widget, args=("annual_pension_income",))
            money_input(assumptions_labels["annual_other_income"], min_value=0.0, key=shared_widget_key("annual_other_income"), on_change=commit_shared_widget, args=("annual_other_income",))

            st.subheader(assumptions_labels["market_tax"])
            percent_input(assumptions_labels["annual_return"], min_value=0.0, max_value=0.20, key=shared_widget_key("annual_return"), on_change=commit_shared_widget, args=("annual_return",))
            percent_input(assumptions_labels["inflation"], min_value=0.0, max_value=0.10, key=shared_widget_key("inflation"), on_change=commit_shared_widget, args=("inflation",))
            percent_input(assumptions_labels["state_tax_rate"], min_value=0.0, max_value=0.20, key=shared_widget_key("state_tax_rate"), on_change=commit_shared_widget, args=("state_tax_rate",))



def validate_assumptions() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    current_age = int(st.session_state.current_age)
    retirement_age = int(st.session_state.retirement_age)
    life_expectancy = int(st.session_state.life_expectancy)
    claim_age = int(st.session_state.social_security_claim_age)

    zh = st.session_state.get("language", "en") == "zh"

    if retirement_age <= current_age:
        errors.append("退休年龄必须大于当前年龄。" if zh else "Retirement age must be greater than current age.")
    if life_expectancy <= retirement_age:
        errors.append("预期寿命必须大于退休年龄。" if zh else "Life expectancy must be greater than retirement age.")
    if claim_age < 62 or claim_age > 75:
        errors.append("社保领取年龄必须在 62 到 75 岁之间。" if zh else "Social Security claim age must stay between 62 and 75.")
    if claim_age > life_expectancy:
        errors.append("社保领取年龄不能晚于预期寿命。" if zh else "Social Security claim age cannot be later than life expectancy.")

    if float(st.session_state.annual_return) <= float(st.session_state.inflation):
        warnings.append("年化收益率小于或等于通胀率；长期实际增长可能偏弱。" if zh else "Annual return is less than or equal to inflation; long-term real growth may be weak.")
    if float(st.session_state.annual_retirement_spending) > get_fixed_retirement_income() + get_total_portfolio() * 0.06:
        warnings.append("计划退休支出相对当前资产和固定收入看起来偏高。" if zh else "Planned retirement spending looks high relative to current assets and fixed income.")
    return errors, warnings



def get_total_portfolio() -> float:
    return float(st.session_state.traditional_balance) + float(st.session_state.roth_balance) + float(st.session_state.taxable_balance)



def get_fixed_retirement_income() -> float:
    return float(st.session_state.annual_social_security_benefit) + float(st.session_state.annual_pension_income)
