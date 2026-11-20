
"""Tests du module ``data.preprocessing`` (feature 1)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from tests.test_loader import make_raw_df

from data.preprocessing import (
    RANDOM_SEED,
    TEST_SIZE,
    SurvivalSplit,
    clean_telco,
    encode_features,
    make_survival_arrays,
    scale_features,
    train_test_split_survival,
)


def make_dataset(n: int = 200, seed: int = 0) -> pd.DataFrame:
    """Crée un jeu brut synthétique varié avec environ 25 % de churn."""
    rng = np.random.default_rng(seed)
    df = make_raw_df(n)

    df["customerID"] = [f"{i:05d}-ID" for i in range(n)]
    df["gender"] = rng.choice(["Female", "Male"], n)
    df["Contract"] = rng.choice(
        ["Month-to-month", "One year", "Two year"], n
    )
    df["InternetService"] = rng.choice(
        ["DSL", "Fiber optic", "No"], n
    )
    df["PaymentMethod"] = rng.choice(
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)",
        ],
        n,
    )

    no_net = df["InternetService"] == "No"

    for col in (
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
    ):
        df[col] = np.where(
            no_net,
            "No internet service",
            rng.choice(["Yes", "No"], n),
        )

    df["tenure"] = rng.integers(0, 72, n)
    df["MonthlyCharges"] = rng.uniform(20, 110, n).round(2)
    df["TotalCharges"] = (
        df["tenure"] * df["MonthlyCharges"]
    ).round(2).astype(str)

    df.loc[df["tenure"] == 0, "TotalCharges"] = " "
    df["Churn"] = np.where(
        rng.random(n) < 0.25,
        "Yes",
        "No",
    )

    return df


# ---------------------------------------------------------------------------
# Paramètres et conteneur
# ---------------------------------------------------------------------------


def test_default_parameters() -> None:
    assert RANDOM_SEED == 42
    assert TEST_SIZE == 0.2


def test_survival_split_container() -> None:
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


# ---------------------------------------------------------------------------
# make_survival_arrays
# ---------------------------------------------------------------------------


def test_make_survival_arrays() -> None:
    df = pd.DataFrame(
        {
            "tenure": [1, 2, 0],
            "Churn": ["Yes", "No", "Yes"],
        }
    )

    duration, event = make_survival_arrays(df)

    assert duration.dtype == float
    assert event.dtype.kind == "i"

    np.testing.assert_array_equal(duration, [1.0, 2.0, 0.0])
    np.testing.assert_array_equal(event, [1, 0, 1])


def test_make_survival_arrays_accepts_numeric_event() -> None:
    df = pd.DataFrame(
        {
            "tenure": [1, 2],
            "Churn": [1, 0],
        }
    )

    duration, event = make_survival_arrays(df)

    np.testing.assert_array_equal(duration, [1.0, 2.0])
    np.testing.assert_array_equal(event, [1, 0])


@pytest.mark.parametrize(
    "df",
    [
        pd.DataFrame({"tenure": [1]}),
        pd.DataFrame({"tenure": [-1], "Churn": ["No"]}),
        pd.DataFrame({"tenure": [1], "Churn": ["Maybe"]}),
        pd.DataFrame({"tenure": [np.nan], "Churn": ["Yes"]}),
        pd.DataFrame({"tenure": [1], "Churn": [2]}),
    ],
)
def test_make_survival_arrays_errors(df: pd.DataFrame) -> None:
    with pytest.raises(ValueError):
        make_survival_arrays(df)


# ---------------------------------------------------------------------------
# clean_telco
# ---------------------------------------------------------------------------


def test_clean_telco() -> None:
    raw = make_dataset()

    assert (raw["tenure"] == 0).any()

    cleaned = clean_telco(raw)

    assert "customerID" not in cleaned.columns
    assert cleaned.shape == (len(raw), 20)

    assert pd.api.types.is_float_dtype(cleaned["TotalCharges"])
    assert cleaned["TotalCharges"].notna().all()

    assert (
        cleaned.loc[
            cleaned["tenure"] == 0,
            "TotalCharges",
        ] == 0
    ).all()

    assert pd.api.types.is_integer_dtype(cleaned["tenure"])
    assert pd.api.types.is_integer_dtype(cleaned["SeniorCitizen"])

    # Le DataFrame d'origine ne doit pas être modifié.
    assert "customerID" in raw.columns


def test_clean_telco_missing_columns() -> None:
    raw = make_dataset().drop(columns=["Contract"])

    with pytest.raises(ValueError, match="manquantes"):
        clean_telco(raw)


def test_clean_telco_rejects_invalid_total_charges() -> None:
    raw = make_dataset()
    raw.loc[0, "TotalCharges"] = "invalid"

    # Si tenure > 0, une valeur TotalCharges invalide doit être rejetée.
    raw.loc[0, "tenure"] = 10

    with pytest.raises(ValueError):
        clean_telco(raw)


# ---------------------------------------------------------------------------
# encode_features
# ---------------------------------------------------------------------------


def test_encode_features_numeric_and_stable_columns() -> None:
    enc = encode_features(clean_telco(make_dataset()))

    assert all(
        pd.api.types.is_numeric_dtype(dtype)
        for dtype in enc.dtypes
    )
    assert not enc.isna().any().any()
    assert set(enc["Churn"].unique()) <= {0, 1}

    expected_columns = (
        "gender_Male",
        "Contract_Two year",
        "InternetService_Fiber optic",
        "PaymentMethod_Electronic check",
    )

    for col in expected_columns:
        assert col in enc.columns

    for col in (
        "gender",
        "Contract",
        "InternetService",
        "PaymentMethod",
    ):
        assert col not in enc.columns

    # Les colonnes doivent rester identiques même si une modalité manque.
    sub = make_dataset(30, seed=3)
    sub = sub[sub["Contract"] != "Two year"]

    assert list(
        encode_features(clean_telco(sub)).columns
    ) == list(enc.columns)


def test_encode_features_unknown_category() -> None:
    cleaned = clean_telco(make_dataset())
    cleaned.loc[0, "Contract"] = "Weekly"

    with pytest.raises(ValueError, match="Contract"):
        encode_features(cleaned)


# ---------------------------------------------------------------------------
# scale_features
# ---------------------------------------------------------------------------


def test_scale_features_fit_on_train_only() -> None:
    train = pd.DataFrame(
        {
            "x": [0.0, 10.0, 20.0, 30.0],
            "flag": [0, 1, 0, 1],
        }
    )

    test = pd.DataFrame(
        {
            "x": [100.0, 200.0],
            "flag": [1, 0],
        }
    )

    tr, te = scale_features(train, test)

    # Le train est centré et réduit.
    assert tr["x"].mean() == pytest.approx(0.0, abs=1e-12)
    assert tr["x"].std(ddof=0) == pytest.approx(1.0)

    # Le test utilise les paramètres appris sur le train.
    mean = train["x"].mean()
    std = train["x"].std(ddof=0)

    np.testing.assert_allclose(
        te["x"],
        (test["x"] - mean) / std,
    )

    # Les indicateurs binaires restent inchangés.
    assert tr["flag"].tolist() == [0, 1, 0, 1]
    assert te["flag"].tolist() == [1, 0]

    # Les entrées ne sont pas modifiées.
    assert train["x"].tolist() == [0.0, 10.0, 20.0, 30.0]


def test_scale_features_rejects_different_columns() -> None:
    train = pd.DataFrame({"x": [1.0, 2.0, 3.0]})
    test = pd.DataFrame({"y": [4.0, 5.0]})

    with pytest.raises(ValueError, match="mêmes colonnes"):
        scale_features(train, test)


def test_scale_features_rejects_missing_values() -> None:
    train = pd.DataFrame({"x": [1.0, np.nan, 3.0]})
    test = pd.DataFrame({"x": [4.0, 5.0]})

    with pytest.raises(ValueError, match="manquantes"):
        scale_features(train, test)


# ---------------------------------------------------------------------------
# train_test_split_survival
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def split_and_df() -> tuple[SurvivalSplit, pd.DataFrame]:
    enc = encode_features(clean_telco(make_dataset(1000)))
    return train_test_split_survival(enc), enc


def test_split_shapes_and_alignment(split_and_df) -> None:
    split, enc = split_and_df

    assert (
        len(split.X_train)
        == len(split.duration_train)
        == len(split.event_train)
        == 800
    )

    assert (
        len(split.X_test)
        == len(split.duration_test)
        == len(split.event_test)
        == 200
    )

    assert list(split.X_train.columns) == list(split.X_test.columns)

    assert "tenure" not in split.X_train.columns
    assert "Churn" not in split.X_train.columns

    assert split.X_train.shape[1] == enc.shape[1] - 2


def test_split_event_binary_and_durations_valid(split_and_df) -> None:
    split, _ = split_and_df

    for event in (split.event_train, split.event_test):
        assert set(np.unique(event)) <= {0, 1}

    for duration in (split.duration_train, split.duration_test):
        assert duration.dtype == float
        assert np.isfinite(duration).all()
        assert (duration >= 0).all()


def test_split_is_really_stratified(split_and_df) -> None:
    split, enc = split_and_df

    overall = enc["Churn"].mean()

    assert split.event_train.mean() == pytest.approx(
        overall,
        abs=0.002,
    )

    assert split.event_test.mean() == pytest.approx(
        overall,
        abs=0.005,
    )


def test_split_is_reproducible_and_seed_sensitive() -> None:
    enc = encode_features(clean_telco(make_dataset(300)))

    a = train_test_split_survival(enc)
    b = train_test_split_survival(enc)
    c = train_test_split_survival(enc, seed=7)

    pd.testing.assert_frame_equal(a.X_train, b.X_train)

    np.testing.assert_array_equal(
        a.duration_test,
        b.duration_test,
    )

    assert not np.array_equal(
        a.duration_train,
        c.duration_train,
    )


def test_split_scaling_has_no_leakage(split_and_df) -> None:
    split, _ = split_and_df

    assert split.X_train["MonthlyCharges"].mean() == pytest.approx(
        0.0,
        abs=1e-9,
    )

    assert split.X_train["MonthlyCharges"].std(ddof=0) == pytest.approx(
        1.0
    )

    assert split.X_test["MonthlyCharges"].mean() != pytest.approx(
        0.0,
        abs=1e-9,
    )


def test_split_rejects_non_numeric_features() -> None:
    raw = clean_telco(make_dataset(50))

    with pytest.raises(ValueError, match="numériques"):
        train_test_split_survival(raw)


def test_split_rejects_invalid_test_size() -> None:
    enc = encode_features(clean_telco(make_dataset(100)))

    with pytest.raises(ValueError, match="test_size"):
        train_test_split_survival(enc, test_size=1.0)
