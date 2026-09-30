# Quick start

This page is for a new collaborator on Windows or Linux.

## 1. Clone the private repository

Install Git and Git LFS first, then run:

```bash
git lfs install
git clone <PRIVATE_REPOSITORY_URL>
cd iclr27
git lfs pull
```

For a light clone that skips large files until they are needed (PowerShell):

```powershell
$env:GIT_LFS_SKIP_SMUDGE = "1"
git clone <PRIVATE_REPOSITORY_URL>
cd iclr27
git lfs pull --include="data/manifests/**,paper/releases/**"
```

Without Git LFS, large files remain pointer files and cannot be used as
inputs. Install LFS before running experiments.

## 2. Create the research environment

The pinned environment is at `environment.yml`:

```bash
conda env create -f environment.yml
conda activate r049-facepot
```

The environment includes the Python packages used by the current studies.
GPU-specific replay may require a matching CUDA driver.

## 3. Run the lightweight checks

```bash
python scripts/check_repo_layout.py
python -m compileall -q scripts tests experiments
python -m pytest -q tests/test_theory_facepot_v2.py tests/test_set_separation_integration.py
```

The full study replay is intentionally separate from the quick check. Read
the relevant experiment `README.md`, `protocol.json`, and `freeze.json`
before launching it.

## 4. Build the paper

```bash
cd paper/latex/facepot
latexmk -C
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The generated PDF is local build output. Keep intermediate LaTeX files out of
commits; the clean source and the explicitly retained release PDF are the
reviewable artifacts.

## 5. Find data and results

Start with [data/README.md](data/README.md),
[docs/reproducibility.md](docs/reproducibility.md), and
`data/manifests/`. The active experiment bundles remain under
`experiments/` where their frozen relative paths and receipts stay valid.

## 6. Submit a change

```bash
git switch -c codex/short-description
git status
git add <files>
git commit -m "docs: clarify experiment entry point"
git push -u origin codex/short-description
```

Open a pull request into `main`. Do not commit credentials, local caches,
unreviewed checkpoints, or generated LaTeX intermediates.
