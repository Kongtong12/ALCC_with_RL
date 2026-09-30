# Round 0: longer training and partition robustness

AS_OF: 2026-09-16. Mode: experiment-design / method-design. Effort: standard. Local research, no search subagents. Four targeted search queries followed by four primary paper pages opened. Claims below distinguish published facts from hypotheses about this experiment.

## Decision

Run the three unchanged core objectives on the same cumulative head for up to 6,000 updates, including fresh Digits source partitions. Select checkpoints and hyperparameters using validation only. Confirm on fresh paired units. Keep all original 600-step evidence and the Warcraft study immutable.

## Evidence ledger

| ID | Evidence / claim | Primary source | Assessment and use |
|---|---|---|---|
| E1 | A proper binary score composed with a link has optimization properties depending on both the score and link. Properness alone does not rank finite trained networks. | Reid & Williamson, AISTATS 2010, https://proceedings.mlr.press/v9/reid10a.html | Confirmed, high confidence. Separate statistical targets from logit-space gradients; do not attribute the BCE/Brier gap solely to calibration. |
| E2 | Distributional losses can improve regression performance; this is prior art for learning a number with richer targets. | Imani & White, ICML 2018, https://proceedings.mlr.press/v80/imani18a.html | Confirmed, high confidence. The present study is a controlled target/score comparison, not invention of classification-based regression. |
| E3 | Classification-based value learning can outperform squared regression in deep RL settings. | Farebrother et al., ICML 2024, https://proceedings.mlr.press/v235/farebrother24a.html | Confirmed within that paper's settings. It is not a shortest-path or convergence guarantee for the present model. |
| E4 | SPO+ is an established convex surrogate for decision regret under linear-cost optimization, with assumptions on its consistency results. | Elmachtoub & Grigas, Smart Predict then Optimize, https://arxiv.org/abs/1710.08005 | Confirmed, high confidence. A same-head BCE+SPO+ candidate would combine existing ingredients, not constitute a novel surrogate by itself. |
| E5 | BCE's logit derivative is (q-t)/m, Brier's is 2(q-t)q(1-q)/m on the independent sigmoid head. | Direct differentiation of the frozen objectives; E1 supplies composite-loss context. | Confirmed algebraically. Gradient attenuation is a plausible optimization factor, not a proven cause of observed generalization gaps. |
| E6 | Dividing the Brier logit gradient exactly by 2q(1-q) recovers the BCE gradient where q is interior. | Direct differentiation. | Confirmed. Do not market this exact cancellation as a distinct algorithmic gain or spend a full training matrix rediscovering BCE. Clipping/preconditioning would be a different intervention needing its own controls. |
| E7 | Longer training will preserve the current BCE advantages. | Unknown until the new sealed study completes. | Uncertain. Training curves, selected-checkpoint test outcomes and negative results will adjudicate it. |
| E8 | Decision-aware hybrid losses will improve beyond equally tuned BCE. | Earlier local study had mixed hybrid results; E4 does not guarantee the neural finite-budget setting. | Uncertain. Only a development-screened candidate and fresh confirmation can support this. |

Research statistics: 8 claims, 6 confirmed (with stated scope), 0 refuted, 2 uncertain. No novelty or state-of-the-art claim made. The search does not imply an exhaustive literature review.

## Attribution, after each completed stage

1. Compare each objective's training and validation error/regret at common steps and at the validation-selected checkpoint. A widening train/validation gap suggests overfitting; it is not proof of a particular regularization mechanism.
2. Inspect logit, trunk and head gradient norms; saturation and wrong-saturated-label rates; residual dispersion and threshold crossings. Gradients at the same trained parameter vector give a controlled local comparison, not causal mediation of test outcomes.
3. Check selected learning rates/weight decays for boundary choices, selected-step distribution for early peaks or continued improvement, and across-partition effect direction for conditionality.
4. Propose at most a small development-only candidate set from the observed failure mode. Preserve output head and decoder for a loss-only claim; separately label any architecture change.
5. Before the next confirmation, freeze candidate, controls, search budget, new seeds/partitions, primary metric and alpha allocation. Keep every failed candidate and confirmation in the ledger.

## Campaign rules

The initial occupied-time guard is four hours, including calibration and scientific execution. Code/analysis work is outside device occupation. Pause/resume is supported. A new adaptive round must account for prior occupation rather than reset the campaign budget. Confirmation alpha is spent prospectively: .025 for round0; .05/2^(r+1) for later round r, without reclaiming failed tests. Within a round, correct the planned comparison family. Additional candidate search is exploratory; fixed-step and mechanism plots are diagnostic.

Strong advantage requires a meaningful effect and regret checks in addition to a small p-value. The registered round0 gate requires BCE to improve at least one percentage point and ten percent relatively over both matched controls on at least two tasks, pass the planned correction, and not show the specified adverse error/regret pattern. If the gate fails, record the actual conclusion; do not silently relax it or declare success from a favorable slice.
