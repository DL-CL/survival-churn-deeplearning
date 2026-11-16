# Notebooks

Convention de nommage : `NN_objectif.ipynb` (numéro croissant).

| Notebook | Feature | Contenu |
|---|---|---|
| `01_eda_telco.ipynb` | 1 | EDA : distributions, taux de censure, Kaplan-Meier par segment |

Règles :

- Les notebooks servent à **explorer et raconter** ; tout calcul réutilisable migre vers
  `src/` et est testé dans `tests/`.
- Commiter avec les sorties nettoyées :
  `jupyter nbconvert --clear-output --inplace 01_eda_telco.ipynb`.
- Les données brutes restent dans `data/raw/` (git-ignoré) — utiliser des chemins
  relatifs depuis la racine du dépôt.
