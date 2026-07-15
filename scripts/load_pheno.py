"""Phenotype loading with holdout p-factor guarded out.

The RBC phenotype file contains the McElroy bifactor scores for ALL PNC
participants, including the instructor-held-out test subjects. Never read
this file with a bare pd.read_csv -- use these functions.
"""
import pandas as pd
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
PHENO = DATA / "PNC_participants.tsv"

# All four are from the same 22-item McElroy bifactor model. All are leaks.
PFACTOR_COLS = [
    "p_factor_mcelroy_harmonized_all_samples",
    "internalizing_mcelroy_harmonized_all_samples",
    "externalizing_mcelroy_harmonized_all_samples",
    "attention_mcelroy_harmonized_all_samples",
]


def load_covariates(path=PHENO):
    """Demographics only. Bifactor scores never enter memory."""
    df = pd.read_csv(path, sep="\t")
    return df[[c for c in df.columns if c not in PFACTOR_COLS]]


def load_training_labels(train_ids, path=PHENO):
    """P-factor for explicitly-listed training subjects ONLY.

    train_ids: sequence of participant_id values from the instructors'
    training set. Passing anything else defeats the guard.
    """
    train_ids = list(train_ids)
    df = pd.read_csv(path, sep="\t")
    out = df[df["participant_id"].isin(train_ids)]
    assert len(out) == len(train_ids), (
        f"ID mismatch: asked for {len(train_ids)}, matched {len(out)}"
    )
    return out[["participant_id"] + PFACTOR_COLS]
