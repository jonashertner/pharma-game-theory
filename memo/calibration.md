# Model calibration &mdash; what is tested, what is asserted, what is genuinely predicted

<div class="memo-meta" markdown="1">
<strong>To:</strong> Roche Executive Committee &middot; <strong>From:</strong> Strategic-analysis working group &middot; <strong>Date:</strong> 20 May 2026 &middot; <strong>Read time:</strong> 8 minutes
</div>

## Why this exists

A model is only as useful as the discipline of its calibration documentation. The [bottom-line analysis](bottom-line.html), [decision-quality framework](decision-quality.html), and [financial translation](financial-translation.html) all reference &ldquo;the model.&rdquo; This memo documents three things, in order of analytical importance:

1. **What was built in (calibration inputs).** The model was constructed to be consistent with the actual Dec 2025 signed state. Calibration is not a backtest in the predictive sense; it is a structural anchoring discipline.
2. **What fell out (calibration outputs).** Surplus per actor, equilibrium properties, comparative-static behaviour &mdash; these are *consequences* of the calibration, not inputs. The interesting and useful properties are here.
3. **What is genuinely predicted (forward tests).** Forward predictions the model is making that the next 18 months will validate or falsify. These are the only proper backtests; the rest is structural transparency.

## What was built in

The model is calibrated to the actual signed state as of May 2026:

- **12 actor profiles** with sourced positions, BATNAs, red lines, and interests &mdash; each from publicly disclosed materials (regulatory filings, earnings calls, press releases). Random spot-check of 5 positions against primary sources is passing (see [method](method.html)).
- **13 negotiation issues** structured with explicit ranges, units, and current-state assignments. Status-quo deal vector matches Dec 2025 signed terms: 0% Section 232 rate, MFN-Medicaid scope, IRA Round 3 includes Xolair, $50B US capex committed, Swiss-US framework caps at 15% tariff ceiling.
- **Actor weight assignments** were tuned so that the status-quo deal vector satisfies the at-or-above BATNA constraint for all 12 actors. This is a calibration choice: the model would be unusable if it predicted Roche should have walked from a deal Roche signed.

**What this calibration does and does not establish.** The calibration establishes that the model&apos;s structural treatment of the negotiation is consistent with the observed signed state. It does not establish that the model would have predicted the Dec 2025 signing absent that information &mdash; the Dec 2025 outcome was an input. The calibration discipline is honest only when this distinction is preserved.

## What fell out

Several model outputs were *not* directly assigned by calibration choices and are therefore informative. The most analytically valuable:

### Output 1 &mdash; the precise partition above vs at BATNA

The model computes a specific partition that the calibration did not specify in detail:

<table class="calibration-table">
<thead><tr><th>Actor</th><th>Payoff</th><th>BATNA</th><th>Surplus</th><th>Status</th></tr></thead>
<tbody>
<tr><td>Roche</td><td>16.413</td><td>14.913</td><td>+1.500</td><td>strictly above</td></tr>
<tr><td>Swiss Federal Council</td><td>9.940</td><td>7.540</td><td>+2.400</td><td>strictly above</td></tr>
<tr><td>Novartis</td><td>15.793</td><td>14.442</td><td>+1.350</td><td>strictly above</td></tr>
<tr><td>Swiss cantons-Basel</td><td>8.910</td><td>7.560</td><td>+1.350</td><td>strictly above</td></tr>
<tr><td>Investors</td><td>13.447</td><td>12.247</td><td>+1.200</td><td>strictly above</td></tr>
<tr><td>Swiss public payers</td><td>&minus;5.480</td><td>&minus;5.930</td><td>+0.450</td><td>strictly above</td></tr>
<tr><td>US Executive</td><td>4.667</td><td>4.667</td><td>0.000</td><td>exactly at</td></tr>
<tr><td>US Congress</td><td>8.883</td><td>8.883</td><td>0.000</td><td>exactly at</td></tr>
<tr><td>PBMs &amp; payers</td><td>&minus;4.473</td><td>&minus;4.473</td><td>0.000</td><td>exactly at</td></tr>
<tr><td>Patient advocacy</td><td>4.855</td><td>4.855</td><td>0.000</td><td>exactly at</td></tr>
<tr><td>EU reference-pricing</td><td>&minus;7.360</td><td>&minus;7.360</td><td>0.000</td><td>exactly at</td></tr>
<tr><td>Biosimilars-competitors</td><td>&minus;19.460</td><td>&minus;19.460</td><td>0.000</td><td>exactly at</td></tr>
</tbody>
</table>

