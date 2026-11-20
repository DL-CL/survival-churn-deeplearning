
"""Tests du module ``data.loader`` (feature 1)."""

from __future__ import annotations

import inspect
from pathlib import Path

import pandas as pd
import pytest

from data.loader import (
    DURATION_COLUMN,
    EVENT_COLUMN,
    EVENT_POSITIVE_VALUE,
    EXPECTED_COLUMNS,
    download_telco,
    load_telco,
)


def make_raw_df(n: int = 3) -> pd.DataFrame:
    """Mini jeu brut avec les 21 colonnes attendues."""
    row = {
        "customerID": "0001-ABCDE",
        "gender": "Female",
        "SeniorCitizen": 0,
        "Partner": "Yes",
        "Dependents": "No",
        "tenure": 5,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "DSL",
        "OnlineSecurity": "No",
        "OnlineBackup": "Yes",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "No",
        "StreamingMovies": "No",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 29.85,
        "TotalCharges": "149.25",
        "Churn": "No",
    }

    return pd.DataFrame(
        [dict(row, customerID=f"{i:04d}-X") for i in range(n)]
    )


def test_survival_constants() -> None:
    """Les colonnes clés du dataset sont bien ``tenure`` et ``Churn``."""
    assert DURATION_COLUMN == "tenure"
    assert EVENT_COLUMN == "Churn"
    assert EVENT_POSITIVE_VALUE == "Yes"
    assert len(EXPECTED_COLUMNS) == 21


def test_load_telco_signature() -> None:
    """``load_telco`` expose le contrat : un paramètre ``path``."""
    assert "path" in inspect.signature(load_telco).parameters


def test_load_telco_ok(tmp_path: Path) -> None:
    """Un CSV valide est chargé tel quel (aucune transformation)."""
    csv = tmp_path / "telco.csv"
    make_raw_df(4).to_csv(csv, index=False)

    df = load_telco(csv)

    assert df.shape == (4, 21)
    assert list(df.columns) == list(EXPECTED_COLUMNS)


def test_load_telco_accepts_str_path(tmp_path: Path) -> None:
    """load_telco accepte un chemin de type str."""
    csv = tmp_path / "telco.csv"
    make_raw_df().to_csv(csv, index=False)

    assert load_telco(str(csv)).shape[0] == 3


def test_load_telco_missing_file(tmp_path: Path) -> None:
    """Un fichier absent déclenche FileNotFoundError."""
    with pytest.raises(FileNotFoundError, match="introuvable"):
        load_telco(tmp_path / "absent.csv")


def test_load_telco_missing_columns(tmp_path: Path) -> None:
    """Des colonnes obligatoires absentes déclenchent ValueError."""
    csv = tmp_path / "bad.csv"
    make_raw_df().drop(columns=["Churn", "tenure"]).to_csv(
        csv,
        index=False,
    )

    with pytest.raises(ValueError, match="manquantes") as exc:
        load_telco(csv)

    assert "Churn" in str(exc.value)
    assert "tenure" in str(exc.value)


def test_download_telco_from_local_url(tmp_path: Path) -> None:
    """Téléchargement testé hors réseau via une URL file://."""
    src = tmp_path / "source.csv"
    make_raw_df().to_csv(src, index=False)

    dest = tmp_path / "raw"
    path = download_telco(url=src.as_uri(), dest=dest)

    assert path.is_file()
    assert path.parent == dest
    assert not list(dest.glob("*.part"))
    assert load_telco(path).shape == (3, 21)


def test_download_telco_invalid_csv_preserves_existing_file(
    tmp_path: Path,
) -> None:
    """Un CSV invalide ne doit pas remplacer un fichier valide existant."""
    dest = tmp_path / "raw"
    dest.mkdir()

    target = dest / "telco-customer-churn.csv"
    make_raw_df().to_csv(target, index=False)

    original_content = target.read_bytes()

    invalid_src = tmp_path / "invalid.csv"
    pd.DataFrame({"wrong_column": [1, 2, 3]}).to_csv(
        invalid_src,
        index=False,
    )

    with pytest.raises(RuntimeError):
        download_telco(url=invalid_src.as_uri(), dest=dest)

    assert target.read_bytes() == original_content
    assert not list(dest.glob("*.part"))
