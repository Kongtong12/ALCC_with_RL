# Round 0 independent result-to-claim review

Date: 2026-09-16. Verdict: **claim_supported: no** for the prespecified strong BCE advantage. Confidence: **high** that this gate failed; **medium** for broader performance and mechanism conclusions.

Reviewer: an available secondary GPT-6 Codex agent. The skill requests gpt-5.4, which was unavailable; this is a disclosed secondary-agent fallback, not a gpt-5.4 review. Scope: bounded read-only assessment of the completed round, its frozen source, and development attribution. No training, manuscript edit, or change to frozen artifacts was performed. Only these review files were added. The parent agent should record the verdict in its findings/pipeline record as required by the skill.

## What the results support

The matched 6,000-update protocol compares three losses on the same cumulative sigmoid head, initialization, batch stream, architecture, data, candidate count, and validation checkpoint rule. It evaluates the selected training procedures, not losses at convergence.

| Task | BCE error % | Brier error % | Mean-MSE error % |
|---|---:|---:|---:|
| ReLU teacher | 10.7617 | 10.1025 | 12.6270 |
| Quadratic teacher | 14.5850 | 13.5840 | 17.1973 |
| Digits routing | 7.6318 | 8.4424 | 8.5010 |

Within the frozen nine-comparison family at alpha .025, Brier has lower nonoptimal-decision error than Mean-MSE on both synthetic tasks (Holm p=.017578 each), and BCE has lower error than Mean-MSE on the quadratic task (p=.017578). Brier also has lower error than BCE on ReLU (0.6592 percentage points; p=.023438). These are conditional on the paired sign-symmetry assumption used by the exact sign-flip test.

BCE versus Mean-MSE on ReLU has an observed -1.8652 point difference, but p=.029297 exceeds the allocated alpha. All Digits contrasts are nonsignificant after correction. Nonsignificance does not establish equivalence. The marginal percentile intervals cannot override the corrected decision rule.

The strong BCE gate plainly fails: BCE does not beat both controls on any task. Its numerical Digits advantages are below 1 percentage point, and its mean regret is slightly larger than Brier's there. There is no basis to round the result to partial support for the stated strong claim.

Suggested claim revision: “Under a matched 6,000-update, validation-selected protocol, objective choice affects performance, but BCE does not show a consistent advantage over both matched controls. Threshold Brier improves upon decoded-mean MSE on both synthetic tasks; the Digits comparisons remain inconclusive under multiplicity correction.” This is a research conclusion for the parent to assess, not authorization to edit the manuscript.

## Statistical and engineering assessment

- I independently recomputed all nine exact sign-flip tail counts from the integer unit error counts. Every count matches the saved analysis. The Holm step-down implementation is correct. All five frozen source/data hashes match the current files. No material engineering defect was identified in this bounded inspection.
- The analyzer checks completion and gate receipts, reconstructs all 120 models, verifies selected and four fixed snapshots against saved arrays, and independently calculates exact integer path scores. This is strong consistency evidence. I inspected that implementation and its completion report; I did not rerun the 600 model-snapshot forward passes. Replay cannot establish the scientific assumptions behind an estimator.
- The inferential unit is correctly the synthetic teacher/data seed or the mean of two optimizer runs within a Digits partition. Using 20 Digits optimizer runs as 20 independent data units would be incorrect. The current code does not do that.
- Exact sign-flips are exact under independent, sign-symmetric paired differences under the null (or an appropriate exchangeability/randomization justification). They are not assumption-free tests of equality of means. With ten units, checking symmetry reliably is difficult. Keep this qualification visible.
- The 95% bootstrap intervals are marginal, not simultaneous, and have only ten units. They are descriptive uncertainty summaries; do not use an interval excluding zero as an alternative route to a familywise claim.
- The .025 round-0 allocation followed by .05/2**(r+1) for rounds r>=1 sums to .05 over the entire campaign. This controls campaign familywise error by a union bound only if each later confirmatory family has valid conditional error control after adaptation. Preserve fresh confirmation randomness, frozen selection, the full family, and failed rounds; do not recycle alpha.
- For nine two-sided exact sign-flip contrasts, the smallest possible Holm p with ten nonzero paired units is 9*(2/2**10)=.017578. Thus a round-1 alpha .0125 cannot reject anything with ten units. At least eleven units are necessary for a possible rejection; twelve is a sensible minimum, not a power guarantee. If many later rounds are contemplated, their decreasing alpha requires a fresh discreteness/power calculation.
- The strong gate combines significance against zero with observed >=1 point and >=10% differences. Even a future gate pass would not prove the population effect exceeds both minimum-effect thresholds. Such a claim would require uncertainty/testing against the corresponding margins. A mean-regret guard is likewise an observed guard, not statistical proof of noninferiority.

