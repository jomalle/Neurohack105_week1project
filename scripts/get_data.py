#!/usr/bin/env python
"""Fetch the two RBC datasets into data/ (gitignored).

1. PNC FreeSurfer derivatives, QC-passed subjects only (DataLad + git-annex).
   Pulls the *_brainmeasures.tsv (global/subcortical) and *_regionsurfacestats.tsv
   (per-region) files, ~3.9 GB -- the full recon-all tarballs in the same dataset
   would be ~375 GB.
2. PNC harmonized phenotypes, including the McElroy p-factor (plain TSV).

Both are openly accessible; content comes from the public fcp-indi S3 bucket.

Prereqs: brew install git-annex && uv tool install datalad
"""

import subprocess
import urllib.request
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
FS = DATA / "PNC_FreeSurfer"
QC_BRANCH = "complete-pass-0.1"
BIDS_RAW = "https://raw.githubusercontent.com/ReproBrainChart/PNC_BIDS/main"


def run(cmd, cwd=None):
    subprocess.run(cmd, cwd=cwd, check=True)


def main():
    DATA.mkdir(exist_ok=True)

    if not FS.exists():
        run(["datalad", "clone",
             "https://github.com/ReproBrainChart/PNC_FreeSurfer.git", str(FS)])
        # datalad clone has no -b flag; check out the QC-passed branch after.
        run(["git", "checkout", QC_BRANCH], cwd=FS)

    # Global/subcortical measures, and per-region stats (Schaefer, Glasser, etc.).
    for pattern, label in (
        ("freesurfer/*/*_brainmeasures.tsv", "brainmeasures"),
        ("freesurfer/*/*_regionsurfacestats.tsv", "regionsurfacestats"),
    ):
        tsvs = subprocess.run(
            ["git", "ls-files", pattern],
            cwd=FS, capture_output=True, text=True, check=True,
        ).stdout.split()
        run(["datalad", "get", "-J", "8", *tsvs], cwd=FS)
        print(f"{label}: {len(tsvs)} subjects")

    for name in ("study-PNC_desc-participants.tsv", "study-PNC_desc-participants.json"):
        dest = DATA / name.replace("study-PNC_desc-", "PNC_")
        urllib.request.urlretrieve(f"{BIDS_RAW}/{name}", dest)
        print(f"phenotype: {dest.name}")


if __name__ == "__main__":
    main()