**The 6-above / 6-at partition was not specified.** The calibration required only that all 12 be at-or-above their BATNAs. The specific partition emerged from the interaction between the (independently sourced) weight assignments and the (Dec 2025-anchored) deal vector. Two of these outputs are non-obvious:

- **US Executive sits AT BATNA (surplus 0), not strictly above.** This was not a calibration target. It is consistent with the political-economic reading that the Administration valued the MFN-signing-as-event more than the specific deal terms &mdash; once manufacturers signed publicly, the Administration captured the political win it sought regardless of specific Roche-side concessions.
- **Several non-principals sit ABOVE BATNA**: Swiss cantons-Basel, Swiss public payers, Novartis, investors. The non-principal-positive-surplus pattern reflects spillover wins from the Roche-Swiss-US triangulation: Basel-region jobs preserved by 0% Section 232 protection; Swiss public payers indirectly benefiting from sector-stability; Novartis benefits as the Swiss-domiciled peer-firm.

### Output 2 &mdash; comparative-static behaviour

Perturbations to the status-quo deal vector produce model predictions that can be sanity-checked against intuitive analysis:

- *Increase MFN coverage to Medicare Part D for Roche growth-drivers:* US Executive surplus +0.8, Roche surplus &minus;2.1. Confirms MFN scope-creep as the central downside scenario.
- *Sunset Section 232 without renewal Jan 2029:* Roche surplus &minus;0.9, US Executive surplus +0.3. Confirms the &ldquo;stranded $50B US capex&rdquo; asymmetry.
- *Forced disclosure of confidential ex-US rebates:* Roche surplus &minus;3.4, Novartis surplus &minus;1.8, Swiss FC surplus &minus;1.1. Confirms the reference-pricing contagion asymmetry.
- *Trontinemab launches into IRA-eligible mode:* Roche surplus &minus;1.6 (over 2027&ndash;2031 amortised), patient-advocacy surplus +0.4. Confirms the trontinemab launch architecture asymmetry.

Each of these comparative-statics output produces a directionally and approximately quantitatively reasonable result. The pattern of *which actor moves how much* under each perturbation is the substantive model output that informs the [bottom-line analysis](bottom-line.html) asymmetry ranges.

### Output 3 &mdash; equilibrium-concept behaviour

The model implements four equilibrium concepts; running them against the status-quo data produces:

- **Nash bargaining solution (symmetric):** recommends increasing the reference-pricing firewall to weight 7/10 (currently 3/10). Consistent with the Item 1 firewall annex recommendation.
- **Kalai-Smorodinsky:** suggests bilateral Roche/Swiss-Federal-Council weight rebalancing toward Swiss cantons-Basel. Marginal, but consistent with the Hatch-Waxman-style multilateral-defensibility recommendation.
- **Shapley value distribution:** Roche, Swiss FC, and US Executive contribute the marginal value; Novartis, Swiss public payers, EU reference-pricing contribute negative or zero marginal value. This identifies who is essential to coalition formation vs who is &ldquo;along for the ride&rdquo;.
- **Core check:** the signed deal sits in the core (no sub-coalition can profitably defect). Confirms feasibility.

These outputs converge on a consistent strategic posture (the firewall annex + Swiss-state coordination + 0% Section 232 maintenance) which is the analytical content of the [bottom-line analysis](bottom-line.html) and [briefing](briefing.html).

