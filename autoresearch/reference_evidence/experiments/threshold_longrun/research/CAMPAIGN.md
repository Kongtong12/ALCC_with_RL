# Autonomous continuation contract

User authorization (2026-09-16): complete the longer-budget / partition robustness experiment, perform attribution and web research after each round, and optimize algorithm or code toward a strong advantage. Pause/resume remains required. The desired favorable result is not assumed.

## Current state and next actions

**CLOSED 2026-09-16 after the final mean-blend screen failed.** No training is active and no candidate advances. The bounded small-intervention search is complete, but the intended strong algorithmic advantage was not achieved. Read `AUTO_RESEARCH_REPORT_ZH.md`, `MEANBLEND_SCREEN_RESULTS.md`, `MEANBLEND_RESULT_REVIEW.md` and the final `CAMPAIGN_REASSESSMENT_REVIEW.md`. Do not launch a further coefficient/optimizer rescue or confirmation. Automated follow-up is paused; a substantively different direction needs an explicit revised research decision. All below-mentioned launches are historical.

- **Updated 2026-09-16:** round0 is complete; its BCE strong-advantage gate failed. Read `ROUND0_RESULTS.md`, `ROUND0_CLAIM_REVIEW.md` and `findings.md` before interpreting results.
- **Schedule screen complete:** all 72 fits passed technical checks but the development gate failed; error worsened 0.6583 pp overall. Do not launch its cosine confirmation. All outcomes are in `experiments/threshold_schedule_screen/work/screen_analysis.json`.
- **SPO screen complete:** all 108 development fits and 432 selected/final train/validation replays passed. Independent integer decoding agrees. Common alpha .1 fails the gate: mean error worsens .564236 pp and normalized regret increases. Do not confirm it or carve out the favorable Digits cells. Read `SPO_SCREEN_RESULTS.md` and `SPO_RESULT_AND_NEXT_REVIEW.md`.
- **Smoothing screen complete:** all84 fits and336 model/split replays pass. Common delta.1 fails every gate; mean error worsens.716146pp, all three task means worsen, regret increases. Wrong saturation falls but decisions do not improve. No confirmation. Read `SMOOTHING_SCREEN_RESULTS.md` and `SMOOTHING_RESULT_AND_EMA_REVIEW.md`.
- **EMA screen complete:** 36 optimizer trajectories with raw and two correlated shadows; all 432 selected/final train/validation replays pass, including independent integer decisions. Common EMA .99 improves error only .130208 pp, below the declared .3 pp gate. No confirmation. Read `EMA_SCREEN_RESULTS.md` and `EMA_RESULT_AND_NEXT_REVIEW.md`. Lower checkpoint fluctuations did not yield the required gain.
- **Final completed stage:** `experiments/threshold_meanblend_screen/work`. Read `MEANBLEND_SCREEN_RESEARCH.md` and `MEANBLEND_PREFREEZE_REVIEW.md`. This was the final bounded simple-intervention screen. Final source-bound QA and fresh calibration pass; the review's minor Delta/Rho report header carryover was corrected before freeze and both checks repeated. Freeze: `2f8b144c4f1bd9f9d50524261f9858f4edf0bb84c3e079dd78635672db2b1176`. Controller launched 2026-09-16 13:46 Hong Kong, PID75828 and completed84/84 runs with a closed session. Cumulative occupation is6720.883851766586seconds. Never restart completed studies.
- Mean-blend design: 84 optimizer trajectories, original hard labels/head/decoder/constant Adam and matched initialization/batches, with `(1-rho)*threshold_loss + rho*MeanMSE`, rho 0/.25/.5 for BCE and Brier. Unchanged Mean-MSE runs once per unit. Fresh seeds start at9511001/9511101/9511201; teacher/partition remains the independent unit. No EMA, SPO, smoothing, test access or p-values. Select one common positive rho over six modified cells, then require >=.3 pp mean improvement, >=2 task means improve, no cell harmed>1 pp and normalized regret nonincrease.
- All84 mean-blend runs and336 selected/final train/validation replays pass, including independent integer decoding, selected argmin and residual identity. Descriptive attribution is complete. Common rho.5 improves only.119358pp (<.3), and DigitsBCE harms1.757813pp (>1). The full gate fails. No confirmation, no additional alpha spent, no favorable subset rescue. The final review assesses this closed outcome; all coefficients and controls remain in the records.
- EMA closed at6326.257195949554 cumulative seconds. Mean-blend inherits this once and adds failed/passing QA, report-label QA refresh, both calibration attempts and scientific training. Later stages inherit the final active_seconds once, never sum cumulative records or reset to zero. The initial14400-second guard remains; analysis/code timing is separate under `ROUND0_RESEARCH.md`.
- Completed independent study: `experiments/threshold_longrun/round0`.
- Baseline code is frozen. Do not edit the files listed by `round0/freeze.json`.
- Controller entry: `run.py all` or explicit `resume`; study status and logs are in round0.
- Calibration passed with projected 7,854 CPU wall seconds (about 2.18 h) including a 1.5 multiplier. Initial occupation guard: 14,400 seconds across the campaign; subtract all prior round budgets from later allocations. Existing unrelated GPU processes belong to iclr27-drift-wm and must not be interrupted.
- After round0 completes, run/verify the full analyzer, then use the attribution script on DEVELOPMENT records, and inspect confirmation outcomes only to assess the frozen claims.
- Attribution command from repository root: `python experiments/threshold_longrun/research/attribute_round.py --work experiments/threshold_longrun/round0`. It also works immediately after development selection is sealed; it never reads test labels.
- Apply the result-to-claim skill for an independent judgment where available. Its hardcoded old model may be unavailable; use an available reviewer without claiming the unavailable model was used. This is a bounded claim-review subtask, not permission to launch unbounded search agents.

