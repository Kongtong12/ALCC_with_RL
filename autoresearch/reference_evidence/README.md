# ICLR 2027 research repository

This private repository contains the current manuscript, reproducible study
code, evidence records, and review material for the ICLR 2027 project.

## Current paper

**Learning Costs for Decisions: Matching Targets Before Comparing Losses**

The current anonymous manuscript is [paper/latex/facepot/main.pdf](paper/latex/facepot/main.pdf), with editable LaTeX in the same directory. The central evidence line is:

- threshold objectives and long-budget screens;
- matched continuation studies;
- allocation regularization;
- a matched Warcraft study.

The repository records what each experiment supports. Failed screens and
superseded manuscripts are not silently promoted to evidence.

## Start here

New collaborators should read [QUICKSTART.md](QUICKSTART.md), then
[CONTRIBUTING.md](CONTRIBUTING.md). The Chinese overview is
[docs/zh/START_HERE.md](docs/zh/START_HERE.md).

## Repository map

| Path | Purpose |
| --- | --- |
| `paper/latex/facepot/` | Current paper source and figures |
| `paper/theory/` | Formal theory packages and proofs |
| `experiments/` | Protocol-bound study code and frozen evidence |
| `data/` | Data layers and manifests; large files use Git LFS |
| `results/` | Curated tables, figures, and audits |
| `reviews/current/` | Reviews that still inform the current paper |
| `artifacts/packages/` | Retained portable review packages |
| `scripts/` and `tests/` | Analysis, verification, and tests |
| `docs/` | Project map and reproducibility notes |

For old paths and the safe migration boundary, see
[docs/project-map.md](docs/project-map.md). For the first private GitHub push
and branch protection, see [docs/github-setup.md](docs/github-setup.md).

## Collaboration rule

`main` is the shared protected branch. Work is proposed through pull
requests, with at least one review and the repository checks passing. Large
scientific files are stored with Git LFS; source code, protocols, text, and
small metadata remain ordinary Git files.
