# Mean-blend result-to-claim review

Date: 2026-09-16. Independent reviewer: available secondary GPT-6 Codex agent, disclosed fallback for unavailable gpt-5.4. Bounded review of the closed development screen; no training, scientific evaluation access, frozen-source mutation, or manuscript edit.

## Verdict

**claim_supported: no** for advancement of the common mean-blend candidate or a strong BCE advantage. **Confidence: high** in the frozen gate decision; low for causal or general method-family conclusions. The final simple-intervention campaign closes: none of its five development candidates advances, and no new confirmation is justified by these outcomes.

The selected common positive coefficient is rho .5. Independently reconstructing all 21 group errors from the audit's saved integer error counts, averaging Digits initializations within each of three partitions first, reproduces the screen. Six-cell selected validation error falls from 11.2738715% to 11.1545139%: **+.119357638889 percentage-point improvement**, below the declared .3-point minimum. Rho .25 worsens error by .3146701 points. Mean-MSE is unchanged, shown once per unit, and excluded from coefficient selection.

| Task | BCE improvement pp | Brier improvement pp | Task mean improvement pp |
|---|---:|---:|---:|
| ReLU | +.455729 | -.065104 | +.195313 |
| Quadratic | +.065104 | +2.083333 | +1.074219 |
| Digits | -1.757813 | -.065104 | -.911458 |

Two guards fail: the aggregate improvement is too small, and Digits BCE is harmed by more than one point. The two-task improvement guard passes. Aggregate normalized regret falls by .000506796324, from .012527385086 to .012020588762, so that guard also passes. Passing two guards does not override the conjunction. The favorable quadratic Brier cell does not license a task/loss-specific rescue; the other two Brier cells each worsen slightly, and the common coefficient was the frozen target.

## Independent verification

I independently recomputed the positive-coefficient selection, six-cell aggregates, task and individual-cell differences, normalized-regret aggregate, and all four Boolean decisions. The negligible last-decimal difference from the saved aggregate is floating-point summation order; the exact integer-count reconstruction gives the same route. All 21 reported group errors match the audit's counts.

The audit reports 84 runs and 336 selected/final train/validation model-split replays, exact metric and selected-checkpoint argmin agreement, independent integer path decoding, and the threshold Brier/mean/residual identity. I inspected its implementation and verified these bindings against actual files:

- freeze to all eight source files and work protocol;
- screen and audit to the freeze;
- audit and choice artifact to the complete screen analysis;
- diagnostics to the audit;
- audit and diagnostic records to their actual scripts;
- all 84 unique result files to both the report's and audit's saved result hashes.

The session is closed, and no evaluation gate or confirmation results exist. I did not repeat the 336 model forward passes. No material inconsistency was found in this bounded review.

Binding identifiers: freeze `2f8b144c4f1bd9f9d50524261f9858f4edf0bb84c3e079dd78635672db2b1176`; analysis `0079ca1e8150c35401500273a7da09f641036aa1ccd0ee71ada68a491862fd5d`; audit `bd465b193bc1c1d28aadb8172b499865252d6e22f16cb3ac486ad800c7ac146d`; diagnostics `379434ab7d3bf290767ee8b1436b60f9b6893e6b9016bdc0f55b4675baca8233`.

## Attribution and claim limits

The descriptive gradient summaries agree with independently recomputed summaries of the saved probes. All 144 local base-versus-mean gradient cosines are positive and defined. Median mean/base norm ratios for BCE are .198672/.190091/.032972 on ReLU/quadratic/Digits; Brier's are .499715/.520544/.461387. These probes use selected rho-zero models and six diagnostic training batches per trajectory. They do not measure the intervened trajectories or establish that alignment caused the observed gains or harms. The result offers no support for instantaneous negative alignment at these probes as an explanation.

The common coefficient substantially changes relative gradient forces, particularly for Digits BCE. Fixed Adam recipes and weight decay entangle objective tradeoffs with optimization geometry and scale. The Brier identity isolates a residual-variation coefficient algebraically in probability space, but the experiment does not identify that coefficient as the causal source of a general decision benefit. BCE has a different nonquadratic mixture. Population propriety does not guarantee finite-network, finite-budget performance.

Supported: a small descriptive aggregate validation improvement for this common coefficient, heterogeneous cell responses, a favorable quadratic Brier response, a materially unfavorable Digits BCE response, and failure of the complete predeclared route. Unsupported: statistical superiority, strong BCE advantage, an optimal rho, the ineffectiveness of all possible mean-blend methods, equivalence to controls, a universal role for residual variance, or a new scoring-rule invention. Three development units per task and optimistic validation selection cannot sustain those stronger claims.

## Final routing

Do not launch blend confirmation, expand the rho grid, carve out quadratic Brier, switch endpoints, or lower a guard. Preserve all 21 cells and 84 trajectories. The final cumulative occupied time is **6720.883851766586 / 14400 seconds**; unused capacity is not grounds to extend this closed intervention sequence.

The campaign establishes no prespecified strong BCE advantage. Round 0's corrected conditional findings remain valid: Brier improves upon Mean-MSE on both synthetic tasks, BCE improves upon Mean-MSE on quadratic, and Brier improves upon BCE on ReLU. Digits contrasts remain inconclusive after correction. These narrower findings and the full exploratory negative ledger are the appropriate basis for claim revision. See the now-final `CAMPAIGN_REASSESSMENT_REVIEW.md`.
