# Financial translation &mdash; drugs, exposures, scenarios

<div class="memo-meta" markdown="1">
<strong>To:</strong> Roche Executive Committee &middot; <strong>From:</strong> Strategic-analysis working group &middot; <strong>Date:</strong> 20 May 2026 &middot; <strong>Read time:</strong> 15 minutes
</div>

## What this is

The [model layer](dynamics.html) outputs ordinal payoff weights. The [bottom-line analysis](bottom-line.html) compresses those into three CHF NPV asymmetries (reference-pricing contagion CHF 25&ndash;60B, trontinemab launch architecture CHF 20&ndash;30B, stranded US capex CHF 4&ndash;10B). This memo defends &mdash; or refines &mdash; those numbers bottom-up. It maps each of the 13 model issues onto Roche&apos;s top-12 marketed drugs and the trontinemab pipeline, computes 2027&ndash;2031 revenue paths under each decision-tree branch, and rolls up to portfolio impact.

**Sourcing standard.** Every FY2025 revenue figure is from the Roche FY25 IR Update of 29 January 2026 ([source](https://www.roche.com/investors/updates/inv-update-2026-01-29)). Forward-year projections are derived from disclosed growth rates &times; explicit assumption sets; assumptions are tabled in the appendix. Where a per-drug US share is computed from disclosed lines it is shown precisely; where it is estimated, it is flagged.

## The portfolio at a glance &mdash; FY2025

Pharmaceuticals Division total: **CHF 47,669m** (+9% CER, +3% CHF). US Pharma: **CHF 25,355m** (+8% CER), **53.2% of Pharma**. The top-5 growth drivers combined: **CHF 21.4B**, 45% of Pharma. The top-12 below cover **CHF 37.2B**, **78% of Pharma**.

<table class="product-portfolio">
<thead>
<tr>
<th>#</th><th>Drug</th><th>FY25 global</th><th>+/&minus; CER</th><th>FY25 US</th><th>US share</th><th>Primary exposure</th>
</tr>
</thead>
<tbody>
<tr><td>1</td><td><strong>Ocrevus</strong></td><td>7,010</td><td>+9%</td><td>4,874</td><td>69.5%</td><td>Refp contagion (very high); Section 232 (high)</td></tr>
<tr><td>2</td><td><strong>Hemlibra</strong></td><td>4,754</td><td>+11%</td><td>2,665</td><td>56.1%</td><td>Refp contagion (very high); Section 232 (high)</td></tr>
<tr><td>3</td><td><strong>Vabysmo</strong></td><td>4,102</td><td>+12%</td><td>2,857</td><td>69.7%</td><td>Refp contagion (high); future IRA Part B candidate</td></tr>
<tr><td>4</td><td><strong>Tecentriq</strong></td><td>3,566</td><td>+3%</td><td>1,640</td><td>46.0%</td><td>Biosimilar (late 2020s); declining baseline</td></tr>
<tr><td>5</td><td><strong>Xolair</strong></td><td>3,075</td><td>+32%</td><td>3,075</td><td>100%*</td><td><strong>IRA Round 3 locked in</strong>; biosimilar Sept 2026</td></tr>
<tr><td>6</td><td><strong>Perjeta</strong></td><td>2,968</td><td>&minus;13%</td><td>1,268</td><td>42.7%</td><td>Internal cannibalisation by Phesgo</td></tr>
<tr><td>7</td><td><strong>Actemra</strong></td><td>2,470</td><td>&minus;2%</td><td>1,206</td><td>48.8%</td><td>Biosimilar (live); already in decline</td></tr>
<tr><td>8</td><td><strong>Phesgo</strong></td><td>2,441</td><td>+48%</td><td>708</td><td>29.0%</td><td>Refp contagion (moderate); Perjeta substitute</td></tr>
<tr><td>9</td><td><strong>Kadcyla</strong></td><td>2,025</td><td>+7%</td><td>768</td><td>37.9%</td><td>Refp contagion (low-moderate)</td></tr>
<tr><td>10</td><td><strong>Evrysdi</strong></td><td>1,757</td><td>+13%</td><td>612</td><td>34.8%</td><td>Refp contagion (moderate); ex-US heavy</td></tr>
<tr><td>11</td><td><strong>Alecensa</strong></td><td>1,562</td><td>+6%</td><td>565</td><td>36.2%</td><td>Refp contagion (moderate); long runway</td></tr>
<tr><td>12</td><td><strong>Polivy</strong></td><td>1,470</td><td>+38%</td><td>688</td><td>46.8%</td><td>Section 232 (high — ADC); China NRDL exposure</td></tr>
<tr><td colspan="2"><em>Top-12 total</em></td><td><em>37,200</em></td><td></td><td><em>20,926</em></td><td><em>56.3%</em></td><td></td></tr>
<tr><td colspan="2"><em>% of Pharma Division</em></td><td><em>78.0%</em></td><td></td><td><em>82.5%</em></td><td></td><td></td></tr>
</tbody>
</table>

<small>* Xolair: Roche books US revenue only; Novartis books ex-US. Combined Xolair franchise is materially larger; only the Roche line is shown.</small>

**The concentration story.** The top-5 single-source biologics &mdash; Ocrevus, Hemlibra, Vabysmo, Xolair, Tecentriq &mdash; account for **CHF 15.2B of US Pharma revenue, or 60% of the US Pharma total**. Any scenario that perturbs these five disproportionately moves the portfolio. The remaining 40% is more diversified and more biosimilar-eroded; its forward-scenario sensitivity is lower.

## The five exposures &mdash; how the 13 model issues map to drug economics

The model&apos;s 13 negotiation issues collapse into five distinct CHF-impact mechanisms when translated to product economics.

### Exposure A &mdash; IRA Maximum Fair Price

**Mapped from:** Issue 2 (IRA MFP), partly Issue 10 (patent / pill-penalty), partly Issue 11 (IP).

**Mechanism.** Selected drug pays MFP as net price to Medicare beneficiaries; effective 7-year (small molecule) or 11-year (biologic) post-launch eligibility window; CMS-disclosed price cuts in Round 1 ranged from 38&ndash;79% off WAC.

**Roche current exposure.** **Xolair only** (Round 3, MFP effective 1 January 2028). Estimated MFP cut 50&ndash;65% off WAC based on Round 1/2 precedent. Annual revenue impact at Xolair scale: **CHF 1.0&ndash;1.5B/year US revenue lost from 1 Jan 2028**, partially offset by volume retention and partially compounded by Sept 2026 biosimilar entry.

**Forward exposure.** Future rounds: **Vabysmo** is the most likely next-round Part B selection (high Medicare spend, single-source, anti-VEGF class). **Hemlibra** is plausible Round 5+ selection if specialty Part D thresholds tighten. **Ocrevus** is plausible Round 6+ if biosimilar timing slips.

### Exposure B &mdash; Section 232 tariff

**Mapped from:** Issue 3 (Section 232), Issue 4 (manufacturing footprint).

**Mechanism.** Tariff on Swiss-origin biologics imported into the US. Current rate under MFN-deal track: **0% through 20 January 2029**. Statutory rate without deal: 100%. With US&ndash;Switzerland framework but no MFN deal: 15% ceiling.

**Roche current exposure.** All five top biologics (Ocrevus, Hemlibra, Vabysmo, Tecentriq, Xolair) plus Phesgo and Perjeta are largely Swiss-origin (Basel, Kaiseraugst, Penzberg). US revenue at risk = CHF 18B (sum of US lines for these seven). At 15% landed-cost surcharge (the no-deal fallback), the gross-margin hit would be **CHF 2.7B/year**. At 100% (full Section 232), economically unviable on these volumes &mdash; product would shift channels or pricing would be re-engineered.

**Forward exposure.** The 20 Jan 2029 sunset is a cliff. Renewal under a successor administration vs sunset is binary. The $50B US capex plan is designed to shift the manufacturing centre of gravity by 2029&ndash;2031, but the build is in tranches and is not complete by sunset.

### Exposure C &mdash; MFN coverage and TrumpRx DTC

**Mapped from:** Issue 1 (MFN coverage), Issue 6 (TrumpRx).

**Mechanism.** MFN-implied net price applies to Medicaid (current scope) or expands to Medicare/commercial (forward scope creep). TrumpRx DTC channel offers manufacturer-discount platform.

**Roche current exposure.** **None of the top-7 biologics is in MFN scope as of December 2025.** Only Xofluza was ceded for Medicaid MFN access. The exposure here is forward, not current.

**Forward exposure.** If MFN scope expands to commercial markets (2028+ policy possibility), Vabysmo / Ocrevus / Hemlibra could be pulled in. At MFN-implied prices (referencing G7 average), the net-price haircut is 30&ndash;50% vs current WAC. The 2028 election outcome dominates this exposure.

### Exposure D &mdash; International reference-pricing contagion

**Mapped from:** Issue 7 (international reference-pricing protection), Issue 12 (diplomatic carve-outs).

**Mechanism.** If US net prices (whether IRA-set, MFN-implied, or TrumpRx-disclosed) become legible to EU AMNOG, UK NICE, Swiss BAG, JP NHI, or other reference-pricing jurisdictions, the **confidential-rebate architecture** that supports current ex-US net prices erodes. The mechanism operates either as gradual leakage (each AMNOG cycle resets downward) or as forced disclosure (EU pharmaceutical strategy mandates transparency).

**Roche current exposure.** **The largest single exposure.** High-WAC biologics ex-US = **CHF 7.3B/year** (sum of global &minus; US for the top six biologics). Spillover impact ranges:

- *Gradual spillover (low):* 15&ndash;25% net-price erosion on confidential-rebate biologics &asymp; **CHF 1.1&ndash;1.8B/year** EBIT impact.
- *Aggressive spillover (central):* 30&ndash;40% net-price erosion &asymp; **CHF 2.2&ndash;2.9B/year**.
- *EU forced disclosure (tail):* full confidential-net exposure on broader ex-US specialty portfolio &asymp; **CHF 4&ndash;7B/year**.

Plus second-order US drag: if reference-pricing contagion pulls down ex-US prices, US commercial channels following Medicare/Medicaid benchmarks see additional 0.5&times;&ndash;1.0&times; of the ex-US impact. Total annual EBIT swing thus **CHF 2&ndash;11B/year** depending on spillover scenario.

### Exposure E &mdash; Biosimilar / loss-of-exclusivity

**Mapped from:** Issue 10 (patent / pill-penalty), Issue 11 (IP), market mechanics.

**Mechanism.** Patent expiry and biosimilar entry erode net price and volume. Acute erosion in first 3 years post-LOE; baseline reset thereafter.

**Roche current exposure.** Drugs already eroded: Avastin, Herceptin, MabThera/Rituxan (down 17&ndash;22% in 2025), Actemra (multiple biosimilars), Lucentis (Susvimo plus competitor biosims). Drugs facing entry in window: **Xolair (Sept 2026 biosim launch)**. Drugs with long runway: Vabysmo (post-2032), Hemlibra (post-2030), Ocrevus (late 2030s in EU, biosim signal building in US).

**Forward exposure.** The Ocrevus biosim signal in 2030&ndash;2032 is the largest single LOE event in the portfolio &mdash; CHF 5B+ revenue at risk over 3 years post-entry depending on biosimilar uptake curves and Ocrevus SC formulation defensibility.

## Per-drug deep dives &mdash; the five highest-leverage products

### Ocrevus &mdash; CHF 7.0B, 70% US, the cornerstone

Ocrevus is **20% of Roche US Pharma revenue all by itself**. The 2027&ndash;2031 base case assumes +6% CER growth (conservative vs the FY25 +9%) to a 2031 run-rate of CHF 9.4B, of which ~CHF 6.5B US.

**Scenario impacts (5-year cumulative revenue, CHF):**

- *Branch A (firewall executes):* base case CHF 41B cumulative 2027&ndash;2031. Minor refp contagion, no MFN scope creep, Section 232 stays at 0%. Ocrevus SC franchise extends value.
- *Branch B (conditional):* base &minus; CHF 0.5&ndash;1B cumulative.
- *Branch C (defer to Q3 2026):* base &minus; CHF 1&ndash;2B cumulative (window of vulnerability extended).
- *Branch D (reject firewall):* base &minus; CHF 4&ndash;8B cumulative if severe spillover; up to &minus;CHF 12B if EU forced disclosure occurs.

**Why Ocrevus carries the most contagion risk in absolute terms.** The combination of (a) highest US revenue line in the portfolio, (b) high confidential ex-US net prices (CHF 2.1B ex-US revenue at large per-patient WAC), and (c) Genentech-launched single-net-price model means a single AMNOG reset cascades quickly. The 2030&ndash;2032 biosimilar signal compounds the urgency &mdash; refp contagion in 2027&ndash;2029 reduces NPV that would otherwise be defended by SC formulation extension and lifecycle management.

### Hemlibra &mdash; CHF 4.75B, 56% US, the specialty bellwether

Hemlibra&apos;s ~$500&ndash;700K/patient annual WAC sits at the extreme end of the confidential-rebate architecture. Ex-US net prices are a fraction of WAC. Forced disclosure or aggressive spillover hits Hemlibra harder in percentage terms than any other product.

**Scenario impacts (5-year cumulative revenue, CHF):**

- *Branch A:* base case CHF 28B cumulative 2027&ndash;2031 (+10% CER assumed).
- *Branch D:* &minus;CHF 3&ndash;6B cumulative in severe-spillover; &minus;CHF 8&ndash;12B in forced-disclosure tail.

**Forward IRA risk.** Hemlibra is a plausible Round 5+ specialty Part D candidate if CMS extends selection thresholds to small-population specialty drugs. The Round 3 selection of Xolair (a smaller population than typical Round 1/2 selections) signals CMS appetite for specialty.

### Vabysmo &mdash; CHF 4.1B, 70% US, the IRA Part B target

The fastest-growing major (+12% CER). Most likely next-round IRA Part B candidate among Roche products: high Medicare Part B spend, single-source mechanism, growing patient population.

**Scenario impacts (5-year cumulative revenue, CHF):**

- *Branch A:* base case CHF 27B cumulative (+12% CER held for 3 years, slowing to +6%).
- *Branch D + Vabysmo IRA Round 5 selection:* &minus;CHF 6&ndash;9B cumulative.

**Susvimo franchise defense.** The Susvimo refillable port extends franchise NPV but does not block IRA selection on the underlying anti-VEGF mechanism. The defensive move is **launch differentiation under a new code** rather than reliance on patent extension.

### Xolair &mdash; CHF 3.08B US, the locked-in IRA hit

Xolair&apos;s IRA Round 3 selection is settled. MFP effective 1 January 2028. Biosimilar Omlyclo expected September 2026 &mdash; biosim erosion begins *before* IRA MFP takes effect.

**Scenario impacts (5-year cumulative revenue, CHF):**

- *All branches:* CHF 8&ndash;11B cumulative 2027&ndash;2031 (down from a CHF 15B+ trajectory absent IRA + biosim).
- Branch differentials are small for Xolair &mdash; the hit is locked in; the firewall annex does not change this.

**Calibration value.** Xolair is the test case for forward IRA cuts. If Xolair&apos;s effective net-price cut comes in at the low end of the Round 1/2 range (~40&ndash;50%), forward-IRA scenarios for Vabysmo/Hemlibra should be modelled toward the lower end; if at the high end (~70&ndash;80%), forward scenarios should be modelled toward the upper end.

### The Perjeta + Phesgo franchise &mdash; CHF 5.4B combined, stable

Perjeta is declining (&minus;13% CER) as Phesgo absorbs patients (+48% CER). Combined franchise stable at CHF 5.4B. The SC combo product has materially better COGS (subcutaneous vs IV infusion logistics) and similar net price &mdash; *gross margin* on the franchise is improving even though gross revenue is flat.

**Scenario impacts.** Lower than other top-5 because (a) combined franchise less exposed to refp contagion than the pure biologics, (b) US share is only 29% for Phesgo, lower asymmetry. Branch A vs D differential ~CHF 2&ndash;4B cumulative.

## The scenario engine &mdash; portfolio rollup

Mapping the five exposures across the top-12 marketed portfolio plus trontinemab pipeline under each decision-tree branch:

<table class="scenario-rollup">
<thead>
<tr>
<th>Branch</th>
<th>Refp contagion</th>
<th>Section 232</th>
<th>MFN expansion</th>
<th>Forward IRA</th>
<th>Trontinemab launch</th>
<th>5-yr cumulative impact vs base</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>A &mdash; Endorse all</strong></td>
<td>Blocked</td>
<td>0% to sunset</td>
<td>Held at MFN-Medicaid only</td>
<td>Xolair only (locked)</td>
<td>Optionality preserved</td>
<td><strong>Base (CHF 0)</strong></td>
</tr>
<tr>
<td><strong>B &mdash; Conditional</strong></td>
<td>Partial block</td>
<td>0% to sunset</td>
<td>Held</td>
<td>Xolair only</td>
<td>Optionality preserved</td>
<td>&minus;CHF 3&ndash;6B</td>
</tr>
<tr>
<td><strong>C &mdash; Defer to Q3 2026</strong></td>
<td>Gradual spillover starts</td>
<td>0% to sunset</td>
<td>Held</td>
<td>Xolair only</td>
<td>Delay decision absorbs cost</td>
<td>&minus;CHF 6&ndash;12B</td>
</tr>
<tr>
<td><strong>D &mdash; Reject firewall</strong></td>
<td>Severe to forced</td>
<td>0% to sunset (capex justified)</td>
<td>Stays in scope</td>
<td>Xolair + Vabysmo Round 5</td>
<td>Constrained launch</td>
<td>&minus;CHF 18&ndash;32B (without forced disclosure); &minus;CHF 35&ndash;55B (with)</td>
</tr>
</tbody>
</table>

Plus the trontinemab pipeline asymmetry, which is largely orthogonal to the four-branch firewall decision:

- *Trontinemab launches at full label, pre-IRA-eligible window:* CHF 25&ndash;40B NPV captured (2028&ndash;2035).
- *Trontinemab launches into IRA-eligible mode:* CHF 12&ndash;20B NPV captured.
- *Trontinemab Phase 3 fails on safety (black swan #4):* CHF 25&ndash;40B written off plus platform franchise impact.

And the US capex strategic-purpose asymmetry, also orthogonal:

- *Section 232 renewed past 2029 (2028 populist successor scenario):* +CHF 6&ndash;12B capex revaluation as tariff insurance.
- *Section 232 sunsets without renewal:* &minus;CHF 4&ndash;10B carrying-cost-only asset.

## Calibration vs the bottom-line claims

The [bottom-line analysis](bottom-line.html) claimed three asymmetry ranges. The financial-translation math supports them with the following refinements:

1. **Reference-pricing contagion: claimed CHF 25&ndash;60B NPV swing &rarr; refined to CHF 18&ndash;55B over 2027&ndash;2031**, with the band splitting as:
   - *Mild spillover:* CHF 18&ndash;28B (the central case under Branch D).
   - *Severe spillover or forced disclosure:* CHF 35&ndash;55B.
   - The CHF 60B upper bound is only reachable in a forced-disclosure scenario that combines black swan #3 (EU transparency mandate) with Branch D. Probability-weighted, the *expected* contagion exposure is closer to CHF 22&ndash;30B.

2. **Trontinemab launch architecture: claimed CHF 20&ndash;30B NPV swing &rarr; confirmed at CHF 15&ndash;35B**, with the band splitting as:
   - *Launch pre-IRA-eligible vs IRA-constrained:* CHF 15&ndash;20B.
   - *Launch successful vs Phase 3 platform failure:* CHF 25&ndash;40B.
   - The two scenarios are not additive; treat as alternative paths.

3. **Strategic purpose of the $50B US capex: claimed CHF 4&ndash;10B NPV swing &rarr; confirmed at CHF 4&ndash;12B**, with upside skew if 2028 election produces extended tariff regime.

**Net.** The bottom-line ranges hold up against bottom-up product math, with the contagion claim trimmed slightly at the high end (the CHF 60B was only reachable in tail-conditional scenarios). The trontinemab and capex ranges are confirmed.

## What this changes for the 2026 board agenda

Three implications fall directly out of the financial-translation work:

1. **The top-5 single-source biologics are 60% of US Pharma revenue.** This concentration is the lever the firewall annex protects. The [Item 1 unpacked](item-1.html) action plan should reference this concentration explicitly as the asset under protection &mdash; not the contagion risk abstractly.

2. **Vabysmo is the most likely next-round IRA Part B selection.** A 2026 work-stream should pre-stage Vabysmo&apos;s forward-IRA defence: differentiation through Susvimo, indication sequencing, payer-channel optionality, and pre-negotiation with CMS through industry channels.

3. **The Perjeta &rarr; Phesgo substitution is a quiet win &mdash; it should not be quietly absorbed.** The franchise economics improved meaningfully (lower COGS, similar net price) without any 2026 decision. Communicate this to investors as a portfolio-management capability example, supporting the credibility of forward franchise-defence claims (Ocrevus SC, Tecentriq Hybreza, Vabysmo Susvimo).

## Assumptions appendix

All forward projections use these defaults unless flagged otherwise in-text.

- **Discount rate:** 10% (Roche WACC consensus range 8&ndash;11%; using midpoint).
- **CHF/USD:** held at FY25 level for simplicity; FX is a layer above the strategic scenarios.
- **Base-case growth (top-12):** drug-specific from FY25 CER &times; convergence to long-run +4% by 2030. Specifically:
  - Ocrevus: +9% &rarr; +6% by 2030
  - Hemlibra: +11% &rarr; +6% by 2030
  - Vabysmo: +12% &rarr; +8% by 2030
  - Tecentriq: +3% &rarr; flat by 2028
  - Xolair: +32% &rarr; &minus;15% post-biosim (Sept 2026) &rarr; &minus;30% post-IRA (Jan 2028)
  - Perjeta: &minus;13% &rarr; cannibalisation complete by 2028
  - Actemra: &minus;2% &rarr; &minus;8% biosim erosion
  - Phesgo: +48% &rarr; +15% by 2029 as substitution completes
  - Kadcyla, Polivy, Evrysdi, Alecensa: drug-specific moderate growth
- **IRA price cuts:** modelled at 55% off WAC (midpoint of Round 1/2 disclosed range 38&ndash;79%) for any selected drug.
- **Section 232 scenarios:**
  - Branch A&ndash;C: 0% to 20 January 2029, then 0% if renewed under successor (treated as 50/50 absent successor signal).
  - Branch D: 0% to sunset, then 15% post-sunset (US-Switzerland framework rate without MFN-deal preference).
- **Reference-pricing contagion scenarios:**
  - *Mild:* 20% net-price erosion on ex-US confidential-rebate biologics, gradual over 3-year window.
  - *Severe:* 35% net-price erosion plus 50% US commercial drag.
  - *Forced disclosure:* 50% net-price erosion plus 80% US commercial drag, compressed into 12&ndash;18 months.
- **Trontinemab penetration:**
  - *Pre-IRA-eligible launch:* 8% peak penetration of mild-moderate AD market by year 5, $30K annual WAC, 65% gross margin.
  - *IRA-constrained launch:* 5% peak penetration, $22K post-MFP WAC, 60% gross margin.
- **Biosimilar erosion curves:** 30% volume loss + 25% price erosion in year 1; 60% volume loss + 35% price erosion in year 3 (anti-CD20 / anti-IgE archetype).
- **US-Pharma share by drug:** disclosed in Roche FY25 IR Update except where flagged.

---

**See also:** [Bottom line](bottom-line.html) &middot; [Black swans](black-swans.html) &middot; [Executive briefing](briefing.html) &middot; [Item 1 firewall annex unpacked](item-1.html) &middot; data file: [`data/products.yaml`](https://github.com/jonashertner/pharma-game-theory/blob/main/data/products.yaml)
