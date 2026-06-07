# Retirement Planning Web App Roadmap

## Goal
Build a useful suite of retirement planning calculators that cover the main questions people actually revisit:
- Am I on track?
- When can I retire?
- How should I claim Social Security?
- How do I avoid unnecessary taxes?
- How do I turn assets into stable retirement income?
- What can go wrong, and how sensitive is the plan?

---

## Suggested build order

### Phase 1 - Core traffic and utility
These are the best first apps because they solve common problems and have broad appeal.

#### 1) Retirement income gap / readiness calculator
**Why it matters:**
The most universal retirement question is whether someone is on track.

**Core inputs:**
- Current age / retirement age
- Current savings by account type
- Annual contributions
- Expected annual spending in retirement
- Social Security estimate
- Pension / other income
- Inflation assumption
- Pre-retirement and post-retirement return assumptions

**Outputs:**
- Projected nest egg at retirement
- Estimated monthly/annual retirement income
- Income shortfall or surplus
- Probability bands / scenario ranges
- “Need to save X more per month” guidance

**MVP notes:**
- Keep assumptions editable but simple
- Add optimistic / base / conservative scenarios
- Focus on clarity over Monte Carlo complexity in v1

---

#### 2) Social Security claiming optimizer
**Why it matters:**
This is one of the highest-interest retirement tools and drives repeat usage.

**Core inputs:**
- Birth year
- FRA
- Estimated PIA / monthly benefit at FRA
- Desired claim age
- Spouse age / benefit if applicable
- Longevity assumptions
- Discount / inflation assumptions

**Outputs:**
- Monthly benefit at 62 / FRA / 70
- Lifetime benefit comparison by claim age
- Break-even age charts
- Spousal / survivor comparison where applicable

**MVP notes:**
- Start with single-person modeling
- Add married / survivor logic in v2
- Include plain-English warnings about breakeven uncertainty

---

#### 3) Roth conversion planner
**Why it matters:**
This is a high-value tax planning tool, especially before RMD age.

**Status:**
There is already app work in this project around Roth conversion, so this should be treated as an active pillar rather than a future idea.

**Core inputs:**
- Current age / retirement age / RMD start age
- Traditional IRA / 401(k) balances
- Roth balances
- Taxable assets / cash available to pay tax
- Annual income before conversion
- Filing status
- Tax bracket assumptions
- Future return assumptions

**Outputs:**
- Suggested annual conversion ranges
- Marginal tax bracket fill analysis
- Future RMD reduction estimate
- Lifetime tax comparison with and without conversions

**MVP notes:**
- Prioritize bracket-filling workflows
- Show year-by-year conversion ladder visuals
- Keep assumptions transparent and editable

---

#### 4) Tax-aware withdrawal order calculator
**Why it matters:**
Many retirees want help deciding which accounts to draw from first.

**Core inputs:**
- Taxable / tax-deferred / Roth balances
- Annual spending need
- Tax filing status
- Capital gains basis info
- Social Security and pension income
- Target tax bracket / guardrail settings

**Outputs:**
- Suggested drawdown sequence by year
- Estimated taxes by strategy
- Account depletion timeline
- Comparison of naive vs tax-aware strategy

**MVP notes:**
- Start with rule-based heuristics
- Later add optimization logic across multiple years

---

#### 5) Sequence-of-returns risk visualizer
**Why it matters:**
This is a strong educational app and can be very shareable.

**Core inputs:**
- Starting portfolio
- Withdrawal rate / amount
- Time horizon
- Average return assumption
- Volatility or scenario set

**Outputs:**
- Comparison of identical average return with different return order
- Portfolio survival charts
- Worst-case vs best-case outcomes
- Visual explanation of early-loss risk

**MVP notes:**
- Make this visual and intuitive
- Use preset scenarios first, Monte Carlo later

---

## Phase 2 - Deep planning tools
These add real value for people already in or near retirement.

#### 6) Safe withdrawal / guardrails simulator
**Why it matters:**
People want a more realistic answer than a fixed 4% rule.

**Core inputs:**
- Starting balance
- Spending target
- Equity / bond allocation
- Return assumptions
- Guardrail parameters
- Floor and ceiling withdrawal limits

**Outputs:**
- Fixed withdrawal vs dynamic guardrail comparison
- Portfolio survival estimates
- Spending adjustment frequency
- Historical or simulated scenario outcomes

**MVP notes:**
- Support 4% baseline and one dynamic method first
- Add Guyton-Klinger / VPW variants later

---

#### 7) Medicare IRMAA cliff calculator
**Why it matters:**
This is highly actionable for retirees doing Roth conversions or large gain realizations.

**Core inputs:**
- Filing status
- MAGI estimate
- Conversion amount / capital gain / income event
- Relevant IRMAA thresholds by year

**Outputs:**
- Whether IRMAA threshold is triggered
- Incremental Medicare premium impact
- “Safe remaining room” before next cliff

**MVP notes:**
- Keep this fast and simple
- Great candidate for embedding inside the Roth conversion tool as well

