"""Tests du contrat de comparaison des modèles (squelette — feature 4).

Ces tests vérifient que les 3 fonctions de comparaison existent et seront
**remplacés/étendus** par des tests à valeurs de référence en feature 4.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from evaluation.compare import compare_models, cross_validate_survival, evaluate_model


def _dummy_model_factory() -> object:
    """Fabrique factice conforme à la signature de ``cross_validate_survival``."""
    return object()


def test_stub_raises() -> None:
    """Avant la feature 4, chaque fonction lève NotImplementedError (stubs)."""
    X = pd.DataFrame({"feature": [1.0, 2.0, 3.0]})
    duration = np.array([5.0, 8.0, 3.0])
    event = np.array([1, 0, 1])
    with pytest.raises(NotImplementedError):
        evaluate_model(object(), X, duration, event, np.array([1.0, 2.0]))
    with pytest.raises(NotImplementedError):
        compare_models({"cox": {"c_index": 0.8}})
    with pytest.raises(NotImplementedError):
        cross_validate_survival(_dummy_model_factory, X, duration, event)
