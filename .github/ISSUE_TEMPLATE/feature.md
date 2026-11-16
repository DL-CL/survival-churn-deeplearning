---
name: Feature
about: Nouvelle feature du pipeline (données, modèles, évaluation, app)
title: "[Feature x/4] "
labels: ["feature"]
---

## 🧭 Contexte

<!-- Pourquoi cette feature ? Où se situe-t-elle dans le pipeline du projet ? -->

## 🎯 Objectif

<!-- Résultat attendu, mesurable -->

## 📁 Fichiers concernés

<!-- Fichiers du squelette concernés (voir docs/architecture.md pour les contrats) -->

## ✅ Tâches

- [ ] …

## 🎓 Critères d'acceptation

- [ ] CI verte (`ruff check .` + `pytest`)
- [ ] …

## 🔗 Dépendances

<!-- PR à fusionner AVANT celle-ci (ordre 1 → 2 → 3 → 4) -->

## 🌿 Branche

`feature/<n>-<nom-court>` — créée depuis `develop`, PR vers `develop`,
labels `feature` + `merge-order-n`.
