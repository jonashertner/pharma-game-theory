# Sensitivity tornado &mdash; which assumption drives the answer most

<div class="memo-meta" markdown="1">
<strong>To:</strong> Roche Executive Committee &middot; <strong>From:</strong> Strategic-analysis working group &middot; <strong>Date:</strong> 20 May 2026 &middot; <strong>Read time:</strong> 7 minutes
</div>

## Why this exists

The [decision-quality framework](decision-quality.html) ranks the four branches on expected utility under the working group&apos;s central probability and impact assumptions. The headline result &mdash; Branch B has highest EU at CHF 10.0B, Branch A second at CHF 8.7B &mdash; depends on ~10 distinct numerical assumptions. **Which of those assumptions does the recommendation depend on most?** If the recommendation is robust to large swings in some assumptions and fragile to small swings in others, the working group should focus its data-gathering on the latter, and the board should focus its scrutiny there.

This memo computes the impact of a 1-standard-deviation (or 1-band) shift in each assumption on EU(Branch A), and ranks them. The visualisation is a horizontal &ldquo;tornado&rdquo; chart: assumptions sorted by absolute impact, bars sized proportional to swing. Top of the tornado = highest leverage; bottom = least.

## The full assumption set

The decision-quality framework uses the following inputs to compute EU(Branch A):

| # | Assumption | Central value | Low / high band |
| --- | --- | --- | --- |
| 1 | P(USTR back-channel positive signal) | 45% | 30% / 60% |
| 2 | P(SECO MRA-transfer memo clears) | 70% | 55% / 85% |
| 3 | P(no peer firm pre-empts with rival annex) | 67% | 55% / 80% |
| 4 | P(no 2026 election-year backlash) | 60% | 45% / 75% |
| 5 | Cross-pre-condition correlation | 0.35 | 0.15 / 0.55 |
| 6 | Contagion severity (annex captures, CHF B) | 32.5 | 18 / 47 |
| 7 | Sunk cost on failure (CHF B) | 1.5 | 0.5 / 3 |
| 8 | Discount rate | 10% | 8% / 12% |
| 9 | Time horizon | 5 yr | 4 yr / 7 yr |
| 10 | Trontinemab launch impact on annex value | none | none / +CHF 5B |

## The tornado

Each bar below shows EU(Branch A) under low-band vs high-band of each assumption, with central case as the reference. Wider bars = greater leverage.

<div class="tornado-chart" aria-label="Sensitivity tornado — assumptions ranked by EU impact">

<div class="tornado-row">
  <div class="tornado-label">Contagion severity (CHF 18&ndash;47B)</div>
  <div class="tornado-bar-container">
    <div class="tornado-bar-neg" style="width: 38%;"><span>&minus;CHF&nbsp;4.4B</span></div>
    <div class="tornado-mid"></div>
    <div class="tornado-bar-pos" style="width: 38%;"><span>+CHF&nbsp;4.4B</span></div>
  </div>
  <div class="tornado-impact">CHF&nbsp;8.7B swing</div>
</div>

<div class="tornado-row">
  <div class="tornado-label">P(USTR back-channel positive)</div>
  <div class="tornado-bar-container">
    <div class="tornado-bar-neg" style="width: 26%;"><span>&minus;CHF&nbsp;3.0B</span></div>
    <div class="tornado-mid"></div>
    <div class="tornado-bar-pos" style="width: 22%;"><span>+CHF&nbsp;2.5B</span></div>
  </div>
  <div class="tornado-impact">CHF&nbsp;5.5B swing</div>
</div>

<div class="tornado-row">
  <div class="tornado-label">P(no 2026 election-year backlash)</div>
  <div class="tornado-bar-container">
    <div class="tornado-bar-neg" style="width: 18%;"><span>&minus;CHF&nbsp;2.1B</span></div>
    <div class="tornado-mid"></div>
    <div class="tornado-bar-pos" style="width: 17%;"><span>+CHF&nbsp;1.9B</span></div>
  </div>
  <div class="tornado-impact">CHF&nbsp;4.0B swing</div>
</div>

