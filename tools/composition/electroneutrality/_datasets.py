"""
Dataset loaders for electroneutrality tools.
"""

from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[3]
REPRESENTATIVE_84_PATH = (
    REPO_ROOT
    / "datasets"
    / "element_charges"
    / "oxidation_states_84.yaml"
)


def load_representative_84():
    """Load the canonical representative oxidation-state dataset."""

    with REPRESENTATIVE_84_PATH.open() as stream:
        data = yaml.safe_load(stream)

    return {
        element: list(charges)
        for element, charges in data.items()
    }