---

#### 8) Retirement budget / spending smile planner
**Why it matters:**
Retirement spending usually changes over time, and static spending assumptions are often wrong.

**Core inputs:**
- Retirement age
- Base annual spending
- Travel / lifestyle phase assumptions
- Healthcare cost growth
- Late-life care assumptions

**Outputs:**
- Spending by phase: go-go, slow-go, no-go
- Lifetime spending curve
- Comparison to flat-spending assumption

**MVP notes:**
- Use editable phase templates
- Pair well with readiness and withdrawal tools

---

#### 9) Required savings rate / catch-up calculator
**Why it matters:**
Good for younger users and late starters.

**Core inputs:**
- Current age
- Target retirement age
- Current savings
- Desired retirement income or portfolio target
- Contribution assumptions
- Return assumptions

**Outputs:**
- Required monthly savings
- Catch-up contribution estimate
- Delay-retirement vs save-more tradeoff

**MVP notes:**
- Very easy to build
- Good top-of-funnel tool for broad audiences

---

## Phase 3 - Niche but valuable advanced tools
These are useful differentiators once the core suite exists.

#### 10) Longevity / long-term care scenario planner
**Why it matters:**
People underestimate how much very long lifespans and care costs can change outcomes.

**Core inputs:**
- Longevity scenarios
- Healthcare inflation assumptions
- LTC event probability / cost ranges
- Existing insurance coverage

**Outputs:**
- Portfolio impact under long-life scenarios
- Asset depletion risk under care events
- Sensitivity analysis

**MVP notes:**
- Start deterministic, not actuarial-heavy
- Keep the focus on scenario stress testing

---

#### 11) Annuity vs DIY drawdown comparer
**Why it matters:**
Useful for people deciding whether to exchange assets for guaranteed income.

**Core inputs:**
- Premium amount
- Quoted annuity payout
- Age / spouse details
- Alternative portfolio return assumptions
- Inflation assumptions

**Outputs:**
- Income comparison
- Breakeven longevity estimate
- Liquidity tradeoff analysis
- Legacy / bequest comparison

**MVP notes:**
- Use simple SPIA-style comparison first
- Add deferred income and joint-life cases later

---

#### 12) Asset location optimizer
**Why it matters:**
Helpful for tax efficiency, though less emotionally compelling than claiming or income tools.

**Core inputs:**
- Balances by account type
- Asset classes
- Expected yields / turnover assumptions
- Tax rates

**Outputs:**
- Suggested asset placement across taxable / traditional / Roth
- Estimated tax drag reduction

**MVP notes:**
- Best positioned as an advanced planning helper
- Could later integrate with withdrawal and Roth tools

---

## Product packaging ideas
Instead of shipping these as isolated calculators forever, the suite could evolve into a few clear product buckets:

### Track A: Accumulation
- Required savings rate / catch-up calculator
- Retirement income gap / readiness calculator

### Track B: Retirement transition
- Social Security claiming optimizer
- Roth conversion planner
- IRMAA calculator

### Track C: Decumulation
- Withdrawal order calculator
- Safe withdrawal / guardrails simulator
- Spending smile planner
- Sequence-of-returns visualizer

### Track D: Advanced scenarios
- Longevity / LTC planner
- Annuity vs DIY drawdown comparer
- Asset location optimizer

---

## Recommended roadmap priorities
If the goal is to maximize usefulness and momentum, this is the order I’d recommend:

1. Retirement income gap / readiness calculator
2. Social Security claiming optimizer
3. Roth conversion planner
4. IRMAA calculator
5. Tax-aware withdrawal order calculator
6. Sequence-of-returns risk visualizer
7. Safe withdrawal / guardrails simulator
8. Spending smile planner
9. Required savings rate / catch-up calculator
10. Longevity / LTC scenario planner
11. Annuity vs DIY drawdown comparer
12. Asset location optimizer

---

## Best near-term MVP lineup
If you want a strong initial web app collection, these first five make the most sense:
- Retirement readiness calculator
- Social Security optimizer
- Roth conversion planner
- IRMAA calculator
- Sequence-of-returns visualizer

That set gives you:
- one broad planning tool
- one high-interest decision tool
- one high-value tax tool
- one practical Medicare tax trap tool
- one educational / engagement tool

---

## Build principles
- Prefer simple, transparent assumptions over black-box complexity
- Show comparisons, not just one “answer”
- Keep tax assumptions editable by year where possible
- Use charts heavily; retirement planning is easier to trust when visual
- Make every calculator exportable or shareable
- Reuse a common assumptions panel across the suite
- Add clear disclaimers that tools are educational, not tax/legal/financial advice

---

## Nice future extension
Once several calculators exist, combine them into a unified retirement planning workspace where a user enters core facts once and reuses them across:
- readiness
- Social Security
- Roth conversion
- withdrawals
- IRMAA
- longevity stress tests

That would be much more compelling than a loose pile of standalone calculators.
