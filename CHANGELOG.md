# Changelog

Toutes les modifications notables de ce projet sont documentées dans ce fichier.
Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/) ;
versionnement selon [SemVer](https://semver.org/lang/fr/).

## [Non publié]

### Ajouté

- Squelette du projet : `src/` (data, models, evaluation), `tests/`, `app/`, `docs/`,
  `notebooks/`, `data/raw|processed/`.
- Workflow CI (ruff + pytest) sur les PR et pushes vers `main`, `develop`, `release/**`,
  `hotfix/**`.
- Gitflow manuel (`main`, `develop`, `feature/*`, `release/*`, `hotfix/*`) documenté dans
  `CONTRIBUTING.md`, runbook release/hotfix dans `docs/RELEASE.md`.
- Stubs typés (fonctions vides + docstrings) fixant les contrats d'interface entre les
  4 features — voir `docs/architecture.md`.
- Templates d'issues (feature, bug) et de pull request ; labels `merge-order-1` à
  `merge-order-4`.

## [0.1.0] - 2026-11-16

### Ajouté

- Initialisation du dépôt : README, licence MIT, branche par défaut `develop`.
