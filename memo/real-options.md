# Real options &mdash; the firewall annex as a financial option

<div class="memo-meta" markdown="1">
<strong>To:</strong> Roche Executive Committee &middot; <strong>From:</strong> Strategic-analysis working group &middot; <strong>Date:</strong> 20 May 2026 &middot; <strong>Read time:</strong> 9 minutes
</div>

## Why this framing exists

The [decision-quality framework](decision-quality.html) treats Item 1 as a probability-weighted lottery. The bottom-up [financial translation](financial-translation.html) defends the underlying CHF impact ranges. This memo adds a third lens: **treating the firewall annex as a real option on a stochastic underlying** (the trajectory of US&ndash;EU reference-pricing contagion). This is the framing a financial-derivatives professional would bring to the same problem &mdash; and it surfaces structure the lottery-based decision-quality framework cannot.

A real option is the right, not the obligation, to take a specific action at a specific cost in the future. The firewall annex meets the definition: Roche commits CHF 5&ndash;8M of working-group resources now (the &ldquo;premium&rdquo;) and *acquires the right* to execute a treaty-level protection structure if pre-conditions clear. The execution requires CHF 8&ndash;12M of additional capital (the &ldquo;strike&rdquo;) and produces protection valued at CHF 18&ndash;55B (the &ldquo;intrinsic value&rdquo; of the option at execution). Like any option, the annex&apos;s pre-execution value depends on (a) the intrinsic value distribution, (b) time to expiration, (c) volatility of the underlying, and (d) interest rate / discount rate assumptions.

This memo computes those values and surfaces three implications conventional decision analysis misses.

## The option specification

Modelled as a European call option (single exercise window) on the contagion-protection payoff:

- **Underlying.** The trajectory of US&ndash;EU reference-pricing contagion, measured as cumulative ex-US net-price erosion over 2027&ndash;2031. Current expected value: CHF 22B of erosion (severe-spillover central case from [financial translation](financial-translation.html)).
- **Strike (K).** The execution cost of the annex: working-group time, USTR back-channel negotiation, GC drafting, SECO coordination, peer-firm peer-test. Estimated CHF 8&ndash;12M; use CHF 10M as central.
- **Premium (paid now).** Working-group resourcing through the 60-day pre-condition window: CHF 5&ndash;8M; use CHF 6.5M as central.
- **Time to expiration.** 60 days for the pre-condition test, then a wider execution window through Q3 2026. Effective $T$: 4 months.
- **Volatility ($\sigma$).** The standard deviation of the contagion trajectory. Working-group estimate: contagion outcomes span CHF 0 (no leakage) to CHF 60B (forced disclosure) with central CHF 22B. Implied annual standard deviation ~CHF 18B, or **~80% of the underlying value &mdash; high-volatility regime**.
- **Risk-free rate (r).** Use 3% for short-dated Swiss government yield (May 2026 indicative).

## Intrinsic value, time value, and total option value

The annex&apos;s value can be decomposed:

**Intrinsic value** = max(0, contagion-protection-captured &minus; strike) at the exercise moment. If executed at central case (CHF 22B protection captured) less strike (CHF 10M), intrinsic value = **CHF 21.99B**. The strike is operationally negligible relative to intrinsic value &mdash; this is *deep-in-the-money* relative to strike.

**Time value** = the premium attributable to the chance that the underlying moves *up* over the option&apos;s life (i.e., contagion turns out more severe than central case, so the annex&apos;s value rises). With 80% volatility and 4-month time to expiration, the time-value component is material: roughly 15&ndash;20% of intrinsic value, or **CHF 3&ndash;4B of additional option value**.

**Total option value** = intrinsic + time value = **CHF 25&ndash;26B** at central case before pre-condition test resolution.

But this central-case point estimate hides the substantive structure. The annex is in fact an option *on whether to commit to* an option (a compound option): the pre-condition test is the first option; execution conditional on the test is the second. Compound option theory gives a different value:

- **Stage-1 option** (60-day pre-condition resourcing): strike CHF 6.5M, payoff = stage-2 option value if pre-conditions clear.
- **Stage-2 option** (formal annex execution): strike CHF 10M, payoff = protection captured if annex ratifies.

The compound structure&apos;s key insight: **the working group&apos;s 60-day budget is itself an option premium**, and the EV of paying the premium depends on the conditional EV of the stage-2 option. This is the financial-options analog of the Bayesian decision rule from [decision-quality](decision-quality.html), but framed as a structured product rather than a lottery.

## Vega &mdash; the option&apos;s sensitivity to contagion volatility

Vega measures option value change per 1-point change in volatility. For the firewall annex:

- Current volatility estimate: 80% (high uncertainty about contagion trajectory).
- If contagion volatility falls to 50% (more confident central forecast): time value drops from CHF 3&ndash;4B to CHF 1.5&ndash;2B; total option value drops to CHF 23&ndash;24B.
- If contagion volatility rises to 110% (e.g., EU policy uncertainty spikes): time value rises to CHF 5&ndash;6B; total option value rises to CHF 27&ndash;28B.

**Implication: the annex is more valuable in high-volatility environments.** Counterintuitively, *bad news about EU policy uncertainty makes the annex more valuable*, not less. The annex is a hedge whose price rises with the underlying threat&apos;s uncertainty &mdash; the canonical option-buyer posture. Two operational consequences:

