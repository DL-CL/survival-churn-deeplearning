"""Chargement du jeu de données Telco Customer Churn (Feature 1).

Le fichier brut ``telco-customer-churn.csv`` doit être placé dans ``data/raw/``
(non versionné, voir ``.gitignore``). Chaque ligne = un client ; colonnes clés :

- ``tenure`` : durée d'abonnement en mois (variable de temps, censure à droite) ;
- ``Churn``  : ``"Yes"``/``"No"`` (événement : résiliation observée si ``"Yes"``).
"""

from __future__ import annotations

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


def download_telco(url: str = TELCO_CSV_URL, dest: Path = Path("data/raw")) -> Path:
    """Télécharge le CSV brut Telco Churn vers ``dest`` et renvoie le chemin du fichier.

    Args:
        url: URL du CSV brut.
        dest: dossier de destination (créé si besoin).

    Returns:
        Chemin complet du fichier téléchargé.
    """
    raise NotImplementedError("TODO(feature-1)")


def load_telco(path: Path | str = RAW_CSV_PATH) -> pd.DataFrame:
    """Charge le CSV Telco Churn brut et vérifie les colonnes attendues.

    Args:
        path: chemin du fichier CSV brut.

    Returns:
        DataFrame brut (7 043 lignes × 21 colonnes), sans transformation.

    Raises:
        FileNotFoundError: si le fichier est absent.
        ValueError: si des colonnes obligatoires sont manquantes.
    """
    raise NotImplementedError("TODO(feature-1)")
