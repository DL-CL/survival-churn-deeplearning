"""Tests du contrat du module ``data.loader`` (squelette — feature 1).

Les stubs lèvent ``NotImplementedError`` : ces tests valident le contrat
(constantes, signature) et seront **remplacés/étendus** par la feature 1.
"""

from __future__ import annotations

import inspect
from pathlib import Path

import pytest

from data.loader import DURATION_COLUMN, EVENT_COLUMN, EVENT_POSITIVE_VALUE, load_telco


def test_survival_constants() -> None:
    """Les colonnes clés du dataset sont bien ``tenure`` et ``Churn``."""
    assert DURATION_COLUMN == "tenure"
    assert EVENT_COLUMN == "Churn"
    assert EVENT_POSITIVE_VALUE == "Yes"


def test_load_telco_signature() -> None:
    """``load_telco`` expose le contrat : un paramètre ``path``."""
    sig = inspect.signature(load_telco)
    assert "path" in sig.parameters


def test_load_telco_stub_raises(tmp_path: Path) -> None:
    """Avant la feature 1, le stub lève NotImplementedError (à remplacer ensuite)."""
    with pytest.raises(NotImplementedError):
        load_telco(tmp_path / "absent.csv")
