# CONTRIBUTING — Guide de contribution (Gitflow manuel)

Bienvenue dans l'équipe **survival-churn-deeplearning** ! Ce document décrit le workflow Git
que tout le monde suit. Il est volontairement **manuel** : pas d'extension git-flow,
uniquement des commandes `git` standard.

## 🗺️ Vue d'ensemble du Gitflow

| Branche | Créée depuis | Fusionne dans | Rôle |
|---|---|---|---|
| `main` | — | — | Code de production, **uniquement des versions taguées** (`vX.Y.Z`) |
| `develop` | `main` | — | Intégration continue des features |
| `feature/<n>-<nom-court>` | `develop` | `develop` (PR) | Une feature = un numéro (1 à 4), ex : `feature/1-data-eda` |
| `release/X.Y.Z` | `develop` | `main` **puis** `develop` (back-merge) | Stabilisation uniquement : version, changelog, docs, corrections mineures |
| `hotfix/X.Y.Z` | `main` | `main` **puis** `develop` (back-merge) | Correctif urgent de production |

### Schéma ASCII

```
main      ────●───────────────────────●───────────────●─────►  production (tags vX.Y.Z)
               \                     /│\             /
                \   release/1.0.0   / │ \           /   back-merge
                 \_________________/  │  \_________/    (PR → develop)
                                      │
hotfix/1.0.1 ────────────────────────┘     ← créée depuis main, merge --no-ff dans main

develop   ──●──●──●──●──●──────────────●──────●─────────►  intégration continue
             \  \  \  \  \            /      │
              \  \  \  \  \          /       │
feature/1 ─────●  │  │  │  │                 │   PR n°1 (merge-order-1)
feature/2 ────────●  │  │  │                 │   PR n°2 (merge-order-2)
feature/3 ───────────●  │                  /    PR n°3 (merge-order-3)
feature/4 ──────────────●                 │    PR n°4 (merge-order-4)
                                          └── back-merge de release/hotfix dans develop
```

## 🌿 Cycle de vie d'une feature (pas à pas)

1. **Synchroniser** `develop` :
   ```bash
   git checkout develop
   git pull origin develop
   ```
2. **Créer** la branche de feature depuis `develop` (le numéro correspond à votre issue) :
   ```bash
   git checkout -b feature/1-data-eda develop
   ```
3. **Travailler** en petits commits **Conventional Commits** :
   ```bash
   git add src/data/loader.py
   git commit -m "feat: implémente load_telco avec validation des colonnes"
   ```
4. **Pousser** régulièrement :
   ```bash
   git push -u origin feature/1-data-eda
   ```
5. **Ouvrir la PR vers `develop`** (jamais vers `main` !) :
   - titre clair, la description référence l'issue (`Closes #1`) ;
   - ajouter le label `feature` **et** le label `merge-order-n` correspondant ;
   - compléter la checklist du template de PR.
6. **Rester à jour** de `develop` pendant la revue :
   ```bash
   git fetch origin
   git merge origin/develop    # ou git rebase origin/develop si vous êtes seul·e sur la branche
   git push
   ```
7. **Fusionner** via le bouton **« Create a merge commit »** (équivalent à
   `git merge --no-ff`) quand tous les feux sont au vert (voir plus bas). La branche de
   feature est supprimée automatiquement après la fusion.

## 🔢 La règle d'ordre des PR (1 → 2 → 3 → 4)

Les 4 features sont interdépendantes (chaque étape consomme la sortie de la précédente).
Pour avancer vite et éviter les conflits, elles fusionnent **dans l'ordre** :

| Ordre | Issue | Branche | Label | Peut fusionner quand… |
|---|---|---|---|---|
| 1 | Données, nettoyage et analyse exploratoire | `feature/1-data-eda` | `merge-order-1` | rien à attendre |
| 2 | Modèles baselines | `feature/2-baselines` | `merge-order-2` | PR 1 fusionnée |
| 3 | Modèles deep learning | `feature/3-deep-models` | `merge-order-3` | PR 2 fusionnée |
| 4 | Évaluation, démo et rapport | `feature/4-evaluation-app-report` | `merge-order-4` | PR 3 fusionnée |

**Règle absolue : la PR n ne fusionne que si la PR n−1 est déjà fusionnée.**
Avant d'ouvrir votre PR, vérifiez que la PR d'ordre inférieur est fusionnée ; si elle ne
l'est pas, attendez ou aidez-la à fusionner. Les labels `merge-order-n` portent cet ordre ;
les titres d'issues rappellent leur numéro (`[Feature n/4] …`).

