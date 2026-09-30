# SPO+ development screen: negative outcome and attribution

Date: 2026-09-16. Scope: development only. This report does not use confirmation labels.

All 108 fixed-recipe runs finished. The chosen common positive weight is 0.1. Relative to the three unmodified objectives, equal-task/equal-objective validation error **increases by 0.564236 pp**, and normalized regret increases from 0.01136137 to 0.01244629. The frozen development gate fails. No SPO+ confirmation is authorized by this outcome.

| Task | Error improvement, control minus hybrid (pp) |
|---|---:|
| ReLU | -1.497396 |
| Quadratic | -0.911458 |
| Digits | +0.716146 |

All six synthetic objective/task cells worsen. Digits improves for BCE and Mean-MSE and ties for Brier. Weight 1 is worse in aggregate. The complete 27-cell table and seed results remain in `../../threshold_spo_screen/work/SCREEN_REPORT.md` and `screen_analysis.json`; no favorable subset replaces the common-weight gate.

## Verification

`development_replay_audit.json` checks all 108 receipt/checkpoint bindings. Selected and final models were replayed on training and validation data (432 model/split evaluations). Every saved metric matched exactly. Independent integer arithmetic on exactly scaled binary32 predicted costs reproduced the nonoptimal-path counts and true regret. No evaluation gate or confirmation run exists. Frozen sources remain unchanged.

The same audit probes base and normalized SPO+ parameter gradients on six fixed training batches per zero-weight model. `postmortem_diagnostics.json` adds crossing magnitudes. These are local descriptive measurements at selected models, not a causal decomposition of training trajectories.

## What the diagnostics say

- BCE training errors average 0.13%, 0.13%, and 0.00% on ReLU, quadratic, and Digits, versus validation errors 9.05%, 13.61%, and 5.92%. Brier has similarly large train/validation gaps. This motivates testing regularization, but it does not establish overconfidence as the cause.
- The median ratio of normalized SPO+ gradient norm to base gradient norm ranges from 0.178 to 23.629 across cells. A common numerical weight is not a common relative force. The failed screen does not establish that optimally tuned SPO+ hybrids cannot help.
- Synthetic base/SPO+ gradient cosines are positive in all probes; observed harm cannot be attributed to simple instantaneous negative alignment on this evidence.
- Digits raw crossing rates near 99% count **any** adjacent positive difference, however small. For BCE/Brier, the fractions with a crossing exceeding 0.01 are 9.70%/30.67%, and average positive adjacent differences are 0.00138/0.00316. Synthetic BCE/Brier crossing magnitudes are much smaller. Keep the original metric; do not translate it into a frequency of wrong paths.
- Sorting threshold probabilities would preserve their sum in real arithmetic and hence preserve decoded costs. Raw crossings alone do not justify a claim that enforcing monotonicity would improve decisions.

## Routing

Independent review: `SPO_RESULT_AND_NEXT_REVIEW.md`. Do not confirm this common-weight candidate or declare a Digits-only gain. The next bounded hypothesis is local ordinal target smoothing that preserves each label's mean; its rationale and limits are in `SMOOTHING_SCREEN_RESEARCH.md`. It changes threshold supervision and must not be framed as an isolated scoring-rule comparison.

Final cumulative occupied training/engineering time: **5698.4090695381165 / 14400 seconds**. Subsequent stages inherit this value once, then add their own QA, calibration and active training. Analysis and writing are outside the device-occupation contract.