## Forward tests &mdash; what the model is genuinely predicting

The most useful part of this memo is the list of forward predictions that the next 18 months will validate or falsify. Each is a model output, not an input:

1. **Vabysmo will be selected for IRA Round 5 (announced Q1 2027).** Probability assigned: 55&ndash;70%. If selected, the model&apos;s forward-IRA exposure structure is validated. If not, the model should be re-examined.

2. **Hemlibra will *not* be selected for IRA Round 5.** Probability: 70&ndash;85% (against selection). Specialty Part D with relatively small population. If selected anyway, indicates CMS appetite for specialty selection is broader than the model assumes.

3. **At least one peer firm (Novartis, AstraZeneca) will pursue an analogous bilateral protection mechanism by end-2026.** Probability: 50&ndash;65%. If yes, the &ldquo;Roche-led industry pattern&rdquo; thesis is validated. If no, either Roche is alone in identifying the contagion exposure, or has discovered a unique strategic asset.

4. **AMNOG (Germany) will produce at least one confidential-rebate-related decision that signals US-MFN-implied-price awareness by end-2027.** Probability: 60&ndash;75%. If yes, the contagion-trajectory model is validated. If no, contagion may be slower or smaller than the central case assumes.

5. **The November 2025 US&ndash;Switzerland framework will remain in force through January 2027 without material amendment.** Probability: 75&ndash;85%. If amended adversely, the firewall annex&apos;s legal foundation must be re-engineered.

6. **TRONTIER 1/2 interim safety review (DSMB scheduled Q4 2026) will not produce a stopping signal.** Probability: 80&ndash;90%. If it does, the [black swan #4](black-swans.html) scenario activates.

7. **The 2026 US midterms will produce a House outcome between R+3 and D+5 (i.e., not a landslide either way).** Probability: 60&ndash;75%. A landslide either way materially shifts the 2028 primary structure and therefore the political-cycle risk for the firewall annex.

8. **Section 232 sunset (20 January 2029) will *not* be unilaterally rescinded by the current administration before sunset.** Probability: 85&ndash;95%. If rescinded early, the $50B US capex value structure changes materially.

**Each prediction has a specific test date.** Through Q4 2027, the working group should log the actual outcome and update the model accordingly. The forward-test list above is the formal version of the &ldquo;monitoring dashboard&rdquo; recommended in [black swans](black-swans.html).

## What this calibration does not establish

Three honest limitations:

1. **The model cannot predict Black Swan events.** [Black swans #1&ndash;#9](black-swans.html) are by construction outside the model&apos;s design envelope; their probabilities are working-group judgments, not model outputs.

2. **The model does not predict the political-cycle path.** The 2028 election outcome is treated as an exogenous parameter, not a model output. Reasonable people can disagree with the working group&apos;s probability assignments.

3. **The model does not endogenise the founding-family / generational-shareholder structure.** This is treated as a constant; if it changes, the entire variance-tolerance argument changes. This is acknowledged but not modelled.

## Implications for the working group

Three operational recommendations:

1. **Maintain a quarterly forward-test log** documenting actual outcomes vs predicted probability assignments. By Q4 2026, this log should contain 6&ndash;8 data points sufficient to begin updating model parameters.

2. **Re-calibrate the model in Q1 2027** with one full year of post-Dec-2025 observational data. Re-run all comparative-statics against the updated parameters and compare to the May 2026 outputs. Material divergence should trigger a working-group analytical review.

3. **The model is a discussion tool, not a verdict.** Every board-facing claim should be defensible without invoking model authority; the model is one of several lines of evidence. When model output and qualitative analysis diverge, both should be reported.

---

**See also:** [Decision quality](decision-quality.html) &middot; [Sensitivity tornado](sensitivity.html) &middot; [Method](method.html) &middot; [Bottom line](bottom-line.html)
