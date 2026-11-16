"""Tests du contrat du module ``data.preprocessing`` (squelette — feature 1).

Le conteneur ``SurvivalSplit`` est le contrat de sortie consommé par les features
2 et 3 : sa structure est testée dès maintenant.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from data.preprocessing import RANDOM_SEED, TEST_SIZE, SurvivalSplit, make_survival_arrays


def test_default_parameters() -> None:
    """Graine (42) et proportion de test (0.2) par défaut du contrat."""
    assert RANDOM_SEED == 42
    assert TEST_SIZE == 0.2


def test_survival_split_container() -> None:
    """``SurvivalSplit`` porte les 6 champs alignés (features, durées, événements)."""
    split = SurvivalSplit(
        X_train=pd.DataFrame({"feature": [1.0, 2.0]}),
        X_test=pd.DataFrame({"feature": [3.0]}),
        duration_train=np.array([5.0, 8.0]),
        duration_test=np.array([3.0]),
        event_train=np.array([1, 0]),
        event_test=np.array([1]),
    )
    assert split.X_train.shape == (2, 1)
    assert split.X_test.shape == (1, 1)
    assert split.duration_train.shape == (2,)
    assert split.duration_test.shape == (1,)
    assert split.event_train.shape == (2,)
    assert split.event_test.shape == (1,)


def test_make_survival_arrays_stub_raises() -> None:
    """Avant la feature 1, le stub lève NotImplementedError (à remplacer ensuite)."""
    df = pd.DataFrame({"tenure": [1, 2], "Churn": ["Yes", "No"]})
    with pytest.raises(NotImplementedError):
        make_survival_arrays(df)
