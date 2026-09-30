# Campaign reassessment: final evidence and routing

Date: 2026-09-16. Independent reviewer: available secondary GPT-6 Codex agent, disclosed fallback for unavailable gpt-5.4. Scope: final result-to-claim review of the completed round-0 confirmation and all five completed development screens. Mean-blend is **closed and audited**. Its scientific results were inspected only after closure. No training, scientific evaluation access, frozen-source edit, or manuscript edit was performed.

## Verdict on the intended strong advantage

**claim_supported: no. Confidence: high for failure of the prespecified strong BCE claim.** Round 0 has zero qualifying tasks, and none of the five completed development screens passed its advancement gate. The planned simple-intervention campaign now closes with no candidate advancing. Those screens cannot supply confirmatory support for a claim that round 0 failed. This verdict does not erase the narrower corrected findings, establish equivalence, or claim that no useful method can exist.

Round 0 is the campaign's only completed inferential performance study. Its 6,000-update, validation-selected procedures use a matched architecture, tuning candidate count, initialization/batches within comparisons, and independent confirmation units. At the nine-comparison family allocation .025, the supported error findings are:

- Brier improves upon decoded Mean-MSE on ReLU and quadratic teachers: differences -2.524 and -3.613 percentage points; Holm p=.017578 for each.
- BCE improves upon Mean-MSE on quadratic: -2.612 points, p=.017578.
- Brier improves upon BCE on ReLU: BCE minus Brier +.659 points, p=.023438.
- BCE versus Mean-MSE on ReLU does not pass the allocation despite its favorable observed difference; p=.029297. No Digits contrast passes correction.

The test interpretation is conditional on independent, sign-symmetric paired differences, not assumption-free. Ten teachers/partitions per task give limited precision. Brier's numerical quadratic advantage over BCE is not corrected evidence for that contrast. The favorable synthetic Brier comparisons do not establish a new across-task strong advantage over both controls. BCE's lower mean Digits error also is not a corrected or regret advantage there.

The honest supported message is that objective choice affects these trained procedures and that BCE's claimed consistent advantage over matched controls does not survive this broader protocol. Threshold Brier's improvements over decoded-mean supervision on the two synthetic tasks are useful positive evidence with a defined scope.

## Completed development ledger

Positive numbers below mean lower selected validation error than that stage's matched control. They are descriptive development quantities, not independent test estimates or comparable estimates from a common randomized multi-intervention trial.

| Screen | Trajectories | Frozen common choice | Aggregate improvement (pp) | Routing |
|---|---:|---|---:|---|
| Constant versus cosine schedule | 72 | Cosine to 5% of starting rate | -.658275 | Failed; no confirmation |
| Base objective plus SPO+ | 108 | Alpha .1 | -.564236 | Failed; regret also increases |
| Mean-preserving local smoothing | 84 | Delta .1 | -.716146 | Failed all four guards |
| Raw versus EMA | 36 raw optimizer trajectories, 108 correlated outputs | Beta .99 | +.130208 | Below the .3-point requirement; no confirmation |
| Threshold/mean blend | 84 | Rho .5 | +.119358 | Below .3 points and Digits BCE harm exceeds 1 point; no confirmation |

The schedule threshold was .2 points; the later thresholds were .3 points. The schedule/SPO/EMA aggregates include nine task/objective cells; smoothing and mean-blend include six modified cells and exclude unchanged Mean-MSE. Do not present the numbers as a league table ranking optimally tuned interventions. Each stage used fresh development units and fixed round-0 development recipes, so changing baseline levels across stages are not intervention effects. A common numerical coefficient also imposes different relative gradient strength across losses.

The audits report exact receipt/model/metric replay and independent integer-decoder agreement for the completed studies. Those checks make an unnoticed bookkeeping or decoding explanation less likely; they do not establish the scientific mechanism, adequacy of the recipe grid, or generality. Development has three teacher/partition units per task. Selected validation and selection of a coefficient using it are optimistic; no significance or equivalence claims should be attached to these screens.

## What the negative interventions teach

Smoothing substantially reduced wrong saturation while worsening training and validation decisions on synthetic tasks. EMA reduced late adjacent validation fluctuations in all nine cells without attaining the required aggregate improvement. These observations show that improving those measured proxies was insufficient for the tested procedures. They weaken a simple diagnostic story that desaturation or smoother curves alone would fix the observed ranking. They do not establish that confidence or stochastic optimization is irrelevant.

