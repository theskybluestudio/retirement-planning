#!/usr/bin/env python3
from __future__ import annotations

import streamlit as st

from app_i18n import section
from app_ui import render_header, render_note


TOOLS = {
    "en": {
        "Getting started": [
            ("Home", "A quick tour of the app and how it fits together."),
            ("Shared Assumptions", "Set the common retirement facts once and let the other pages reuse them."),
            ("Feedback", "Open the GitHub project and share bugs, ideas, or suggestions."),
        ],
        "Basic tools": [
            ("Retirement Readiness", "Estimate whether projected savings and income cover retirement spending."),
            ("Social Security Optimizer", "Compare claiming ages and lifetime benefits with break-even views."),
            ("Savings Rate / Catch-Up", "Estimate how much more to save if you start later or want to retire earlier."),
            ("Spending Smile Planner", "Model spending across go-go, slow-go, and no-go retirement phases."),
            ("Mega Backdoor Roth", "Estimate current-year after-tax 401(k) room available for Mega Backdoor Roth contributions."),
        ],
        "Advanced tools": [
            ("RMD / Roth Conversion Strategy", "Compare conversion vs no-conversion paths and estimate future RMD impact."),
            ("Medicare IRMAA", "See whether income events trigger IRMAA surcharges and how much room remains."),
            ("Sequence Risk Visualizer", "Show how early bad returns can change retirement outcomes even with the same average return."),
            ("Safe Withdrawal Guardrails", "Compare fixed spending with flexible guardrail-style withdrawals."),
            ("Withdrawal Order", "Test taxable vs traditional vs Roth withdrawal mixes for tax-aware drawdown."),
        ],
    },
    "zh": {
        "从这里开始": [
            ("首页", "快速了解这个应用，以及它怎么配合使用。"),
            ("共享假设", "一次设置通用退休信息，并让其他页面复用。"),
            ("反馈", "打开 GitHub 项目并提交 bug、想法或建议。"),
        ],
        "基础工具": [
            ("退休准备度", "估算预计储蓄和收入是否足以覆盖退休支出。"),
            ("社保优化器", "比较不同领取年龄、终身收益和盈亏平衡情况。"),
            ("储蓄率 / 追赶储蓄", "估算晚起步或想提前退休时需要增加多少储蓄。"),
            ("支出微笑曲线", "按 go-go、slow-go、no-go 阶段建模退休支出。"),
            ("Mega Backdoor Roth", "估算本年度还能进行多少税后 401(k) 供款并转入 Mega Backdoor Roth。"),
        ],
        "进阶工具": [
            ("RMD / Roth 转换策略", "比较转换与不转换路径，并估算未来 RMD 影响。"),
            ("Medicare IRMAA", "查看收入事件是否触发 IRMAA 附加费，以及剩余空间。"),
            ("收益顺序风险可视化", "展示在平均收益相同的情况下，前期差回报如何改变退休结果。"),
            ("安全提款护栏", "比较固定支出与带护栏的灵活提款策略。"),
            ("提款顺序", "测试 taxable、traditional 与 Roth 的提款组合对税务的影响。"),
        ],
    },
}


SEO_COPY = {
    "en": {
        "what_it_is": "This is a retirement planning calculator suite for people who want practical answers about retirement readiness, Social Security timing, Roth conversions, Medicare IRMAA, withdrawal strategy, and sequence risk.",
        "why_it_matters": "If you're searching for a retirement planning calculator, this page is the best entry point: one place to explore the most common retirement decisions and move into the tool that matches your question.",
        "search_terms": "Common searches this app covers: retirement planning calculator, retirement readiness calculator, Social Security claiming calculator, Roth conversion calculator, IRMAA calculator, safe withdrawal rate calculator, and withdrawal order calculator.",
        "faq": [
            ("Is this a financial advice tool?", "No. It is an educational planning tool for estimates and comparisons, not tax, legal, investment, or financial advice."),
            ("Do I need to re-enter the same facts on every page?", "No. Shared assumptions keep the main numbers in one place so the calculators can reuse them."),
            ("What should I start with?", "Start with Shared Assumptions, then open the calculator for the decision you want to test."),
            ("Does this app cover Roth conversions and RMD planning?", "Yes. The app includes an RMD / Roth Conversion Strategy page plus Medicare IRMAA checks and other retirement income tools."),
        ],
    },
    "zh": {
        "what_it_is": "这是一个退休规划计算器套件，适合想快速了解退休准备度、社保领取时点、Roth 转换、Medicare IRMAA、提款策略和收益顺序风险的人。",
        "why_it_matters": "如果你在找退休规划计算器，这一页就是最好的入口：在一个地方浏览最常见的退休决策，并进入对应工具。",
        "search_terms": "本应用覆盖的常见搜索词包括：退休规划计算器、退休准备度计算器、社保领取计算器、Roth 转换计算器、IRMAA 计算器、安全提款率计算器和提款顺序计算器。",
        "faq": [
            ("这是理财建议工具吗？", "不是。它是用于估算和比较的教育性规划工具，不构成税务、法律、投资或财务建议。"),
            ("每个页面都要重复输入同样的信息吗？", "不用。共享假设会把主要数字保存在一个地方，让各计算器复用。"),
            ("应该先从哪里开始？", "先打开“共享假设”，再进入你想测试的具体计算器。"),
            ("这个应用包含 Roth 转换和 RMD 规划吗？", "包含。应用里有 RMD / Roth 转换策略页面，也有 Medicare IRMAA 和其他退休收入工具。"),
        ],
    },
}


def render_page() -> None:
    lang = st.session_state.get("language", "en")
    suite_labels = section("suite")
    home_labels = section("home")
    nav_labels = section("navigation")
    render_header(
        suite_labels["title"],
        suite_labels["home_subtitle"],
    )

    col1, col2 = st.columns([1.25, 1.0])
    with col1:
        render_note(home_labels["privacy_note"])
        st.markdown(f"**{SEO_COPY[lang]['what_it_is']}**")
        st.markdown(SEO_COPY[lang]["why_it_matters"])
        st.subheader(home_labels["included_apps"])
        for group_label, items in TOOLS[lang].items():
            st.markdown(f"**{group_label}**")
            for name, description in items:
                st.markdown(f"- **{name}** — {description}")

        st.markdown(f"### {suite_labels['live_tools']}")
        st.markdown(SEO_COPY[lang]["search_terms"])

    with col2:
        st.subheader(home_labels["how_to_use"])
        st.markdown(
            f"{home_labels['step_1']}\n"
            f"{home_labels['step_2']}\n"
            f"{home_labels['step_3']}\n"
            f"{home_labels['step_4']}"
        )
        render_note(home_labels["note"])

        st.markdown("### FAQ")
        for question, answer in SEO_COPY[lang]["faq"]:
            with st.expander(question):
                st.markdown(answer)
