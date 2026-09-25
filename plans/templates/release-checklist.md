# Template: release checklist (owner)

Copy into the release PR description or `memory/HANDOFF.md` and tick every
line. It applies to v0.1 (the first public, résumé-eligible release) and v1.0
(finished). For P0 Nurse Handoff, also follow the gate steps in
[P0](../projects/P0-nurse-handoff.md).

## Content
- [ ] `docs/clinical-spec.md` is final, owner-authored, and versioned
- [ ] All data is synthetic or public; no employer material; no real-patient identifiers
- [ ] Licensed instruments excluded or permission documented (overview licensing table)
- [ ] Every source attributed; MedlinePlus, NINDS and other citations present
- [ ] Canary GUIDs present (NurseBench); held-out split backed up offline

## Evidence
- [ ] Every number in README and results comes from a committed result file
- [ ] Each result records model ID and version, run date, item count and seed
- [ ] Limitations section states what the numbers do not show
- [ ] Grader-based metrics report kappa against owner labels

## Engineering
- [ ] CI green on the release commit
- [ ] Tests pass locally with the documented command
- [ ] Secrets scan clean (`git log -p | Select-String -Pattern 'sk-|api[_-]?key|BEGIN .*PRIVATE'`)
- [ ] README "Run it yourself" steps work from a clean clone

## Repo files
- [ ] README follows the scaffold outline, with a demo GIF or sample output
- [ ] DISCLAIMER.md, LICENSE (Apache-2.0), DATA_LICENSE (CC BY 4.0)
- [ ] CHANGELOG entry for this version

## Release
- [ ] Repo, history and write-up searched for the employer's name and abbreviations; none found
- [ ] `git tag vX.Y.Z` and push the tag; GitHub release notes written from the CHANGELOG
- [ ] Visibility switched from private to public (D-4: public at release)

## After release
- [ ] Hub README projects table updated (status, link, headline result)
- [ ] `plans/PROGRESS.md` milestone ticked, dashboard row updated, session-log row added
- [ ] Résumé line filled from real numbers only
- [ ] Write-up of 600–900 words (at v1.0; a short post at v0.1): the bedside
      problem, what was built, how it was evaluated, one real finding,
      one limitation, a link
