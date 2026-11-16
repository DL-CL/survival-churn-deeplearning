# Rapport final — Analyse de survie avec Deep Learning

> Document à compléter par la **feature 4** (issue « [Feature 4/4] Évaluation, démo et
> rapport »). Ce squelette fixe le plan du rapport ; chaque section est remplie au fil
> des features 1 à 3.

## 1. Contexte et problématique

Prédire **quand** un client résilie (churn), et pas seulement **si** : l'analyse de survie
gère explicitement la **censure** (clients encore actifs en fin d'observation).
Jeu de données : Telco Customer Churn.

## 2. Données

- Source, dictionnaire de variables, volume (7 043 clients × 21 colonnes).
- Variable de temps : `tenure` (mois) ; événement : `Churn` (Yes/No).
- Taux de censure global et par segment : _à remplir (feature 1)_.

## 3. Méthodologie

- Nettoyage, encodage, normalisation : _à remplir (feature 1)_.
- Split train/test stratifié sur l'événement, seed 42.
- Discrétisation du temps pour les modèles discrets : _à remplir (feature 3)_.

## 4. Modèles

1. **Cox PH** (lifelines) — baseline statistique.
2. **Random Survival Forest** (scikit-survival) — baseline non paramétrique.
3. **DeepSurv** (pycox) — réseau de neurones + perte de Cox.
4. **Logistic-Hazard ou DeepHit** (pycox) — temps discret.

## 5. Résultats

| Modèle | C-index ↑ | Brier intégré ↓ | Calibration |
|---|---|---|---|
| Cox PH | — | — | — |
| Random Survival Forest | — | — | — |
| DeepSurv | — | — | — |
| Logistic-Hazard / DeepHit | — | — | — |

À compléter : courbes de Kaplan-Meier par segment, courbes de calibration, validation
croisée (5 folds), interprétation.

## 6. Application de démonstration

Application Streamlit : profil client → courbe de survie personnalisée `S(t | profil)`,
score de risque, survie médiane. _À documenter (feature 4)._

## 7. Limites et perspectives

À compléter : hypothèses des modèles (PH, proportionnalité), qualité des données,
extrapolation temporelle, données actualisées.
