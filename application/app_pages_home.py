#!/usr/bin/env python3
from __future__ import annotations

import streamlit as st

from app_i18n import section, t
from app_ui import render_header, render_note


TOOLS = {
    "en": [
        ("Shared Assumptions", "Set the common retirement facts once and let the other pages reuse them via session state."),
        ("RMD / Roth Conversion Strategy", "Compare conversion vs no-conversion paths and estimate future RMD impact."),
        ("Retirement Readiness", "Estimate whether projected savings and income cover retirement spending."),
        ("Social Security Optimizer", "Compare claiming ages and lifetime benefits with break-even views."),
        ("Medicare IRMAA", "See whether income events trigger IRMAA surcharges and how much room remains."),
        ("Sequence Risk Visualizer", "Show how early bad returns can change retirement outcomes even with the same average return."),
        ("Safe Withdrawal Guardrails", "Compare fixed spending with flexible guardrail-style withdrawals."),
        ("Withdrawal Order", "Test taxable vs traditional vs Roth withdrawal mixes for tax-aware drawdown."),
        ("Spending Smile Planner", "Model spending across go-go, slow-go, and no-go retirement phases."),
        ("Savings Rate / Catch-Up", "Estimate how much more to save if you start later or want to retire earlier."),
    ],
    "zh": [
        ("共享假设", "一次设置通用退休信息，并通过 session state 在其他页面复用。"),
        ("RMD / Roth 转换策略", "比较转换与不转换路径，并估算未来 RMD 影响。"),
        ("退休准备度", "估算预计储蓄和收入是否足以覆盖退休支出。"),
        ("社保优化器", "比较不同领取年龄、终身收益和盈亏平衡情况。"),
        ("Medicare IRMAA", "查看收入事件是否触发 IRMAA 附加费，以及剩余空间。"),
        ("收益顺序风险可视化", "展示在平均收益相同的情况下，前期坏收益如何改变退休结果。"),
        ("安全提款护栏", "比较固定支出与带护栏的灵活提款策略。"),
        ("提款顺序", "测试 taxable、traditional 与 Roth 的提款组合对税务的影响。"),
        ("支出微笑曲线", "按 go-go、slow-go、no-go 阶段建模退休支出。"),
        ("储蓄率 / 追赶储蓄", "估算晚起步或想提前退休时需要增加多少储蓄。"),
    ],
}


def render_page() -> None:
    lang = st.session_state.get("language", "en")
    suite_labels = section("suite")
    home_labels = section("home")
    render_header(
        suite_labels["title"],
        suite_labels["home_subtitle"],
    )

    c1, c2, c3 = st.columns(3)
    c1.metric(suite_labels["live_tools"], "10")
    c2.metric(suite_labels["most_complete_page"], "RMD strategy" if lang == "en" else "RMD 策略")
    c3.metric("Navigation" if lang == "en" else "导航", suite_labels["native_sidebar"])

    col1, col2 = st.columns([1.25, 1.0])
    with col1:
        st.subheader(home_labels["included_apps"])
        for name, description in TOOLS[lang]:
            st.markdown(f"- **{name}** — {description}")

    with col2:
        st.subheader(home_labels["how_to_use"])
        st.markdown(
            f"{home_labels['step_1']}\n"
            f"{home_labels['step_2']}\n"
            f"{home_labels['step_3']}\n"
            f"{home_labels['step_4']}"
        )
        render_note(home_labels["note"])

    st.subheader(home_labels["current_structure"])
    if lang == "en":
        st.markdown(
            "- **Core planners** — readiness, Social Security, RMD strategy, IRMAA, sequence risk\n"
            "- **Income & withdrawals** — guardrails, withdrawal order, spending phases, savings catch-up\n"
            "- **Shared assumptions** — common facts entered once\n"
            "- **Reference** — product roadmap"
        )
    else:
        st.markdown(
            "- **核心规划** — 退休准备度、社保、RMD 策略、IRMAA、收益顺序风险\n"
            "- **收入与提款** — 护栏提款、提款顺序、阶段支出、追赶储蓄\n"
            "- **共享假设** — 一次输入通用信息\n"
            "- **参考** — 产品路线图"
        )