## Candidate decisions after results

The prospective guidance below governed the completed sequence. It does not authorize bypassing the final-screen stopping rule recorded above.

Use development records to distinguish slow fitting, overfitting, saturation, residual cancellation and partition sensitivity. These are hypotheses, not causal conclusions from a plot. Search primary literature for a concrete intervention corresponding to the observed failure mode. Prefer one small, explained candidate family at a time. Examples to consider only after diagnosis include common learning-rate schedules, a controlled mean-error regularizer, or a same-head decision-aware term. Do not call an established combination novel without checking prior work.

No new candidate may use confirmation errors to choose its hyperparameters or select its best checkpoint. No task/seed/method may be removed for being unfavorable. Preserve empty/failing/negative runs as such; do not manufacture valid results. Additional candidates get new protocol IDs, source hashes and development/confirmation seeds. Digits still reuses the public 1797-image pool; random partitions are not new independent datasets.

## Confirmation and stopping

Round0 alpha is .025 for its nine-test family. Later confirmation round r has alpha .05/2^(r+1); also apply its declared within-round correction. Plan enough independent units for an exact test to reach that level, before training. Failed allocations are not recycled. Report marginal intervals separately from multiplicity-adjusted tests.

Use the strong-advantage gate in each frozen protocol. Achieving a small p-value alone is insufficient; require effect size, consistency and regret guardrails. If the gate is met, seek one locked independent replication when budget permits, then revise the manuscript with the exact supported claim. If gains vanish, record the finite-budget or conditional finding. If the initial device-time budget is exhausted, preserve state and notify the user with results and the evidence-based next step instead of silently exceeding the guard or declaring success.

## Communication and automation

An app heartbeat may continue this same thread after training stages. It should be quiet while training remains healthy and unchanged, and notify on stage completion, important findings, failures, budget exhaustion or user action needed. Honor a user's PAUSE/stop instruction; never automatically remove a user-created PAUSE marker. Resume only when the user has explicitly requested it or when recovering a technical crash within the already authorized run and after confirming that no manual pause is intended.

Created heartbeat ID: `automation`, name `累加头长训练与逐轮研究`, every 15 minutes, attached to this thread. The separate automation `rl` belongs to `iclr27-drift-wm`; do not update or pause it for this project.

Keep a per-round research ledger with sources and dates, observation vs explanation, all candidate outcomes, and allowed/disallowed paper claims. Update the top-level project entry only with verified progress. Do not claim ICLR acceptance is assured.
