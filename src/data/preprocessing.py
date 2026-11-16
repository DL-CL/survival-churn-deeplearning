"""Nettoyage, encodage et découpage train/test pour l'analyse de survie (Feature 1).

Contrat de sortie (voir ``docs/architecture.md``) : :class:`SurvivalSplit` contient
les matrices de features et les tableaux alignés ``duration`` (``tenure``, en mois)
et ``event`` (1 = churn observé, 0 = censuré à droite).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

#: Graine aléatoire par défaut (reproductibilité).
RANDOM_SEED = 42
#: Proportion du jeu de test par défaut.
TEST_SIZE = 0.2


@dataclass
class SurvivalSplit:
    """Conteneur du découpage train/test aligné sur la survie.

    Attributes:
        X_train: features d'entraînement (100 % numériques).
        X_test: features de test (mêmes colonnes que ``X_train``).
        duration_train: durées d'entraînement (mois, >= 0).
        duration_test: durées de test (mois, >= 0).
        event_train: événements d'entraînement (1 = churn, 0 = censuré).
        event_test: événements de test (1 = churn, 0 = censuré).
    """

    X_train: pd.DataFrame
    X_test: pd.DataFrame
    duration_train: np.ndarray
    duration_test: np.ndarray
    event_train: np.ndarray
    event_test: np.ndarray


def make_survival_arrays(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Extrait les tableaux ``(duration, event)`` alignés depuis le DataFrame.

    Args:
        df: DataFrame contenant ``tenure`` et ``Churn``.

    Returns:
        Un couple ``(duration, event)`` : durées en float, événements en int 0/1.
    """
    raise NotImplementedError("TODO(feature-1)")


def clean_telco(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoie le jeu brut : types, ``TotalCharges`` vide -> NaN -> numérique, etc.

    Args:
        df: DataFrame brut issu de :func:`data.loader.load_telco`.

    Returns:
        DataFrame nettoyé (types homogènes, ``customerID`` retirée).

    Raises:
        ValueError: si les colonnes attendues sont absentes.
    """
    raise NotImplementedError("TODO(feature-1)")


def encode_features(df: pd.DataFrame) -> pd.DataFrame:
    """Encode les variables catégorielles (one-hot / binaire) pour les modèles.

    Args:
        df: DataFrame nettoyé.

    Returns:
        DataFrame entièrement numérique, prêt pour le découpage.
    """
    raise NotImplementedError("TODO(feature-1)")


def scale_features(
    train: pd.DataFrame, test: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Normalise les colonnes numériques (ajusté sur le train uniquement).

    Args:
        train: features d'entraînement numériques.
        test: features de test numériques.

    Returns:
        Le couple ``(train_scaled, test_scaled)``.
    """
    raise NotImplementedError("TODO(feature-1)")


def train_test_split_survival(
    df: pd.DataFrame,
    test_size: float = TEST_SIZE,
    seed: int = RANDOM_SEED,
) -> SurvivalSplit:
    """Découpe en train/test stratifié sur l'événement et renvoie un ``SurvivalSplit``.

    Args:
        df: DataFrame entièrement numérique (après encodage).
        test_size: proportion du jeu de test.
        seed: graine aléatoire.

    Returns:
        Le :class:`SurvivalSplit` aligné (features + durée + événement).
    """
    raise NotImplementedError("TODO(feature-1)")
