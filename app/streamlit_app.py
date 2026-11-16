"""Application de démonstration Streamlit (Feature 4).

Lancement : ``streamlit run app/streamlit_app.py``.

Scénario : l'utilisateur saisit un profil client dans la barre latérale
(tenure simulée non nécessaire : le modèle prédit en fonction du profil),
l'application affiche la courbe de survie personnalisée ``S(t | profil)``,
le score de risque et la durée de survie médiane estimée (mois avant churn).
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st  # noqa: F401 — utilisé par les fonctions implémentées en feature 4

#: Titre affiché en haut de page.
APP_TITLE = "Prédiction de churn par analyse de survie"

#: Dossier des artefacts (modèles entraînés, pipeline), git-ignoré.
ARTIFACTS_DIR = Path("models")


def load_artifacts(artifacts_dir: Path = ARTIFACTS_DIR) -> dict[str, object]:
    """Charge les modèles entraînés et le pipeline de preprocessing sauvegardés.

    Args:
        artifacts_dir: dossier des artefacts.

    Returns:
        Dictionnaire ``{nom du modèle: instance ajustée}`` (+ pipeline de
        preprocessing partagé).
    """
    raise NotImplementedError("TODO(feature-4)")


def build_profile_input() -> dict[str, object]:
    """Construit le profil client depuis les widgets de la barre latérale.

    Returns:
        Dictionnaire ``colonne -> valeur`` saisie par l'utilisateur
        (types cohérents avec les features d'entraînement).
    """
    raise NotImplementedError("TODO(feature-4)")


def render_survival_curve(profile: dict[str, object]) -> None:
    """Affiche la courbe de survie personnalisée et la survie médiane.

    Args:
        profile: profil client saisi (:func:`build_profile_input`).
    """
    raise NotImplementedError("TODO(feature-4)")


def main() -> None:
    """Point d'entrée de l'application Streamlit."""
    raise NotImplementedError("TODO(feature-4)")


if __name__ == "__main__":
    main()
