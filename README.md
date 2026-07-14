# Neurohack105 — Week 1 Project

## Setup

Everything is managed by [uv](https://docs.astral.sh/uv/). Clone, then:

```bash
uv sync
```

That creates `.venv/` and installs the exact versions pinned in `uv.lock`. No manual venv activation needed.

## Running things

```bash
uv run jupyter lab          # start JupyterLab
uv run python script.py     # run any script
```

In JupyterLab, pick the kernel named **neurohack105-week1**.

## Adding a package

```bash
uv add seaborn              # updates pyproject.toml + uv.lock and installs
uv remove seaborn
```

Commit `pyproject.toml` and `uv.lock` so the environment stays reproducible.

## Notes

- PyTorch uses the Apple Silicon GPU via the `mps` device.
- `data/` is gitignored — keep raw data out of the repo.

## Data

```bash
brew install git-annex && uv tool install datalad   # one-time
uv run scripts/get_data.py
```

Pulls into `data/` (gitignored):

- **`PNC_FreeSurfer/`** — Reproducible Brain Charts PNC FreeSurfer derivatives,
  `complete-pass-0.1` branch (QC-passed only), **1,439 subjects**. Two file types per
  subject: `*_brainmeasures.tsv` (global/subcortical measures) and
  `*_regionsurfacestats.tsv` (per-region stats: Schaefer, Glasser, AAL, and others).
  The script fetches only these TSVs (~3.9 GB); the full recon-all tarballs in the
  same dataset are ~375 GB.
- **`PNC_participants.tsv`** — harmonized phenotypes, including the McElroy p-factor
  (`p_factor_mcelroy_harmonized_all_samples`) plus internalizing/externalizing/attention.

Both are openly accessible via the public `fcp-indi` S3 bucket — no DUA, no dbGaP.

Join on `participant_id` (strip the `sub-` prefix from FreeSurfer's `subject_id`):
1,439 subjects match, 1,438 with complete p-factor + age + sex.
