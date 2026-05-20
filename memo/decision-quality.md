# Decision quality &mdash; the firewall annex as a probability-weighted bet

<div class="memo-meta" markdown="1">
<strong>To:</strong> Roche Executive Committee &middot; <strong>From:</strong> Strategic-analysis working group &middot; <strong>Date:</strong> 20 May 2026 &middot; <strong>Read time:</strong> 10 minutes
</div>

## Why this exists

The [bottom-line analysis](bottom-line.html) frames three structural asymmetries. The [briefing](briefing.html) puts them in front of the board as four agenda items with four response branches. What is missing &mdash; and what good decision-making requires &mdash; is the **explicit probability &times; outcome math** that translates "Branch A has the highest upside" into a defensible expected-utility ranking under stated uncertainty.

This memo does that for **Item 1 (the firewall annex)**, the highest-stakes board decision. The same framework is then sketched for Items 2 and 3.

**Read this as a decision-quality discipline, not a forecast.** The probabilities below are the working group&apos;s best subjective estimates from the May 2026 information set. The framework&apos;s value is that it makes those estimates explicit and revisable: a board member who disagrees with any probability can substitute their own and re-run the math. If the recommended decision changes under reasonable alternative probability sets, the recommendation is fragile; if it persists, it is robust.

## The four branches as conditional lotteries

Item 1 (firewall annex endorsement) is best modelled not as a single decision but as a sequence: the board endorses one of four branches; pre-condition tests then resolve over 60 days; execution proceeds (or does not) based on test outcomes. The expected utility of each branch is therefore:

$$ EU(\text{branch}) = P(\text{execute} \mid \text{branch}) \times NPV(\text{annex captured}) + P(\text{fail} \mid \text{branch}) \times NPV(\text{outcome on failure}) $$

The four branches differ in (a) what conditional probability of execution they imply, (b) what annex scope they target, and (c) what failure mode they create.

### Branch A &mdash; Endorse all four items

**P(execute) ~ 30% (range 20&ndash;40%).** Branch A requires all four pre-conditions favourable within 60 days. Pre-conditions and rough conditional probabilities:

| Pre-condition | P(favourable in 60 days) |
| --- | --- |
| 1. USTR back-channel sounding produces positive signal | 35&ndash;55% |
| 2. Peer-firm peer-test confirms no rival annex undermines | 60&ndash;75% |
| 3. SECO Federal Council MRA-transfer memo lands clean | 60&ndash;80% |
| 4. No 2026 election-year backlash on confidentiality language | 50&ndash;70% |

Pre-conditions are positively correlated (favourable USTR posture predicts favourable backlash absence; SECO clarity predicts peer-firm alignment). Joint probability under positive correlation: **~25&ndash;40%**, centred at 30%.

- *NPV if executes:* CHF 25&ndash;40B over 2027&ndash;2031 (reference-pricing contagion blocked at central case; upside if forced-disclosure tail also averted).
- *NPV if fails:* CHF &minus;1 to &minus;2B sunk cost (working-group time, USTR back-channel relationships, GC memo investment).
- *Expected utility:* **0.30 &times; CHF 32.5B + 0.70 &times; CHF &minus;1.5B = +CHF 8.7B.**

### Branch B &mdash; Conditional endorsement

**P(execute) ~ 50% (range 40&ndash;60%).** Branch B endorses contingent on pre-conditions clearing &mdash; the board commits to *try* but does not pre-commit to *execute* under all pre-condition outcomes. This raises P(execute | pre-conditions favourable) because the implementation team can adapt the annex scope to the pre-condition findings. Effectively requires 3 of 4 pre-conditions favourable rather than 4 of 4.

- *NPV if executes:* CHF 15&ndash;25B (annex scope smaller because adaptive; lower confidentiality coverage).
- *NPV if fails:* CHF 0 (no sunk cost because conditional; relationships preserved).
- *Expected utility:* **0.50 &times; CHF 20B + 0.50 &times; 0 = +CHF 10.0B.**

### Branch C &mdash; Defer to Q3 2026

**P(execute) ~ 25% (range 15&ndash;35%).** Defer slips the window by 90 days. Same pre-conditions but with materially less time to resolve, plus parallel pressure from contagion already starting to leak.

