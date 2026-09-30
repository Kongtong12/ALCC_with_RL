# Reproducibility

## Source of truth

The source of truth is the protocol-bound experiment directory plus its
`protocol.json`, selection record, freeze record, status file, and validation
receipt. The paper and result tables must point back to those records.

## Environment

Create the pinned environment with `conda env create -f environment.yml`.
The environment contains Python 3.12, PyTorch, NumPy, SciPy, pandas,
matplotlib, pytest, and the small utilities used by the current studies. GPU
replay additionally depends on a compatible local driver.

## Data provenance

`data/manifests/studies.json` indexes the active study data roots and records
source, license boundary, creating commit, protocol, and freeze/status paths.
Large binary files use Git LFS. External data with unclear redistribution
rights must remain a download instruction plus hash, not a copied file.

## Validation

The lightweight baseline is:

```bash
python scripts/check_repo_layout.py
python -m compileall -q scripts tests experiments
python -m pytest -q tests/test_theory_facepot_v2.py tests/test_set_separation_integration.py
```

For a paper change, use a clean LaTeX build and inspect the log for undefined
references and citations. For a study change, rerun the study-specific
verification script named in its README and compare its receipt to the
manifest.

## Claim boundary

The repository distinguishes positive evidence, diagnostic evidence, and
failed screens. A result is not promoted into a paper claim only because a
file exists; the protocol and audit must admit it. This is especially
important for the threshold screens and the matched Warcraft results.
