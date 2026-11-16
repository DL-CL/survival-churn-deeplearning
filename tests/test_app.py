"""Tests structurels de l'app Streamlit (squelette — feature 4).

On analyse le fichier avec ``ast`` plutôt que de l'importer, afin de ne pas imposer
l'installation de streamlit à chaque environnement d'exécution des tests.
"""

from __future__ import annotations

import ast
from pathlib import Path

APP_PATH = Path(__file__).resolve().parents[1] / "app" / "streamlit_app.py"

EXPECTED_FUNCTIONS = {
    "main",
    "load_artifacts",
    "build_profile_input",
    "render_survival_curve",
}


def test_app_defines_expected_entry_points() -> None:
    """L'app expose les fonctions du contrat (main, profil, courbe, artefacts)."""
    tree = ast.parse(APP_PATH.read_text(encoding="utf-8"))
    functions = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
    assert EXPECTED_FUNCTIONS <= functions