<div class="tornado-row">
  <div class="tornado-label">Cross-pre-condition correlation</div>
  <div class="tornado-bar-container">
    <div class="tornado-bar-neg" style="width: 14%;"><span>&minus;CHF&nbsp;1.6B</span></div>
    <div class="tornado-mid"></div>
    <div class="tornado-bar-pos" style="width: 18%;"><span>+CHF&nbsp;2.0B</span></div>
  </div>
  <div class="tornado-impact">CHF&nbsp;3.6B swing</div>
</div>

<div class="tornado-row">
  <div class="tornado-label">P(SECO MRA-transfer clears)</div>
  <div class="tornado-bar-container">
    <div class="tornado-bar-neg" style="width: 14%;"><span>&minus;CHF&nbsp;1.6B</span></div>
    <div class="tornado-mid"></div>
    <div class="tornado-bar-pos" style="width: 14%;"><span>+CHF&nbsp;1.6B</span></div>
  </div>
  <div class="tornado-impact">CHF&nbsp;3.2B swing</div>
</div>

<div class="tornado-row">
  <div class="tornado-label">P(no peer-firm pre-emption)</div>
  <div class="tornado-bar-container">
    <div class="tornado-bar-neg" style="width: 11%;"><span>&minus;CHF&nbsp;1.3B</span></div>
    <div class="tornado-mid"></div>
    <div class="tornado-bar-pos" style="width: 12%;"><span>+CHF&nbsp;1.4B</span></div>
  </div>
  <div class="tornado-impact">CHF&nbsp;2.7B swing</div>
</div>

<div class="tornado-row">
  <div class="tornado-label">Time horizon (4&ndash;7 yr)</div>
  <div class="tornado-bar-container">
    <div class="tornado-bar-neg" style="width: 10%;"><span>&minus;CHF&nbsp;1.2B</span></div>
    <div class="tornado-mid"></div>
    <div class="tornado-bar-pos" style="width: 13%;"><span>+CHF&nbsp;1.5B</span></div>
  </div>
  <div class="tornado-impact">CHF&nbsp;2.7B swing</div>
</div>

<div class="tornado-row">
  <div class="tornado-label">Trontinemab co-benefit</div>
  <div class="tornado-bar-container">
    <div class="tornado-bar-neg" style="width: 0%;"></div>
    <div class="tornado-mid"></div>
    <div class="tornado-bar-pos" style="width: 13%;"><span>+CHF&nbsp;1.5B</span></div>
  </div>
  <div class="tornado-impact">CHF&nbsp;1.5B swing</div>
</div>

<div class="tornado-row">
  <div class="tornado-label">Discount rate (8&ndash;12%)</div>
  <div class="tornado-bar-container">
    <div class="tornado-bar-neg" style="width: 6%;"><span>&minus;0.7</span></div>
    <div class="tornado-mid"></div>
    <div class="tornado-bar-pos" style="width: 6%;"><span>+0.7</span></div>
  </div>
  <div class="tornado-impact">CHF&nbsp;1.4B swing</div>
</div>

<div class="tornado-row">
  <div class="tornado-label">Sunk cost on failure</div>
  <div class="tornado-bar-container">
    <div class="tornado-bar-neg" style="width: 5%;"><span>&minus;0.6</span></div>
    <div class="tornado-mid"></div>
    <div class="tornado-bar-pos" style="width: 5%;"><span>+0.6</span></div>
  </div>
  <div class="tornado-impact">CHF&nbsp;1.2B swing</div>
</div>

<div class="tornado-caption">
EU(Branch A) is CHF&nbsp;8.7B at central case. Each row shows the EU swing under low- vs high-band of one assumption, holding all others at central.
</div>

</div>

## What the tornado tells us

**Three assumptions dominate.** Contagion severity, P(USTR back-channel positive), and P(no 2026 election-year backlash) together drive ~CHF 18B of cumulative swing &mdash; more than the remaining seven assumptions combined.

**Implication 1: working-group resourcing should concentrate on the top three.** The CHF 5&ndash;8M working-group budget over 60 days should disproportionately fund: (a) better contagion-severity forecasting (EU pharmaceutical strategy monitoring, AMNOG cycle analysis), (b) USTR back-channel relationship development and signal-collection capacity, (c) political-monitoring infrastructure for 2026 election-year drug-pricing rhetoric. Resourcing on the bottom three (sunk-cost estimation, discount-rate calibration, peer-firm pre-emption tracking) is lower-priority.

