#!/usr/bin/env python3
from __future__ import annotations

import pandas as pd
import streamlit as st

from app_i18n import section, tooltip
from app_state import render_shared_assumptions_panel
from app_ui import format_currency, format_dataframe, format_percent, money_input, percent_input, render_explainer, render_header, render_note
from roth_conversion_engine import PlanInputs, compare_strategies, project_late_life_metrics, result_rows


def _strategy_label(key: str, zh: bool = False) -> str:
    return {
        "conversion": "Guardrail conversion strategy" if not zh else "护栏式转换策略",
        "bracket_fill_only": "Full bracket-fill strategy" if not zh else "满档转换策略",
        "no_conversion": "No-conversion baseline" if not zh else "不转换基准策略",
    }.get(key, key.replace("_", " ").title())


def _strategy_note_text(key: str, zh: bool) -> str:
    notes = {
        "conversion": (
            "Respects ACA before 65 and IRMAA after 65, so it may stop at 12% even when you choose 22%/24%."
            if not zh
            else "考虑 65 岁前的 ACA 和 65 岁后的 IRMAA，所以即使你选了 22%/24%，也可能停在 12%。"
        ),
        "bracket_fill_only": (
            "Ignores ACA/IRMAA caps and fills the selected bracket ceiling as aggressively as possible."
            if not zh
            else "忽略 ACA / IRMAA 上限，尽可能把所选税档填满。"
        ),
        "no_conversion": (
            "No Roth conversions at all." if not zh else "完全不做 Roth 转换。"
        ),
    }
    return notes[key]


def _strategy_banner_label(key: str, zh: bool) -> str:
    return _strategy_label(key, zh)


def _bold_recommended_column(col: pd.Series, recommended_label: str) -> list[str]:
    style = "font-weight: bold; background-color: rgba(15, 118, 110, 0.08);" if col.name == recommended_label else ""
    return [style for _ in col]


def _set_selected_strategy(strategy_key: str) -> None:
    st.session_state["rmd_selected_strategy"] = strategy_key
    st.session_state["rmd_selected_strategy_source"] = "banner"


