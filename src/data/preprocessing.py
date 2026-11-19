
"""Nettoyage, encodage et découpage train/test pour l'analyse de survie (Feature 1).

Contrat de sortie (voir ``docs/architecture.md``) : :class:`SurvivalSplit` contient
les matrices de features et les tableaux alignés ``duration`` (``tenure``, en mois)
et ``event`` (1 = churn observé, 0 = censuré à droite).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from data.loader import (
    DURATION_COLUMN,
    EVENT_COLUMN,
    EVENT_POSITIVE_VALUE,
    EXPECTED_COLUMNS,
)

#: Graine aléatoire par défaut (reproductibilité).
RANDOM_SEED = 42

#: Proportion du jeu de test par défaut.
TEST_SIZE = 0.2

#: Identifiant client : sans valeur prédictive, retiré au nettoyage.
ID_COLUMN = "customerID"

#: Colonne dont les chaînes vides deviennent NaN puis numérique.
TOTAL_CHARGES_COLUMN = "TotalCharges"

#: Colonnes binaires Yes/No -> 1/0.
YES_NO_COLUMNS = (
    "Partner",
    "Dependents",
    "PhoneService",
    "MultipleLines",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "PaperlessBilling",
)

#: Modalités sans service assimilées à No.
NO_SERVICE_VALUES = ("No internet service", "No phone service")

#: Modalités fixes pour garantir des colonnes stables.
#: La première modalité est supprimée (catégorie de référence).
CATEGORICAL_LEVELS: dict[str, tuple[str, ...]] = {
    "InternetService": ("DSL", "Fiber optic", "No"),
    "Contract": ("Month-to-month", "One year", "Two year"),
    "PaymentMethod": (
        "Bank transfer (automatic)",
        "Credit card (automatic)",
        "Electronic check",
        "Mailed check",
    ),
}


@dataclass
class SurvivalSplit:
    """Conteneur du découpage train/test aligné sur la survie."""

    X_train: pd.DataFrame
    X_test: pd.DataFrame
    duration_train: np.ndarray
    duration_test: np.ndarray
    event_train: np.ndarray
    event_test: np.ndarray


def make_survival_arrays(
    df: pd.DataFrame,
) -> tuple[np.ndarray, np.ndarray]:
    """Extrait les durées et les indicateurs d'événement."""

    _require_columns(df, [DURATION_COLUMN, EVENT_COLUMN])

    duration = pd.to_numeric(
        df[DURATION_COLUMN], errors="coerce"
    ).to_numpy(dtype=float)

    if not np.isfinite(duration).all():
        raise ValueError(
            f"'{DURATION_COLUMN}' contient des valeurs manquantes "
            "ou non numériques."
        )

    if (duration < 0).any():
        raise ValueError(
            f"'{DURATION_COLUMN}' contient des durées négatives."
        )

    churn = df[EVENT_COLUMN]

    if (
        pd.api.types.is_numeric_dtype(churn)
        or pd.api.types.is_bool_dtype(churn)
    ):
        event = churn.to_numpy()
    else:
        event = churn.map(
            {EVENT_POSITIVE_VALUE: 1, "No": 0}
        ).to_numpy()

    if pd.isna(event).any() or not np.isin(event, (0, 1)).all():
        raise ValueError(
            f"'{EVENT_COLUMN}' doit contenir uniquement Yes/No ou 0/1."
        )

    return duration, event.astype(int)



