"""Métriques d'évaluation pour l'analyse de survie (Feature 4).

C-index (discrimination), Brier score intégré (calibration globale dans le temps),
courbe de calibration par bins de risque. Voir ``docs/architecture.md``.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def make_time_grid(duration_train: np.ndarray, n_points: int = 20) -> np.ndarray:
    """Construit la grille commune d'instants d'évaluation (mois).

    La grille doit couvrir une fenêtre où le risque de censure reste raisonnable
    (éviter les extrêmes), et être identique pour tous les modèles afin de
    comparer les fonctions de survie et calculer l'IBS.

    Args:
        duration_train: durées du jeu d'entraînement.
        n_points: nombre d'instants souhaités.

    Returns:
        Grille croissante d'instants (mois), à l'intérieur de la plage observée.
    """
    raise NotImplementedError("TODO(feature-4)")


def concordance_index(risk: np.ndarray, duration: np.ndarray, event: np.ndarray) -> float:
    """Calcule le C-index (concordance) à partir des scores de risque.

    Args:
        risk: scores de risque prédits (croissant = plus risqué).
        duration: durées observées (mois).
        event: événements (1 = churn observé, 0 = censuré).

    Returns:
        C-index ∈ [0, 1] (0.5 = aléatoire, 1.0 = parfait).
    """
    raise NotImplementedError("TODO(feature-4)")


def integrated_brier_score(
    duration_train: np.ndarray,
    event_train: np.ndarray,
    duration_test: np.ndarray,
    event_test: np.ndarray,
    survival_estimates: np.ndarray,
    times: np.ndarray,
) -> float:
    """Calcule le Brier score intégré (IBS) sur la fenêtre ``times``.

    Args:
        duration_train: durées d'entraînement (estimation KM de la censure).
        event_train: événements d'entraînement.
        duration_test: durées de test.
        event_test: événements de test.
        survival_estimates: prédictions ``S(t | x)``, tableau ``(n_test, len(times))``.
        times: grille d'instants (mois).

    Returns:
        IBS (plus bas = mieux).
    """
    raise NotImplementedError("TODO(feature-4)")


def calibration_curve(
    risk: np.ndarray,
    duration: np.ndarray,
    event: np.ndarray,
    n_bins: int = 10,
) -> pd.DataFrame:
    """Construit la courbe de calibration par bins de risque.

    Args:
        risk: scores de risque prédits (croissant = plus risqué).
        duration: durées observées (mois).
        event: événements (1 = churn observé, 0 = censuré).
        n_bins: nombre de bins de risque.

    Returns:
        DataFrame avec au minimum les colonnes ``risk_pred`` (moyenne du risque
        prédit dans le bin), ``churn_obs`` (taux d'événement observé) et ``n``
        (effectif du bin).
    """
    raise NotImplementedError("TODO(feature-4)")