## ✅ Quand une PR est-elle prête à fusionner ?

Toutes ces conditions doivent être réunies :

- **CI verte** — le workflow `CI` (lint `ruff check .` + tests `pytest`) passe sur la PR ;
- **1 approbation** d'un autre membre — *l'auteur d'une PR ne peut pas l'approuver
  lui-même* (règle GitHub), et **tout membre peut approuver** : pas de règles CODEOWNERS,
  pas d'intégrateur dédié ;
- branche **à jour avec `develop`** (exigé par la protection de branche) ;
- **toutes les conversations de review résolues** (exigé par la protection de branche) ;
- checklist du template de PR complétée ;
- pour la PR n : la PR n−1 est fusionnée.

Les protections de branches appliquent automatiquement ces règles (voir plus bas). Les
**admins peuvent contourner en cas d'urgence** — à réserver aux vrais cas d'urgence.

## ✍️ Conventional Commits

Format : `<type>: <description courte en minuscules>`, sans point final.

| Type | Usage | Exemple |
|---|---|---|
| `feat` | nouvelle fonctionnalité | `feat: encode les variables catégorielles en one-hot` |
| `fix` | correction de bug | `fix: corrige la coercition de TotalCharges vide` |
| `docs` | documentation | `docs: complète le contrat des modèles dans architecture.md` |
| `test` | tests | `test: ajoute un test de stratification du split` |
| `refactor` | refactoring sans changement de comportement | `refactor: factorise l'interpolation des courbes de survie` |
| `chore` | maintenance, config, outils | `chore: bump la version à 1.0.0` |
| `ci` | pipeline CI/CD | `ci: ajoute le cache pip au workflow` |

Les releases et hotfixes utilisent en plus `chore(release):` et les tags annotés `vX.Y.Z`.

## 🚀 Releases & hotfixes

Les runbooks pas à pas (commandes exactes, tag annoté, GitHub Release, back-merge) sont
dans **[docs/RELEASE.md](docs/RELEASE.md)** — réservés au release manager.

Rappel des règles :

- `release/X.Y.Z` : créée depuis `develop` quand les 4 features sont fusionnées ;
  **stabilisation uniquement** (version, changelog, docs, petites corrections) ; fusionnée
  dans `main` **puis** back-merge dans `develop` ; `git merge --no-ff` + tag annoté
  `vX.Y.Z` sur `main` + GitHub Release.
- `hotfix/X.Y.Z` : créée depuis `main` ; fusionnée dans `main` **puis** dans `develop`
  (ou dans la release en cours si elle existe) ; même protocole de tag et de release.

## 🧪 CI

Le workflow `.github/workflows/ci.yml` tourne sur chaque PR et chaque push vers `main`,
`develop`, `release/**` et `hotfix/**` :

1. `ruff check .` — lint (config dans `pyproject.toml`) ;
2. `pytest -v` — tests (Python 3.11, installation de `requirements.txt` avec cache).

Gardez les tests **rapides et sans données brutes** : la CI n'a pas accès à `data/raw/`
(git-ignoré). Utilisez des jeux de données **synthétiques** dans les tests.

## 🔒 Protections de branches (déjà configurées)

- **`main` et `develop`** : push direct interdit, PR obligatoire, 1 approbation minimale,
  l'auteur ne peut pas approuver sa propre PR (règle GitHub), conversations résolues
  obligatoires, historique linéaire **non** exigé (merges « Create a merge commit »
  conservés), force-push et suppression interdits, admins autorisés à contourner en cas
  d'urgence.
- **`release/**` et `hotfix/**`** : mêmes règles, appliquées via des **rulesets** de dépôt
  (patterns `refs/heads/release/*` et `refs/heads/hotfix/*`), avec contournement admin.

## ⚙️ Réglages du dépôt (déjà configurés)

- Branche par défaut : **`develop`** (les nouvelles PR ciblent `develop`).
- Seules les fusions **« Create a merge commit »** sont autorisées (pas de squash ni de
  rebase merge → l'historique des commits est préservé, équivalent aux `--no-ff`).
- **Suppression automatique des branches de tête** après fusion des PR.
- Environnement cible : **Python 3.10 à 3.12** (CI sur 3.11) — contrainte liée à numpy<2.0
  (compatibilité pycox).
