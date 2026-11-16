"""Comparaison des 4 modèles de survie (Feature 4).

``evaluate_model`` produit les métriques d'un modèle ajusté, ``compare_models``
assemble le tableau comparatif, ``cross_validate_survival`` fait la validation
croisée. Voir ``docs/architecture.md``.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
import pandas as pd


def evaluate_model(
    model: object,
    X_test: pd.DataFrame,
    duration_test: np.ndarray,
    event_test: np.ndarray,
    times: np.ndarray,
) -> dict[str, float]:
    """Évalue un modèle ajusté sur le jeu de test.

    Args:
        model: modèle ajusté respectant le contrat commun (``predict_survival``,
            ``predict_risk``).
        X_test: features de test.
        duration_test: durées de test (mois).
        event_test: événements de test (1 = churn, 0 = censuré).
        times: grille d'instants (mois), issue de ``metrics.make_time_grid``.

    Returns:
        Dictionnaire ``{nom de la métrique: valeur}`` (au minimum ``c_index`` et
        ``ibs``).
    """
    raise NotImplementedError("TODO(feature-4)")


def compare_models(results: dict[str, dict[str, float]]) -> pd.DataFrame:
    """Assemble les résultats de plusieurs modèles en tableau comparatif.

    Args:
        results: dictionnaire ``{nom du modèle: {métrique: valeur}}``.

    Returns:
        DataFrame indexé par modèle, colonnes = métriques, trié par métrique
        principale décroissante.
    """
    raise NotImplementedError("TODO(feature-4)")


def cross_validate_survival(
    model_factory: Callable[[], object],
    X: pd.DataFrame,
    duration: np.ndarray,
    event: np.ndarray,
    n_splits: int = 5,
    seed: int = 42,
) -> pd.DataFrame:
    """Validation croisée K-fold stratifiée sur l'événement.

    Args:
        model_factory: fonction sans argument renvoyant une **nouvelle** instance
            de modèle (pour refit à chaque fold).
        X: features complètes.
        duration: durées complètes (mois).
        event: événements complets (1 = churn, 0 = censuré).
        n_splits: nombre de folds.
        seed: graine aléatoire du découpage.

    Returns:
        DataFrame ``{fold, c_index, ibs, ...}`` (une ligne par fold).
    """
    raise NotImplementedError("TODO(feature-4)")