- *NPV if executes:* CHF 10&ndash;15B (smaller window, weaker annex).
- *NPV if fails:* CHF &minus;3 to &minus;7B (window erosion damage; gradual spillover starts before annex executes).
- *Expected utility:* **0.25 &times; CHF 12.5B + 0.75 &times; CHF &minus;5B = &minus;CHF 0.6B.**

### Branch D &mdash; Reject firewall

**P(contagion materialises) ~ 75% (range 60&ndash;85%).** Rejection means no protection. The relevant probability is whether contagion materialises naturally over 2027&ndash;2031 absent active defence. Working-group view: high. Several pathways converge (EU pharmaceutical strategy implementation Q3 2026, AMNOG reset cycle 2027, OECD reference-pricing harmonisation work) and no single defensive intervention is in place.

- *NPV if contagion materialises:* CHF &minus;22B central case (refp contagion realised at &ldquo;severe&rdquo; level over 2027&ndash;2031).
- *NPV if contagion does not materialise:* CHF 0 (world stays as is).
- *Expected utility:* **0.75 &times; CHF &minus;22B + 0.25 &times; CHF 0 = &minus;CHF 16.5B.**

## Ranking and the non-obvious result

<table class="decision-quality-table">
<thead>
<tr><th>Branch</th><th>P(success)</th><th>Outcome if success</th><th>Outcome if failure</th><th>Expected utility</th></tr>
</thead>
<tbody>
<tr><td><strong>A</strong> &mdash; Endorse all</td><td>30%</td><td>+CHF 32.5B</td><td>&minus;CHF 1.5B</td><td><strong>+CHF 8.7B</strong></td></tr>
<tr class="ev-winner"><td><strong>B</strong> &mdash; Conditional</td><td>50%</td><td>+CHF 20B</td><td>CHF 0</td><td><strong>+CHF 10.0B</strong> &mdash; <em>highest EU</em></td></tr>
<tr><td><strong>C</strong> &mdash; Defer</td><td>25%</td><td>+CHF 12.5B</td><td>&minus;CHF 5B</td><td><strong>&minus;CHF 0.6B</strong></td></tr>
<tr><td><strong>D</strong> &mdash; Reject</td><td>25%*</td><td>CHF 0</td><td>&minus;CHF 22B</td><td><strong>&minus;CHF 16.5B</strong></td></tr>
</tbody>
</table>

<small>* For Branch D, "success" = contagion does not materialise of its own accord.</small>

**The non-obvious result.** Branch B has the highest expected utility, not Branch A &mdash; despite Branch A&apos;s higher upside. The mechanism: Branch B&apos;s adaptive scope and zero-failure-cost preserve option value that Branch A&apos;s full commitment burns. Under risk-neutral expected-utility maximisation, **Branch B beats Branch A by CHF 1.3B**.

**Why the briefing still recommends Branch A.** Two reasons.

First, Roche&apos;s strategic posture is *long-horizon variance-tolerant*, not risk-neutral. The board&apos;s asymmetric capacity to absorb downside in service of upside (the founding-family generational structure) means a +CHF 32.5B upside captured at 30% probability is worth more than the same EV captured via a conservative path. This is a *preference*, not an arithmetic claim.

Second, **the EV gap is small relative to estimation noise**. The probabilities in this memo are accurate to perhaps &plusmn;10 percentage points each. The CHF 1.3B EV gap is well within that estimation noise. Reasonable people can prefer the higher-upside path under acknowledged uncertainty.

## Sensitivity analysis &mdash; when does the recommendation flip?

Three sensitivity sweeps that shift the recommendation:

### Sweep 1 &mdash; P(execute | Branch A) lower than 25%

If pre-conditions are more correlated negatively than the working group estimates (e.g., USTR posture turns negative AND drags peer-firm and election-cycle pre-conditions with it), Branch A&apos;s P(execute) could fall to 15&ndash;20%.

At P=20%: EU(A) = 0.20 &times; 32.5 + 0.80 &times; &minus;1.5 = **+CHF 5.3B**.
At P=15%: EU(A) = 0.15 &times; 32.5 + 0.85 &times; &minus;1.5 = **+CHF 3.6B**.

Branch B at 50% remains at +10B. **Branch B becomes the dominant recommendation, not just the marginal one, below P(Branch A) ~ 25%.**

**Decision rule:** if USTR back-channel sounding produces negative signal by 15 July 2026 (re-rating P(Branch A) downward), switch the formal endorsement from Branch A to Branch B at the Q3 2026 board.

