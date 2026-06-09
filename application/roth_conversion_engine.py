#!/usr/bin/env python3
"""Richer Roth conversion planning engine.

This model is still an approximation, but it is meaningfully closer to real planning than the
first toy version. It adds:
- filing status
- current Roth / taxable balances
- Social Security claim age and benefit
- other retirement income / pension
- federal ordinary income tax
- taxable Social Security estimate
- Medicare IRMAA estimate
- ACA subsidy drag estimate before age 65
- yearly suggested Roth conversion amounts from retirement through age 75
- comparison against a no-conversion baseline

All dollar values are in today's dollars unless noted otherwise.
This is for planning / education only, not tax or legal advice.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, List, Literal, Optional

FilingStatus = Literal["single", "mfj"]

DEFAULT_ANNUAL_RETURN = 0.06
DEFAULT_INFLATION = 0.02
DEFAULT_TARGET_BRACKET = "24%"
DEFAULT_LIFE_EXPECTANCY = 90

FEDERAL_TAX = {
    "single": {
        "standard_deduction": 15500.0,
        "brackets": [
            (11925.0, 0.10),
            (48475.0, 0.12),
            (103350.0, 0.22),
            (197300.0, 0.24),
            (250525.0, 0.32),
            (626350.0, 0.35),
            (float("inf"), 0.37),
        ],
    },
    "mfj": {
        "standard_deduction": 31000.0,
        "brackets": [
            (23850.0, 0.10),
            (96950.0, 0.12),
            (206700.0, 0.22),
            (394600.0, 0.24),
            (501050.0, 0.32),
            (751600.0, 0.35),
            (float("inf"), 0.37),
        ],
    },
}

IRMAA_2026 = {
    "single": [
        (109000.0, 0.0),
        (137000.0, 1080.0),
        (171000.0, 2700.0),
        (205000.0, 4320.0),
        (500000.0, 5940.0),
        (float("inf"), 6480.0),
    ],
    "mfj": [
        (218000.0, 0.0),
        (274000.0, 1080.0 * 2),
        (342000.0, 2700.0 * 2),
        (410000.0, 4320.0 * 2),
        (750000.0, 5940.0 * 2),
        (float("inf"), 6480.0 * 2),
    ],
}

# Approximate benchmark ACA subsidy setup for planning drag only.
ACA_FPL_2026 = {
    "single": 15650.0,
    "mfj": 21150.0,
}
ACA_EXPECTED_PREMIUM_RATE = [
    (1.5, 0.00),
    (2.0, 0.02),
    (2.5, 0.04),
    (3.0, 0.06),
    (4.0, 0.085),
    (float("inf"), 0.085),
]
ACA_BENCHMARK_PREMIUM = {
    "single": 9000.0,
    "mfj": 18000.0,
}

UNIFORM_LIFETIME_FACTORS = {
    75: 24.6,
    76: 23.7,
    77: 22.9,
    78: 22.0,
    79: 21.1,
    80: 20.2,
    81: 19.4,
    82: 18.5,
    83: 17.7,
    84: 16.8,
    85: 16.0,
    86: 15.2,
    87: 14.4,
    88: 13.7,
    89: 12.9,
    90: 12.2,
}

TARGET_RATE_BY_LABEL = {
    "12%": 0.12,
    "22%": 0.22,
    "24%": 0.24,
    "32%": 0.32,
}


@dataclass
class PlanInputs:
    current_age: int
    retirement_age: int
    current_401k_balance: float
    annual_contribution: float
    has_roth_ira: bool
    has_taxable_brokerage: bool
    annual_retirement_spending: float

    filing_status: FilingStatus = "mfj"
    current_roth_balance: float = 0.0
    current_taxable_balance: float = 0.0
    annual_other_income: float = 0.0
    annual_pension_income: float = 0.0
    social_security_claim_age: int = 70
    annual_social_security_benefit: float = 0.0
    annual_return: float = DEFAULT_ANNUAL_RETURN
    inflation: float = DEFAULT_INFLATION
    target_bracket: str = DEFAULT_TARGET_BRACKET
    state_tax_rate: float = 0.0
    use_aca_model: bool = True
    use_irmaa_model: bool = True
    life_expectancy: int = DEFAULT_LIFE_EXPECTANCY


@dataclass
class YearResult:
    age: int
    start_traditional: float
    start_roth: float
    start_taxable: float
    spending_need: float
    spending_from_taxable: float
    spending_from_traditional: float
    spending_from_roth: float
    social_security_gross: float
    social_security_taxable: float
    other_income: float
    pension_income: float
    recommended_conversion: float
    gross_income: float
    estimated_federal_tax: float
    estimated_state_tax: float
    aca_subsidy_loss: float
    irmaa_surcharge: float
    effective_marginal_bracket: str
    end_traditional: float
    end_roth: float
    end_taxable: float


@dataclass
class PlanResult:
    scenario_name: str
    yearly: List[YearResult]
    traditional_balance_at_75: float
    roth_balance_at_75: float
    taxable_balance_at_75: float
    estimated_rmd_at_75: float
    total_federal_tax_to_life_expectancy: float
    total_state_tax_to_life_expectancy: float
    total_aca_drag_to_life_expectancy: float
    total_irmaa_to_life_expectancy: float

    @property
    def total_cost_to_life_expectancy(self) -> float:
        return (
            self.total_federal_tax_to_life_expectancy
            + self.total_state_tax_to_life_expectancy
            + self.total_aca_drag_to_life_expectancy
            + self.total_irmaa_to_life_expectancy
        )


def tax_config(status: FilingStatus) -> Dict[str, object]:
    return FEDERAL_TAX[status]


def taxable_ss(gross_ss: float, other_provisional_income: float, status: FilingStatus) -> float:
    if gross_ss <= 0:
        return 0.0
    base1, base2 = (25000.0, 34000.0) if status == "single" else (32000.0, 44000.0)
    provisional = other_provisional_income + 0.5 * gross_ss
    if provisional <= base1:
        return 0.0
    if provisional <= base2:
        return min(0.5 * (provisional - base1), 0.5 * gross_ss)
    taxable = 0.85 * (provisional - base2) + min(0.5 * (base2 - base1), 0.5 * gross_ss)
    return min(taxable, 0.85 * gross_ss)


def federal_tax_from_taxable_income(taxable_income: float, status: FilingStatus) -> float:
    if taxable_income <= 0:
        return 0.0
    brackets = tax_config(status)["brackets"]
    lower = 0.0
    remaining = taxable_income
    tax = 0.0
    for upper, rate in brackets:
        span = upper - lower
        taxed = min(remaining, span)
        if taxed > 0:
            tax += taxed * rate
            remaining -= taxed
        if remaining <= 0:
            break
        lower = upper
    return tax


def federal_tax(gross_ordinary_income: float, status: FilingStatus) -> float:
    deduction = float(tax_config(status)["standard_deduction"])
    taxable_income = max(0.0, gross_ordinary_income - deduction)
    return federal_tax_from_taxable_income(taxable_income, status)


def marginal_bracket(gross_ordinary_income: float, status: FilingStatus) -> str:
    deduction = float(tax_config(status)["standard_deduction"])
    taxable_income = max(0.0, gross_ordinary_income - deduction)
    for upper, rate in tax_config(status)["brackets"]:
        if taxable_income <= upper:
            return f"{rate * 100:.2f}%"
    return "37.00%"


def gross_income_cap_for_target_bracket(status: FilingStatus, bracket_label: str) -> float:
    target_rate = TARGET_RATE_BY_LABEL[bracket_label]
    top_taxable = 0.0
    for upper, rate in tax_config(status)["brackets"]:
        top_taxable = upper
        if rate == target_rate:
            break
    deduction = float(tax_config(status)["standard_deduction"])
    return deduction + top_taxable


def estimate_aca_drag(magi: float, status: FilingStatus) -> float:
    fpl = ACA_FPL_2026[status]
    benchmark = ACA_BENCHMARK_PREMIUM[status]
    ratio = magi / fpl if fpl > 0 else float("inf")
    expected_rate = ACA_EXPECTED_PREMIUM_RATE[-1][1]
    for upper_ratio, rate in ACA_EXPECTED_PREMIUM_RATE:
        if ratio <= upper_ratio:
            expected_rate = rate
            break
    expected_contribution = magi * expected_rate
    subsidy = max(0.0, benchmark - expected_contribution)
    out_of_pocket = benchmark - subsidy
    return out_of_pocket


def irmaa_surcharge(magi: float, status: FilingStatus) -> float:
    for threshold, surcharge in IRMAA_2026[status]:
        if magi <= threshold:
            return surcharge
    return IRMAA_2026[status][-1][1]


def project_pre_retirement(inp: PlanInputs) -> tuple[float, float, float]:
    trad = inp.current_401k_balance
    roth = inp.current_roth_balance
    taxable = inp.current_taxable_balance
    for _age in range(inp.current_age, inp.retirement_age):
        trad = trad * (1 + inp.annual_return) + inp.annual_contribution
        roth *= 1 + inp.annual_return
        taxable *= 1 + inp.annual_return
    return trad, roth, taxable


def annual_ss_benefit_for_age(inp: PlanInputs, age: int) -> float:
    if age < inp.social_security_claim_age:
        return 0.0
    return inp.annual_social_security_benefit


def spending_need_for_age(inp: PlanInputs, age: int) -> float:
    years_since_retirement = max(0, age - inp.retirement_age)
    return inp.annual_retirement_spending * ((1 + inp.inflation) ** years_since_retirement)


def choose_conversion(inp: PlanInputs, age: int, base_income: float, trad_balance: float) -> float:
    target_cap = gross_income_cap_for_target_bracket(inp.filing_status, inp.target_bracket)

    # Before Medicare, if ACA model is on, stay a bit more conservative by default.
    if inp.use_aca_model and age < 65:
        aca_soft_cap = 0.0
        # 400% FPL is not a hard cliff anymore, but it remains a useful planning waypoint.
        aca_soft_cap = ACA_FPL_2026[inp.filing_status] * 4.0
        if aca_soft_cap > 0:
            target_cap = min(target_cap, max(base_income, aca_soft_cap))

    # Starting at 63, MAGI affects Medicare IRMAA two years later.
    if inp.use_irmaa_model and age >= 63:
        first_irmaa_threshold = IRMAA_2026[inp.filing_status][0][0]
        target_cap = min(target_cap, max(base_income, first_irmaa_threshold))

    room = max(0.0, target_cap - base_income)
    return min(room, max(0.0, trad_balance))


def _withdraw_for_spending(spending_need: float, taxable: float, trad: float, roth: float) -> tuple[float, float, float, float, float, float]:
    from_taxable = min(spending_need, taxable)
    taxable -= from_taxable
    remaining = spending_need - from_taxable

    from_trad = min(remaining, trad)
    trad -= from_trad
    remaining -= from_trad

    from_roth = min(remaining, roth)
    roth -= from_roth
    remaining -= from_roth

    unmet = remaining
    return from_taxable, from_trad, from_roth, taxable, trad, roth, unmet


def simulate_plan(inp: PlanInputs, do_conversions: bool = True, scenario_name: str = "conversion") -> PlanResult:
    trad, roth, taxable = project_pre_retirement(inp)
    yearly: List[YearResult] = []

    total_federal_tax = 0.0
    total_state_tax = 0.0
    total_aca_drag = 0.0
    total_irmaa = 0.0
    prior_year_magi: Dict[int, float] = {}

    for age in range(inp.retirement_age, 76):
        start_trad, start_roth, start_taxable = trad, roth, taxable
        spending_need = spending_need_for_age(inp, age)

        ss_gross = annual_ss_benefit_for_age(inp, age)
        other_income = inp.annual_other_income
        pension_income = inp.annual_pension_income
        provisional_other = other_income + pension_income
        ss_taxable = taxable_ss(ss_gross, provisional_other, inp.filing_status)

        spending_from_taxable, spending_from_traditional, spending_from_roth, taxable, trad, roth, unmet_spending = _withdraw_for_spending(
            spending_need, taxable, trad, roth
        )
        if unmet_spending > 0:
            # If the plan runs out of money, record it as extra traditional need if available is zero.
            spending_from_traditional += unmet_spending

        ordinary_income_before_conversion = other_income + pension_income + ss_taxable + spending_from_traditional
        conversion = choose_conversion(inp, age, ordinary_income_before_conversion, trad) if do_conversions and age < 75 else 0.0
        trad -= conversion
        roth += conversion

        gross_income = ordinary_income_before_conversion + conversion
        federal = federal_tax(gross_income, inp.filing_status)
        state = gross_income * inp.state_tax_rate
        magi = other_income + pension_income + ss_gross + spending_from_traditional + conversion

        aca_drag = estimate_aca_drag(magi, inp.filing_status) if inp.use_aca_model and age < 65 else 0.0
        irmaa = irmaa_surcharge(prior_year_magi.get(age - 2, 0.0), inp.filing_status) if inp.use_irmaa_model and age >= 65 else 0.0
        prior_year_magi[age] = magi

        total_federal_tax += federal
        total_state_tax += state
        total_aca_drag += aca_drag
        total_irmaa += irmaa

        tax_bill = federal + state + aca_drag + irmaa
        if inp.has_taxable_brokerage:
            tax_from_taxable = min(tax_bill, taxable)
            taxable -= tax_from_taxable
            tax_bill -= tax_from_taxable
        if tax_bill > 0:
            tax_from_trad = min(tax_bill, trad)
            trad -= tax_from_trad
            tax_bill -= tax_from_trad
        if tax_bill > 0:
            roth -= min(tax_bill, roth)

        trad *= 1 + inp.annual_return
        roth *= 1 + inp.annual_return
        taxable *= 1 + inp.annual_return

        yearly.append(
            YearResult(
                age=age,
                start_traditional=start_trad,
                start_roth=start_roth,
                start_taxable=start_taxable,
                spending_need=spending_need,
                spending_from_taxable=spending_from_taxable,
                spending_from_traditional=spending_from_traditional,
                spending_from_roth=spending_from_roth,
                social_security_gross=ss_gross,
                social_security_taxable=ss_taxable,
                other_income=other_income,
                pension_income=pension_income,
                recommended_conversion=conversion,
                gross_income=gross_income,
                estimated_federal_tax=federal,
                estimated_state_tax=state,
                aca_subsidy_loss=aca_drag,
                irmaa_surcharge=irmaa,
                effective_marginal_bracket=marginal_bracket(gross_income, inp.filing_status),
                end_traditional=trad,
                end_roth=roth,
                end_taxable=taxable,
            )
        )

    traditional_at_75 = yearly[-1].end_traditional if yearly else trad
    roth_at_75 = yearly[-1].end_roth if yearly else roth
    taxable_at_75 = yearly[-1].end_taxable if yearly else taxable
    rmd_75 = traditional_at_75 / UNIFORM_LIFETIME_FACTORS[75] if traditional_at_75 > 0 else 0.0

    post75 = project_post75_costs(
        traditional_at_75,
        roth_at_75,
        taxable_at_75,
        inp,
        prior_year_magi,
    )
    total_federal_tax += post75["federal"]
    total_state_tax += post75["state"]
    total_aca_drag += post75["aca"]
    total_irmaa += post75["irmaa"]

    return PlanResult(
        scenario_name=scenario_name,
        yearly=yearly,
        traditional_balance_at_75=traditional_at_75,
        roth_balance_at_75=roth_at_75,
        taxable_balance_at_75=taxable_at_75,
        estimated_rmd_at_75=rmd_75,
        total_federal_tax_to_life_expectancy=total_federal_tax,
        total_state_tax_to_life_expectancy=total_state_tax,
        total_aca_drag_to_life_expectancy=total_aca_drag,
        total_irmaa_to_life_expectancy=total_irmaa,
    )


def project_post75_costs(
    traditional: float,
    roth: float,
    taxable: float,
    inp: PlanInputs,
    prior_year_magi: Dict[int, float],
) -> Dict[str, float]:
    total_federal = 0.0
    total_state = 0.0
    total_aca = 0.0
    total_irmaa = 0.0
    trad = traditional
    roth_bal = roth
    taxable_bal = taxable

    for age in range(76, inp.life_expectancy + 1):
        factor = UNIFORM_LIFETIME_FACTORS.get(age, max(2.0, UNIFORM_LIFETIME_FACTORS[90] - (age - 90) * 0.7))
        spending_need = spending_need_for_age(inp, age)
        ss_gross = annual_ss_benefit_for_age(inp, age)
        other_income = inp.annual_other_income
        pension_income = inp.annual_pension_income
        ss_taxable = taxable_ss(ss_gross, other_income + pension_income, inp.filing_status)
        rmd = min(trad, trad / factor) if trad > 0 else 0.0
        ordinary_income = other_income + pension_income + ss_taxable + rmd
        federal = federal_tax(ordinary_income, inp.filing_status)
        state = ordinary_income * inp.state_tax_rate
        magi = other_income + pension_income + ss_gross + rmd
        irmaa = irmaa_surcharge(prior_year_magi.get(age - 2, 0.0), inp.filing_status) if inp.use_irmaa_model and age >= 65 else 0.0
        prior_year_magi[age] = magi

        tax_bill = federal + state + irmaa
        total_federal += federal
        total_state += state
        total_irmaa += irmaa

        trad -= rmd
        leftover_rmd_after_spend = max(0.0, rmd - max(0.0, spending_need - (ss_gross + other_income + pension_income)))
        taxable_bal += max(0.0, leftover_rmd_after_spend - tax_bill)

        trad *= 1 + inp.annual_return
        roth_bal *= 1 + inp.annual_return
        taxable_bal *= 1 + inp.annual_return

    return {
        "federal": total_federal,
        "state": total_state,
        "aca": total_aca,
        "irmaa": total_irmaa,
    }


def project_post75_balances(
    traditional: float,
    roth: float,
    taxable: float,
    inp: PlanInputs,
    prior_year_magi: Dict[int, float],
) -> Dict[str, float]:
    trad = traditional
    roth_bal = roth
    taxable_bal = taxable

    for age in range(76, inp.life_expectancy + 1):
        factor = UNIFORM_LIFETIME_FACTORS.get(age, max(2.0, UNIFORM_LIFETIME_FACTORS[90] - (age - 90) * 0.7))
        spending_need = spending_need_for_age(inp, age)
        ss_gross = annual_ss_benefit_for_age(inp, age)
        other_income = inp.annual_other_income
        pension_income = inp.annual_pension_income
        ss_taxable = taxable_ss(ss_gross, other_income + pension_income, inp.filing_status)
        rmd = min(trad, trad / factor) if trad > 0 else 0.0
        ordinary_income = other_income + pension_income + ss_taxable + rmd
        federal = federal_tax(ordinary_income, inp.filing_status)
        state = ordinary_income * inp.state_tax_rate
        magi = other_income + pension_income + ss_gross + rmd
        irmaa = irmaa_surcharge(prior_year_magi.get(age - 2, 0.0), inp.filing_status) if inp.use_irmaa_model and age >= 65 else 0.0
        prior_year_magi[age] = magi

        tax_bill = federal + state + irmaa

        trad -= rmd
        leftover_rmd_after_spend = max(0.0, rmd - max(0.0, spending_need - (ss_gross + other_income + pension_income)))
        taxable_bal += max(0.0, leftover_rmd_after_spend - tax_bill)

        trad *= 1 + inp.annual_return
        roth_bal *= 1 + inp.annual_return
        taxable_bal *= 1 + inp.annual_return

    return {
        "traditional": trad,
        "roth": roth_bal,
        "taxable": taxable_bal,
        "total": trad + roth_bal + taxable_bal,
    }


def project_late_life_metrics(
    traditional: float,
    roth: float,
    taxable: float,
    inp: PlanInputs,
    prior_year_magi: Dict[int, float],
) -> Dict[str, float]:
    trad = traditional
    roth_bal = roth
    taxable_bal = taxable
    max_rmd = 0.0
    max_magi = 0.0

    for age in range(76, inp.life_expectancy + 1):
        factor = UNIFORM_LIFETIME_FACTORS.get(age, max(2.0, UNIFORM_LIFETIME_FACTORS[90] - (age - 90) * 0.7))
        spending_need = spending_need_for_age(inp, age)
        ss_gross = annual_ss_benefit_for_age(inp, age)
        other_income = inp.annual_other_income
        pension_income = inp.annual_pension_income
        ss_taxable = taxable_ss(ss_gross, other_income + pension_income, inp.filing_status)
        rmd = min(trad, trad / factor) if trad > 0 else 0.0
        ordinary_income = other_income + pension_income + ss_taxable + rmd
        federal = federal_tax(ordinary_income, inp.filing_status)
        state = ordinary_income * inp.state_tax_rate
        magi = other_income + pension_income + ss_gross + rmd
        irmaa = irmaa_surcharge(prior_year_magi.get(age - 2, 0.0), inp.filing_status) if inp.use_irmaa_model and age >= 65 else 0.0
        prior_year_magi[age] = magi

        tax_bill = federal + state + irmaa
        max_rmd = max(max_rmd, rmd)
        max_magi = max(max_magi, magi)

        trad -= rmd
        leftover_rmd_after_spend = max(0.0, rmd - max(0.0, spending_need - (ss_gross + other_income + pension_income)))
        taxable_bal += max(0.0, leftover_rmd_after_spend - tax_bill)

        trad *= 1 + inp.annual_return
        roth_bal *= 1 + inp.annual_return
        taxable_bal *= 1 + inp.annual_return

    return {
        "traditional": trad,
        "roth": roth_bal,
        "taxable": taxable_bal,
        "total": trad + roth_bal + taxable_bal,
        "max_rmd": max_rmd,
        "max_magi": max_magi,
    }


def compare_strategies(inp: PlanInputs) -> Dict[str, PlanResult]:
    conversion = simulate_plan(inp, do_conversions=True, scenario_name="conversion")
    baseline = simulate_plan(inp, do_conversions=False, scenario_name="no_conversion")
    return {
        "conversion": conversion,
        "no_conversion": baseline,
    }


def money(value: float) -> str:
    return f"${value:,.0f}"


def format_comparison(conversion: PlanResult, baseline: PlanResult) -> str:
    lines = []
    lines.append("=== 退休后到75岁的详细 Roth Conversion 路线图 ===")
    lines.append(
        f"{'Age':>4} {'Start Trad':>13} {'Taxable':>11} {'Roth':>11} {'Spend':>11} {'Conv':>11} {'Bracket':>8} {'FedTax':>11} {'ACA':>9} {'IRMAA':>9} {'End Trad':>13}"
    )
    for row in conversion.yearly:
        lines.append(
            f"{row.age:>4} {money(row.start_traditional):>13} {money(row.start_taxable):>11} {money(row.start_roth):>11} "
            f"{money(row.spending_need):>11} {money(row.recommended_conversion):>11} {row.effective_marginal_bracket:>8} "
            f"{money(row.estimated_federal_tax):>11} {money(row.aca_subsidy_loss):>9} {money(row.irmaa_surcharge):>9} {money(row.end_traditional):>13}"
        )
    lines.append("")
    lines.append("=== 摘要 ===")
    lines.append(f"75岁时传统账户余额: {money(conversion.traditional_balance_at_75)}")
    lines.append(f"75岁时 Roth 余额:   {money(conversion.roth_balance_at_75)}")
    lines.append(f"75岁时 Taxable余额: {money(conversion.taxable_balance_at_75)}")
    lines.append(f"75岁首年 RMD 估算:  {money(conversion.estimated_rmd_at_75)}")
    lines.append(f"不转换时 75岁 RMD:  {money(baseline.estimated_rmd_at_75)}")
    lines.append(f"转换策略总成本:      {money(conversion.total_cost_to_life_expectancy)}")
    lines.append(f"不转换策略总成本:    {money(baseline.total_cost_to_life_expectancy)}")
    lines.append(f"预计节省:            {money(baseline.total_cost_to_life_expectancy - conversion.total_cost_to_life_expectancy)}")
    lines.append("")
    lines.append("注：总成本 = 联邦税 + 州税 + ACA保费拖累 + Medicare IRMAA 估算。")
    return "\n".join(lines)


def result_rows(plan: PlanResult) -> List[Dict[str, float | str | int]]:
    return [asdict(row) for row in plan.yearly]