def render_page() -> None:
    zh = st.session_state.get("language", "en") == "zh"
    common = section("common")
    assumptions = section("assumptions")
    labels = section("rmd")
    render_header(labels["title"], labels["subtitle"])
    render_explainer(common["about_tool"], labels["about_body"])

    render_shared_assumptions_panel(common, assumptions)

    with st.sidebar:
        st.divider()
        st.header(common["page_specific_inputs"])
        target_bracket = st.selectbox(labels["target_bracket"], options=["12%", "22%", "24%", "32%"], key="rmd_target_bracket", help=tooltip("rmd", "target_bracket"))
        use_aca_model = st.checkbox(labels["aca"], key="rmd_use_aca_model", help=tooltip("rmd", "aca"))
        use_irmaa_model = st.checkbox(labels["irmaa"], key="rmd_use_irmaa_model", help=tooltip("rmd", "irmaa"))

    current_age = int(st.session_state.current_age)
    retirement_age = int(st.session_state.retirement_age)
    current_401k_balance = float(st.session_state.traditional_balance)
    annual_contribution = float(st.session_state.annual_contribution)
    annual_retirement_spending = float(st.session_state.annual_retirement_spending)
    filing_status = str(st.session_state.filing_status)
    current_roth_balance = float(st.session_state.roth_balance)
    current_taxable_balance = float(st.session_state.taxable_balance)
    has_roth_ira = current_roth_balance > 0
    has_taxable_brokerage = current_taxable_balance > 0
    annual_other_income = float(st.session_state.annual_other_income)
    annual_pension_income = float(st.session_state.annual_pension_income)
    social_security_claim_age = int(st.session_state.social_security_claim_age)
    annual_social_security_benefit = float(st.session_state.annual_social_security_benefit)
    annual_return = float(st.session_state.annual_return)
    state_tax_rate = float(st.session_state.state_tax_rate)
    life_expectancy = int(st.session_state.life_expectancy)

    inputs = PlanInputs(
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

    results = compare_strategies(inputs)
    scenario_map = dict(results)
    scenario_order = [key for key in ["conversion", "bracket_fill_only", "no_conversion"] if key in scenario_map]
    scenario_order.extend([key for key in scenario_map.keys() if key not in scenario_order])
    scenario_labels = {key: _strategy_label(key, zh) for key in scenario_map}

    recommended_key = min(scenario_map, key=lambda key: scenario_map[key].total_cost_to_life_expectancy)
    if st.session_state.get("rmd_selected_strategy") not in scenario_map:
        st.session_state["rmd_selected_strategy"] = recommended_key

    savings = scenario_map["no_conversion"].total_cost_to_life_expectancy - scenario_map[recommended_key].total_cost_to_life_expectancy if "no_conversion" in scenario_map else 0.0

    comparison_df = pd.DataFrame(
        [
            {
                "strategy": key,
                "scenario": scenario_labels[key],
                "traditional_at_75": plan.traditional_balance_at_75,
                "roth_at_75": plan.roth_balance_at_75,
                "taxable_at_75": plan.taxable_balance_at_75,
                "rmd_at_75": plan.estimated_rmd_at_75,
                "federal_tax_total": plan.total_federal_tax_to_life_expectancy,
                "state_tax_total": plan.total_state_tax_to_life_expectancy,
                "aca_drag_total": plan.total_aca_drag_to_life_expectancy,
                "irmaa_total": plan.total_irmaa_to_life_expectancy,
                "total_cost": plan.total_cost_to_life_expectancy,
            }
            for key, plan in ((key, scenario_map[key]) for key in scenario_order)
        ]
    ).set_index("strategy")
    comparison_display_df = format_dataframe(
        comparison_df.copy(),
        currency_columns=["traditional_at_75", "roth_at_75", "taxable_at_75", "rmd_at_75", "federal_tax_total", "state_tax_total", "aca_drag_total", "irmaa_total", "total_cost"],
    )

    st.subheader(labels.get("strategy_notes", "Strategy notes" if not zh else "策略说明"))
    strategy_banner_cols = st.columns(3)
    current_selected = st.session_state.get("rmd_selected_strategy", recommended_key)
    for col, key in zip(strategy_banner_cols, scenario_order):
        with col:
            with st.container(border=True):
                st.button(
                    _strategy_banner_label(key, zh),
                    width="stretch",
                    type="primary" if current_selected == key else "secondary",
                    key=f"rmd_strategy_banner_{key}",
                    on_click=_set_selected_strategy,
                    args=(key,),
                )
                st.markdown(
                    f"<div style='min-height: 4.5rem; font-size: 0.92rem; color: rgba(250,250,250,0.78);'>{_strategy_note_text(key, zh)}</div>",
                    unsafe_allow_html=True,
                )

    render_note(
        f"I’d recommend **{scenario_labels[recommended_key]}** here because it has the lowest modeled total cost ({format_currency(scenario_map[recommended_key].total_cost_to_life_expectancy)})."
        if not zh
        else f"我会推荐 **{scenario_labels[recommended_key]}**，因为它的模型估算总成本最低（{format_currency(scenario_map[recommended_key].total_cost_to_life_expectancy)}）。"
    )

    selected_strategy = st.session_state.get("rmd_selected_strategy", recommended_key)
    selected_plan = scenario_map[selected_strategy]
    selected_df = pd.DataFrame(result_rows(selected_plan))
    savings = scenario_map["no_conversion"].total_cost_to_life_expectancy - selected_plan.total_cost_to_life_expectancy if "no_conversion" in scenario_map else 0.0

    total_roth_conversions = sum(row.recommended_conversion for row in selected_plan.yearly)
    late_life = project_late_life_metrics(
        selected_plan.traditional_balance_at_75,
        selected_plan.roth_balance_at_75,
        selected_plan.taxable_balance_at_75,
        inputs,
        {row.age: (row.gross_income) for row in selected_plan.yearly},
    )
    weighted_avg_cost = (
        sum(row.recommended_conversion * float(row.effective_marginal_bracket.rstrip("%")) / 100.0 for row in selected_plan.yearly if row.recommended_conversion > 0)
        / total_roth_conversions
        if total_roth_conversions
        else 0.0
    )

    baseline_plan = scenario_map.get("no_conversion", selected_plan)

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    st.caption(f"Key metrics showing: {scenario_labels[selected_strategy]}" if not zh else f"关键指标显示：{scenario_labels[selected_strategy]}")
    c1.metric(labels["rmd_conv"], format_currency(selected_plan.estimated_rmd_at_75), help="Estimated required minimum distribution at age 75 for the selected strategy." if not zh else "所选策略在 75 岁时的预估最低强制提款（RMD）。")
    c2.metric(labels["rmd_base"], format_currency(baseline_plan.estimated_rmd_at_75), help="Estimated RMD at age 75 under the no-conversion baseline." if not zh else "不做转换基准策略在 75 岁时的预估 RMD。")
    c3.metric(labels["trad75"], format_currency(selected_plan.traditional_balance_at_75), help="Projected traditional IRA / 401(k) balance at age 75." if not zh else "75 岁时预估的传统 IRA / 401(k) 余额。")
    c4.metric("Total cost", format_currency(selected_plan.total_cost_to_life_expectancy), help="Estimated lifetime taxes + ACA drag + IRMAA for this strategy." if not zh else "该策略的预估终身税费 + ACA 拖累 + IRMAA。")
    c5.metric(labels.get("total_roth_conversions", "Total Roth conversions"), format_currency(total_roth_conversions), help="Total Roth conversions recommended over the modeled years." if not zh else "模型期内建议执行的 Roth 转换总额。")
    c6.metric(labels["savings"], format_currency(savings), help="Estimated savings versus the no-conversion baseline." if not zh else "相较于不转换基准策略的预估节省。")

    st.caption(
        f"Using shared assumptions: age {current_age}, retire at {retirement_age}, {format_currency(current_401k_balance)} traditional, {format_currency(current_roth_balance)} Roth, {format_currency(current_taxable_balance)} taxable, and {format_percent(annual_return)} annual return."
        if not zh
        else f"使用共享假设：当前年龄 {current_age}，退休年龄 {retirement_age}，traditional {format_currency(current_401k_balance)}，Roth {format_currency(current_roth_balance)}，taxable {format_currency(current_taxable_balance)}，年化收益率 {format_percent(annual_return)}。"
    )

    overview_tab, path_tab, detail_tab, comparison_tab = st.tabs([labels["overview"], labels["balance_path"], labels["annual_detail"], labels["strategy_comparison"]])

    with overview_tab:
        st.caption(f"Selected: {scenario_labels[st.session_state.get('rmd_selected_strategy', recommended_key)]}")

        before_ss_df = selected_df[selected_df["age"] < social_security_claim_age]
        after_ss_before_rmd_df = selected_df[(selected_df["age"] >= social_security_claim_age) & (selected_df["age"] < 75)]
        after_rmd_years = max(0, life_expectancy - 74)
        stage_summary = pd.DataFrame(
            [
                {
                    "stage": "A：社保前" if zh else "A: before SS",
                    "age_range": f"{retirement_age}-{max(retirement_age, social_security_claim_age - 1)}",
                    "years": len(before_ss_df),
                    "total_conversion": before_ss_df["recommended_conversion"].sum(),
                    "avg_annual_conversion": before_ss_df["recommended_conversion"].mean() if len(before_ss_df) else 0.0,
                },
                {
                    "stage": "B：社保后、RMD 前" if zh else "B: after SS before RMD",
                    "age_range": f"{max(retirement_age, social_security_claim_age)}-74",
                    "years": len(after_ss_before_rmd_df),
                    "total_conversion": after_ss_before_rmd_df["recommended_conversion"].sum(),
                    "avg_annual_conversion": after_ss_before_rmd_df["recommended_conversion"].mean() if len(after_ss_before_rmd_df) else 0.0,
                },
                {
                    "stage": "C：RMD 后" if zh else "C: after RMD",
                    "age_range": f"75-{life_expectancy}",
                    "years": after_rmd_years,
                    "total_conversion": 0.0,
                    "avg_annual_conversion": 0.0,
                },
            ]
        ).rename(columns={
            "stage": "阶段" if zh else "Stage",
            "age_range": "年龄区间" if zh else "Age range",
            "years": "年数" if zh else "Years",
            "total_conversion": "转换总额" if zh else "Total conversion",
            "avg_annual_conversion": "年均转换" if zh else "Avg annual conversion",
        })
        st.subheader(labels["stage_summary"])
        st.dataframe(
            format_dataframe(
                stage_summary,
                currency_columns=["转换总额" if zh else "Total conversion", "年均转换" if zh else "Avg annual conversion"],
                integer_columns=["年数" if zh else "Years"],
            ),
            width="stretch",
            hide_index=True,
        )

        with st.expander(labels.get("interpretation_summary", "结果解读摘要" if zh else "Interpretation summary"), expanded=True):
            if zh:
                st.markdown(
                    f"本情景累计 Roth Conversion 约 {format_currency(total_roth_conversions)}，按转换额加权平均边际成本(也就是每 1 美元 Roth 转换的平均税率)约 {format_percent(weighted_avg_cost)}。\n\n"
                    f"RMD 开始（75 岁）时 IRA 约 {format_currency(selected_plan.traditional_balance_at_75)}，当年 RMD 约 {format_currency(selected_plan.estimated_rmd_at_75)}。\n\n"
                    f"模拟期最高 RMD 约 {format_currency(late_life['max_rmd'])}；最高 MAGI 约 {format_currency(late_life['max_magi'])}。\n\n"
                    f"到 {life_expectancy} 岁：Roth {format_currency(late_life['roth'])}，IRA {format_currency(late_life['traditional'])}，Taxable {format_currency(late_life['taxable'])}。"
                )
            else:
                st.markdown(
                    f"This scenario totals about {format_currency(total_roth_conversions)} of Roth conversions, with a conversion-weighted average marginal cost (the average tax rate paid per $1 of Roth conversion) of about {format_percent(weighted_avg_cost)}.\n\n"
                    f"At RMD start (age 75), IRA is about {format_currency(selected_plan.traditional_balance_at_75)} and the first RMD is about {format_currency(selected_plan.estimated_rmd_at_75)}.\n\n"
                    f"Peak RMD during the simulation is about {format_currency(late_life['max_rmd'])}; peak MAGI is about {format_currency(late_life['max_magi'])}.\n\n"
                    f"At age {life_expectancy}: Roth {format_currency(late_life['roth'])}, IRA {format_currency(late_life['traditional'])}, Taxable {format_currency(late_life['taxable'])}."
                )

    with comparison_tab:
        st.subheader(labels["strategy_comparison"])
        st.caption(f"Selected: {scenario_labels[selected_strategy]}")
        comparison_transposed = comparison_df.copy().transpose()
        comparison_transposed.columns = [scenario_labels[key] for key in comparison_transposed.columns]
        comparison_transposed.index = [
            {
                "scenario": "Scenario",
                "traditional_at_75": labels["trad75"],
                "roth_at_75": "Roth balance at 75" if not zh else "75 岁 Roth 余额",
                "taxable_at_75": "Taxable balance at 75" if not zh else "75 岁 Taxable 余额",
                "rmd_at_75": "RMD at 75" if not zh else "75 岁 RMD",
                "federal_tax_total": "Federal tax total" if not zh else "联邦税总额",
                "state_tax_total": "State tax total" if not zh else "州税总额",
                "aca_drag_total": "ACA drag total" if not zh else "ACA 拖累总额",
                "irmaa_total": "IRMAA total" if not zh else "IRMAA 总额",
                "total_cost": "Total cost",
            }.get(idx, idx)
            for idx in comparison_transposed.index
        ]
        comparison_transposed_display = comparison_transposed.copy()
        for row_label in comparison_transposed_display.index:
            if row_label != "Scenario":
                comparison_transposed_display.loc[row_label] = comparison_transposed_display.loc[row_label].map(format_currency)
        st.dataframe(
            comparison_transposed_display.style.apply(_bold_recommended_column, axis=0, recommended_label=scenario_labels[recommended_key]),
            width="stretch",
            hide_index=False,
        )

    with path_tab:
        chart_df = selected_df[["age", "recommended_conversion", "end_traditional", "end_roth", "end_taxable"]].set_index("age")
        st.subheader(labels["ladder_path"])
        st.line_chart(chart_df)

    with detail_tab:
        st.subheader(labels["annual_path"])
        detail_df = selected_df[[
            "age",
            "filing_status",
            "spending_need",
            "spending_from_taxable",
            "ltcg",
            "end_taxable",
            "dividends",
            "end_traditional",
            "rmd",
            "social_security_gross",
            "social_security_taxable",
            "recommended_conversion",
            "end_roth",
            "magi",
            "estimated_federal_tax",
            "ltcg_tax",
            "niit_tax",
            "total_tax",
            "tax_paid_from_taxable",
            "tax_paid_from_roth",
            "irmaa_surcharge",
            "effective_marginal_bracket",
            "total_assets",
            "start_taxable",
            "start_traditional",
            "start_roth",
            "gross_income",
            "estimated_state_tax",
            "aca_subsidy_loss",
        ]].rename(columns={
            "age": "年龄" if zh else "Age",
            "filing_status": "申报" if zh else "Filing",
            "spending_need": "开支" if zh else "Spending",
            "spending_from_taxable": "Taxable取款" if zh else "Taxable draw",
            "ltcg": "LTCG",
            "end_taxable": "Taxable余额" if zh else "Ending taxable",
            "dividends": "股息" if zh else "Dividends",
            "end_traditional": "IRA余额" if zh else "Ending IRA",
            "rmd": "RMD",
            "social_security_gross": "SS",
            "social_security_taxable": "应税SS" if zh else "Taxable SS",
            "recommended_conversion": "转换" if zh else "Conversion",
            "end_roth": "Roth余额" if zh else "Ending Roth",
            "magi": "MAGI",
            "estimated_federal_tax": "普通税" if zh else "Ordinary tax",
            "ltcg_tax": "LTCG税" if zh else "LTCG tax",
            "niit_tax": "NIIT",
            "total_tax": "总税" if zh else "Total tax",
            "tax_paid_from_taxable": "税从Taxable" if zh else "Tax from taxable",
            "tax_paid_from_roth": "税从Roth" if zh else "Tax from Roth",
            "irmaa_surcharge": "Medicare",
            "effective_marginal_bracket": "边际成本" if zh else "Marginal cost",
            "total_assets": "总资产" if zh else "Total assets",
            "start_taxable": "期初Taxable" if zh else "Starting taxable",
            "start_traditional": "期初IRA" if zh else "Starting IRA",
            "start_roth": "期初Roth" if zh else "Starting Roth",
            "gross_income": "普通收入" if zh else "Ordinary income",
            "estimated_state_tax": "州税" if zh else "State tax",
            "aca_subsidy_loss": "ACA拖累" if zh else "ACA drag",
        })
        st.dataframe(
            format_dataframe(
                detail_df,
                currency_columns=[
                    "开支" if zh else "Spending",
                    "Taxable取款" if zh else "Taxable draw",
                    "LTCG",
                    "Taxable余额" if zh else "Ending taxable",
                    "股息" if zh else "Dividends",
                    "IRA余额" if zh else "Ending IRA",
                    "RMD",
                    "SS",
                    "应税SS" if zh else "Taxable SS",
                    "转换" if zh else "Conversion",
                    "Roth余额" if zh else "Ending Roth",
                    "MAGI",
                    "普通税" if zh else "Ordinary tax",
                    "LTCG税" if zh else "LTCG tax",
                    "NIIT",
                    "总税" if zh else "Total tax",
                    "税从Taxable" if zh else "Tax from taxable",
                    "税从Roth" if zh else "Tax from Roth",
                    "Medicare",
                    "总资产" if zh else "Total assets",
                    "期初Taxable" if zh else "Starting taxable",
                    "期初IRA" if zh else "Starting IRA",
                    "期初Roth" if zh else "Starting Roth",
                    "普通收入" if zh else "Ordinary income",
                    "州税" if zh else "State tax",
                    "ACA拖累" if zh else "ACA drag",
                ],
            ),
            width="stretch",
        )

        st.download_button(
            "Download annual detail CSV",
            data=detail_df.to_csv(index=False).encode("utf-8"),
            file_name=f"rmd_{selected_strategy}_annual_detail.csv",
            mime="text/csv",
        )

        st.caption(
            f"Showing annual detail for: {scenario_labels[selected_strategy]}"
            if not zh
            else f"当前年度明细显示：{scenario_labels[selected_strategy]}"
        )
        st.caption(
            "注：上表已尽量补齐所请求列。当前模型还没有真正建模 Taxable 资本利得、股息、LTCG 税、NIIT，且年度路径在 75 岁前不做真实 RMD 计算，所以这些列目前大多为 0。"
            if zh
            else "Note: the table now includes as many requested columns as the current model supports. The engine does not yet truly model taxable-account capital gains, dividends, LTCG tax, NIIT, or live RMDs in the pre-75 annual path, so those columns are currently mostly zero."
        )

    st.caption(labels["caption"])