### Sweep 2 &mdash; Contagion baseline weaker than central case

If reference-pricing contagion is mild rather than severe (CHF 10&ndash;15B over 5 years rather than CHF 22B central), the value of the annex falls proportionally.

At mild contagion (annex captures only CHF 12B if executes):
- EU(A) = 0.30 &times; 12 + 0.70 &times; &minus;1.5 = +CHF 2.5B
- EU(B) = 0.50 &times; 8 + 0.50 &times; 0 = +CHF 4.0B
- EU(C) = 0.25 &times; 5 + 0.75 &times; &minus;2.5 = &minus;CHF 0.6B
- EU(D) = 0.75 &times; &minus;10 + 0.25 &times; 0 = &minus;CHF 7.5B

**Branch ordering is preserved (B &gt; A &gt; C &gt; D) but the absolute EVs all compress.** The recommendation is robust to contagion severity within plausible bounds.

### Sweep 3 &mdash; Loss aversion (regret minimisation rather than EU)

Under a regret-minimisation frame &mdash; minimise the worst-case loss across all branches &mdash; the ordering changes:

- Branch A worst case: &minus;CHF 1.5B
- Branch B worst case: CHF 0
- Branch C worst case: &minus;CHF 5B
- Branch D worst case: &minus;CHF 22B

**Branch B wins under regret-minimisation by an even wider margin than under expected utility.** Branches C and D are dominated under both frames.

## What this changes for the board

Three implications.

1. **The default recommendation should be Branch B, with Branch A as an aspirational target conditional on early USTR posture.** This is a *refinement* of the current briefing, which lists Branch A as the recommendation. The refinement: endorse Branch A in principle, but specify that the operational fallback is Branch B if any one of the four pre-conditions resolves negative by 15 July 2026.

2. **The 60-day pre-condition test gates a Branch A &rarr; Branch B re-rating, not a Branch A &rarr; failure binary.** Communicating this to the management team is important: a negative pre-condition test should trigger plan adaptation, not abandonment.

3. **The estimation noise in the probability assignments is itself an analytical asset.** A board member who finds P(execute | Branch A) of 30% optimistic can plug in 20% and see EU(A) drop to +5.3B; one who finds it pessimistic can plug in 40% and see EU(A) rise to +12.4B. The framework is a discussion tool, not a verdict.

## Sketches for Items 2 and 3

**Item 2 (capex flexibility for +$5B acceleration).** Decision-quality math here is simpler because the option is asymmetric upside: if Section 232 is renewed past 2029, the accelerated capex captures additional value; if Section 232 sunsets, the capex is no worse than baseline. EU(authorise) &gt; EU(refuse) under any reasonable probability of Section 232 renewal. **Recommendation: authorise.**

**Item 3 (patient OOP cap).** Binary decide-or-defer. The decision-quality math depends on (a) cost of the OOP cap (CHF 200&ndash;400M/year estimated), (b) probability that CMS rulemaking forces a similar cap regardless (50&ndash;70% by 2027), (c) reputational value of voluntary commitment. Working group view: defer is mildly EV-positive, but voluntary commitment has option value if rulemaking timing slips. **Recommendation: defer with explicit re-decision in Q4 2026.**

**Item 4 (tail-risk hedge).** Note-only; no decision-quality math needed. Q1 2027 exploratory workstream stands.

## Assumptions appendix

The framework above uses these defaults; all are negotiable.

- **Discount rate:** 10% (Roche WACC consensus).
- **Time horizon for NPV:** 2027&ndash;2031 (5-year window matching board agenda).
- **Risk preference:** risk-neutral expected utility for primary recommendation; regret-minimisation as a sanity check (not as primary rule).
- **Probability dependency:** pre-conditions positively correlated (range 0.2&ndash;0.5 pairwise correlation); joint probabilities computed under correlation assumption, not independent.
- **NPV calibration:** the contagion impact range CHF 18&ndash;55B from [financial translation](financial-translation.html) is held; CHF 22B used as central case.

---

**See also:** [Bottom line](bottom-line.html) &middot; [Financial translation](financial-translation.html) &middot; [Executive briefing](briefing.html) &middot; [Item 1 unpacked](item-1.html) &middot; [Adversarial review](adversarial.html)
