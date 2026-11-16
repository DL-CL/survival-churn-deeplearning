"""Modèles de survie en deep learning : DeepSurv, Logistic-Hazard / DeepHit (Feature 3).

Implémentation avec pycox (+ torch). Même contrat commun que les baselines :
``fit``, ``predict_survival``, ``predict_risk`` (voir ``docs/architecture.md``).
Graines aléatoires fixées (reproductibilité) ; early stopping via callbacks.
Le choix discret attendu est **Logistic-Hazard ou DeepHit** ; les deux stubs sont
fournis, l'implémentation peut en couvrir un seul (DeepHit optionnel en bonus).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def set_seed(seed: int = 42) -> None:
    """Fixe toutes les graines aléatoires (python, numpy, torch) pour la reproductibilité.

    Args:
        seed: valeur de la graine.
    """
    raise NotImplementedError("TODO(feature-3)")


class DeepSurvModel:
    """DeepSurv : réseau de neurones + perte de Cox (``pycox.models.CoxPH``).

    Attributes:
        hidden_layers: tailles des couches cachées du MLP.
        dropout: taux de dropout du MLP.
        seed: graine aléatoire.
        max_epochs: nombre maximum d'époques d'entraînement.
        batch_size: taille des lots.
        early_stopping_patience: patience du callback d'early stopping.
        model: modèle pycox sous-jacent (``None`` avant ``fit``).
    """

    def __init__(
        self,
        hidden_layers: tuple[int, ...] = (64, 32),
        dropout: float = 0.1,
        seed: int = 42,
        max_epochs: int = 100,
        batch_size: int = 256,
        early_stopping_patience: int = 10,
    ) -> None:
        """Initialise le modèle (hyper-paramètres du MLP et de l'entraînement)."""
        self.hidden_layers = hidden_layers
        self.dropout = dropout
        self.seed = seed
        self.max_epochs = max_epochs
        self.batch_size = batch_size
        self.early_stopping_patience = early_stopping_patience
        self.model = None

    def fit(
        self,
        X: pd.DataFrame,
        duration: np.ndarray,
        event: np.ndarray,
        val_data: tuple[pd.DataFrame, np.ndarray, np.ndarray] | None = None,
    ) -> DeepSurvModel:
        """Entraîne le modèle, avec early stopping si ``val_data`` est fourni.

        Args:
            X: features d'entraînement (numériques).
            duration: durées observées (mois).
            event: événements (1 = churn observé, 0 = censuré).
            val_data: couple ``(X_val, duration_val, event_val)`` optionnel.

        Returns:
            Le modèle ajusté (``self``).
        """
        raise NotImplementedError("TODO(feature-3)")

    def predict_survival(self, X: pd.DataFrame, times: np.ndarray) -> np.ndarray:
        """Prédit la fonction de survie ``S(t | x)`` aux instants ``times``.

        Args:
            X: features (n échantillons).
            times: instants d'évaluation (mois).

        Returns:
            Tableau ``(n, len(times))`` avec ``S(t)`` ∈ [0, 1].
        """
        raise NotImplementedError("TODO(feature-3)")

    def predict_risk(self, X: pd.DataFrame) -> np.ndarray:
        """Prédit un score de risque par échantillon (croissant = plus risqué).

        Args:
            X: features (n échantillons).

        Returns:
            Tableau ``(n,)`` de scores de risque.
        """
        raise NotImplementedError("TODO(feature-3)")

    def save(self, path: Path | str) -> None:
        """Sauvegarde le réseau entraîné (mécanisme natif pycox), dossier ``models/``.

        Args:
            path: chemin de sortie.
        """
        raise NotImplementedError("TODO(feature-3)")

    @classmethod
    def load(cls, path: Path | str) -> DeepSurvModel:
        """Recharge un modèle sauvegardé avec :meth:`save`.

        Args:
            path: chemin du modèle sauvegardé.

        Returns:
            L'instance rechargée.
        """
        raise NotImplementedError("TODO(feature-3)")


class LogisticHazardModel:
    """Logistic-Hazard à temps discret (``pycox.models.LogisticHazard``).

    Le temps est discrétisé sur une grille dérivée de ``duration_train`` ;
    les prédictions sont interpolées sur la grille commune ``times`` pour
    respecter le contrat d'interface.
    """

    def __init__(
        self,
        hidden_layers: tuple[int, ...] = (64, 32),
        dropout: float = 0.1,
        seed: int = 42,
        max_epochs: int = 100,
        batch_size: int = 256,
        early_stopping_patience: int = 10,
        n_time_bins: int = 100,
    ) -> None:
        """Initialise le modèle (``n_time_bins`` = intervalles de discrétisation du temps)."""
        self.hidden_layers = hidden_layers
        self.dropout = dropout
        self.seed = seed
        self.max_epochs = max_epochs
        self.batch_size = batch_size
        self.early_stopping_patience = early_stopping_patience
        self.n_time_bins = n_time_bins
        self.model = None

    def fit(
        self,
        X: pd.DataFrame,
        duration: np.ndarray,
        event: np.ndarray,
        val_data: tuple[pd.DataFrame, np.ndarray, np.ndarray] | None = None,
    ) -> LogisticHazardModel:
        """Entraîne le modèle, avec early stopping si ``val_data`` est fourni."""
        raise NotImplementedError("TODO(feature-3)")

    def predict_survival(self, X: pd.DataFrame, times: np.ndarray) -> np.ndarray:
        """Prédit ``S(t | x)`` aux instants ``times`` (tableau ``(n, len(times))``)."""
        raise NotImplementedError("TODO(feature-3)")

    def predict_risk(self, X: pd.DataFrame) -> np.ndarray:
        """Prédit un score de risque par échantillon (tableau ``(n,)``)."""
        raise NotImplementedError("TODO(feature-3)")

    def save(self, path: Path | str) -> None:
        """Sauvegarde le réseau entraîné (mécanisme natif pycox)."""
        raise NotImplementedError("TODO(feature-3)")

    @classmethod
    def load(cls, path: Path | str) -> LogisticHazardModel:
        """Recharge un modèle sauvegardé avec :meth:`save`."""
        raise NotImplementedError("TODO(feature-3)")


class DeepHitModel:
    """DeepHit à temps discret (``pycox.models.DeepHit``) — variante compétitive (bonus).

    Même comportement que :class:`LogisticHazardModel` ; à implémenter uniquement
    si le temps le permet (voir issue Feature 3).
    """

    def __init__(
        self,
        hidden_layers: tuple[int, ...] = (64, 32),
        dropout: float = 0.1,
        seed: int = 42,
        max_epochs: int = 100,
        batch_size: int = 256,
        early_stopping_patience: int = 10,
        n_time_bins: int = 100,
    ) -> None:
        """Initialise le modèle."""
        self.hidden_layers = hidden_layers
        self.dropout = dropout
        self.seed = seed
        self.max_epochs = max_epochs
        self.batch_size = batch_size
        self.early_stopping_patience = early_stopping_patience
        self.n_time_bins = n_time_bins
        self.model = None

    def fit(
        self,
        X: pd.DataFrame,
        duration: np.ndarray,
        event: np.ndarray,
        val_data: tuple[pd.DataFrame, np.ndarray, np.ndarray] | None = None,
    ) -> DeepHitModel:
        """Entraîne le modèle, avec early stopping si ``val_data`` est fourni."""
        raise NotImplementedError("TODO(feature-3)")

    def predict_survival(self, X: pd.DataFrame, times: np.ndarray) -> np.ndarray:
        """Prédit ``S(t | x)`` aux instants ``times`` (tableau ``(n, len(times))``)."""
        raise NotImplementedError("TODO(feature-3)")

    def predict_risk(self, X: pd.DataFrame) -> np.ndarray:
        """Prédit un score de risque par échantillon (tableau ``(n,)``)."""
        raise NotImplementedError("TODO(feature-3)")

    def save(self, path: Path | str) -> None:
        """Sauvegarde le réseau entraîné (mécanisme natif pycox)."""
        raise NotImplementedError("TODO(feature-3)")

    @classmethod
    def load(cls, path: Path | str) -> DeepHitModel:
        """Recharge un modèle sauvegardé avec :meth:`save`."""
        raise NotImplementedError("TODO(feature-3)")
