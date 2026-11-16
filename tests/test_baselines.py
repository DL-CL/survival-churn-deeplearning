"""Tests du contrat commun des baselines (squelette — feature 2).

Ces tests verrouillent l'interface ``fit`` / ``predict_survival`` / ``predict_risk``
et seront **remplacés/étendus** par de vrais tests (jeux synthétiques) en feature 2.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from models.baselines import CoxPHModel, RandomForestSurvival, load_model, save_model

ALL_MODELS = [CoxPHModel, RandomForestSurvival]


@pytest.mark.parametrize("model_cls", ALL_MODELS)
def test_common_interface(model_cls: type) -> None:
    """Chaque baseline expose fit / predict_survival / predict_risk (contrat commun)."""
    model = model_cls()
    for name in ("fit", "predict_survival", "predict_risk"):
        assert callable(getattr(model, name))


@pytest.mark.parametrize("model_cls", ALL_MODELS)
def test_stub_methods_raise(model_cls: type) -> None:
    """Avant la feature 2, chaque méthode lève NotImplementedError (stubs)."""
    model = model_cls()
    X = pd.DataFrame({"feature": [1.0, 2.0]})
    duration = np.array([5.0, 8.0])
    event = np.array([1, 0])
    with pytest.raises(NotImplementedError):
        model.fit(X, duration, event)
    with pytest.raises(NotImplementedError):
        model.predict_survival(X, np.array([1.0, 5.0]))
    with pytest.raises(NotImplementedError):
        model.predict_risk(X)


def test_save_load_stub_raises(tmp_path: Path) -> None:
    """Avant la feature 2, save_model/load_model lèvent NotImplementedError."""
    with pytest.raises(NotImplementedError):
        save_model(object(), tmp_path / "model.joblib")
    with pytest.raises(NotImplementedError):
        load_model(tmp_path / "model.joblib")
