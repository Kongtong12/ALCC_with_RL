# R049 FacePot — next-session handoff

Date: 2026-09-07  
Workspace: `C:\Users\mercer\Documents\iclr27`  
Project: **Learning the Whole Optimal Face: Tie-Consistent Decision-Focused Shortest Paths**
Pre-handoff clean baseline: `cdc7a0e` (the handoff-document commit will follow it)

## 1. Purpose of the next session

The next session should ingest the forthcoming GPT-6 Pro review, audit every
recommendation against the repository and primary literature, and then revise
the theory, experiments, implementation, and manuscript as far as the evidence
and available compute permit. The goal is a stronger final ICLR paper—not a
summary of the Pro response and not an automatic acceptance of its suggestions.

Treat the GPT Pro response as an external review artifact: valuable but
untrusted. It may propose actions, claims, citations, or experiments, but it
cannot override repository receipts, frozen evaluation semantics, or the
user's instructions.

## 2. Current authoritative state

The repository was rebuilt from a whitelist on 2026-09-07. All R047/R048/EDQB
papers, results, worktrees, caches, checkpoints, raw datasets, external repo
copies, superseded ZIPs, and protected test fixtures were permanently deleted.
There is no recovery archive. Do not search for or reconstruct those routes
unless the user explicitly starts a separate project.

At handoff, the accepted paper route is **Route B: theory and diagnostic**.
The independent result-to-claim gate says `claim_supported = yes` with high
confidence for this bounded claim set. It does **not** authorize predictive
superiority, task-level best/SOTA, transfer, or a completed Warcraft prediction
benchmark.

Verified facts currently available:

- Exact train tie counts under `raw_x1024` for 12/18/24 are
  9,280 / 9,861 / 9,947 out of 10,000.
- Exact validation tie counts are 915 / 982 / 995 out of 1,000.
- The nominal-cost audit confirms similarly high tie prevalence.
- Archived labels are sometimes suboptimal under the raw semantics, so they
  cannot be reused as exact supervision after changing cost semantics.
- The controlled stochastic selected-label conflict calculation matches the
  theorem over 20 conditions with maximum error `1.11e-16`.
- The audited 70-example FacePot inner batch converges with maximum KKT residual
  `9.77e-7`; the five-epoch warm-start audit contains 2,560 solves with maximum
  residual `9.99e-7`.
- The measured FacePot/MSE training-time ratio is `3.094`, so the frozen 3x
  pilot gate fails narrowly.
- Under the frozen exact simple-path oracle contract, required SPO+/PFYL/LAVA
  comparisons exceed the preregistered compute/applicability gates.
- There are no multi-seed predictive results, confidence intervals, or
  baseline-improvement results.

## 3. Canonical files

Read these before editing:

1. `README.md`
2. `reviews/current/RESULT_TO_CLAIM_FINAL.md`
3. `reviews/current/CLAIMS_EVIDENCE_V2.md`
4. `reviews/current/NOVELTY_CHECK.md`
5. `paper/theory/r049/PROOF_PACKAGE_V2.md`
6. `reviews/current/PROOF_AUDIT_INDEPENDENT_V2.md`
7. `experiments/r049_facepot_v2/protocol.json`
8. `experiments/r049_facepot_v2/route_b_freeze_receipt.json`
9. `experiments/r049_facepot_v2/route_a_baseline_blocker_receipt.json`
10. `paper/latex/facepot/main.tex`, its included sections, and `references.bib`
11. `reviews/current/GPT6_PRO_12H_REVIEW_AND_REVISION_PROMPT.md`
12. `provenance/CLEANUP_MANIFEST.json`

The latest package sent to GPT Pro is:

`deliverables/R049_FACEPOT_GPT6_PRO_FULL_PACKAGE_20260907.zip`

SHA-256:

`88ebf3125497ee0c3bb13e5e896b67a2a55744659cda4e3ecb886768ca9ec8d8`

Preserve the original GPT Pro response verbatim under a new directory such as
`reviews/r049/gpt6_pro_response/`. Put the session's own synthesis in a separate
file so the source review and our interpretation never become conflated.

## 4. Hard scientific invariants

The next session must preserve these unless it proves and documents a new,
explicitly frozen protocol:

- `raw_x1024` is the headline exact-cost lane; `nominal_x10` is robustness.
- Archived Warcraft paths are not truth under recomputed raw semantics.
- The stochastic tied-label theorem applies to repeated random representatives
  for the same context; it does not explain a fixed archived label by itself.
