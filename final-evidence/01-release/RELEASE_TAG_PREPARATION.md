# Release Tag Preparation (NOT EXECUTED)

No tag has been created and no commit SHA exists. Run only after every finding in `docs/PHASE3_CERTIFICATION_FINDINGS.md` is resolved and re-validated.

```bash
# 1. all corrections, reports and evidence committed; working tree clean
git status
# 2. record versions
python scripts/certification/run_phase3_checks.py --regen --out final-evidence/06-intelligence-contract/contract_check.json   # must be 0 failures
# 3. commit, then capture the SHA into docs/PHASE3_RELEASE_MANIFEST.md and commit that too
git add . && git commit -m "Complete Phase 3 Data Science and Decision Intelligence"
git rev-parse HEAD                       # certified commit SHA -> manifest
# 4. generate the FINAL Repomix only now (guide section 30); commit it if it is part of the repo
npx repomix --output repomix-phase3-final.md
# 5. tag the certified commit (the commit whose SHA is in the manifest) and push
git tag -a phase3-v1.0.0 -m "Phase 3 certified release"
git push origin main && git push origin phase3-v1.0.0
```
Order matters: if the manifest or Repomix is committed after the SHA is recorded, the manifest must name that final commit and the tag must point to it.
