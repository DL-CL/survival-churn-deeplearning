"""Modèles de survie de référence : Cox PH et Random Survival Forest (Feature 2).

Contrat commun (voir ``docs/architecture.md``) : chaque modèle expose
``fit(X, duration, event)``, ``predict_survival(X, times)`` et ``predict_risk(X)``.
Ces baselines servent de référence pour juger les modèles deep learning (Feature 3).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


class CoxPHModel:
    """Cox à risques proportionnels (lifelines), baseline statistique classique.

    Attributes:
        penalizer: force de la régularisation L2 (ridge) de lifelines.
        model: modèle lifelines sous-jacent (``None`` avant ``fit``).
    """

    def __init__(self, penalizer: float = 0.1) -> None:
        """Initialise le modèle.

        Args:
            penalizer: force de la régularisation L2 de lifelines.
        """
        self.penalizer = penalizer
        self.model = None

    def fit(self, X: pd.DataFrame, duration: np.ndarray, event: np.ndarray) -> CoxPHModel:
        """Ajuste le modèle sur les données d'entraînement.

        Args:
            X: features d'entraînement (numériques).
            duration: durées observées (mois).
            event: événements (1 = churn observé, 0 = censuré).

        Returns:
            Le modèle ajusté (``self``).
        """
        raise NotImplementedError("TODO(feature-2)")

    def predict_survival(self, X: pd.DataFrame, times: np.ndarray) -> np.ndarray:
        """Prédit la fonction de survie ``S(t | x)`` aux instants ``times``.

        Args:
            X: features (n échantillons).
            times: instants d'évaluation (mois).

        Returns:
            Tableau ``(n, len(times))`` avec ``S(t)`` ∈ [0, 1].
        """
        raise NotImplementedError("TODO(feature-2)")

    def predict_risk(self, X: pd.DataFrame) -> np.ndarray:
        """Prédit un score de risque par échantillon (croissant = plus risqué).

        Args:
            X: features (n échantillons).

        Returns:
            Tableau ``(n,)`` de scores de risque.
        """
        raise NotImplementedError("TODO(feature-2)")


class RandomForestSurvival:
    """Random Survival Forest (scikit-survival), baseline non paramétrique.

    Attributes:
        n_estimators: nombre d'arbres de la forêt.
        random_state: graine aléatoire (reproductibilité).
        model: modèle scikit-survival sous-jacent (``None`` avant ``fit``).
    """

    def __init__(self, n_estimators: int = 100, random_state: int = 42) -> None:
        """Initialise le modèle.

        Args:
            n_estimators: nombre d'arbres.
            random_state: graine aléatoire.
        """
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.model = None

    def fit(
        self, X: pd.DataFrame, duration: np.ndarray, event: np.ndarray
    ) -> RandomForestSurvival:
        """Ajuste la forêt sur les données d'entraînement.

        Args:
            X: features d'entraînement (numériques).
            duration: durées observées (mois).
            event: événements (1 = churn observé, 0 = censuré).

        Returns:
            Le modèle ajusté (``self``).
        """
        raise NotImplementedError("TODO(feature-2)")

    def predict_survival(self, X: pd.DataFrame, times: np.ndarray) -> np.ndarray:
        """Prédit la fonction de survie ``S(t | x)`` aux instants ``times``.

        Args:
            X: features (n échantillons).
            times: instants d'évaluation (mois).

        Returns:
            Tableau ``(n, len(times))`` avec ``S(t)`` ∈ [0, 1].
        """
        raise NotImplementedError("TODO(feature-2)")

    def predict_risk(self, X: pd.DataFrame) -> np.ndarray:
        """Prédit un score de risque par échantillon (croissant = plus risqué).

        Args:
            X: features (n échantillons).

        Returns:
            Tableau ``(n,)`` de scores de risque.
        """
        raise NotImplementedError("TODO(feature-2)")


def save_model(model: object, path: Path | str) -> None:
    """Sauvegarde un modèle ajusté sur disque (joblib), dossier ``models/`` (git-ignoré).

    Args:
        model: instance ajustée du modèle.
        path: chemin de sortie.
    """
    raise NotImplementedError("TODO(feature-2)")


def load_model(path: Path | str) -> object:
    """Recharge un modèle sauvegardé avec :func:`save_model`.

    Args:
        path: chemin du modèle sauvegardé.

    Returns:
        L'instance rechargée.
    """
    raise NotImplementedError("TODO(feature-2)")
