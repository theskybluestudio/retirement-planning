#!/usr/bin/env python3
from __future__ import annotations

import json

import streamlit as st


SHARED_DEFAULTS = {
    "current_age": 45,
    "retirement_age": 65,
    "life_expectancy": 90,
    "filing_status": "mfj",
    "traditional_balance": 1_200_000.0,
    "roth_balance": 300_000.0,
    "taxable_balance": 400_000.0,
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


SCENARIO_PRESETS = {
    "Base": {},
    "Conservative": {
        "annual_return": 0.045,
        "inflation": 0.03,
        "annual_retirement_spending": 130_000.0,
        "readiness_withdrawal_rate": 0.035,
        "rmd_target_bracket": "22%",
    },
    "Aggressive": {
        "annual_return": 0.075,
        "inflation": 0.022,
        "annual_retirement_spending": 115_000.0,
        "readiness_withdrawal_rate": 0.045,
        "rmd_target_bracket": "24%",
    },
    "Early Retirement": {
        "retirement_age": 58,
        "life_expectancy": 95,
        "annual_contribution": 40_000.0,
        "annual_retirement_spending": 110_000.0,
        "social_security_claim_age": 70,
        "ss_longevity_age": 95,
        "readiness_withdrawal_rate": 0.038,
    },
}


ALL_DEFAULTS = SHARED_DEFAULTS | PAGE_DEFAULTS



def _persist_key(key: str) -> str:
    return f"_persist_{key}"


def shared_widget_key(key: str) -> str:
    return f"_widget_{key}"


def prime_shared_widget(key: str) -> None:
    st.session_state[shared_widget_key(key)] = st.session_state.get(key, ALL_DEFAULTS[key])


def commit_shared_widget(key: str) -> None:
    value = st.session_state[shared_widget_key(key)]
    st.session_state[key] = value
    st.session_state[_persist_key(key)] = value



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



def reset_assumptions() -> None:
    for key, value in ALL_DEFAULTS.items():
        st.session_state[key] = value
        st.session_state[_persist_key(key)] = value
        st.session_state[shared_widget_key(key)] = value



def apply_preset(name: str) -> None:
    reset_assumptions()
    for key, value in SCENARIO_PRESETS.get(name, {}).items():
        st.session_state[key] = value
        st.session_state[_persist_key(key)] = value
        st.session_state[shared_widget_key(key)] = value



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
    if float(st.session_state.taxable_balance) == 0 and bool(st.session_state.has_taxable_brokerage):
        warnings.append("已勾选应税投资账户，但应税余额为 0。" if zh else "Taxable brokerage is checked, but the taxable balance is zero.")
    if float(st.session_state.roth_balance) == 0 and bool(st.session_state.has_roth_ira):
        warnings.append("已勾选 Roth IRA，但 Roth 余额为 0。" if zh else "Roth IRA is checked, but the Roth balance is zero.")

    return errors, warnings



def get_total_portfolio() -> float:
    return float(st.session_state.traditional_balance) + float(st.session_state.roth_balance) + float(st.session_state.taxable_balance)



def get_fixed_retirement_income() -> float:
    return float(st.session_state.annual_social_security_benefit) + float(st.session_state.annual_pension_income)