**Implication 2: the recommendation is robust to discount-rate and sunk-cost assumptions.** A board member who thinks the working group is using the wrong discount rate (or who has a different view on sunk costs) can substitute their own value and see EU(Branch A) shift by less than CHF 1B. The recommendation does not depend on these. This is useful for board discipline: focus debate on the high-impact assumptions; do not debate the low-impact ones.

**Implication 3: cross-pre-condition correlation is more impactful than expected.** A working-group estimate of 0.35 correlation between pre-conditions (positively correlated &mdash; one favourable signal predicts others) is uncertain. If correlation is actually 0.15 (less correlated), EU(A) drops by CHF 1.6B because pre-conditions become less compound-favorable. If correlation is 0.55 (more correlated), EU(A) rises by CHF 2.0B. This is the single most under-discussed assumption in the framework. Recommend: the working group document specifically what correlation level is assumed and how it could be measured.

## Two-factor sensitivity &mdash; where does the recommendation flip?

The single-factor tornado shows what moves the EU(A) most. The two-factor analysis shows where the *recommendation* (Branch A vs B vs C vs D) changes:

| Combined shift | EU(A) result | New recommendation |
| --- | --- | --- |
| Contagion severity low + P(USTR) low | +CHF 1.3B | Branch B (was A) |
| Contagion severity low + correlation low | +CHF 4.0B | Branch A (still) |
| P(USTR) low + 2026 backlash low | +CHF 3.7B | Branch B (was A) |
| Three weakest pre-conditions low | &minus;CHF 1.2B | Branch B clear |
| All three top assumptions low | &minus;CHF 7.5B | Branch B clear (large margin) |
| All three top assumptions high | +CHF 17.5B | Branch A (large margin) |

**The recommendation flips from A to B when (contagion severity drops to low band) AND (any one of the three top-probability assumptions drops to low band).** Equivalently: Branch A is robustly optimal only when *both* the underlying threat materialises *and* execution probability is at central or above. If either condition weakens to low-band, the EV gap closes and Branch B becomes preferable.

**Operational implication:** the Item 1 endorsement should be drafted with a contingent re-rating clause. The board endorses Branch A *conditional on the contagion-severity and execution-probability assessments holding at central or above through the 60-day pre-condition window*. If either drops to low-band during the window, the formal endorsement re-rates to Branch B without re-convening the board.

## What this changes for the working group

Four specific re-prioritisations:

1. **Contagion severity** is the highest-leverage forecast. Working-group analytical effort should disproportionately fund: AMNOG decision monitoring through Q4 2027, EU pharmaceutical strategy implementation tracking, joint procurement scope expansion analysis. Hire one full-time analyst dedicated to this monitoring.

2. **USTR back-channel** is the highest-leverage relationship. Working-group political effort should concentrate on a specific named USTR official (currently under-resourced) with weekly contact frequency through Q3 2026.

3. **2026 election-year monitoring** should be active by Q2 2026 (now) with explicit weekly tracking of pharma-pricing rhetoric in midterm primary fields. Cost: CHF 0.3&ndash;0.5M/yr; impact bracket: CHF 4B.

4. **Cross-pre-condition correlation** should be documented explicitly in the working-group methodology. Currently estimated at 0.35; the assumption should be tested by examining historical pre-condition resolution patterns (where comparable bilateral negotiations have produced documented pre-condition outcomes).

## What this changes for the board

The single most useful thing for the board to take from this analysis is: **stop debating discount rate and sunk-cost assumptions; focus board time on contagion-severity and USTR-posture assumptions.** The first set does not move the recommendation; the second can flip it.

Recommend that the [briefing](briefing.html)&apos;s Item 1 endorsement include the contingent-re-rating clause described above. This is a small change with material decision-quality improvement.

---

**See also:** [Decision quality](decision-quality.html) &middot; [Real options](real-options.html) &middot; [Financial translation](financial-translation.html) &middot; [Item 1 unpacked](item-1.html)
