#!/usr/bin/env python3
from __future__ import annotations

from roth_conversion_defaults import DEFAULTS
from roth_conversion_engine import (
    PlanInputs,
    compare_strategies,
    format_comparison,
)


def ask_int(prompt: str, default: int | None = None) -> int:
    while True:
        suffix = f" [{default}]" if default is not None else ""
        raw = input(f"{prompt}{suffix}: ").strip()
        if raw == "" and default is not None:
            return default
        try:
            value = int(raw)
            if value < 0:
                raise ValueError
            return value
        except ValueError:
            print("请输入非负整数")


def ask_float(prompt: str, default: float | None = None) -> float:
    while True:
        suffix = f" [{default}]" if default is not None else ""
        raw = input(f"{prompt}{suffix}: ").strip().replace(",", "")
        if raw == "" and default is not None:
            return default
        try:
            value = float(raw)
            if value < 0:
                raise ValueError
            return value
        except ValueError:
            print("请输入非负数字")


def ask_bool(prompt: str, default: bool | None = None) -> bool:
    while True:
        if default is None:
            suffix = ""
        else:
            suffix = " [y]" if default else " [n]"
        raw = input(f"{prompt} (y/n){suffix}: ").strip().lower()
        if raw == "" and default is not None:
            return default
        if raw in {"y", "yes"}:
            return True
        if raw in {"n", "no"}:
            return False
        print("请输入 y 或 n")


def ask_status(prompt: str, default: str = "mfj") -> str:
    while True:
        raw = input(f"{prompt} [single/mfj, 默认 {default}]: ").strip().lower()
        if raw == "":
            return default
        if raw in {"single", "mfj"}:
            return raw
        print("请输入 single 或 mfj")


def ask_bracket(prompt: str, default: str = "24%") -> str:
    allowed = {"12%", "22%", "24%", "32%"}
    while True:
        raw = input(f"{prompt} [12%/22%/24%/32%, 默认 {default}]: ").strip()
        if raw == "":
            return default
        if raw in allowed:
            return raw
        print("请输入 12%、22%、24% 或 32%")


def collect_inputs() -> PlanInputs:
    print("Roth Conversion 模拟器（增强版）\n")
    print("先输入基础参数，再输入可选高级参数；直接回车可使用默认值。\n")

    current_age = ask_int("当前年龄", int(DEFAULTS["current_age"]))
    retirement_age = ask_int("预计退休年龄（55岁是否确定，可直接输入年龄）", int(DEFAULTS["retirement_age"]))
    current_401k_balance = ask_float("当前401(k)余额", float(DEFAULTS["current_401k_balance"]))
    annual_contribution = ask_float("每年计划存入多少（退休前）", float(DEFAULTS["annual_contribution"]))
    has_roth_ira = ask_bool("是否已有 Roth IRA", bool(DEFAULTS["has_roth_ira"]))
    has_taxable_brokerage = ask_bool("是否有 Taxable Brokerage", bool(DEFAULTS["has_taxable_brokerage"]))
    annual_retirement_spending = ask_float("预计退休后每年花费", float(DEFAULTS["annual_retirement_spending"]))

    print("\n--- 高级参数（更真实，但可选）---")
    filing_status = ask_status("报税身份", str(DEFAULTS["filing_status"]))
    current_roth_balance = ask_float("当前 Roth 余额", float(DEFAULTS["current_roth_balance"]))
    current_taxable_balance = ask_float("当前 Taxable Brokerage 余额", float(DEFAULTS["current_taxable_balance"]))
    annual_other_income = ask_float("退休后每年其他普通收入（如兼职/利息等）", float(DEFAULTS["annual_other_income"]))
    annual_pension_income = ask_float("退休后每年 pension 收入", float(DEFAULTS["annual_pension_income"]))
    social_security_claim_age = ask_int("Social Security 领取年龄", int(DEFAULTS["social_security_claim_age"]))
    annual_social_security_benefit = ask_float("开始领取后每年 Social Security 金额", float(DEFAULTS["annual_social_security_benefit"]))
    annual_return = ask_float("假设年化收益率（例如 0.06 = 6%）", float(DEFAULTS["annual_return"]))
    state_tax_rate = ask_float("州税率（例如 0.05 = 5%）", float(DEFAULTS["state_tax_rate"]))
    target_bracket = ask_bracket("目标 conversion 税档上沿", str(DEFAULTS["target_bracket"]))
    use_aca_model = ask_bool("是否估算 65 岁前 ACA 保费拖累", bool(DEFAULTS["use_aca_model"]))
    use_irmaa_model = ask_bool("是否估算 65 岁后 Medicare IRMAA", bool(DEFAULTS["use_irmaa_model"]))
    life_expectancy = ask_int("比较总成本时模拟到几岁", int(DEFAULTS["life_expectancy"]))

    if retirement_age < current_age:
        raise ValueError("退休年龄不能小于当前年龄")
    if retirement_age > 75:
        raise ValueError("当前版本假设退休年龄不晚于75岁")

    return PlanInputs(
        current_age=current_age,
        retirement_age=retirement_age,
        current_401k_balance=current_401k_balance,
        annual_contribution=annual_contribution,
        has_roth_ira=has_roth_ira,
        has_taxable_brokerage=has_taxable_brokerage,
        annual_retirement_spending=annual_retirement_spending,
        filing_status=filing_status,
        current_roth_balance=current_roth_balance,
        current_taxable_balance=current_taxable_balance,
        annual_other_income=annual_other_income,
        annual_pension_income=annual_pension_income,
        social_security_claim_age=social_security_claim_age,
        annual_social_security_benefit=annual_social_security_benefit,
        annual_return=annual_return,
        state_tax_rate=state_tax_rate,
        target_bracket=target_bracket,
        use_aca_model=use_aca_model,
        use_irmaa_model=use_irmaa_model,
        life_expectancy=life_expectancy,
    )


def main() -> None:
    inputs = collect_inputs()
    results = compare_strategies(inputs)
    print()
    print(format_comparison(results["conversion"], results["no_conversion"]))
    if not inputs.has_roth_ira:
        print("\n提醒：如果现在没有 Roth IRA，实际执行 conversion 前需要先准备接收转换的 Roth 账户。")
    print("\n说明：这版已经比基础版真实不少，但仍然是规划近似，不是报税软件。")


if __name__ == "__main__":
    main()