1. **The annex&apos;s opportunity cost is highest in low-volatility environments.** If May&ndash;July 2026 produces clarity on EU pharmaceutical strategy implementation (volatility falls), the option becomes relatively cheaper to delay. If volatility rises (e.g., AMNOG announces an unexpected confidential-rebate enforcement action), execution urgency rises.

2. **Roche should be a vega buyer, not a vega seller, in adjacent decisions.** Other 2026 commitments that *increase* contagion-trajectory uncertainty (e.g., engaging in EU-level transparency consultations that prolong the policy uncertainty window) raise annex value. Other commitments that *reduce* uncertainty (e.g., publishing Roche-specific net-price data on Roche initiative) lower it. The strategic posture should be vega-long.

## Time value and the cost of waiting

A standard option-pricing result: option time value decays as expiration approaches (theta). For the firewall annex, theta is approximately:

- Each month of delay reduces time value by ~CHF 0.5B (from the CHF 3&ndash;4B base).
- If the 60-day pre-condition test completes on schedule (15 July 2026), time value at execution decision is ~CHF 2.5&ndash;3B.
- If pre-conditions slip and execution is deferred to October 2026, time value at execution is ~CHF 1.5&ndash;2B.
- If execution slips to January 2027 (Branch C territory), time value is ~CHF 0.5&ndash;1B.

**The cost of waiting is CHF 0.5B/month in time-value erosion.** This is the financial-options framing of why Branch C (defer to Q3 2026) has lower NPV than Branches A or B in the decision-quality framework. The CHF 0.5B/month figure is the *quantitative cost of delay* in a frame the financial-trained board member will immediately understand.

## The hedge ratio &mdash; how much annex protection to seek

Standard option-pricing logic: how much of the underlying should be hedged. Roche&apos;s exposed underlying (ex-US revenue at risk of contagion) is **CHF 7.3B/year for high-WAC biologics**, or **CHF 22.3B/year for all ex-US Pharma revenue**.

Three hedge-ratio strategies:

1. **Full hedge** (covers all CHF 22.3B exposure). Requires broad annex scope: confidentiality protection on the entire Roche ex-US portfolio. Execution probability: lower (US side may resist breadth); annex commercial value if executes: maximum (CHF 35&ndash;55B captured).

2. **Targeted hedge** (covers the CHF 7.3B high-WAC biologics). Requires annex scope limited to specific drug classes. Execution probability: higher (narrower scope easier to drft); annex value: CHF 18&ndash;28B.

3. **Catastrophic-only hedge** (covers the difference between gradual spillover and forced disclosure). Requires annex with explicit force-majeure-style triggers. Execution probability: high (US side may even encourage this framing); annex value: CHF 10&ndash;20B but narrowly targeted.

**The Branch A recommendation in the [briefing](briefing.html) implicitly assumes a targeted hedge.** The CHF 18&ndash;55B range is consistent with targeted hedge at lower bound and full hedge at upper bound. **Recommendation: explicitly specify in working-group output which hedge strategy is targeted.** Leaving it ambiguous reduces both execution probability (because USTR cannot evaluate proposal without knowing scope) and value capture (because Roche cannot allocate resources without scope clarity).

## Three things the lottery framing misses

The real-options framing produces three insights the decision-quality lottery framing does not:

**1. The 60-day pre-condition window is a CHF 0.5B/month-worth purchase, not just a procedural step.** Treating it as a procedural gate undervalues the optionality acquired by paying the small premium. The board should authorise the resourcing with explicit recognition that it is buying optionality, not just &ldquo;exploring feasibility.&rdquo;

**2. Roche should be vega-long across adjacent 2026 decisions.** Other strategic commitments that increase contagion-trajectory uncertainty raise annex value. This implies (a) avoid premature commitments on net-price disclosure in any other channel, (b) lean into adjacent uncertainty-increasing moves (industry-coalition engagement at EU level, public-policy uncertainty about pharmaceutical strategy timing).

**3. The hedge strategy should be explicit and singular, not implicit.** &ldquo;Endorse the firewall annex&rdquo; without specifying targeted-vs-full-vs-catastrophic hedge leaves CHF 5&ndash;20B of value on the table through scope ambiguity.

## What this changes for the board

Three implications.

1. **Authorise the CHF 5&ndash;8M working-group resourcing as an option premium, not as &ldquo;exploration funding.&rdquo;** The financial framing makes the asymmetric payoff structure clear and justifies the spend with quantitative rigour.

2. **Add a vega-management instruction to the strategic-communications committee.** Roche&apos;s public-policy positioning across 2026 should be explicitly evaluated for its effect on contagion-trajectory uncertainty. Premature net-price disclosure on any axis is option-destroying.

3. **Specify the hedge strategy in Item 1 endorsement.** Recommend explicit endorsement of the *targeted hedge* (high-WAC biologics scope) as the default, with provision for working-group adaptation to full or catastrophic-only scope based on USTR feedback in the 60-day window.

---

**See also:** [Decision quality](decision-quality.html) &middot; [Hatch-Waxman analog](hatch-waxman.html) &middot; [Financial translation](financial-translation.html) &middot; [Item 1 unpacked](item-1.html) &middot; [Bottom line](bottom-line.html)
