"""Tests du contrat commun des modèles deep learning (squelette — feature 3).

Ces tests verrouillent l'interface ``fit`` / ``predict_survival`` / ``predict_risk``
(+ ``save``/``load`` et ``set_seed``) et seront **remplacés/étendus** en feature 3.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from models.deep_models import DeepHitModel, DeepSurvModel, LogisticHazardModel, set_seed

ALL_MODELS = [DeepSurvModel, LogisticHazardModel, DeepHitModel]


@pytest.mark.parametrize("model_cls", ALL_MODELS)
def test_common_interface(model_cls: type) -> None:
    """Chaque modèle deep expose fit / predict_survival / predict_risk / save / load."""
    model = model_cls()
    for name in ("fit", "predict_survival", "predict_risk", "save", "load"):
        assert callable(getattr(model, name))


@pytest.mark.parametrize("model_cls", ALL_MODELS)
def test_stub_methods_raise(model_cls: type) -> None:
    """Avant la feature 3, chaque méthode lève NotImplementedError (stubs)."""
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
    with pytest.raises(NotImplementedError):
        model.save("models/model.pycox")


def test_set_seed_stub_raises() -> None:
    """Avant la feature 3, ``set_seed`` est un stub (à remplacer ensuite)."""
    with pytest.raises(NotImplementedError):
        set_seed(42)
