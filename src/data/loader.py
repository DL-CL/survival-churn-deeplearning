
"""Chargement du jeu de données Telco Customer Churn (Feature 1).

Le fichier brut ``telco-customer-churn.csv`` doit être placé dans ``data/raw/``
(non versionné, voir ``.gitignore``). Chaque ligne représente un client.

Colonnes clés :
- ``tenure`` : durée d'abonnement en mois (durée observée).
- ``Churn`` : ``"Yes"``/``"No"`` (événement observé si ``"Yes"``,
  censure à droite si ``"No"``).
"""

from __future__ import annotations

import shutil
import tempfile
import urllib.request
from pathlib import Path

import pandas as pd

#: Colonne contenant la durée observée (en mois).
DURATION_COLUMN = "tenure"

#: Colonne contenant l'événement (churn).
EVENT_COLUMN = "Churn"

#: Valeur de ``Churn`` correspondant à l'événement observé.
EVENT_POSITIVE_VALUE = "Yes"

#: URL publique du jeu de données Telco Customer Churn (miroir IBM).
TELCO_CSV_URL = (
    "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/"
    "master/data/Telco-Customer-Churn.csv"
)

#: Chemin par défaut du CSV brut.
RAW_CSV_PATH = Path("data/raw/telco-customer-churn.csv")

#: Les 21 colonnes attendues du CSV brut.
EXPECTED_COLUMNS: tuple[str, ...] = (
    "customerID",
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges",
    "Churn",
)


def load_telco(path: Path | str = RAW_CSV_PATH) -> pd.DataFrame:
    """Charge le CSV Telco Churn brut et vérifie son schéma.

    Args:
        path: chemin du fichier CSV brut.

    Returns:
        DataFrame brut, sans transformation ni nettoyage.

    Raises:
        FileNotFoundError: si le fichier est absent.
        ValueError: si des colonnes attendues sont manquantes.
    """
    path = Path(path)

    if not path.is_file():
        raise FileNotFoundError(
            f"Fichier introuvable : {path}. Placez le CSV dans data/raw/ "
            "ou lancez download_telco()."
        )

    df = pd.read_csv(path)

    missing = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(
            f"Colonnes obligatoires manquantes dans {path} : {missing}"
        )

    return df


def download_telco(
    url: str = TELCO_CSV_URL,
    dest: Path = Path("data/raw"),
) -> Path:
    """Télécharge le CSV brut Telco Churn vers ``dest``.

    Le téléchargement est effectué dans un fichier temporaire.
    Le fichier définitif n'est remplacé qu'après validation du CSV.

    Args:
        url: URL du CSV brut.
        dest: dossier de destination (créé si nécessaire).

    Returns:
        Chemin du fichier téléchargé.

    Raises:
        RuntimeError: si le téléchargement échoue.
        ValueError: si le fichier téléchargé ne respecte pas le schéma attendu.
    """
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)

    target = dest / RAW_CSV_PATH.name

    # Création d'un fichier temporaire dans le dossier de destination.
    with tempfile.NamedTemporaryFile(
        dir=dest,
        suffix=".part",
        delete=False,
    ) as tmp:
        tmp_path = Path(tmp.name)

    try:
        # Téléchargement du fichier.
        with urllib.request.urlopen(url, timeout=60) as response:
            with tmp_path.open("wb") as output:
                shutil.copyfileobj(response, output)

        # Validation avant remplacement du fichier définitif.
        load_telco(tmp_path)

        # Remplacement atomique du fichier cible.
        tmp_path.replace(target)

    except Exception as exc:
        raise RuntimeError(
            f"Impossible de télécharger ou de valider le dataset Telco : {exc}"
        ) from exc

    finally:
        # Suppression du fichier temporaire, même en cas d'échec.
        tmp_path.unlink(missing_ok=True)

    return target
