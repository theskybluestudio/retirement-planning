#!/usr/bin/env python3
from __future__ import annotations

from typing import Any

import streamlit as st


LANGUAGES = {
    "en": "English",
    "zh": "中文",
}


CATALOG: dict[str, Any] = {
    "common": {
        "language": {"en": "Language", "zh": "语言"},
        "english": {"en": "English", "zh": "英文"},
        "chinese": {"en": "Chinese", "zh": "中文"},
        "page_specific_inputs": {"en": "Page-specific inputs", "zh": "页面专用输入"},
        "using_shared_assumptions": {"en": "This page uses shared assumptions", "zh": "本页面使用共享假设"},
        "update_shared_assumptions": {"en": "Update balances and annual spending on the Shared Assumptions page.", "zh": "请在“共享假设”页面更新余额和年度支出。"},
        "yes": {"en": "yes", "zh": "是"},
        "no": {"en": "no", "zh": "否"},
    },
    "suite": {
        "title": {"en": "Retirement Planning Suite", "zh": "退休规划工具套件"},
        "home_subtitle": {
            "en": "A native Streamlit multipage collection of retirement planning calculators, built around one shared assumptions page plus focused calculator pages.",
            "zh": "一个基于 Streamlit 原生多页面的退休规划计算器集合，围绕一个共享假设页面和多个聚焦型计算页面构建。",
        },
        "live_tools": {"en": "Live tools", "zh": "可用工具"},
        "most_complete_page": {"en": "Most complete page", "zh": "最完整页面"},
        "native_sidebar": {"en": "Native sidebar", "zh": "原生侧边栏"},
    },
    "assumptions": {
        "title": {"en": "Shared Assumptions", "zh": "共享假设"},
        "subtitle": {
            "en": "Set the common planning inputs once here. Other pages read these values from Streamlit session state so you do not have to keep re-entering the same facts.",
            "zh": "在这里一次性设置通用规划输入。其他页面会从 Streamlit session state 读取这些值，这样你就不必反复输入相同信息。",
        },
        "scenario_presets": {"en": "Scenario presets", "zh": "情景预设"},
        "reset_defaults": {"en": "Reset all assumptions to defaults", "zh": "重置所有假设为默认值"},
        "download_json": {"en": "Download assumptions JSON", "zh": "下载假设 JSON"},
        "load_json": {"en": "Load assumptions from JSON", "zh": "从 JSON 加载假设"},
        "loaded_json_success": {"en": "Assumptions loaded from JSON.", "zh": "已从 JSON 加载假设。"},
        "load_json_error": {"en": "Could not load assumptions file:", "zh": "无法加载假设文件："},
        "personal": {"en": "Personal", "zh": "个人信息"},
        "accounts": {"en": "Accounts", "zh": "账户"},
        "cash_flow": {"en": "Cash flow", "zh": "现金流"},
        "market_tax": {"en": "Market & tax", "zh": "市场与税务"},
        "current_age": {"en": "Current age", "zh": "当前年龄"},
        "retirement_age": {"en": "Retirement age", "zh": "退休年龄"},
        "life_expectancy": {"en": "Life expectancy", "zh": "预期寿命"},
        "filing_status": {"en": "Filing status", "zh": "报税身份"},
        "traditional_balance": {"en": "Traditional IRA / 401(k)", "zh": "传统 IRA / 401(k)"},
        "roth_balance": {"en": "Roth balance", "zh": "Roth 余额"},
        "taxable_balance": {"en": "Taxable brokerage", "zh": "应税投资账户"},
        "has_roth_ira": {"en": "Already has Roth IRA", "zh": "已有 Roth IRA"},
        "has_taxable_brokerage": {"en": "Has taxable brokerage", "zh": "有应税投资账户"},
        "annual_contribution": {"en": "Annual contribution", "zh": "年度投入"},
        "annual_retirement_spending": {"en": "Annual retirement spending", "zh": "退休后年度支出"},
        "annual_ss_benefit": {"en": "Annual Social Security benefit", "zh": "年度社保收入"},
        "annual_ss_benefit_fra": {"en": "Annual Social Security benefit at FRA", "zh": "FRA 时年度社保收入"},
        "ss_claim_age": {"en": "Social Security claim age", "zh": "社保领取年龄"},
        "annual_pension_income": {"en": "Annual pension income", "zh": "年度养老金收入"},
        "annual_other_income": {"en": "Annual other ordinary income", "zh": "年度其他普通收入"},
        "annual_return": {"en": "Annual return", "zh": "年化收益率"},
        "inflation": {"en": "Inflation", "zh": "通胀率"},
        "state_tax_rate": {"en": "State tax rate", "zh": "州税率"},
        "consistent": {"en": "Assumptions look internally consistent.", "zh": "这些假设在内部看起来是一致的。"},
        "total_portfolio": {"en": "Total investable portfolio", "zh": "总投资资产"},
        "planned_spending": {"en": "Planned annual spending", "zh": "计划年度支出"},
        "note": {
            "en": "These values are stored in Streamlit session state for this browser session. You can now apply scenario presets, reset everything to defaults, download the current assumptions to JSON, or load a saved JSON file back into the app.",
            "zh": "这些值会保存在当前浏览器会话的 Streamlit session state 中。你现在可以应用情景预设、重置为默认值、下载当前假设为 JSON，或把已保存的 JSON 重新加载回应用。",
        },
    },
    "presets": {
        "base": {"en": "Base", "zh": "基础"},
        "conservative": {"en": "Conservative", "zh": "保守"},
        "aggressive": {"en": "Aggressive", "zh": "激进"},
        "early_retirement": {"en": "Early Retirement", "zh": "提前退休"},
    },
    "home": {
        "included_apps": {"en": "Included apps", "zh": "已包含应用"},
        "how_to_use": {"en": "How to use it", "zh": "使用方式"},
        "step_1": {"en": "1. Pick a page from Streamlit’s sidebar.", "zh": "1. 在 Streamlit 侧边栏中选择页面。"},
        "step_2": {"en": "2. Start with Shared Assumptions and set the common facts once.", "zh": "2. 从“共享假设”开始，一次性设置通用信息。"},
        "step_3": {"en": "3. Open a calculator page and adjust only page-specific inputs.", "zh": "3. 打开具体计算页面，只调整该页面特有的输入。"},
        "step_4": {"en": "4. Move between calculators without re-entering the shared facts.", "zh": "4. 在多个计算页面之间切换时，无需重新输入共享信息。"},
        "note": {
            "en": "The app now uses Streamlit’s native multipage structure plus session state, so shared facts persist while each page stays focused on its own question.",
            "zh": "应用现在使用 Streamlit 原生多页面结构和 session state，因此共享信息会保留，而每个页面仍聚焦自己的问题。",
        },
        "current_structure": {"en": "Current structure", "zh": "当前结构"},
    },
    "navigation": {
        "core_planners": {"en": "Core planners", "zh": "核心规划"},
        "income_withdrawals": {"en": "Income & withdrawals", "zh": "收入与提款"},
        "reference": {"en": "Reference", "zh": "参考"},
        "roadmap": {"en": "Roadmap", "zh": "路线图"},
    },
    "rmd": {
        "title": {"en": "RMD / Roth Conversion Strategy", "zh": "RMD / Roth 转换策略"},
        "subtitle": {"en": "Compare conversion and no-conversion paths, estimate future RMDs, and inspect the year-by-year ladder.", "zh": "比较转换与不转换路径，估算未来 RMD，并查看逐年转换阶梯。"},
        "target_bracket": {"en": "Target conversion bracket ceiling", "zh": "目标转换税档上限"},
        "aca": {"en": "Estimate ACA drag before 65", "zh": "估算 65 岁前 ACA 拖累"},
        "irmaa": {"en": "Estimate IRMAA after 65", "zh": "估算 65 岁后 IRMAA"},
        "rmd_conv": {"en": "RMD at 75 (conversion)", "zh": "75 岁 RMD（转换）"},
        "rmd_base": {"en": "RMD at 75 (no conversion)", "zh": "75 岁 RMD（不转换）"},
        "savings": {"en": "Estimated total savings", "zh": "预计总节省"},
        "trad75": {"en": "Traditional balance at 75", "zh": "75 岁传统账户余额"},
        "overview": {"en": "Overview", "zh": "概览"},
        "balance_path": {"en": "Balance path", "zh": "余额路径"},
        "annual_detail": {"en": "Annual detail", "zh": "年度明细"},
        "strategy_comparison": {"en": "Strategy comparison", "zh": "策略对比"},
        "rmd_age_75": {"en": "RMD at age 75", "zh": "75 岁 RMD"},
        "ladder_path": {"en": "Conversion ladder and balance path", "zh": "转换阶梯与余额路径"},
        "annual_path": {"en": "Annual conversion path", "zh": "年度转换路径"},
        "caption": {"en": "Planning approximation only. Verify actual tax execution with CPA or tax software.", "zh": "仅供规划近似使用。实际执行前请用 CPA 或报税软件复核。"},
    },
    "readiness": {
        "title": {"en": "Retirement Readiness", "zh": "退休准备度"},
        "subtitle": {"en": "Project a nest egg, convert it into income, and see whether the plan covers retirement spending.", "zh": "预测退休资产、将其转化为收入，并查看方案是否覆盖退休支出。"},
        "withdrawal_rate": {"en": "Withdrawal rate", "zh": "提款率"},
        "nest_egg": {"en": "Projected nest egg", "zh": "预计退休资产"},
        "real_nest_egg": {"en": "Inflation-adjusted nest egg", "zh": "通胀调整后资产"},
        "total_income": {"en": "Total retirement income", "zh": "退休总收入"},
        "funding_ratio": {"en": "Funding ratio", "zh": "覆盖率"},
        "growth": {"en": "Projected portfolio growth", "zh": "资产增长预测"},
        "interpretation": {"en": "Interpretation", "zh": "解读"},
        "covers": {"en": "On this simplified model, projected income covers target retirement spending.", "zh": "在这个简化模型中，预计收入可以覆盖目标退休支出。"},
        "table": {"en": "Projection table", "zh": "预测表"},
        "caption": {"en": "This version is still deterministic. It now shows both nominal and inflation-adjusted growth, but it still does not model taxes or volatility.", "zh": "这个版本仍是确定性模型。它现在展示名义增长和通胀调整后的增长，但仍未建模税务或波动率。"},
    },
    "social_security": {
        "title": {"en": "Social Security Optimizer", "zh": "社保优化器"},
        "subtitle": {"en": "Compare claiming ages, annual benefits, and simple lifetime payout tradeoffs.", "zh": "比较领取年龄、年度收益和简单的终身领取权衡。"},
        "longevity_age": {"en": "Longevity age for comparison", "zh": "比较用寿命年龄"},
        "highlight_age": {"en": "Highlight claim age", "zh": "高亮领取年龄"},
        "best_age": {"en": "Best claim age", "zh": "最佳领取年龄"},
        "best_lifetime": {"en": "Best lifetime benefit", "zh": "最佳终身收益"},
        "annual_vs_lifetime": {"en": "Annual vs lifetime benefits", "zh": "年度 vs 终身收益"},
        "quick_read": {"en": "Quick read", "zh": "快速解读"},
        "comparison": {"en": "Claiming comparison", "zh": "领取对比"},
        "caption": {"en": "This MVP uses simplified claiming factors and ignores taxation, COLA details, spousal benefits, and discount rates.", "zh": "这个 MVP 使用了简化的领取系数，未纳入税务、COLA、配偶收益和贴现率。"},
    },
    "irmaa": {
        "title": {"en": "Medicare IRMAA", "zh": "Medicare IRMAA 附加费"},
        "subtitle": {"en": "Check how much MAGI headroom remains before a higher Medicare premium tier kicks in.", "zh": "查看在更高 Medicare 保费档位触发前，还剩多少 MAGI 空间。"},
        "extra_income": {"en": "Extra income event", "zh": "额外收入事件"},
        "total_magi": {"en": "Total MAGI", "zh": "总 MAGI"},
        "annual_surcharge": {"en": "Annual IRMAA surcharge", "zh": "年度 IRMAA 附加费"},
        "room": {"en": "Room to tier ceiling", "zh": "距当前档位上限空间"},
        "modeled_extra": {"en": "Extra income modeled", "zh": "模拟的额外收入"},
        "thresholds": {"en": "2026 thresholds", "zh": "2026 档位"},
        "quick_read": {"en": "Quick read", "zh": "快速解读"},
        "caption": {"en": "This page uses the same 2026 threshold table as the conversion model. Real Medicare billing uses lookback rules and other details.", "zh": "该页面使用与转换模型相同的 2026 档位表。真实 Medicare 计费还涉及回溯规则和其他细节。"},
    },
    "sequence": {
        "title": {"en": "Sequence of Returns Risk", "zh": "收益顺序风险"},
        "subtitle": {"en": "Use the same average return set in different orders and watch retirement outcomes split apart.", "zh": "用相同的平均收益集合，但改变顺序，观察退休结果如何分化。"},
        "bad_early": {"en": "Ending balance: bad early", "zh": "坏收益在前的期末余额"},
        "bad_late": {"en": "Ending balance: bad late", "zh": "坏收益在后的期末余额"},
        "difference": {"en": "Difference", "zh": "差额"},
        "paths": {"en": "Portfolio paths", "zh": "资产路径"},
        "details": {"en": "Scenario details", "zh": "情景详情"},
        "caption": {"en": "These two scenarios use the same return set in a different order. That order alone can materially change outcomes once withdrawals begin.", "zh": "这两个情景使用相同的收益集合，只是顺序不同。一旦开始提款，顺序本身就可能显著改变结果。"},
    },
    "safe_withdrawal": {
        "title": {"en": "Safe Withdrawal Guardrails", "zh": "安全提款护栏"},
        "subtitle": {"en": "Compare fixed withdrawals with a flexible guardrail-style spending rule across a mixed return path.", "zh": "比较固定提款与带护栏的灵活支出规则在混合收益路径下的表现。"},
        "lower_guardrail": {"en": "Lower withdrawal-rate guardrail", "zh": "提款率下护栏"},
        "upper_guardrail": {"en": "Upper withdrawal-rate guardrail", "zh": "提款率上护栏"},
        "fixed_end": {"en": "Fixed ending balance", "zh": "固定策略期末余额"},
        "guardrails_end": {"en": "Guardrails ending balance", "zh": "护栏策略期末余额"},
        "fixed_withdrawals": {"en": "Fixed withdrawals", "zh": "固定提款总额"},
        "guardrail_withdrawals": {"en": "Guardrail withdrawals", "zh": "护栏提款总额"},
        "ending_path": {"en": "Ending portfolio path", "zh": "期末资产路径"},
        "withdrawal_path": {"en": "Withdrawal path", "zh": "提款路径"},
        "scenario_detail": {"en": "Scenario detail", "zh": "情景详情"},
        "caption": {"en": "This is a simple illustrative guardrails model, not a complete Guyton-Klinger or VPW implementation.", "zh": "这是一个用于说明概念的简化护栏模型，不是完整的 Guyton-Klinger 或 VPW 实现。"}
    },
    "withdrawal_order": {
        "title": {"en": "Withdrawal Order", "zh": "提款顺序"},
        "subtitle": {"en": "Compare a few simple withdrawal sequences to see how taxes and remaining balances shift.", "zh": "比较几种简单提款顺序，看看税负和剩余余额如何变化。"},
        "lowest_tax": {"en": "Lowest estimated tax", "zh": "最低估算税负"},
        "tax_cost": {"en": "Tax cost", "zh": "税负成本"},
        "unfunded_need": {"en": "Unfunded need", "zh": "未覆盖支出"},
        "strategy_comparison": {"en": "Strategy comparison", "zh": "策略对比"},
        "estimated_taxes": {"en": "Estimated taxes", "zh": "估算税负"},
        "balances_after_year": {"en": "Balances after one year", "zh": "一年后的余额"},
        "caption": {"en": "This is a rule-of-thumb comparison. It does not yet model tax brackets, Social Security taxation, or multi-year optimization.", "zh": "这是一个经验法则式比较。它尚未建模税档、社保税务或多年优化。"}
    },
    "spending_smile": {
        "title": {"en": "Spending Smile Planner", "zh": "支出微笑曲线"},
        "subtitle": {"en": "Model retirement spending across go-go, slow-go, and no-go phases instead of assuming one flat annual number forever.", "zh": "按 go-go、slow-go 和 no-go 阶段建模退休支出，而不是永远假设为一个固定年度数字。"},
        "go_go_years": {"en": "Go-go years", "zh": "Go-go 年数"},
        "go_go_multiplier": {"en": "Go-go spending multiplier", "zh": "Go-go 支出倍数"},
        "slow_go_years": {"en": "Slow-go years", "zh": "Slow-go 年数"},
        "slow_go_multiplier": {"en": "Slow-go spending multiplier", "zh": "Slow-go 支出倍数"},
        "no_go_years": {"en": "No-go years", "zh": "No-go 年数"},
        "no_go_multiplier": {"en": "No-go spending multiplier", "zh": "No-go 支出倍数"},
        "healthcare_step_up": {"en": "Late-life healthcare step-up", "zh": "晚年医疗支出增量"},
        "years_modeled": {"en": "Years modeled", "zh": "建模年数"},
        "flat_total": {"en": "Flat-spending total", "zh": "固定支出总额"},
        "phase_total": {"en": "Phase-based total", "zh": "分阶段支出总额"},
        "spending_by_age": {"en": "Spending by age", "zh": "按年龄的支出"},
        "phase_averages": {"en": "Phase averages", "zh": "阶段平均值"},
        "detailed_schedule": {"en": "Detailed schedule", "zh": "详细计划表"},
        "caption": {"en": "This is a planning shape tool. It helps avoid the common mistake of assuming retirement spending stays flat forever.", "zh": "这是一个用于规划支出形状的工具。它帮助避免“退休支出永远保持不变”这一常见错误。"}
    },
    "savings_rate": {
        "title": {"en": "Savings Rate / Catch-Up", "zh": "储蓄率 / 追赶储蓄"},
        "subtitle": {"en": "Estimate the annual savings required to reach a target portfolio, and see the tradeoff between saving more and retiring later.", "zh": "估算达到目标资产所需的年度储蓄，并查看多存钱和晚退休之间的权衡。"},
        "target_portfolio": {"en": "Target portfolio", "zh": "目标资产"},
        "projected_portfolio": {"en": "Projected portfolio", "zh": "预计资产"},
        "required_annual_savings": {"en": "Required annual savings", "zh": "所需年度储蓄"},
        "savings_gap": {"en": "Savings gap", "zh": "储蓄缺口"},
        "retire_later": {"en": "Retire 3 years later", "zh": "晚退休 3 年"},
        "tradeoff_ideas": {"en": "Tradeoff ideas", "zh": "权衡建议"},
        "caption": {"en": "This page is intentionally simple: it helps frame the catch-up question quickly before adding taxes or more complex planning assumptions.", "zh": "这个页面有意保持简单：它帮助你在加入税务或更复杂规划假设之前，先快速框定追赶储蓄问题。"}
    },
    "roadmap_page": {
        "title": {"en": "Roadmap", "zh": "路线图"},
        "subtitle": {"en": "Planned calculators and build order for the retirement planning suite.", "zh": "退休规划工具套件的计划计算器与构建顺序。"},
        "missing": {"en": "ROADMAP.md was not found.", "zh": "未找到 ROADMAP.md。"}
    },
}


