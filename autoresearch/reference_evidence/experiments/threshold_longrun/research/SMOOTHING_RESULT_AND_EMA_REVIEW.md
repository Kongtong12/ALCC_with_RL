# Smoothing result and bounded EMA proposal review

Date: 2026-09-16. Independent reviewer: available secondary GPT-6 Codex agent, disclosed fallback for unavailable gpt-5.4. Read-only result-to-claim review and design assessment; no training, scientific test access, paper edits or frozen-source edits.

## Smoothing result-to-claim decision

**claim_supported: no**, for advancing the common smoothing candidate. **Confidence: high** for the failed-gate decision; low for broad causal explanations or rejection of label smoothing generally.

Independent arithmetic reproduces the selected delta .1's -0.7161458 percentage-point mean improvement and normalized-regret increase of +0.000772251. All three task means worsen; five of six modified objective/task cells worsen and the remaining Digits BCE cell ties. All four prespecified gate checks are false. Delta .25 is worse overall as well. No confirmation of this common smoothing candidate is warranted.

The 84-run audit reports 336 selected/final train/validation replays, complete metric-dictionary agreement and independent integer decoding of saved binary32 predictions. Its freeze and audit-script hashes match current files. I inspected the replay logic and checked the aggregate arithmetic; I did not independently repeat all model forward passes.

The postmortem gives a useful negative mechanism check: wrong saturation decreases sharply on the synthetic tasks while both fitting and validation decision quality worsen. For ReLU BCE, training error rises from .456% to 2.930% and validation error from 10.156% to 11.589% at delta .1. Lower saturation therefore cannot be equated with better decisions in these experiments. This supports neither an assertion that saturation was the primary bottleneck nor a claim that smoothing never helps. The intervention changes optimization and finite-model regularization as well as confidence; it is not an isolated causal manipulation of one mediator.

Keep the complete negative result and its original common-delta decision. A favorable individual delta/task slice does not authorize rewriting the gate or claiming held-out improvement. The remaining confirmation allocation is unchanged because this screen used no tests.

## One bounded EMA candidate

**Recommendation: defensible as one small established estimator intervention, with no predicted positive result.** It preserves the hard targets, original three objectives, Adam trajectory, architecture and ordinary decoder. The intervention chooses a temporally averaged parameter vector for prediction. It is not a new objective, not prediction ensembling, and not a convergence guarantee.

The development diagnostics provide modest motivation: late adjacent validation-error changes average approximately .68 to 1.48 points across unsmoothed task/objective groups, with variable drift. They do not measure optimizer noise directly. All checkpoints are evaluated on the same finite validation set; movement can reflect changing boundaries, drift, overfitting and the discontinuous path argmin, not independent fresh validation samples. For example, Digits Brier's substantial late first-to-last deterioration is consistent with drift as well as local fluctuation. EMA might help, do nothing, or retain inferior earlier parameters.

EMA introduces temporal lag and an averaging bias as well as suppressing some rapid parameter changes. With beta .99 and .999, effective averaging windows are roughly 100 and 1000 updates, respectively. Differences between those settings cannot be attributed solely to a noise mechanism. In a nonlinear network, the average parameter vector does not equal the average prediction; averaging along one trajectory does not guarantee lower loss or better decisions. A successful screen would support this estimator procedure, not a causal explanation of the earlier ranking.

## Exact procedure to freeze

Use new development seeds 9501001 onward and the R0 development-selected recipes. There are **36 optimizer trajectories**, each carrying raw parameters plus two shadows. They supply three correlated estimator outcomes per trajectory, not 108 independent fits or additional independent data units. Average two Digits initializations within each partition before comparing units.

Define theta_t as the raw model after update t. At update 600, initialize each shadow by copying theta_600 exactly. For t>600 use

`shadow_t = beta * shadow_(t-1) + (1-beta) * theta_t`.

Use beta in {.99,.999}, with no zero initialization or extra bias correction. Initialize and update after the specified optimizer update; do not leave the ordering implicit. Raw and both shadows should have the same eligible validation checkpoints beginning at 600 and their own identical error/regret/earliest-step selection rules. Their checkpoint-600 predictions must coincide. Retain raw and both shadow trajectories and final outputs, including failures.

Shadows must never enter the optimizer, raw gradients, batches or raw parameters. Evaluate them on a separate model or restore the raw state without mutating optimizer references or RNG. Constant buffers should remain identical; this architecture has no batch-normalization statistics requiring recalibration. Parameter averaging must not silently become logit/probability averaging. Each delivered predictor retains one ordinary forward pass and the same decoder, but additional validation/copy/checkpoint work incurs development compute and memory overhead.

## Common-beta gate

Before outcomes, freeze one beta selected across the nine task/objective cells by equal-task/equal-objective selected validation error, then normalized regret, then a stated deterministic beta tie-break. Compare each chosen-beta cell with its paired raw estimator. Advance only if:

- nine-cell mean error improvement is at least .3 percentage points;
- at least two task means strictly improve;
- no individual objective/task cell worsens by more than 1 point;
- nine-cell mean normalized regret does not increase.

The raw arm has no beta; do not give it fewer validation checkpoints or optimize a per-cell beta for the aggregate claim. Each estimator selects its own checkpoint using the same rule. This gate remains exploratory and selected-validation estimates are optimistic. It is not the original strong-BCE gate: EMA may benefit Brier or Mean-MSE at least as much as BCE. A pass must not be reported as proof of BCE superiority.

## Required engineering evidence

Before freeze, verify the recursion on explicit small parameter sequences; exact initialization at step 600; constant buffers; no tensor aliasing; and limiting beta=0 behavior in an engineering fixture. Most importantly, compare an uninterrupted raw-only run with a shadow-enabled run and require identical raw model, Adam state, batch stream, RNG and raw metrics/history. This directly tests the zero-feedback claim.

Interrupted and forced-kill replay must restore the raw model/optimizer/RNG, both current shadows, their update counters, separate selected states, fixed snapshots and curves. Each estimator needs independently replayable selected/final predictions. Validate complete cell accounting, the common-beta choice, and all gate failure branches. Keep evaluation inaccessible and bind the source, protocol, QA and calibration records as before.

The scientific occupation budget starts at 6061.4976 cumulative seconds within 14400. Under the original `ROUND0_RESEARCH.md` contract, code and analysis work are outside device occupation and their timing is reported separately; QA, calibration and scientific execution are charged. This clarifies any earlier reviewer wording that suggested automatically charging post-hoc analysis replay. Calibrate the complete new workload, including shadow copying and triple validation, rather than assuming it costs exactly one-third of three separately trained models.

If the frozen screen fails, close this candidate without post-hoc beta/start-time expansion. If it passes, a separate equally tuned raw-versus-EMA confirmation can share the raw trajectory wherever the frozen recipe matches, but still needs fresh units, planned hypotheses and the next alpha .0125. Nine within-objective raw-versus-EMA contrasts would match the stated claim; any other superiority claim needs its own declared family. No held-out or manuscript claim follows from the screen alone.

Overall route: record the negative smoothing result; one 36-trajectory EMA screen is reasonable after primary-source and engineering review. Preserve modest interpretation and all negative outcomes.