## Limits of interpretation

**Six thousand updates do not prove convergence.** They address one short-budget concern. Constant-step Adam, stochastic batches, finite model capacity, validation checkpoint selection, and continuing late movement leave optimization and generalization effects entangled. The development quadratic Brier optima at 6000/6000/5700 are direct evidence that the selection boundary remains relevant. Neither low training error nor a small local gradient by itself establishes convergence, stationarity of the full objective, or comparable optimization error across losses.

**Validation selection is optimistic, while the independent test remains appropriate for the selected procedure.** Each run chooses among 19 eligible checkpoints, and development selects among 18 recipes per method. The best validation values and the resulting train/validation gaps are selection-dependent descriptive numbers. On fresh synthetic confirmation units, independent test data provide a legitimate evaluation of the frozen recipe plus per-run validation-selection rule. This is not test selection. On Digits the analogous interpretation is conditional on the fixed source pool and independent partition/board randomness. Choosing a later method, stopping rule, or claim from the reported confirmation/fixed-step results would require new confirmation.

**Same head does not mean same link gradient.** Write q=sigmoid(z), threshold target t, and M=K-1. Ignoring shared averaging constants, BCE has logit gradient q-t; Brier has 2(q-t)q(1-q); decoded-mean MSE has a shared mean residual times 2q(1-q)/M. Thus Brier and Mean-MSE have sigmoid attenuation, whereas BCE-with-logits cancels it in its derivative. BCE still uses the same sigmoid in decoding. The comparison legitimately holds the function class fixed while changing objective geometry. It does not isolate a loss-independent optimization effect.

The development wrong-saturation rates are small and are often larger for BCE than Brier. They do not support a simple story that Brier fails because it uniquely gets stuck at wrong saturated labels. Saturation is expected for well-predicted binary thresholds and is not itself evidence of harmful vanishing gradients. Same-parameter gradient comparisons are local diagnostics; their norms and eight-batch noise summaries do not identify the cause of held-out differences. Adam can attenuate uniform gradient rescaling, and coupled weight decay further makes objective-scale interpretations nontrivial. Dividing Brier's gradient by q(1-q) reproduces BCE's gradient up to scale and is not a distinct methodological contribution.

**Digits is an intra-pool experiment.** The ten independently randomized partitions can be inferential units conditional on the fixed 1,797-image pool even though their memberships overlap. Conditional on that pool, independently generated partition/board randomness yields repeated algorithm evaluations. Those partitions are not ten independently collected datasets, and overlap prevents using this result to claim generalization to new source populations. Source identities are disjoint within each partition, which addresses within-run leakage; an image may legitimately appear in development training and later confirmation test under the explicitly conditional estimand. Broader generalization needs independent source data, datasets, or collection units.

## Next experiment, based on development evidence only

Recommend a **small, fresh-development comparison of constant learning rate against one prespecified common cosine decay**, with all three losses unchanged. Use each task/method's round-0 development-selected LR/WD, matching all other ingredients, 6,000 updates, and identical selection opportunities. Three new development units per task and two initializations per Digits partition imply 72 fits for the two schedules. This is a focused intervention at fixed recipes, not a claim that either schedule has been fully optimized.

The developmental motivation is specific: ReLU Brier selected validation error is 7.031% versus 8.854% at 6000, Mean-MSE is 9.766% versus 12.109%, Digits selected times vary widely, and quadratic Brier often selects the final boundary. Together these justify examining late-update stability and the cost of keeping a fixed learning rate. They do not show that cosine will help, that large learning rates caused the gaps, or that BCE will benefit more than its controls. Selected minima necessarily improve on final validation, so the gap alone is not a causal diagnosis.

Before this screen, freeze the schedule definition, new development seeds, comparison endpoints, and the decision rule for whether to invest in a full round. Assess fixed-step 6000 outcomes and late training/validation movement along with the existing selected endpoint; retain the full trajectories and every failed candidate. Do not search many decay variants or favor BCE based on the confirmation ranking. A zero-ending cosine schedule is one reasonable bounded candidate, but its endpoint and implementation must be fixed before viewing new results.

If the screen warrants a confirmatory round, give all unchanged losses the same candidate-budget and schedule-selection rules, then freeze complete choices and use fresh confirmation units (at least twelve for the proposed next nine-way family). The parent should justify the final candidate using its development screen and source research. If the screen is unhelpful, preserve that negative result and stop or reconsider based on development diagnostics rather than adding favorable-test stopping rules.

Missing evidence for stronger claims includes a supported optimization mechanism, independent confirmation of any candidate intervention, stronger assessment of residual optimization error, adequate unit-level power, and genuinely independent image-source data for population generalization.
