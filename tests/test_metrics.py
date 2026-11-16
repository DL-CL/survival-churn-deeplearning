"""Tests du contrat des métriques de survie (squelette — feature 4).

Ces tests vérifient que les 4 métriques du contrat existent et seront
**remplacés/étendus** par des tests à valeurs de référence en feature 4.
"""

from __future__ import annotations

import numpy as np
import pytest

from evaluation.metrics import (
    calibration_curve,
    concordance_index,
    integrated_brier_score,
    make_time_grid,
)


def test_stub_raises() -> None:
    """Avant la feature 4, chaque métrique lève NotImplementedError (stubs)."""
    duration = np.array([5.0, 8.0, 3.0])
    event = np.array([1, 0, 1])
    risk = np.array([0.2, 0.8, 0.5])
    with pytest.raises(NotImplementedError):
        make_time_grid(duration)
    with pytest.raises(NotImplementedError):
        concordance_index(risk, duration, event)
    with pytest.raises(NotImplementedError):
        integrated_brier_score(
            duration,
            event,
            duration,
            event,
            np.ones((3, 2)),
            np.array([1.0, 2.0]),
        )
    with pytest.raises(NotImplementedError):
        calibration_curve(risk, duration, event)
