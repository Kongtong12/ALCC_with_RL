# Round 0: longer training changes the loss ranking

AS_OF: 2026-09-16. All 648 development and 120 confirmation fits completed. The analyzer replayed all 120 selected models and all 480 fixed snapshots exactly, and independently recomputed shortest-path choices in integer arithmetic.

**Prespecified BCE strong-advantage gate: FAIL (0 qualifying tasks).** Keep this result; do not weaken the gate after observing it.

| Task | Objective | All-context error %, mean ± unit SD | Mean regret |
|---|---|---:|---:|
| ReLU | BCE | 10.762 ± 1.250 | 0.115967 |
| ReLU | Brier | 10.103 ± 1.372 | 0.106396 |
| ReLU | Mean-MSE | 12.627 ± 1.002 | 0.132129 |
| Quadratic | BCE | 14.585 ± 1.767 | 0.161621 |
| Quadratic | Brier | 13.584 ± 1.515 | 0.147412 |
| Quadratic | Mean-MSE | 17.197 ± 1.882 | 0.183496 |
| Digits | BCE | 7.632 ± 2.994 | 0.162695 |
| Digits | Brier | 8.442 ± 2.814 | 0.162646 |
| Digits | Mean-MSE | 8.501 ± 2.821 | 0.190381 |

The unit is a synthetic teacher seed or a Digits source partition averaged over two optimization seeds, with ten units per task. The new primary endpoint is all contexts. Do not compare its synthetic percentages directly to the old tied-only primary endpoint.

| Task | First minus second | Error difference pp | Marginal 95% CI pp | Holm p | Pass α=.025 |
|---|---|---:|---|---:|---|
| ReLU | BCE − Brier | +0.659 | [+0.332, +1.030] | 0.023438 | True |
| ReLU | BCE − Mean-MSE | -1.865 | [-2.607, -1.084] | 0.029297 | False |
| ReLU | Brier − Mean-MSE | -2.524 | [-3.149, -1.899] | 0.017578 | True |
| Quadratic | BCE − Brier | +1.001 | [+0.273, +1.797] | 0.140625 | False |
| Quadratic | BCE − Mean-MSE | -2.612 | [-3.486, -1.684] | 0.017578 | True |
| Quadratic | Brier − Mean-MSE | -3.613 | [-3.989, -3.174] | 0.017578 | True |
| Digits | BCE − Brier | -0.811 | [-1.372, -0.176] | 0.140625 | False |
| Digits | BCE − Mean-MSE | -0.869 | [-2.329, +0.723] | 0.640625 | False |
| Digits | Brier − Mean-MSE | -0.059 | [-1.592, +1.499] | 0.951172 | False |

## Observation, interpretation and next test

1. **Observation:** Brier beats Mean-MSE on both synthetic tasks after correction. Brier also beats BCE on ReLU; its quadratic advantage is not established after correction. BCE has the lowest mean image error, but no image comparison passes the family correction. **Implication:** the old 600-update BCE ordering is not robust to this broader training and selection setup.

2. **Observation:** selected development models nearly fit the training decisions while validation errors remain substantial. Validation minima vary across steps; some quadratic selections reach 6000. All chosen learning rates are interior to the extended grid. **Interpretation:** generalization and training dynamics both remain plausible factors. This does not establish convergence, nor prove that sigmoid saturation causes the score ranking.

3. **Next test:** use only development evidence to choose a bounded intervention, keep each control equally tuned, and use a new frozen confirmation matrix. Do not tune on this test set.

## Same-recipe fixed-step secondary check

These checkpoints use the long-run validation-selected recipes, not recipes tuned separately for each budget. The table cannot isolate the effect of update count from the original study.

| Task | Objective | 600 | 1200 | 3000 | 6000 | Validation-selected |
|---|---|---:|---:|---:|---:|---:|
| ReLU | BCE | 16.592 | 12.842 | 10.894 | 10.269 | 10.762 |
| ReLU | Brier | 13.477 | 11.865 | 10.645 | 10.283 | 10.103 |
| ReLU | Mean-MSE | 14.482 | 14.126 | 13.145 | 12.954 | 12.627 |
| Quadratic | BCE | 25.698 | 17.642 | 14.785 | 14.116 | 14.585 |
| Quadratic | Brier | 28.613 | 19.683 | 14.966 | 13.550 | 13.584 |
| Quadratic | Mean-MSE | 21.528 | 18.589 | 17.441 | 17.090 | 17.197 |
| Digits | BCE | 8.130 | 7.969 | 10.591 | 8.931 | 7.632 |
| Digits | Brier | 9.595 | 9.087 | 8.848 | 8.672 | 8.442 |
| Digits | Mean-MSE | 12.046 | 11.650 | 10.591 | 8.623 | 8.501 |

## Allowed and disallowed claims

- Supported: under the new matched search and 6000-update cap, threshold Brier improves synthetic decisions over decoded-mean MSE; loss rankings depend on training setup.
- Unsupported: BCE uniformly beats Brier, threshold training always improves image routing, 6000 updates establish convergence, gradient diagnostics prove a causal mechanism, or these repeated partitions establish generalization to new image datasets.
- Practical cost matters: Digits BCE regret is 0.162695, versus Brier 0.162646, despite its lower mean nonoptimal rate. Do not describe that comparison as a regret improvement.

Occupied campaign time after round 0: 4306.78 / 14400 seconds. Later rounds must subtract this time before launching.