SPO's common coefficient has markedly different gradient-norm ratios across objectives; its synthetic probes did not show negative alignment. Its failed screen is not proof that gradient conflict caused harm or that independently tuned SPO combinations cannot help. Strict threshold crossings can be tiny tail inversions; a near-100% event rate is not a near-100% path failure rate. None of these postmortem diagnostics is a causal mediation analysis.

Six thousand updates still do not establish convergence. The old and new studies also differ in search range, checkpoint selection, sampling, and the synthetic primary endpoint (tied-only versus all-context). Their ranking difference is evidence of protocol sensitivity, not an isolated causal estimate of extra updates. The cumulative head shares function class but not loss gradients, optimization geometry, or effective finite-budget regularization.

Digits partitions reuse one fixed 1,797-image pool. Averaging two optimizer repetitions within each partition is correct, but fresh partitions do not supply new independent datasets or establish generalization to new source populations. The campaign's teacher and routing results should not be generalized to all decision problems. This review does not assess or invalidate separate formal theorems or unrelated paper experiments.

## Final blend outcome and routing

**The closed, audited mean-blend gate fails.** Independent integer-count reconstruction reproduces the .119357638889-point gain, task gains of +.1953125/+1.07421875/-.91145833, and Digits BCE harm of 1.7578125 points. The aggregate and individual-harm guards fail; task consistency and normalized-regret guards pass. The quadratic Brier gain of 2.083333 points does not replace the common-coefficient target. All 84 runs, 336 selected/final train/validation replays, integer decoding, selector checks, and residual identity checks are reported as passing; source, audit, diagnostics, and all result-hash bindings were independently verified. Details are in `MEANBLEND_RESULT_REVIEW.md` and its JSON record.

Close the entire planned simple-intervention sequence. Retain all coefficients, cells, teachers/partitions, checkpoints, diagnostics, and failed gates. Do not expand rho, lower a threshold, switch to final-step error, choose a favorable task/loss subset, or spend a new confirmation allocation on the rejected procedure. No additional routine optimization or loss tweak is justified merely by unused device time. Final cumulative occupation is 6720.883851766586/14400 seconds; the unused allowance is not a continuation rationale.

The scientific conclusion is: the longer, matched evaluation does not establish the intended strong BCE advantage; it does identify conditional synthetic benefits of threshold Brier over decoded-mean MSE, while a sequence of predeclared, fixed-recipe development interventions did not meet their advancement criteria. This is a bounded negative robustness and sensitivity result, not proof that the objectives are equivalent or that all members of these method families fail.

An eventual research pivot would need a substantive new question and design rather than continuation of this rescue sequence. It is not part of the present recommendation. The immediate deliverable should be the faithful claim revision and complete reproducible negative ledger. The parent can assess how much belongs in the paper versus the supplement or project report, without presenting exploratory outcomes as new confirmations.

No new confirmation allocation was spent by these development screens. The reserved next allocation remains .0125, but its availability does not authorize confirmation of a failed candidate or override the stopping rule. Any later distinct research program would require its own substantive question and prospective protocol; it is not an automatic continuation of this campaign.

## Evidence reviewed

`ROUND0_RESULTS.md`, `ROUND0_CLAIM_REVIEW.md`, the schedule's complete `SCREEN_REPORT.md` and review, `SPO_SCREEN_RESULTS.md`/`SPO_RESULT_AND_NEXT_REVIEW.md`, `SMOOTHING_SCREEN_RESULTS.md`/`SMOOTHING_RESULT_AND_EMA_REVIEW.md`, `EMA_SCREEN_RESULTS.md`/`EMA_RESULT_AND_NEXT_REVIEW.md`, the final mean-blend analysis/audit/diagnostics and `MEANBLEND_RESULT_REVIEW.md`, `CAMPAIGN.md`, and `findings.md`. These synthesize independently verified arithmetic and source-bound audits; no scientific experiments were repeated for this reassessment.

Status: **final: all five screens closed, no candidate advances, and the planned simple-intervention sequence stops.** The narrower round-0 corrected findings remain the campaign's supported inferential conclusions.