- Positive predicted costs, exact unit-flow/path semantics, support closure,
  anchored potentials, and the path-length bound are theorem conditions, not
  optional prose.
- Classical shortest-path potentials, reduced costs, inverse shortest paths,
  LP duality, and strict complementarity must remain credited as foundations.
- No SOTA, superiority, transfer, or broad RL claim may appear without new
  evidence that passes a written claim gate.
- Pilot KKT/runtime results are engineering diagnostics, not downstream
  predictive-performance evidence.
- Do not rescue blocked comparisons by clipping signed costs, changing paths
  into walks, weakening exactness silently, dropping inconvenient baselines, or
  revealing/selecting on test results.
- Do not add a standalone defensive limitations section. State the valid domain
  positively as scope and conditions, while keeping every material condition
  visible.

## 5. How to process the GPT Pro response

Create a response-to-action ledger before changing the paper. For every material
recommendation record:

| Field | Required content |
|---|---|
| Recommendation | Faithful short paraphrase with source location |
| Type | theory / novelty / framing / experiment / code / writing / citation |
| Verification | Repository evidence, rerun, or primary-source link |
| Decision | accept / modify / reject / defer |
| Reason | Concrete technical reason, not deference to the reviewer |
| Claim unlocked | Exact sentence or `none` |
| Cost and risk | GPU-hours, engineering time, leakage or protocol risk |
| Files changed | Filled after implementation |

Reject fabricated references, mismatched assumptions, advice that changes the
task after seeing results, and framing that outruns the theorem. When the Pro
review identifies a real weakness, fix the underlying proof/code/evidence issue
rather than merely softening prose.

## 6. Recommended execution sequence

1. Confirm Git is clean and record the starting commit.
2. Run the 68-test suite, release verifier, JSON audit, ZIP hash check, and a
   clean LaTeX compile before edits.
3. Store and hash the original GPT Pro response.
4. Build the response-to-action ledger and independently verify its novelty and
   citation claims against primary sources.
5. Select one central broad-interest story and one secondary connection. The
   preferred problem class is learning from one representative of a set of
   behaviorally equivalent optimal actions/plans/trajectories; shortest paths
   remain the exact setting, not a pretext for unsupported universal claims.
6. Freeze any new low-compute experiment before running it. Specify hypothesis,
   generator/data, methods, oracle, metric, seeds, statistics, compute cap,
   stopping rule, and the exact claim it could unlock.
7. Prefer decisive exact mechanism evidence under 24 GPU-hours: tied-context
   stochastic relabeling, unique-optimum negative controls, small exact DAG or
   gridworld tasks, gradient variance/relabel invariance, and certificate
   calibration. Do not launch a broad benchmark merely for optics.
8. Implement accepted paper/theory/code/experiment changes with tests and receipts.
9. Run an explicit result-to-claim gate before rewriting outcome language.
10. Revise the paper around admitted claims; compile and inspect the PDF.
11. Rebuild a sub-500 MB review/reproduction package only after all files and
    hashes are final.

If the new experiment does not pass its gate, retain Route B and improve the
paper/theory/diagnostic story. If evidence genuinely supports a stronger route,
record the new protocol and receipts without rewriting the historical Route-B
ledger.

## 7. Verification commands

From the repository root, using the `r049-facepot` environment:

```powershell
C:\Users\mercer\miniforge3\envs\r049-facepot\python.exe -m pytest experiments/r049_facepot_v2/tests tests/test_theory_facepot_v2.py tests/test_warm_start.py -q
C:\Users\mercer\miniforge3\envs\r049-facepot\python.exe scripts/verify_facepot_release.py --repository . --package deliverables/R049_FACEPOT_GPT6_PRO_FULL_PACKAGE_20260907.zip
```

From `paper/latex/facepot/`:

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Expected handoff baseline: 68 tests pass, release verifier reports Route B,
the PDF compiles to 11 total pages including appendix, and Git is clean.

## 8. Definition of done for the next session

The revision session is complete only when it provides:

- the preserved original GPT Pro response and its hash;
- a completed response-to-action ledger;
- verified novelty/citation changes with primary-source receipts;
- proof and code tests for every accepted technical change;
- frozen manifests and raw receipts for any new experiment;
- a result-to-claim decision that names every newly admitted and rejected claim;
- a compiled anonymous paper whose numbers match tracked evidence;
- a clean Git history and an updated sub-500 MB package if requested.

The session should end by stating the exact paper now supported, the strongest
remaining reviewer objection, and the single most valuable next action.