def clean_telco(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie le jeu de données Telco Customer Churn.

    - Vérifie la présence des colonnes attendues.
    - Nettoie les chaînes de caractères.
    - Convertit les colonnes numériques.
    - Traite les valeurs manquantes de TotalCharges.
    - Vérifie la cohérence des données.
    - Supprime customerID.

    Retourne un DataFrame nettoyé sans modifier le DataFrame original.
    """
    _require_columns(df, EXPECTED_COLUMNS)

    out = df.copy()

    # 1. Nettoyage des chaînes de caractères
    for column in out.select_dtypes(include=["object"]).columns:
        out[column] = out[column].str.strip()

    # 2. Conversion des colonnes numériques
    out[TOTAL_CHARGES_COLUMN] = pd.to_numeric(
        out[TOTAL_CHARGES_COLUMN].replace("", np.nan),
        errors="coerce",
    )

    for column in (DURATION_COLUMN, "MonthlyCharges", "SeniorCitizen"):
        out[column] = pd.to_numeric(out[column], errors="coerce")

    # 3. Traitement des valeurs manquantes de TotalCharges
    # Les clients ayant tenure = 0 n'ont pas encore accumulé de charges.
    zero_tenure = out[DURATION_COLUMN] == 0

    out.loc[
        zero_tenure & out[TOTAL_CHARGES_COLUMN].isna(),
        TOTAL_CHARGES_COLUMN,
    ] = 0.0

    if out[TOTAL_CHARGES_COLUMN].isna().any():
        raise ValueError(
            "TotalCharges contient des valeurs manquantes "
            "inexpliquées après nettoyage."
        )

    # 4. Vérification des valeurs numériques
    numeric_columns = [
        DURATION_COLUMN,
        "MonthlyCharges",
        TOTAL_CHARGES_COLUMN,
        "SeniorCitizen",
    ]

    for column in numeric_columns:
        values = out[column].to_numpy(dtype=float)

        if not np.isfinite(values).all():
            raise ValueError(
                f"La colonne {column} contient des valeurs "
                "manquantes ou non finies."
            )

    # 5. Vérification des valeurs non négatives
    for column in (
        DURATION_COLUMN,
        "MonthlyCharges",
        TOTAL_CHARGES_COLUMN,
    ):
        if (out[column] < 0).any():
            raise ValueError(
                f"La colonne {column} ne doit pas contenir "
                "de valeurs négatives."
            )

    # 6. Vérification de SeniorCitizen
    if not out["SeniorCitizen"].isin([0, 1]).all():
        raise ValueError(
            "SeniorCitizen doit contenir uniquement 0 ou 1."
        )

    # 7. Vérification de tenure
    # np.equal fonctionne avec les entiers et les flottants.
    if not np.equal(
        out[DURATION_COLUMN],
        np.floor(out[DURATION_COLUMN]),
    ).all():
        raise ValueError(
            "tenure doit contenir des nombres entiers."
        )

    out[DURATION_COLUMN] = out[DURATION_COLUMN].astype(int)
    out["SeniorCitizen"] = out["SeniorCitizen"].astype(int)

    # 8. Vérification des variables de survie
    make_survival_arrays(out)

    # 9. Suppression de l'identifiant client
    out = out.drop(columns=[ID_COLUMN])

    return out



def encode_features(df: pd.DataFrame) -> pd.DataFrame:
    """Encode les variables catégorielles et conserve duration/event."""

    _require_columns(
        df,
        [
            DURATION_COLUMN,
            EVENT_COLUMN,
            "gender",
            *YES_NO_COLUMNS,
            *CATEGORICAL_LEVELS,
        ],
    )

    out = df.copy()

    # La cible devient un indicateur numérique 0/1.
    _, event = make_survival_arrays(out)
    out[EVENT_COLUMN] = event

    # gender : Male = 1, Female = 0.
    _check_values(out["gender"], {"Female", "Male"}, "gender")
    out["gender_Male"] = (out["gender"] == "Male").astype(int)
    out = out.drop(columns="gender")

    # Variables binaires Yes/No.
    for col in YES_NO_COLUMNS:
        values = out[col].replace(
            list(NO_SERVICE_VALUES), "No"
        )

        _check_values(values, {"Yes", "No"}, col)
        out[col] = (values == "Yes").astype(int)

    # Variables catégorielles à plusieurs modalités.
    for col, levels in CATEGORICAL_LEVELS.items():
        _check_values(out[col], set(levels), col)

        cat = pd.Categorical(
            out[col],
            categories=list(levels),
        )

        dummies = pd.get_dummies(
            cat,
            prefix=col,
            prefix_sep="_",
            drop_first=True,
        ).astype(int)

        dummies.index = out.index

        out = pd.concat(
            [out.drop(columns=col), dummies],
            axis=1,
        )

    # Ordre stable des colonnes.
    features = sorted(
        c for c in out.columns
        if c not in (DURATION_COLUMN, EVENT_COLUMN)
    )

    out = out[
        [DURATION_COLUMN, EVENT_COLUMN, *features]
    ]

    return out.astype({col: float for col in features})


def scale_features(
    train: pd.DataFrame,
    test: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Standardise les variables continues en ajustant sur le train uniquement."""

    if list(train.columns) != list(test.columns):
        raise ValueError(
            "train et test doivent avoir les mêmes colonnes "
            "dans le même ordre."
        )

    for name, data in [("train", train), ("test", test)]:
        if not all(
            pd.api.types.is_numeric_dtype(dtype)
            for dtype in data.dtypes
        ):
            raise ValueError(
                f"Les features {name} doivent être numériques."
            )

        if data.isna().any().any():
            raise ValueError(
                f"Les features {name} contiennent des valeurs manquantes."
            )

        if not np.isfinite(data.to_numpy(dtype=float)).all():
            raise ValueError(
                f"Les features {name} contiennent des valeurs infinies."
            )

    train_out = train.copy()
    test_out = test.copy()

    # Les indicateurs binaires restent en 0/1.
    continuous = [
        col for col in train.columns
        if train[col].nunique(dropna=True) > 2
    ]

    if continuous:
        scaler = StandardScaler()
        scaler.fit(train[continuous])

        train_out[continuous] = scaler.transform(
            train[continuous]
        )

        test_out[continuous] = scaler.transform(
            test[continuous]
        )

    return train_out, test_out


def train_test_split_survival(
    df: pd.DataFrame,
    test_size: float = TEST_SIZE,
    seed: int = RANDOM_SEED,
) -> SurvivalSplit:
    """Effectue un découpage stratifié et renvoie un SurvivalSplit."""

    if not 0 < test_size < 1:
        raise ValueError("test_size doit être compris entre 0 et 1.")

    duration, event = make_survival_arrays(df)

    # Les colonnes duration et event ne doivent jamais entrer dans X.
    X = df.drop(
        columns=[DURATION_COLUMN, EVENT_COLUMN]
    ).reset_index(drop=True)

    if X.empty:
        raise ValueError("Aucune variable explicative disponible.")

    if not all(
        pd.api.types.is_numeric_dtype(dtype)
        for dtype in X.dtypes
    ):
        raise ValueError(
            "Les features doivent être 100 % numériques "
            "(appeler encode_features)."
        )

    if X.isna().any().any():
        raise ValueError(
            "Les features contiennent des valeurs manquantes."
        )

    if not np.isfinite(X.to_numpy(dtype=float)).all():
        raise ValueError(
            "Les features contiennent des valeurs infinies."
        )

    if len(np.unique(event)) != 2:
        raise ValueError(
            "Le découpage stratifié nécessite les deux classes d'événement."
        )

    X_train, X_test, d_train, d_test, e_train, e_test = (
        train_test_split(
            X,
            duration,
            event,
            test_size=test_size,
            random_state=seed,
            stratify=event,
        )
    )

    X_train, X_test = scale_features(
        X_train.reset_index(drop=True),
        X_test.reset_index(drop=True),
    )

    return SurvivalSplit(
        X_train=X_train,
        X_test=X_test,
        duration_train=np.asarray(d_train, dtype=float),
        duration_test=np.asarray(d_test, dtype=float),
        event_train=np.asarray(e_train, dtype=int),
        event_test=np.asarray(e_test, dtype=int),
    )


def _require_columns(
    df: pd.DataFrame,
    columns: list[str] | tuple[str, ...],
) -> None:
    """Vérifie la présence des colonnes requises."""

    missing = [col for col in columns if col not in df.columns]

    if missing:
        raise ValueError(f"Colonnes manquantes : {missing}")


def _check_values(
    series: pd.Series,
    allowed: set[str],
    name: str,
) -> None:
    """Vérifie que les modalités appartiennent à l'ensemble autorisé."""

    unknown = set(series.dropna().unique()) - allowed

    if unknown or series.isna().any():
        raise ValueError(
            f"Modalités inattendues dans '{name}' : "
            f"{sorted(map(str, unknown))}"
        )
