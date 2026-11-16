# RELEASE.md — Runbook du release manager

> À destination du **release manager** (admin du dépôt). Commandes exactes, dans l'ordre.
> Prérequis : les 4 features sont fusionnées dans `develop`, la CI est verte sur `develop`,
> toutes les issues du milestone `v1.0.0` sont fermées.

## Convention de versionnement

[SemVer](https://semver.org/lang/fr/) — `vX.Y.Z` : X = majeur (cassant), Y = mineur
(nouvelle fonctionnalité), Z = patch (correctif). Tags **annotés** posés sur `main`,
GitHub Release associée. Version de référence du projet : `pyproject.toml`.

---

## 🚀 Runbook — Release 1.0.0

### 0. Vérifications préalables

```bash
git checkout develop
git pull origin develop
pytest                  # doit être vert
ruff check .            # doit être vert
gh pr list --base develop          # aucune PR de feature restante
gh issue list --milestone "v1.0.0" # toutes les issues fermées
```

### 1. Créer la branche de release

```bash
git checkout develop
git pull origin develop
git checkout -b release/1.0.0 develop
git push -u origin release/1.0.0
```

### 2. Stabilisation — UNIQUEMENT : version, changelog, docs, corrections mineures

- `pyproject.toml` : passer `version = "1.0.0"` ;
- `CHANGELOG.md` : renommer `## [Non publié]` en `## [1.0.0] - <date du jour>` ;
- relecture rapide : `README.md`, `docs/architecture.md`.

```bash
git add pyproject.toml CHANGELOG.md
git commit -m "chore(release): bump de version vers 1.0.0 + changelog"
git push
```

### 3. PR `release/1.0.0` → `main` puis merge --no-ff

```bash
gh pr create --base main --head release/1.0.0 \
  --title "Release 1.0.0" \
  --label release \
  --body "Stabilisation pour la 1.0.0 : bump de version, CHANGELOG."
gh pr checks                # CI verte avant de fusionner
gh pr merge <numéro> --merge   # bouton « Create a merge commit » = merge --no-ff
```

### 4. Tag annoté + GitHub Release

```bash
git checkout main
git pull origin main
git tag -a v1.0.0 -m "Release 1.0.0 — Analyse de survie avec Deep Learning (Telco churn)"
git push origin v1.0.0
gh release create v1.0.0 --title "v1.0.0" --generate-notes
```

### 5. Back-merge dans `develop`

```bash
gh pr create --base develop --head release/1.0.0 \
  --title "Back-merge release/1.0.0 dans develop" \
  --label release \
  --body "Réintégration des ajustements de stabilisation dans develop."
gh pr merge <numéro> --merge
```

### 6. Supprimer la branche de release

```bash
git branch -d release/1.0.0
git push origin --delete release/1.0.0
```

---

## 🚑 Runbook — Hotfix 1.0.1 (correctif urgent sur `main`)

### 1. Créer la branche depuis `main`

```bash
git checkout main
git pull origin main
git checkout -b hotfix/1.0.1 main
git push -u origin hotfix/1.0.1
```

### 2. Corriger + bump de version + changelog

```bash
# ... correction minimale du bug ...
git add <fichiers_corriges>
git commit -m "fix: <description du correctif>"

# version dans pyproject.toml = 1.0.1 + nouvelle entrée CHANGELOG
git add pyproject.toml CHANGELOG.md
git commit -m "chore(release): bump de version vers 1.0.1"
git push
```

### 3. PR `hotfix/1.0.1` → `main`, merge --no-ff, tag, release

```bash
gh pr create --base main --head hotfix/1.0.1 \
  --title "Hotfix 1.0.1" \
  --label hotfix \
  --body "Correctif urgent : <résumé>."
gh pr checks
gh pr merge <numéro> --merge

git checkout main
git pull origin main
git tag -a v1.0.1 -m "Hotfix 1.0.1 — <résumé>"
git push origin v1.0.1
gh release create v1.0.1 --title "v1.0.1" --generate-notes
```

### 4. Back-merge dans `develop`

```bash
gh pr create --base develop --head hotfix/1.0.1 \
  --title "Back-merge hotfix/1.0.1 dans develop" \
  --label hotfix \
  --body "Réintégration du correctif dans develop."
gh pr merge <numéro> --merge
```

> **Si une release est en cours** (ex : `release/1.1.0` existe) : merger le hotfix
> **aussi** dans la branche de release en cours (PR `hotfix/1.0.1` → `release/1.1.0`)
> AVANT de supprimer la branche de hotfix.

### 5. Supprimer la branche de hotfix

```bash
git branch -d hotfix/1.0.1
git push origin --delete hotfix/1.0.1
```

---

## ✅ Checklist finale de chaque release / hotfix

- [ ] merge **--no-ff** dans `main` (via PR « Create a merge commit »)
- [ ] tag **annoté** `vX.Y.Z` posé sur `main` et poussé
- [ ] GitHub Release créée (`gh release create`)
- [ ] back-merge dans `develop` (via PR)
- [ ] (hotfix) back-merge dans la release en cours si elle existe
- [ ] branche release/hotfix supprimée (locale **et** distante)
- [ ] CI verte sur `main` et `develop` après coup
