<!-- PR vers `develop` (features) — règles détaillées : CONTRIBUTING.md -->

## Description

<!-- Que fait cette PR ? Quelle issue ? -->

Closes #

## Ordre de fusion (1 → 2 → 3 → 4)

- [ ] Cette PR porte le bon label `merge-order-n` (1 = données/EDA, 2 = baselines,
      3 = deep learning, 4 = évaluation/app/rapport)
- [ ] La PR d'ordre inférieur (n−1) est **déjà fusionnée** (sauf pour n = 1)

## Type de changement

- [ ] `feat` — nouvelle fonctionnalité
- [ ] `fix` — correction de bug
- [ ] `docs` — documentation
- [ ] `test` — tests
- [ ] `refactor` / `chore` — maintenance

## Checklist (la PR est prête quand tout est coché)

- [ ] CI verte (`ruff check .` + `pytest`)
- [ ] Branche à jour avec `develop`
- [ ] Au moins **1 approbation** d'un autre membre (l'auteur ne peut pas approuver sa
      propre PR)
- [ ] Toutes les conversations de review sont **résolues**
- [ ] Commits suivant les Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`,
      `refactor:`, `chore:`)
- [ ] Tests ajoutés/mis à jour pour tout nouveau code (pas de données brutes dans les
      tests : jeux synthétiques uniquement)
- [ ] `docs/architecture.md` mis à jour si le contrat d'interface a évolué
- [ ] `CHANGELOG.md` mis à jour si pertinent
