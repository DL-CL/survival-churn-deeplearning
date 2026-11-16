# Survival Churn — Analyse de survie avec Deep Learning

Mini-projet de fin de module **Deep Learning** (data science) : prédire **quand** un client
va résilier son abonnement (*churn*) grâce à l'analyse de survie, avec une gestion explicite
de la **censure** (clients encore actifs à la fin de la période d'observation).

## Jeu de données

[Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) —
7 043 clients, 21 colonnes ; `tenure` = durée d'abonnement en mois (variable de temps),
`Churn` = événement observé (résiliation).

## Modèles

| Type | Modèle | Bibliothèque |
|---|---|---|
| Baseline statistique | Cox PH (Cox Proportional Hazards) | lifelines |
| Baseline non paramétrique | Random Survival Forest | scikit-survival |
| Deep learning | DeepSurv | pycox (torch) |
| Deep learning | Logistic-Hazard / DeepHit | pycox (torch) |

## Métriques

C-index (discrimination), Brier score intégré (calibration globale), courbes de calibration ;
courbes de Kaplan-Meier pour l'exploratoire.

## Démarrage rapide

```bash
# Python 3.10 à 3.12 requis (CI sur 3.11)
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
pytest                           # tests
ruff check .                     # lint
streamlit run app/streamlit_app.py   # démo (feature 4)
```

## Workflow & organisation

- **Gitflow manuel** : `main` (versions taguées), `develop` (intégration), `feature/<n>-<nom>`,
  `release/X.Y.Z`, `hotfix/X.Y.Z` — voir [CONTRIBUTING.md](CONTRIBUTING.md).
- **Runbook release manager** : [docs/RELEASE.md](docs/RELEASE.md).
- **Architecture & contrats d'interface** : [docs/architecture.md](docs/architecture.md).
- 4 features planifiées (issues) : ① données & EDA → ② baselines → ③ deep learning →
  ④ évaluation, app & rapport.

## Licence

MIT — voir [LICENSE](LICENSE).
