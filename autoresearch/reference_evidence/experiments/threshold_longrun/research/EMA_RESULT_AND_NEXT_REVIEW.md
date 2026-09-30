# EMA result and final bounded blend-screen review

Date: 2026-09-16. Independent reviewer: available secondary GPT-6 Codex agent, disclosed fallback for unavailable gpt-5.4. Read-only result-to-claim and design review; no training, test access, paper edit or frozen-source edit.

## EMA verdict

**claim_supported: no** for advancing the common EMA candidate under its frozen gate. **Confidence: high** for that decision; low for mechanism or general efficacy claims.

Independent arithmetic reproduces beta .99's +.1302083 percentage-point mean improvement and normalized-regret decrease of .000134198. Four objective/task cells improve, one ties and four worsen. All three task means are positive, and the harm and regret guards pass, but the required .3-point aggregate improvement does not. Beta .999 is worse overall. The decision is therefore no confirmation, not “almost passed,” partial confirmation, or a license to lower the threshold.

The results support only a small descriptive selected-validation improvement for the common .99 estimator at these fixed recipes. They do not show statistically established improvement, prove noise reduction as its cause, reject EMA generally, or establish a strong BCE advantage. The 36 raw trajectories and 108 output trajectories are correlated through paired data/initialization and the shared raw training path.

The development audit reports 432 selected/final train/validation replays, exact metric and integer-decoder agreement, selected-checkpoint argmin verification, and warm-start equality. I checked its freeze and screen-analysis bindings against actual files and independently recomputed the group differences. I did not repeat the model forward passes. No technical inconsistency was identified.

## Is one more simple intervention justified?

**Conditional yes for this one final 84-fit sensitivity screen; no strong expectation of a favorable result.** The blend addresses a more direct question about the original threshold-versus-mean comparison than another generic schedule or estimator tweak. It leaves the original hard targets intact and tests the coefficient attached to threshold residual variation. That gives it value even if negative.

However, the existing diagnostics do **not** establish that this coefficient is too large. Brier already beats pure Mean-MSE on the two synthetic tasks in round 0; smoothing lowered wrong saturation while worsening fitting/validation; and EMA produced only a small aggregate change. None of those observations predicts that reducing the residual-variation term will improve decisions. The blend should be motivated as a coefficient-sensitivity hypothesis, not as the diagnosed cure for those previous failures.

I would not follow a failed blend screen with more nearby rho grids, task-specific rescue choices or another routine loss combination without a new substantive diagnosis. Close this planned simple-intervention sequence and reassess the campaign using its full negative ledger. A positive screen would justify only its prespecified independent confirmation. Remaining device time is a resource constraint, not a reason to keep generating variants until something wins.

## Algebra and interpretation

Let q be the M=K-1 threshold outputs, t the original hard threshold targets, e=q-t, and mu=mean_j e_j. The normalized decoded-mean loss is L_mean=mu^2; threshold Brier is L_Brier=mean_j e_j^2=mu^2+Var_j(e_j). Therefore

`(1-rho) L_Brier + rho L_mean = mu^2 + (1-rho) Var_j(e_j)`.

For rho 0/.25/.5, this retains unit coefficient on decoded-mean error and varies the residual-variation coefficient through 1/.75/.5. This is a genuine objective family, not an algebraic copy of Brier or Mean-MSE. At rho=1 it becomes Mean-MSE. The decomposition is of **threshold residual variation**, not raw output variance and not a proof of a causal regularization mechanism for held-out decisions.

For BCE, the analogous blend adds a mean-error component and reduces the BCE coefficient; it does not admit the same quadratic residual identity. Do not present the BCE branch as an isolated adjustment of that Brier variance term. The two branches share a mixing parameter but have different numerical loss/gradient scales. Fixed Adam LR and coupled weight decay mean this screen changes optimization geometry and effective regularization as well as the relative objective terms. Its outcome is a fixed-recipe procedure comparison, not a scale-free test of one mechanism.

There is also a useful population distinction from label smoothing. For any rho<1, an unrestricted conditional predictor q=P(Y>j|x) minimizes the threshold score and has sum_j q_j=E[Y|x], so it also minimizes decoded-mean squared risk. A positive-weight strictly proper threshold component therefore retains this common population optimum when mixed with mean-MSE. This follows from both excess risks being nonnegative and the threshold component having a unique probability optimum. It is not a convergence, finite-network, or decision-optimality guarantee; at rho=1 threshold identifiability is lost.

This weighted combination is not a novel scoring-rule invention. The parent is independently checking primary literature; the derivation above establishes the concrete local identity, not prior-art novelty.

## Historical duplication check

I inspected `experiments/allocation_regularization_v2/protocol.json`, `core.py` and `fast_local.py`. That study uses scalar cost outputs, hard continuation values, truthful path-support H, active-node weighting, and a local good-set objective of the form `-log M + alpha KL(U_G || r)`. It uses a different 600-update protocol and trains from H rather than numerical cost labels in the objective.

The proposed cumulative-threshold/decoded-mean blend is therefore **not a duplicate of allocation_regularization_v2**. Both vary an established auxiliary penalty coefficient, which is a methodological analogy rather than an identical experiment. Do not conflate their labels, architectures, objectives or conclusions.

## Exact bounded design

Use the original hard labels, three losses, cumulative head, ordinary decoder, constant Adam and R0 development-selected LR/WD. Do not carry forward SPO+, smoothing, EMA outputs or a schedule intervention. New development seeds supply paired data/initialization/batches.

BCE and Brier each use rho 0/.25/.5; Mean-MSE is unchanged and runs once per unit. With three units per task and two optimizer repeats per Digits partition, this is **84 fits**. Mean-MSE is a descriptive control and is excluded from the common-rho aggregate; counting repeated unchanged controls would dilute the question.

Freeze one positive rho chosen by equal-task/equal-objective selected validation error over the six modified task/objective cells, then normalized regret, then smaller rho. Each cell is compared with its own rho-zero run. The gate is:

- six-cell mean improvement at least .3 percentage points;
- at least two task means strictly improve;
- no individual modified cell worsens by more than 1 point;
- six-cell mean normalized regret does not increase.

Apply the guard to the selected rho; do not choose a different weight or method/task subset after a failure. Preserve all results and the identical checkpoint-selection opportunities. These are development-routing criteria, with optimistic validation selection, not significance or noninferiority findings.

Required pre-freeze QA should establish exact rho-zero original values/gradients, exact rho-one Mean-MSE endpoint in an engineering fixture, unchanged Mean-MSE controls, the Brier decomposition in the correct K-1 normalization, linearity of the mixed gradient, and finite-difference derivatives. Verify all 84 cells, independent-unit aggregation, a single common-rho selector, rejection of individual harm and regret increase, no residual earlier interventions, closed evaluation, and exact interrupted/forced-kill continuation.

The cumulative scientific occupation starts at 6326.257195949554 seconds of 14400. QA, calibration and execution are charged under the campaign contract; code/analysis timing is separate. Calibrate the complete proposed workload before freezing. No test data or p-values belong in this screen. The next confirmation allocation remains .0125, with a fresh equally tuned protocol and a family matched to its named comparisons if advancement is justified.

Overall route: close EMA as a failed advancement gate; permit this single final blend sensitivity screen with the stated interpretation and stopping boundary. Do not presume that the campaign must eventually produce a strong advantage.
