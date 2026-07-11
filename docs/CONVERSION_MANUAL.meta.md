# CONVERSION_MANUAL.md — metadoc

_Created: 11-07-2026 · Last updated: 11-07-2026_

Companion record for
[docs/CONVERSION_MANUAL.md](https://github.com/sanskrit-lexicon/LRV/blob/main/docs/CONVERSION_MANUAL.md).

## Purpose

The operator manual for the LRV OCR→CDSL conversion: the five prep stages,
the QC scans, the reversion round-trip proof, and the post-delivery
`issues/issueNNN/` correction pattern — how to re-run, verify, and extend
without reading the source.

## Audience

- An operator re-running or partially re-running the pipeline after a
  prep-script fix.
- A contributor turning a QC finding into an issue-folder fix.
- A maintainer deciding whether a change is a pipeline stage or a
  post-delivery correction (§9's distinction).

## Provenance

Authored 11-07-2026 by Fable 5 (`claude-fable-5`) under handoff
[H510-Fable_LRV_conversion_pipeline_manual_10.07.26](https://github.com/gasyoun/Uprava/blob/main/handoffs/H510-Fable_LRV_conversion_pipeline_manual_10.07.26.md)
(the H501–H531 per-repo manuals programme, Litpam-Indexator MANUAL.md gold
standard). Commands and formats read from `scripts/redo.sh`,
`quality_check.sh`, `redo_revert.sh`, the prep/QC script docstrings,
`interim/README.md`, `glacier/README.md`, and the issue25/markup_fix
readmes — none invented.

## Ranked improvement backlog

| # | Item | Status |
|---|---|---|
| 1 | Wire [qc_alternate_headwords.py](https://github.com/sanskrit-lexicon/LRV/blob/main/scripts/qc_alternate_headwords.py) into `quality_check.sh` (currently manual-only) | open |
| 2 | Give the QC scripts argv inputs (they hardcode `../interim/…` paths) so they run from anywhere | open |
| 3 | A guard on `redo.sh` (confirm-or-flag) — it silently rewrites five tracked files | open |
| 4 | CI: run `quality_check.sh` + `redo_revert.sh` on PRs touching `scripts/` or `interim/` | open |
| 5 | Clean the mojibake lines in the issue25 readme (annotate, don't alter pinned data) | open |

## Known limitations

- The internals of the `<ls>` citation grammar (stage 3's pattern set) are
  not decoded pattern-by-pattern; the script is the reference.
- The csl-pywork display build (`generate_dict.sh`/`xmlchk_xampp.sh`) is
  documented only as an interface — its own docs live with csl-pywork.
- The manual describes the maintainer XAMPP path convention as-is; org
  clones substitute their own layout.

## Intended use / known misuse

**For:** re-running or partially re-running the LRV `interim/lrv_0.txt` →
`lrv_5.txt` pipeline after a prep-script fix; verifying a re-run with
`quality_check.sh`/`redo_revert.sh`; onboarding a new operator or
contributor without them reading `scripts/lrv_prep*.py` line by line;
scoping a post-conversion defect fix into the `issues/issueNNN/` pattern;
deciding whether a change belongs in the pipeline (a new `lrv_prep6.py`
stage) or in a post-delivery issue folder (§9's distinction).

**Known/likely misuse:**
- Treating `interim/lrv_5.txt` as the editable canonical text — it was
  delivered once; the live text is
  [csl-orig/v02/lrv/lrv.txt](https://github.com/sanskrit-lexicon/csl-orig/blob/master/v02/lrv/lrv.txt)
  and all further fixes go through §5, never a re-run of the pipeline (§7
  table, row 5).
- Running `redo.sh` "just to look" — it rewrites the five tracked
  `interim/lrv_1..5.txt` files in place with no confirm-or-flag guard
  (backlog item 3); an accidental run shows up as a large uncommitted diff.
- Assuming the QC scripts (`qc_*.py`) take a path argument — they hardcode
  `../interim/...` and only run correctly from inside `scripts/` (§9
  observed quirks, backlog item 2).
- Reading the manual as a decoded specification of the `<ls>` citation
  grammar or the Devanāgarī→SLP1 mapping — both are documented only as
  "the script is the reference" (Known limitations); the manual is an
  operator's guide to running and verifying the pipeline, not a formal
  grammar of its transforms.
- Using the maintainer XAMPP path convention (§6) literally in an org clone
  instead of substituting local layout — only §5 steps 3–4 (display-build
  validation) touch that layout at all.

## Maintenance & sunset plan

The subject document tracks the `LRV` repo's `scripts/` + `interim/`
pipeline directly — it is kept alive by whoever next changes a
`lrv_prepN.py`/`revert_Nto(N-1).py` script or the `issues/issueNNN/`
convention, per the [CLAUDE.md](https://github.com/sanskrit-lexicon/LRV/blob/main/CLAUDE.md)
session-state protocol; there is no separate owning pipeline or service.
A human (currently Dr. Mārcis Gasūns) is the final maintainer of record for
the `sanskrit-lexicon` org's per-repo manuals programme
([H501–H531](https://github.com/gasyoun/Uprava/blob/main/handoffs/H510-Fable_LRV_conversion_pipeline_manual_10.07.26.md)).
"Archived/ended" for this document means: the LRV conversion pipeline is
fully retired (the dictionary will never be re-delivered from a new
proofread source, per §9's "what extend really means") AND all
post-conversion correction activity has migrated to a successor convention
— at that point this manual moves to an `archive/` or historical-reference
state rather than being deleted, since it remains the record of how
`csl-orig/v02/lrv/lrv.txt` was produced.

## Deprecation status

`active`

## Related documents

- [README.md](https://github.com/sanskrit-lexicon/LRV/blob/main/README.md) — repo overview with the stage table + verified output sample
- [interim/README.md](https://github.com/sanskrit-lexicon/LRV/blob/main/interim/README.md) — per-stage change notes of record
- [glacier/README.md](https://github.com/sanskrit-lexicon/LRV/blob/main/glacier/README.md) — proofread-delivery provenance
- [CLAUDE.md](https://github.com/sanskrit-lexicon/LRV/blob/main/CLAUDE.md) — repo guide + issue taxonomy
- [csl-corrections correction workflow](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md) — the canonical delivery path for post-conversion fixes

## Revision history

| Date | Change | By |
|---|---|---|
| 11-07-2026 | Initial version (H510) | Fable 5 (`claude-fable-5`) |
| 11-07-2026 | template v2 backfill (H663) | Sonnet 5 (`claude-sonnet-5`) |

---

_Dr. Mārcis Gasūns_
