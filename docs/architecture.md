# Architecture & contrats d'interface

Ce document fixe les **contrats** entre les 4 features : chacun implémente ses fichiers
sans casser les signatures publiques définies ici (les stubs du squelette les matérialisent).

## Vue d'ensemble du pipeline

```
data/raw/telco-customer-churn.csv        (git-ignoré ; via download_telco() ou manuellement)
        │
        ▼  data.loader.load_telco()                  → DataFrame brut (7 043 × 21)
        ▼  data.preprocessing.clean_telco()          → types propres, TotalCharges numérique
        ▼  data.preprocessing.encode_features()      → 100 % numérique
        ▼  data.preprocessing.train_test_split_survival()
        │      → SurvivalSplit(X_train, X_test, duration_train, duration_test,
        │                event_train, event_test)    [split stratifié sur l'événement]
        ▼
┌─────────────────────────────┐   ┌────────────────────────────────┐
│ models.baselines    (F2)    │   │ models.deep_models  (F3)       │
│ CoxPHModel                  │   │ DeepSurvModel                  │
│ RandomForestSurvival        │   │ LogisticHazardModel / DeepHit  │
└──────────────┬──────────────┘   └───────────────┬────────────────┘
               │   même contrat : fit / predict_survival / predict_risk
               ▼
┌────────────────────────────────────────────────────────────────┐
│ evaluation.metrics  (F4) : make_time_grid, concordance_index,  │
│   integrated_brier_score, calibration_curve                    │
│ evaluation.compare  (F4) : evaluate_model, compare_models,     │
│   cross_validate_survival                                      │
└──────────────┬─────────────────────────────────────────────────┘
               ▼
   app/streamlit_app.py (démo interactive)  +  docs/rapport.md
```

## Contrat de données (Feature 1)

**Entrée** — CSV Telco Customer Churn brut. Colonnes clés :

- `tenure` (int) : durée d'abonnement en mois — la **variable de temps** ;
- `Churn` (`"Yes"`/`"No"`) : l'**événement** — 1 si résiliation observée, 0 si censuré ;
- `TotalCharges` : chaîne contenant des vides → à convertir en numérique ;
- `customerID` : identifiant sans valeur prédictive → retiré.

**Sortie** — `data.preprocessing.SurvivalSplit` (dataclass) :

| Champ | Type | Sémantique |
|---|---|---|
| `X_train`, `X_test` | `pd.DataFrame` | features **100 % numériques**, mêmes colonnes |
| `duration_train`, `duration_test` | `np.ndarray` (float) | durées observées en mois (`tenure`), ≥ 0 |
| `event_train`, `event_test` | `np.ndarray` (int) | **1 = churn observé**, 0 = censuré à droite |

Règles : split **stratifié sur l'événement** (`test_size=0.2`, `seed=42`) ; normalisation
ajustée **sur le train uniquement** (aucune fuite de données vers le test).

## Contrat des modèles (Features 2 & 3)

Tout modèle (baseline ou deep) expose **exactement** ces trois méthodes :

```python
def fit(self, X: pd.DataFrame, duration: np.ndarray, event: np.ndarray) -> Self:
    """Ajuste le modèle ; renvoie self."""

def predict_survival(self, X: pd.DataFrame, times: np.ndarray) -> np.ndarray:
    """S(t | x) pour chaque échantillon et chaque instant de `times`.
    Retour : tableau (n_samples, len(times)), valeurs dans [0, 1]."""

def predict_risk(self, X: pd.DataFrame) -> np.ndarray:
    """Score de risque par échantillon : tableau (n_samples,),
    CROISSANT = plus de risque (sémantique attendue par le C-index)."""
```

Notes d'implémentation :

- **Cox PH** : `lifelines.CoxPHFitter` (recoller `X` + `duration` + `event` en un seul
  DataFrame en interne) ;
- **RSF** : `sksurv.ensemble.RandomSurvivalForest` avec `y` structuré
  `[("event", bool), ("time", float)]`, `random_state` fixé ; interpoler les courbes de
  survie sur la grille `times` ;
- **DeepSurv** : `pycox.models.CoxPH` (+ `torchtuples.practical.MLPVanilla`) ;
- **Logistic-Hazard / DeepHit** : temps **discrétisé** (grille sur `duration_train`) ;
  interpoler sur la grille commune `times` pour respecter le contrat ;
- **Graines** : `models.deep_models.set_seed(42)` avant chaque entraînement ; early
  stopping via les callbacks de torchtuples ;
- **Sauvegarde** : dossier `models/` (git-ignoré) — joblib pour les baselines
  (`save_model`/`load_model`), mécanisme natif pycox pour les modèles deep
  (méthodes `save`/`load`).

## Contrat d'évaluation (Feature 4)

- `make_time_grid(duration_train, n_points=20)` : instants d'évaluation **communs à tous
  les modèles** (indispensable pour comparer les `S(t)` et calculer l'IBS) ; rester dans
  une fenêtre où le risque de censure reste raisonnable ;
- `concordance_index(risk, duration, event) → float` : discrimination (0.5 = aléatoire) ;
- `integrated_brier_score(...)` : calibration globale sur la grille (plus bas = mieux) ;
- `calibration_curve(...)` : DataFrame `risk_pred` / `churn_obs` / `n` par bins de risque ;
- `evaluate_model` / `compare_models` / `cross_validate_survival` : métriques d'un modèle →
  tableau comparatif (4 modèles × métriques) → K-fold stratifié sur l'événement.

## Répartition feature ↔ fichiers

| Feature | Branche | Fichiers |
|---|---|---|
| 1 — Données & EDA | `feature/1-data-eda` | `src/data/*`, `notebooks/01_eda_telco.ipynb`, `tests/test_loader.py`, `tests/test_preprocessing.py` |
| 2 — Baselines | `feature/2-baselines` | `src/models/baselines.py`, `tests/test_baselines.py` |
| 3 — Deep learning | `feature/3-deep-models` | `src/models/deep_models.py`, `tests/test_deep_models.py` |
| 4 — Évaluation, app, rapport | `feature/4-evaluation-app-report` | `src/evaluation/*`, `app/streamlit_app.py`, `tests/test_metrics.py`, `tests/test_compare.py`, `tests/test_app.py`, `docs/rapport.md`, `README.md` |

## Règles transverses

- `seed = 42` partout (split, modèles, CV) ;
- les stubs lèvent `NotImplementedError("TODO(feature-n)")` : chaque feature **remplace**
  ses stubs et **étend** ses tests ; les signatures publiques ne changent pas sans
  discussion (mise à jour de ce document dans la PR) ;
- `data/raw/*`, `data/processed/*`, `models/` et les artefacts lourds ne sont pas versionnés ;
- environnement cible : **Python 3.10 à 3.12** (CI sur 3.11) — contrainte numpy<2.0
  (compatibilité pycox).
