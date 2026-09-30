# Final bounded loss-blend screen

Date:2026-09-16. This is a sensitivity test of an existing loss decomposition, not a new scoring-rule contribution. Read `EMA_RESULT_AND_NEXT_REVIEW.md` before interpreting it.

## Why this last intervention

The longer study supports Brier over pure Mean-MSE on the two synthetic tasks, while the original strong-BCE claim fails. Schedules, SPO+ mixtures and soft targets do not pass their screens; EMA produces only a small selected-checkpoint gain. These results do not demonstrate that threshold residual variation is over-penalized. The remaining narrow question is whether an intermediate threshold/mean objective improves the finite-model tradeoff. Expectations are modest, and a negative result will end this sequence of small interventions.

Use the original hard targets and define L_rho=(1-rho)L_threshold+rho L_mean, with rho0,0.25,0.5. For normalized mean loss and the original binary threshold Brier, let e_k=q_k-t_k, m=K-1. Algebra gives

L_rho=mean_k(e_k)^2+(1-rho)Var_k(e_k).

Thus Brier blending preserves the coefficient of the decoded-mean error and reduces the orthogonal threshold-residual penalty. In probability coordinates its Hessian is2(1-rho)I/m+2rho*11^T/m^2:the mean direction retains curvature2/m, orthogonal directions have curvature2(1-rho)/m. This is a parameter of a familiar quadratic objective, not a proof that residual variation causes observed regret. BCE blending changes a different gradient mixture; it does not have that same quadratic interpretation.

## Statistical target and limits

For unrestricted probabilities, let p_k=P(Y>k|x). Then E[Y|x]/m=mean_k p_k. Relative to q=p, expected excess blend risk is

- Brier:(1-rho)mean_k(q_k-p_k)^2+rho*(mean_k(q_k-p_k))^2.
- BCE:(1-rho)mean_k KL(Bern(p_k)||Bern(q_k))+rho*(mean_k(q_k-p_k))^2.

These elementary expressions show the true threshold vector remains the unique probability-space optimum when0<=rho<1, subject to the usual extended-value endpoint conventions for BCE. At rho1 only the mean is identified. Our unconstrained finite network, shared parameters and finite training need not attain that optimum. Properness is not a finite-model, convergence, calibration-improvement or shortest-path guarantee. Outputs are still independent sigmoid coordinates, not necessarily a valid cumulative distribution before fitting.

[Gneiting and Raftery, JASA2007](https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf) provide the established proper-score framework. [Reid and Williamson, AISTATS2010](https://proceedings.mlr.press/v9/reid10a.html) distinguish probability-space scores from composite losses with a link. Both primary sources were checked. The excess-risk calculation above follows by directly expanding these existing objectives; no novelty claim is made for their combination. The old `allocation_regularization_v2` is a different local good-set-mass/KL objective over scalar costs, not a duplicate threshold/mean mixture.

## Fixed design and stopping rule

Study`THRESHOLD-MEANBLEND-SCREEN-20260916-D5`;directory`experiments/threshold_meanblend_screen/work`.

- New development seeds9511001-9511003,9511101-9511103,9511201-9511203. Three teachers per synthetic task; three Digits partitions with two initializations. The teacher/partition, not every method/run, is the independent unit.
- Three rho values each for BCE/Brier, plus one unchanged Mean-MSE control:84 optimizer trajectories. Original model, hard labels, scalar costs, decoder, batch sequence and initialization are matched. No EMA,SPO or label smoothing.
- Constant Adam,6000updates, original round0 development-selected LR/WD per base objective, identical checkpoint-selection rules. This fixed-recipe screen is not the final equally tuned comparison. Gradient scales and optimizer interactions can change.
- Select ONE common positive rho over six modified task/objective cells by mean validation error, normalized regret, then smaller rho. Mean-MSE cannot affect this selection.
- Advance only if mean improvement>=0.3pp,at least two task means strictly improve,no individual modified cell worsens>1pp,aggregate normalized regret does not increase,and every run is valid. Preserve every outcome. No p-values or test access.
- If negative, end nearby parameter rescues:do not add more rho values, adapt them per task, drop a method, or switch endpoints. Reassess the campaign around the supported evidence before any different research direction.
- If positive, a new equally tuned/fresh-unit confirmation is still required. Next family alpha0.0125, at least12 independent units, explicit comparison family, exact-test resolution and full-budget projection. A development gain is not a confirmed scientific advantage.

## Engineering and budget

Test exactrho0 original/rho1 Mean-MSE values and model gradients, unchanged Mean-MSE at every rho, finite-difference derivatives, Brier decomposition/Hessian, invalid-rho rejection, same initialization, access gates, common selection/harm/regret gates and exact interrupted/forced-kill continuation.

The first gradcheck fixture failed because its BCE logits were float64 but targets remained float32, which produces a float32 BCE scalar. A separate two-logit reproduction identified the issue; converting targets along with logits passes without changing tolerance or training code. This pre-freeze attempt is retained and charged; `work/ENGINEERING_NOTES.md` records it. Full source-bound QA and calibration must pass before scientific execution.

Inherited cumulative occupation6326.257195949554seconds. The14400-second cap includes all subsequent QA, calibration and training; analysis remains separately timed. Prior failed stages and their budgets remain unchanged.
