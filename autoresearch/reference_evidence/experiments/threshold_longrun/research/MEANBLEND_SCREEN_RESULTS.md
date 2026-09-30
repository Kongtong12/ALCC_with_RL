# Threshold/mean blend: heterogeneous gains, failed advancement gate

Date: 2026-09-16. All 84 development trajectories completed. The frozen procedure chooses one common positive coefficient, rho .5, across six modified task/objective cells. Mean-MSE controls remain unchanged and outside this selection.

The selected validation error decreases from 11.273872% to 11.154514%, a **0.119358 percentage-point** improvement. This falls below the registered .3-point requirement. Digits BCE worsens 1.7578125 points, violating the maximum one-point individual-cell harm guard. The two-task and aggregate normalized-regret guards pass, but the complete gate **fails**. No blend confirmation will be launched.

| Task | BCE improvement pp | Brier improvement pp | Task mean improvement pp |
|---|---:|---:|---:|
| ReLU | +.455729 | -.065104 | +.195313 |
| Quadratic | +.065104 | +2.083333 | +1.074219 |
| Digits | -1.757813 | -.065104 | -.911458 |

Positive favors the blend over its own rho-zero control. These are selected development estimates, not independent test effects or significance claims. All three coefficients and the unchanged controls are in the 21-cell [complete report](../../threshold_meanblend_screen/work/SCREEN_REPORT.md). The favorable quadratic Brier cell cannot replace the common gate. No coefficient, task, method, endpoint or seed is removed.

## Exact audit

All 84 receipt/checkpoint chains validate against frozen source/protocol/configuration hashes. All 336 selected/final train/validation metric dictionaries reproduce exactly. Independent integer arithmetic on saved binary32 predicted costs reproduces every shortest-path nonoptimal count and regret. Selected checkpoints are reconstructed from their declared validation ordering. The threshold-Brier = decoded-mean-MSE + threshold-residual-variance identity passes on every replay. No evaluation gate, confirmation result or confirmation selection artifact exists.

The audit took 8.168 seconds and the descriptive aggregation .024 seconds, separately counted as analysis under the campaign contract. Final cumulative QA/calibration/training occupation is **6720.883851766586 / 14400 seconds** (1 h 52 min). Source freeze: `2f8b144c4f1bd9f9d50524261f9858f4edf0bb84c3e079dd78635672db2b1176`.

## Attribution: observations and limits

For quadratic Brier, rho .5 reduces selected validation normalized mean-cost MSE from .024047 to .023406 while threshold residual variance rises from .024967 to .025502. Training error rises from .977% to 1.563%, while validation decision error falls from 13.997% to 11.914%. This is compatible with a changed finite-model tradeoff; three development teachers and selection-dependent comparisons do not establish mediation or a transferable optimum.

ReLU Brier and Digits Brier each worsen .065104 points under the same coefficient. Digits BCE rises from 6.771% to 8.529%, and its mean regret rises from .161458 to .214193. Its wrong-saturation rate nevertheless falls from .001831 to .001524. Once again, improving that diagnostic is insufficient for better decisions in the tested procedure.

Local base-versus-mean gradients at selected rho-zero models have positive cosine in all 144 sampled batches; median cosines range .876-.998. Mean-to-base gradient-norm ratios differ substantially: BCE medians .199/.190/.033 for ReLU/quadratic/Digits, versus Brier .500/.521/.461. Thus a common coefficient does not impose an equal relative gradient perturbation. These are same-state local probes, not measurements of causal effects along the blended trajectories. Adam and fixed weight decay also prevent identifying the intervention with a simple scalar learning-rate change.

The score-mixture algebra and primary sources are in [MEANBLEND_SCREEN_RESEARCH.md](MEANBLEND_SCREEN_RESEARCH.md). A new primary-source check of [Cawley and Talbot, JMLR 2010](https://www.jmlr.org/papers/v11/cawley10a.html) reinforces the established distinction between optimizing a finite-sample selection criterion and evaluating a selected procedure independently. It does not prove that any particular favorable cell here is noise. It supports keeping the selected validation numbers explicitly exploratory.

## Routing

This was the final bounded simple-intervention screen. Its failed gate ends the sequence of nearby loss/optimizer adjustments. Do not expand rho, rescue a favorable cell, lower the guard, switch to final-checkpoint results, or launch a rejected candidate's confirmation. No new confirmation alpha was spent. The completed round-0 corrected findings remain valid within their scope; the intended strong BCE advantage remains unsupported.

Independent final review: [MEANBLEND_RESULT_REVIEW.md](MEANBLEND_RESULT_REVIEW.md). Campaign assessment: [CAMPAIGN_REASSESSMENT_REVIEW.md](CAMPAIGN_REASSESSMENT_REVIEW.md). The failed development interventions remain in the research ledger, not as claimed new algorithms in the paper.
