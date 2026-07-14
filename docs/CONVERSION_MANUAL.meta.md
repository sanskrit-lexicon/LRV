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
[H510-Fable_LRV_conversion_pipeline_manual_10.07.26](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H510-Fable_LRV_conversion_pipeline_manual_10.07.26.md)
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

---

_Dr. Mārcis Gasūns_
