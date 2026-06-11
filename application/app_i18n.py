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
        "about_tool": {"en": "What is this tool?", "zh": "这个工具是做什么的？"},
        "shared_inputs": {"en": "Shared assumptions for this tool", "zh": "本工具的共享假设"},
        "page_specific_inputs": {"en": "Page-specific inputs", "zh": "页面专用输入"},
        "using_shared_assumptions": {"en": "This page uses shared assumptions", "zh": "本页面使用共享假设"},
        "update_shared_assumptions": {"en": "Update balances and annual spending on the Shared Assumptions page.", "zh": "请在“共享假设”页面更新余额和年度支出。"},
        "yes": {"en": "yes", "zh": "是"},
        "no": {"en": "no", "zh": "否"},
    },
    "suite": {
        "title": {"en": "Retirement Planning, Demystified", "zh": "退休规划，化繁为简"},
        "home_subtitle": {
            "en": "A simple retirement planning workspace that helps you think through the big questions — how much to save, when to retire, when to claim Social Security, and how to make the money last.",
            "zh": "一个简单的退休规划空间，帮助你理清几个重要问题——要存多少、何时退休、何时领取社保，以及如何让资金撑得更久。",
        },
        "live_tools": {"en": "Live tools", "zh": "可用工具"},
        "most_complete_page": {"en": "Most complete page", "zh": "最完整页面"},
        "native_sidebar": {"en": "Left menu", "zh": "左侧菜单"},
    },
    "assumptions": {
        "title": {"en": "Shared Assumptions", "zh": "共享假设"},
        "subtitle": {
            "en": "Set the common planning inputs here once. The other pages use the same numbers automatically, so you do not have to keep entering them again.",
            "zh": "在这里一次性设置通用规划输入。其他页面会自动使用同一组数字，所以你不必反复输入。",
        },
        "scenario_presets": {"en": "Scenario presets", "zh": "情景预设"},
        "scenario_comparison": {"en": "Scenario comparison", "zh": "情景对比"},
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
        "annual_contribution": {"en": "Annual pre-retirement contribution to IRA/401K", "zh": "退休前年度税前IRA/401K投入"},
        "annual_retirement_spending": {"en": "Annual retirement spending", "zh": "退休后年度支出"},
        "annual_ss_benefit": {"en": "Annual Social Security benefit (planned actual)", "zh": "年度社保收入（按计划实际领取）"},
        "annual_ss_benefit_fra": {"en": "Annual Social Security benefit at FRA (baseline)", "zh": "FRA 时年度社保收入（基准）"},
        "ss_claim_age": {"en": "Social Security claim age", "zh": "社保领取年龄"},
        "annual_pension_income": {"en": "Annual pension income", "zh": "年度养老金收入"},
        "annual_other_income": {"en": "Annual other ordinary income", "zh": "年度其他普通收入"},
        "annual_return": {"en": "Annual return", "zh": "年化收益率"},
        "inflation": {"en": "Inflation", "zh": "通胀率"},
        "state_tax_rate": {"en": "State tax rate", "zh": "州税率"},
        "consistent": {"en": "Assumptions look internally consistent.", "zh": "这些假设在内部看起来是一致的。"},
        "total_portfolio": {"en": "Total investable portfolio", "zh": "总投资资产"},
        "planned_spending": {"en": "Planned annual spending", "zh": "计划年度支出"},
        "about_body": {
            "en": "**1) Concept**\n\nThis is the shared planning profile for the whole app. Retirement tools all depend on the same baseline facts: age, balances, spending, income, return assumptions, and tax assumptions.\n\n**2) What this tool is about**\n\nThis page is where you define those baseline facts once so the rest of the app can reuse them. It acts as the common foundation behind the other calculators.\n\n**3) How to use it**\n\nEnter your best estimates in the controls below. Age, balances, spending, income, return assumptions, and tax assumptions all flow into the other tools, so better inputs here make every calculator more useful.",
            "zh": "**1) 概念**\n\n这是整个应用共用的规划档案。所有退休工具都依赖同一套基础事实：年龄、账户余额、支出、收入、收益假设和税务假设。\n\n**2) 这个工具是做什么的**\n\n这个页面让你先定义这套基础事实，后面其他计算器都会复用它。它相当于整个应用的共同底座。\n\n**3) 如何使用**\n\n先在下面输入你认为最接近现实的数字。年龄、余额、支出、收入、收益假设和税务假设都会流向其他工具，所以这里越准确，后面的计算器越有用。"
        },
        "note": {
            "en": "These values stay saved for this browser session. You can reset everything to defaults, download the current assumptions to JSON, or load a saved JSON file back into the app.",
            "zh": "这些值会保存在当前浏览器会话中。你现在可以重置为默认值、下载当前假设为 JSON，或把已保存的 JSON 重新加载回应用。",
        },
        "help": {
            "current_age": {"en": "Your age today. The app uses this as the starting point for all retirement timing and growth projections.", "zh": "你现在的年龄。应用会用它作为所有退休时间线和资产增长预测的起点。"},
            "retirement_age": {"en": "The age when you stop regular work and begin relying on portfolio income, Social Security, pension income, or withdrawals.", "zh": "你停止常规工作、开始依赖投资组合收入、社保、养老金或提款的年龄。"},
            "life_expectancy": {"en": "The planning horizon for the model. It is not a prediction of your actual lifespan, just how long the plan should try to last.", "zh": "模型使用的规划终点年龄。它不是对真实寿命的预测，只是计划需要撑多久的假设。"},
            "filing_status": {"en": "Tax filing status used for tax brackets, IRMAA thresholds, and some retirement-income rules.", "zh": "用于税档、IRMAA 门槛和部分退休收入规则的报税身份。"},
            "traditional_balance": {"en": "Current balance in pre-tax retirement accounts such as a traditional IRA or 401(k). Withdrawals from these accounts are usually taxable.", "zh": "传统 IRA、401(k) 等税前退休账户的当前余额。这类账户提款通常要缴普通所得税。"},
            "roth_balance": {"en": "Current balance in Roth accounts. Qualified withdrawals are generally tax-free in retirement.", "zh": "Roth 账户的当前余额。符合条件的退休提款通常免税。"},
            "taxable_balance": {"en": "Current balance in taxable investment accounts, such as a brokerage account held outside retirement wrappers.", "zh": "普通应税投资账户的当前余额，比如退休账户之外的券商账户。"},
            "annual_contribution": {"en": "How much you expect to keep contributing each year before retirement to your traditional retirement accounts.", "zh": "你预计在退休前每年继续投入到传统退休账户的金额。"},
            "annual_retirement_spending": {"en": "Your planned yearly spending once retired. Use an all-in estimate that includes normal living costs and discretionary spending.", "zh": "你退休后的年度计划支出。建议用包含日常生活和可选消费在内的全年总额。"},
            "annual_ss_benefit_fra": {"en": "Estimated annual Social Security benefit if you claim at full retirement age (FRA). The app uses this as the baseline to estimate benefits at other claim ages.", "zh": "如果在完全退休年龄（FRA）领取时的年度社保金额。应用会把它当作基准，推算其他领取年龄的社保金额。"},
            "ss_claim_age": {"en": "The age when you plan to start Social Security. Earlier claiming lowers the benefit; later claiming usually increases it up to age 70.", "zh": "你计划开始领取社保的年龄。提早领取会降低金额，延后领取通常会提高金额，最多到 70 岁。"},
            "annual_ss_benefit": {"en": "The app-calculated annual Social Security amount based on your FRA benefit and claim age. It updates automatically and is read-only here.", "zh": "应用根据 FRA 金额和领取年龄自动计算出的年度社保收入。这里会自动更新，为只读字段。"},
            "annual_pension_income": {"en": "Expected annual pension income in retirement, if any. Enter 0 if you do not expect a pension.", "zh": "退休后预计每年的养老金收入。如果没有养老金，就填 0。"},
            "annual_other_income": {"en": "Other ordinary annual income expected in retirement, such as part-time work, annuity income, rental income taxed as ordinary income, or interest.", "zh": "退休后预计的其他年度普通收入，比如兼职收入、年金收入、按普通收入征税的租金收入或利息。"},
            "annual_return": {"en": "Expected long-term annual investment return before inflation. Use a realistic planning assumption, not a best-case number.", "zh": "通胀前的长期年化投资回报假设。建议使用现实的规划假设，而不是最乐观数字。"},
            "inflation": {"en": "Expected yearly inflation rate used to increase future spending needs and translate nominal values into real spending power.", "zh": "用于抬高未来支出需求、并把名义金额换算为实际购买力的年度通胀假设。"},
            "state_tax_rate": {"en": "Estimated marginal state income tax rate applied in the planning model. Use 0 if your state has no income tax or you want to ignore it for now.", "zh": "规划模型里使用的州边际所得税率估算。如果所在州没有所得税，或你暂时不想计入，就填 0。"}
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
        "step_1": {"en": "1. Choose a page from the menu on the left.", "zh": "1. 从左侧菜单选择一个页面。"},
        "step_2": {"en": "2. Start with Shared Assumptions to enter the common facts once.", "zh": "2. 先从“共享假设”开始，一次性输入通用信息。"},
        "step_3": {"en": "3. Open a calculator and adjust only the settings for that page.", "zh": "3. 打开某个计算页面，只调整该页面专有的设置。"},
        "step_4": {"en": "4. Move between pages without re-entering the same facts.", "zh": "4. 在不同页面之间切换时，无需重复输入相同信息。"},
        "note": {
            "en": "The common facts stay with you as you move around, so each page can focus on one question at a time.",
            "zh": "这些通用信息会一直保留，这样每个页面就能专注回答一个问题。",
        },
        "current_structure": {"en": "Current structure", "zh": "当前结构"},
    },
    "navigation": {
        "getting_started": {"en": "Getting started", "zh": "从这里开始"},
        "basic_tools": {"en": "Basic tools", "zh": "基础工具"},
        "advanced_tools": {"en": "Advanced tools", "zh": "进阶工具"},
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
        "total_roth_conversions": {"en": "Total Roth conversions", "zh": "Roth 转换总额"},
        "overview": {"en": "Overview", "zh": "概览"},
        "balance_path": {"en": "Balance path", "zh": "余额路径"},
        "annual_detail": {"en": "Annual detail", "zh": "年度明细"},
        "strategy_comparison": {"en": "Strategy comparison", "zh": "策略对比"},
        "stage_summary": {"en": "Three-stage conversion summary", "zh": "三阶段转换摘要"},
        "rmd_age_75": {"en": "RMD at age 75", "zh": "75 岁 RMD"},
        "ladder_path": {"en": "Conversion ladder and balance path", "zh": "转换阶梯与余额路径"},
        "annual_path": {"en": "Annual conversion path", "zh": "年度转换路径"},
        "about_body": {
            "en": "**1) Concept**\n\nRMDs are required minimum distributions — the IRS forces money out of traditional tax-deferred accounts later in retirement. That matters because RMDs can raise taxable income, push you into a higher bracket, and increase taxes on Social Security or Medicare premiums. Roth conversions can help reduce future RMDs by moving money into a tax-free bucket earlier.\n\n**2) What this tool is about**\n\nThis tool compares a conversion path with a no-conversion path. Its core strategy is to convert just enough each year from traditional accounts into Roth to fill up a chosen tax bracket ceiling, while also showing when ACA subsidy loss or IRMAA surcharges may make extra income more expensive. The goal is to show whether paying some tax earlier through Roth conversions may reduce later RMD pressure and improve your long-term retirement outcome.\n\n**3) How to use it**\n\nUse the controls on the left to set the target bracket and any ACA/IRMAA toggles, then compare conversion vs. no-conversion paths. A higher target bracket usually means more aggressive conversions, while the ACA and IRMAA switches help show when extra income might create hidden costs. The page shows how much tax you may pay now, how RMDs may change later, and whether the conversion strategy improves the long-term picture for your retirement plan.",
            "zh": "**1) 概念**\n\nRMD 是 required minimum distribution（最低强制提款）。到了后期，IRS 会要求你从传统递延税账户中取钱。它之所以重要，是因为 RMD 会抬高应税收入、可能把你推入更高税档，还可能影响社保税和 Medicare 保费。提前做 Roth 转换，可以把一部分钱移到免税账户，从而降低未来 RMD。\n\n**2) 这个工具是做什么的**\n\n这个工具比较“做转换”和“不做转换”两条路径。它的核心策略是：每年从传统账户向 Roth 转换刚好足以填满你设定的目标税档上限，同时提示 ACA 补贴损失或 IRMAA 附加费何时会让额外收入变得更贵。它的目的，是帮助你判断：通过更早做 Roth 转换提前交税，是否能降低未来 RMD 压力，并改善退休长期结果。\n\n**3) 如何使用**\n\n用左侧的控制项设定目标税档，以及是否考虑 ACA / IRMAA，再比较“做转换”和“不做转换”两条路径。目标税档越高，通常代表转换越激进；ACA 和 IRMAA 开关则帮助你看到额外收入可能带来的隐藏成本。这个页面会展示你现在可能多交多少税、未来 RMD 可能怎么变化，以及这个策略是否能改善退休长期结果。"
        },
        "caption": {"en": "Planning approximation only. Verify actual tax execution with CPA or tax software.", "zh": "仅供规划近似使用。实际执行前请用 CPA 或报税软件复核。"},
        "help": {
            "target_bracket": {"en": "Choose the highest federal marginal bracket you are willing to fill with Roth conversions in a given year.", "zh": "选择你愿意通过 Roth 转换填满的最高联邦边际税档。"},
            "aca": {"en": "If checked, the model estimates potential ACA subsidy loss before age 65 when higher income makes health coverage more expensive.", "zh": "勾选后，模型会估算 65 岁前因收入提高而导致 ACA 医保补贴减少的潜在成本。"},
            "irmaa": {"en": "If checked, the model estimates Medicare IRMAA surcharges after 65 when income rises above key thresholds.", "zh": "勾选后，模型会估算 65 岁后因收入超过门槛而产生的 Medicare IRMAA 附加费。"}
        },
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
        "about_body": {
            "en": "**1) Concept**\n\nRetirement readiness is the question of whether your savings and expected income can support your spending for as long as you need. The core idea is simple: growth, contributions, spending, inflation, and retirement income all have to work together.\n\n**2) What this tool is about**\n\nThis tool gives you a quick first-pass estimate of whether your current path appears sufficient. It turns your assumptions into a projected nest egg and compares that with expected retirement spending.\n\n**3) How to use it**\n\nUse the withdrawal rate control on the left as a stress test. A higher rate makes the plan look less durable, while a lower rate makes it look safer. The page estimates your projected portfolio path and compares it with planned retirement spending, so you can quickly see whether you look underfunded, roughly on track, or comfortably ahead.",
            "zh": "**1) 概念**\n\n退休准备度要回答的是：你的储蓄和预计收入，能不能支撑你需要的退休支出。核心很简单：资产增长、持续储蓄、支出、通胀和退休收入必须一起配合。\n\n**2) 这个工具是做什么的**\n\n这个工具给你一个快速的第一层判断：按照你现在的路径，退休计划看起来够不够。它会把你的假设转成预计退休资产，并和预期退休支出做比较。\n\n**3) 如何使用**\n\n把左侧的提款率控制项当成压力测试。更高的提款率会让计划看起来更脆弱，更低的提款率会让计划看起来更安全。这个页面会估算你的资产轨迹，并与退休支出做对比，让你快速判断自己是偏不足、基本打平，还是比较充裕。"
        },
        "caption": {"en": "This version is still deterministic. It now shows both nominal and inflation-adjusted growth, but it still does not model taxes or volatility.", "zh": "这个版本仍是确定性模型。它现在展示名义增长和通胀调整后的增长，但仍未建模税务或波动率。"},
        "help": {
            "withdrawal_rate": {"en": "The percentage of your retirement portfolio you assume can be withdrawn each year to support spending. Higher rates make the plan look less conservative.", "zh": "你假设每年可以从退休投资组合中提取用于支出的比例。比例越高，计划看起来越不保守。"}
        },
    },
    "social_security": {
        "title": {"en": "Social Security Optimizer", "zh": "社保优化器"},
        "subtitle": {"en": "Compare claiming ages, annual benefits, and simple lifetime payout tradeoffs.", "zh": "比较领取年龄、年度收益和简单的终身领取权衡。"},
        "annual_ss_benefit_fra": {"en": "Annual Social Security benefit at FRA (baseline)", "zh": "FRA 时年度社保收入（基准）"},
        "longevity_age": {"en": "Longevity age for comparison", "zh": "比较用寿命年龄"},
        "highlight_age": {"en": "Highlight claim age", "zh": "高亮领取年龄"},
        "best_age": {"en": "Best claim age", "zh": "最佳领取年龄"},
        "best_lifetime": {"en": "Best lifetime benefit", "zh": "最佳终身收益"},
        "annual_vs_lifetime": {"en": "Annual vs lifetime benefits", "zh": "年度 vs 终身收益"},
        "quick_read": {"en": "Quick read", "zh": "快速解读"},
        "comparison": {"en": "Claiming comparison", "zh": "领取对比"},
        "about_body": {
            "en": "**1) Concept**\n\nSocial Security is an inflation-adjusted lifetime income stream, and the claiming age changes the monthly benefit a lot. Claiming early gives you cash sooner but usually at a lower monthly amount; waiting usually increases the check and can help protect against longevity risk.\n\n**2) What this tool is about**\n\nThis tool compares claiming ages and their tradeoffs. It helps you see not just which age gives the highest lifetime total in the model, but also how monthly income changes across choices.\n\n**3) How to use it**\n\nUse the controls on the left to set your longevity horizon and the age you want highlighted, then compare claiming ages side by side. A longer longevity age makes delayed claiming look more valuable, while the highlight age helps you focus on the age you care about most. This helps you weigh monthly cash flow, lifetime income, and the practical tradeoff between starting earlier versus waiting for a larger benefit.",
            "zh": "**1) 概念**\n\n社保是一种带通胀调整的终身收入，而领取年龄会显著影响每月金额。提前领取能更早拿到现金，但通常每月更少；晚一点领取则通常能拿到更高金额，也更能对冲长寿风险。\n\n**2) 这个工具是做什么的**\n\n这个工具比较不同领取年龄及其取舍。它不仅帮助你看模型里哪个年龄的终身总额更高，也帮助你看到每月收入会如何变化。\n\n**3) 如何使用**\n\n用左侧的控制项设定寿命比较年龄，以及你想高亮的领取年龄，再并排比较不同领取年龄。比较的寿命年龄越长，延迟领取看起来越有价值；高亮年龄则帮助你聚焦自己最关心的那个年龄。这能帮助你权衡每月现金流、终身收入，以及“早点开始”和“等更高金额”之间的实际取舍。"
        },
        "caption": {"en": "This MVP uses simplified claiming factors and ignores taxation, COLA details, spousal benefits, and discount rates.", "zh": "这个 MVP 使用了简化的领取系数，未纳入税务、COLA、配偶收益和贴现率。"},
        "help": {
            "longevity_age": {"en": "The age through which the tool compares total lifetime Social Security payouts. A longer horizon usually makes delayed claiming look better.", "zh": "工具用来比较社保终身总领取额的寿命终点。比较期越长，延后领取通常看起来越有利。"}
        },
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
        "about_body": {
            "en": "**1) Concept**\n\nIRMAA is the income-related monthly adjustment amount: a Medicare surcharge that kicks in when your income is high enough. It matters because extra income from Roth conversions, bonuses, capital gains, or withdrawals can raise your Medicare premiums later.\n\n**2) What this tool is about**\n\nThis tool is a threshold checker. It shows whether an income event pushes you into a more expensive Medicare premium tier and how much headroom you have left.\n\n**3) How to use it**\n\nEnter a one-time extra income amount in the controls on the left and see whether it crosses a threshold. Larger income values can push you into a higher IRMAA tier, so this helps you judge whether a Roth conversion or other income move may create hidden Medicare costs.",
            "zh": "**1) 概念**\n\nIRMAA 是 income-related monthly adjustment amount，也就是 Medicare 的收入附加费。只要收入高到一定程度，就会触发这个附加费。它很重要，因为 Roth 转换、奖金、资本利得或提款都可能在之后抬高 Medicare 保费。\n\n**2) 这个工具是做什么的**\n\n这个工具本质上是一个档位检查器。它会显示某个收入事件是否会把你推入更贵的 Medicare 保费档位，以及你距离当前上限还剩多少空间。\n\n**3) 如何使用**\n\n在左侧输入一次性的额外收入，看看它是否跨过档位。收入越高，越可能进入更高的 IRMAA 档位，所以这能帮助你判断 Roth 转换或其他收入动作会不会带来隐藏的 Medicare 成本。"
        },
        "caption": {"en": "This page uses the same 2026 threshold table as the conversion model. Real Medicare billing uses lookback rules and other details.", "zh": "该页面使用与转换模型相同的 2026 档位表。真实 Medicare 计费还涉及回溯规则和其他细节。"},
        "help": {
            "extra_income": {"en": "A one-time extra income amount to test, such as a Roth conversion, bonus, capital gain, or large withdrawal that could push MAGI into a higher IRMAA tier.", "zh": "用于测试的一次性额外收入，比如 Roth 转换、奖金、资本利得或大额提款，这些都可能把 MAGI 推入更高的 IRMAA 档位。"}
        },
    },
    "sequence": {
        "title": {"en": "Sequence of Returns Risk", "zh": "收益顺序风险"},
        "subtitle": {"en": "Use the same average return set in different orders and watch retirement outcomes split apart.", "zh": "用相同的平均收益集合，但改变顺序，观察退休结果如何分化。"},
        "bad_early": {"en": "Ending balance: bad early", "zh": "前期差回报情景的期末余额"},
        "bad_late": {"en": "Ending balance: bad late", "zh": "后期差回报情景的期末余额"},
        "difference": {"en": "Difference", "zh": "差额"},
        "paths": {"en": "Portfolio paths", "zh": "资产路径"},
        "details": {"en": "Scenario details", "zh": "情景详情"},
        "about_body": {
            "en": "**1) Concept**\n\nSequence risk means the order of returns matters. Two portfolios can have the same average return, but the one that suffers losses early in retirement can be hurt much more because withdrawals happen while the balance is down.\n\n**2) What this tool is about**\n\nThis tool is a visual comparison of two return paths with the same average return set but different ordering. Its job is to make sequence risk easy to see instead of just describing it in theory.\n\n**3) How to use it**\n\nThere are no inputs here; the page uses a fixed return sequence so you can compare a bad-early path against a bad-late path. This helps you understand why spending flexibility, cash buffers, or withdrawal timing can matter so much once retirement withdrawals begin.",
            "zh": "**1) 概念**\n\n收益顺序风险的意思是：收益出现的先后顺序很重要。两个组合可能平均收益一样，但如果前期差回报出现在退休早期，伤害会更大，因为那时你还在提款，账户更难恢复。\n\n**2) 这个工具是做什么的**\n\n这个工具把两条平均收益相同、但顺序不同的路径放在一起可视化比较。它的作用，是把收益顺序风险从理论说明变成直观感受。\n\n**3) 如何使用**\n\n这里没有可调输入；页面使用固定的收益序列，方便你对比“前期先出现差回报”和“后期才出现差回报”的路径。这样你就能更直观看到，为什么退休开始提款后，支出弹性、现金缓冲和提款时点会变得很重要。"
        },
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
        "about_body": {
            "en": "**1) Concept**\n\nSafe withdrawal planning is about balancing lifestyle and portfolio survival. A fixed spending rule is simple, but a flexible rule can sometimes help the portfolio last longer by reducing withdrawals when markets are weak and allowing a bit more when markets are strong.\n\n**2) What this tool is about**\n\nThis tool compares a fixed-withdrawal approach against a guardrails approach. It is meant to show the tradeoff between steadier spending and better portfolio resilience.\n\n**3) How to use it**\n\nUse the floor and ceiling controls on the left to decide when spending should flex. A lower floor makes the plan more aggressive about increasing withdrawals, while a tighter ceiling forces cuts sooner. Compare the fixed path with the guardrail path to see how much spending flexibility might improve ending balances or total withdrawals in a rough retirement simulation.",
            "zh": "**1) 概念**\n\n安全提款规划的核心，是在生活质量和资产寿命之间找平衡。固定支出最简单，但灵活规则有时能在市场较弱时少取一点、在市场较强时多取一点，从而延长资产寿命。\n\n**2) 这个工具是做什么的**\n\n这个工具比较固定提款方式和护栏提款方式。它的重点，是让你看到“支出更平稳”和“资产更有韧性”之间的取舍。\n\n**3) 如何使用**\n\n用左侧的上下护栏控制项决定支出何时该变化。更低的下护栏会让计划更积极地增加提款，更紧的上护栏则会更早迫使你削减支出。把固定路径和护栏路径对比一下，看看更灵活的支出是否能改善期末余额或总提款。"
        },
        "caption": {"en": "This is a simple illustrative guardrails model, not a complete Guyton-Klinger or VPW implementation.", "zh": "这是一个用于说明概念的简化护栏模型，不是完整的 Guyton-Klinger 或 VPW 实现。"},
        "help": {
            "lower_guardrail": {"en": "If the current withdrawal rate falls below this level, the model treats spending as flexible enough to step up modestly.", "zh": "如果当前提款率低于这个水平，模型会认为支出可以适度上调。"},
            "upper_guardrail": {"en": "If the current withdrawal rate rises above this level, the model treats spending as needing a cut to protect the portfolio.", "zh": "如果当前提款率高于这个水平，模型会认为需要削减支出来保护投资组合。"}
        }
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
        "about_body": {
            "en": "**1) Concept**\n\nWithdrawal order matters because different account types are taxed differently. Taxable, traditional, and Roth accounts each have different tax rules, so the sequence you withdraw from can change taxes today and the flexibility you keep for later.\n\n**2) What this tool is about**\n\nThis tool compares a few simple withdrawal sequences in a one-year snapshot. Its purpose is to show how taxes and ending balances shift when you pull from different account buckets first.\n\n**3) How to use it**\n\nThis page uses your shared assumptions balances, so make sure those are realistic before comparing orders. Compare a few simple drawdown orders and see which one creates the lowest estimated tax in this one-year snapshot. It is a starting point for thinking about tax-aware retirement spending, not a full optimization engine.",
            "zh": "**1) 概念**\n\n提款顺序很重要，因为不同账户的税务规则不同。taxable、traditional 和 Roth 账户各有不同税法，所以提款顺序会影响现在的税负，也会影响未来保留的灵活性。\n\n**2) 这个工具是做什么的**\n\n这个工具在“一年快照”里比较几种简单提款顺序。它的作用，是让你看到先从不同账户取钱时，税负和期末余额会怎么变化。\n\n**3) 如何使用**\n\n这个页面使用你的共享假设余额，所以在比较顺序前先确认这些数字是现实的。对比几种简单的提款顺序，看看在这一年的快照里，哪一种估算税负最低。它适合作为税务友好型退休支出的起点，但还不是完整的优化引擎。"
        },
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
        "about_body": {
            "en": "**1) Concept**\n\nRetirement spending is often not flat. Many retirees spend more in active early years, less in slower middle years, and potentially more later because healthcare costs rise. A spending smile tries to capture that shape.\n\n**2) What this tool is about**\n\nThis tool turns that spending-smile idea into a simple year-by-year model. It helps you visualize how different life phases can change your retirement spending path.\n\n**3) How to use it**\n\nAdjust the go-go, slow-go, and no-go phase lengths and spending multipliers in the controls on the left to match your own expected lifestyle. Higher early multipliers raise first-years spending, while a bigger healthcare step-up increases late-life costs. The chart helps you turn a vague idea about changing spending into a concrete yearly schedule.",
            "zh": "**1) 概念**\n\n退休支出通常不是一条直线。很多人在退休初期更活跃、花得更多；中期放缓；后期因为医疗成本上升，支出可能再次增加。支出微笑曲线就是用来模拟这种形状。\n\n**2) 这个工具是做什么的**\n\n这个工具把“支出微笑曲线”变成一个简单的逐年模型。它帮助你可视化不同人生阶段如何改变退休支出路径。\n\n**3) 如何使用**\n\n在左侧调整 go-go、slow-go、no-go 三个阶段的年数和支出倍数，以匹配你的生活方式。前期倍数越高，前几年支出越大；医疗增量越高，晚年成本越高。这个图能把“支出会变化”这种模糊想法，变成具体的年度计划。"
        },
        "caption": {"en": "This is a planning shape tool. It helps avoid the common mistake of assuming retirement spending stays flat forever.", "zh": "这是一个用于规划支出形状的工具。它帮助避免“退休支出永远保持不变”这一常见错误。"},
        "help": {
            "go_go_years": {"en": "How many early retirement years you expect to stay active and spend above baseline levels.", "zh": "你预计退休早期还会比较活跃、支出高于基线的年数。"},
            "go_go_multiplier": {"en": "Multiplier applied to baseline spending during the go-go years. For example, 1.15 means spending 15% above baseline.", "zh": "应用于 go-go 阶段基线支出的倍数。比如 1.15 表示比基线高 15%。"},
            "slow_go_years": {"en": "How many middle retirement years you expect spending to settle into a slower lifestyle phase.", "zh": "你预计退休中期进入较慢生活节奏、支出趋稳的年数。"},
            "slow_go_multiplier": {"en": "Multiplier applied to baseline spending during the slow-go years.", "zh": "应用于 slow-go 阶段基线支出的倍数。"},
            "no_go_years": {"en": "How many later retirement years you expect to spend in the no-go phase.", "zh": "你预计退休后期处于 no-go 阶段的年数。"},
            "no_go_multiplier": {"en": "Multiplier applied to baseline spending during the no-go years before any healthcare step-up is added.", "zh": "在加入晚年医疗增量之前，应用于 no-go 阶段基线支出的倍数。"},
            "healthcare_step_up": {"en": "Additional annual spending added in later life to reflect rising healthcare or care-related costs.", "zh": "晚年额外增加的年度支出，用来反映更高的医疗或照护成本。"}
        }
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
        "about_body": {
            "en": "**1) Concept**\n\nSavings rate is the bridge between where you are now and the retirement target you want. If your current savings path is too slow, you either need a higher annual contribution, a better return assumption, or more time.\n\n**2) What this tool is about**\n\nThis tool estimates the catch-up effort needed to reach a target. It shows how much more you may need to save each year, and it also illustrates the effect of giving yourself more time.\n\n**3) How to use it**\n\nSet the target portfolio in the controls on the left, then compare the extra annual savings needed to hit it. A higher target needs more savings, a higher return assumption lowers the required contribution, and more years to retirement make the goal easier to reach. It also shows the effect of retiring a little later, which is often the simplest tradeoff.",
            "zh": "**1) 概念**\n\n储蓄率决定了你从现在走向退休目标的速度。如果当前储蓄路径太慢，你就需要提高年度储蓄、改善收益假设，或者多给自己一点时间。\n\n**2) 这个工具是做什么的**\n\n这个工具估算为了达到目标，你需要补多少“追赶力度”。它会展示你每年可能还要多存多少，也会说明多给自己几年时间会有什么影响。\n\n**3) 如何使用**\n\n在左侧设定目标资产，再比较要达到它还需要多存多少。目标越高，需要的储蓄越多；收益假设越高，所需年度储蓄越低；距离退休的年数越长，目标越容易实现。它也会展示晚一点退休的效果，这通常是最直接的取舍之一。"
        },
        "caption": {"en": "This page is intentionally simple: it helps frame the catch-up question quickly before adding taxes or more complex planning assumptions.", "zh": "这个页面有意保持简单：它帮助你在加入税务或更复杂规划假设之前，先快速框定追赶储蓄问题。"},
        "help": {
            "target_portfolio": {"en": "The portfolio size you want to reach by retirement. The tool uses this to estimate the annual savings required from here to that goal.", "zh": "你希望在退休时达到的投资组合规模。工具会据此估算从现在到目标所需的年度储蓄。"}
        }
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
    "annual_social_security_benefit_fra": "assumptions.annual_ss_benefit_fra",
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
        st.session_state.language = "zh"



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
    return {
        k: t(f"{prefix}.{k}")
        for k, value in node.items()
        if isinstance(value, dict) and ("en" in value or "zh" in value)
    }


def tooltip(prefix: str, key: str) -> str | None:
    lang = st.session_state.get("language", "en")
    value = _resolve_node(f"{prefix}.help.{key}")
    if value is None:
        return None
    return value.get(lang, value.get("en"))



def render_language_switch() -> None:
    current = st.session_state.get("language", "en")
    choice = st.sidebar.radio(
        t("common.language"),
        options=list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index(current),
        format_func=lambda code: "🇺🇸 English" if code == "en" else "🇨🇳 中文",
        key="language_selector",
        horizontal=True,
    )
    st.session_state.language = choice
