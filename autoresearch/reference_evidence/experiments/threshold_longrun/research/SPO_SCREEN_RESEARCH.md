# After the negative schedule screen: a decision-loss intervention

AS_OF: 2026-09-16. Mode: method-design / experiment-design. Effort: quick. Question: does adding an established decision-regret surrogate help the same cost head at fixed developmental recipes?

## Observation and attribution

The full 72-fit schedule screen failed its frozen gate. Equal task/objective selected-validation error worsened by 0.6583 pp; task means worsened by 0.2604/0.3255/1.3889 pp (ReLU/quadratic/Digits). Selected-step opportunity is matched but validation minima are optimistic. At the final step cosine sometimes improves individual synthetic recipes, yet not the primary screen aggregate. Therefore it is not justified to spend confirmation budget on this common cosine candidate. This does not prove that all learning-rate schedules are ineffective or that constant rates are globally optimal.

Round0 development also shows tiny training errors with persistent validation errors, while threshold errors need not align with path costs. The next hypothesis is to add decision information to the training objective, keeping labels, model, decoder, steps and batch streams fixed. Prior local work already tried a BCE/SPO+ hybrid with mixed short-budget results; this is a longer-budget matched screen across all three base objectives, not a new loss invention or an undisclosed rediscovery.

## Primary-source evidence

| ID | Claim | Source and locator | Verdict / constraint |
|---|---|---|---|
| P1 | SPO+ is convex in predicted costs and upper-bounds the decision-regret loss; a subgradient is 2(w*(c)-w*(2c_hat-c)). | Elmachtoub & Grigas, https://arxiv.org/pdf/1710.08005 , Proposition 3, printed page 18. | Confirmed. Convexity in costs does not imply convexity in neural parameters. |
| P2 | Calibration/risk-transfer results for SPO+ require distributional and feasible-set assumptions. | Liu & Grigas, NeurIPS 2021, https://papers.nips.cc/paper/2021/hash/b943325cc7b7422d2871b345bf9b067f-Abstract.html and linked paper. | Confirmed at the paper's scope. Do not apply a continuous conditional-cost consistency theorem directly to deterministic discrete tied labels here. |
| P3 | Decision-focused surrogates do not uniformly dominate MSE; model assumptions and optimization errors matter. | Decision-Focused Learning with Directional Gradients, NeurIPS 2024, https://papers.nips.cc/paper_files/paper/2024/file/907a9fb75a408f6c3a2ae1bf84c39e44-Paper-Conference.pdf . | Confirmed as a competing-method and assumption boundary, not a ranking for our experiment. |
| P4 | The hybrid will improve our validation and future held-out decisions. | Unknown. | Uncertain, subject to the frozen screen and fresh confirmation. |
| P5 | Improving regret necessarily improves nonoptimal-path frequency. | Not implied: magnitude and frequency differ; round0 Digits provides a local counterexample to rank equivalence. | Refuted. Keep both outcomes and a regret guard. |

Two targeted queries and three primary papers opened; five claims, three confirmed with scope, one uncertain, one refuted. No search agents. The earlier independent result-to-claim review remains in the ledger.

## Frozen exploratory screen

In `experiments/threshold_spo_screen`, use new development seeds 9481001 + task offsets. Three units per task; two paired optimization seeds per Digits partition. For every base objective, compare alpha in {0, 0.1, 1} in `L_base + alpha * SPO+ / ((K-1)*max_path_length)`. Constant Adam uses each task/loss's round0 DEVELOPMENT-selected LR/WD. There are 108 fits of 6000 updates. All three objectives keep the same cumulative head and exact argmin decoder. The SPO+ oracle enumerates all paths, including when perturbed costs are negative, and uses float64 arithmetic. Alpha zero returns the original loss exactly.

Select ONE common positive alpha by equal-task/equal-objective validation-selected error, then normalized regret, then smaller alpha. Proceed only if it improves the aggregate by at least 0.3 pp, improves at least two task means, no task mean worsens by more than 1 pp, and average normalized regret does not increase. No test data or significance claim is allowed in this screen. Preserve every result and failed gate.

If positive, the next full confirmation must compare equally tuned original and hybrid methods with new seeds, freeze the complete matrix, allocate alpha .0125 and use at least 12 paired units for its prespecified nine-comparison family (one matched hybrid-vs-base contrast per task/base loss). Do not claim global superiority over all loss families from that family. All stages inherit the previous final cumulative BUDGET: 4781.8378982543945 seconds before this screen, within 14400 total. Engineering QA and calibration are also charged. If the next complete matrix cannot fit, preserve the exploratory result and stop at the budget guard.