LEGACY_KEY_MAP = {
    "language": "common.language",
    "english": "common.english",
    "chinese": "common.chinese",
    "suite_title": "suite.title",
    "shared_assumptions": "assumptions.title",
    "shared_assumptions_subtitle": "assumptions.subtitle",
    "scenario_presets": "assumptions.scenario_presets",
    "base": "presets.base",
    "conservative": "presets.conservative",
    "aggressive": "presets.aggressive",
    "early_retirement": "presets.early_retirement",
    "reset_defaults": "assumptions.reset_defaults",
    "download_json": "assumptions.download_json",
    "load_json": "assumptions.load_json",
    "loaded_json_success": "assumptions.loaded_json_success",
    "load_json_error": "assumptions.load_json_error",
    "personal": "assumptions.personal",
    "accounts": "assumptions.accounts",
    "cash_flow": "assumptions.cash_flow",
    "market_tax": "assumptions.market_tax",
    "current_age": "assumptions.current_age",
    "retirement_age": "assumptions.retirement_age",
    "life_expectancy": "assumptions.life_expectancy",
    "filing_status": "assumptions.filing_status",
    "traditional_balance": "assumptions.traditional_balance",
    "roth_balance": "assumptions.roth_balance",
    "taxable_balance": "assumptions.taxable_balance",
    "has_roth_ira": "assumptions.has_roth_ira",
    "has_taxable_brokerage": "assumptions.has_taxable_brokerage",
    "annual_contribution": "assumptions.annual_contribution",
    "annual_retirement_spending": "assumptions.annual_retirement_spending",
    "annual_ss_benefit": "assumptions.annual_ss_benefit",
    "annual_ss_benefit_fra": "assumptions.annual_ss_benefit_fra",
    "ss_claim_age": "assumptions.ss_claim_age",
    "annual_pension_income": "assumptions.annual_pension_income",
    "annual_other_income": "assumptions.annual_other_income",
    "annual_return": "assumptions.annual_return",
    "inflation": "assumptions.inflation",
    "state_tax_rate": "assumptions.state_tax_rate",
    "assumptions_consistent": "assumptions.consistent",
    "total_portfolio": "assumptions.total_portfolio",
    "planned_spending": "assumptions.planned_spending",
    "assumptions_note": "assumptions.note",
    "home_subtitle": "suite.home_subtitle",
    "live_tools": "suite.live_tools",
    "most_complete_page": "suite.most_complete_page",
    "native_sidebar": "suite.native_sidebar",
    "included_apps": "home.included_apps",
    "how_to_use": "home.how_to_use",
    "home_step_1": "home.step_1",
    "home_step_2": "home.step_2",
    "home_step_3": "home.step_3",
    "home_step_4": "home.step_4",
    "home_note": "home.note",
    "current_structure": "home.current_structure",
    "core_planners": "navigation.core_planners",
    "income_withdrawals": "navigation.income_withdrawals",
    "reference": "navigation.reference",
    "roadmap": "navigation.roadmap",
    "page_specific_inputs": "common.page_specific_inputs",
    "using_shared_assumptions": "common.using_shared_assumptions",
    "update_shared_assumptions": "common.update_shared_assumptions",
}


def _resolve_node(path: str) -> dict[str, str] | None:
    node: Any = CATALOG
    for part in path.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node if isinstance(node, dict) else None



def init_i18n() -> None:
    if "language" not in st.session_state:
        st.session_state.language = "en"



def t(key: str, **kwargs: Any) -> str:
    lang = st.session_state.get("language", "en")
    path = LEGACY_KEY_MAP.get(key, key)
    value = _resolve_node(path)
    if value is None:
        text = key
    else:
        text = value.get(lang, value.get("en", key))
    return text.format(**kwargs) if kwargs else text



def section(prefix: str) -> dict[str, str]:
    node = _resolve_node(prefix)
    if node is None:
        return {}
    return {k: t(f"{prefix}.{k}") for k in node.keys() if isinstance(node.get(k), dict)}



def render_language_switch() -> None:
    current = st.session_state.get("language", "en")
    choice = st.sidebar.selectbox(
        t("common.language"),
        options=list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index(current),
        format_func=lambda code: LANGUAGES[code],
        key="language_selector",
    )
    st.session_state.language = choice
