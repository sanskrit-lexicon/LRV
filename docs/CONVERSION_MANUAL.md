# LRV Conversion Pipeline Manual

_Created: 11-07-2026 · Last updated: 11-07-2026_

The operator manual for the LRV conversion pipeline: turning the proofread
OCR transcript of L. R. Vaidya's *Standard Sanskrit-English Dictionary*
(1889) into CDSL markup through five incremental stages
(`interim/lrv_0.txt` → `lrv_5.txt`), verifying each stage with the QC and
reversion scripts, and fixing post-conversion defects through the
`issues/issueNNN/` pattern. Written so a new operator can re-run, verify, or
extend the pipeline without reading the source.

Companion metadoc: [docs/CONVERSION_MANUAL.meta.md](https://github.com/sanskrit-lexicon/LRV/blob/main/docs/CONVERSION_MANUAL.meta.md).

---

## 1. Cheat-sheet — the whole pipeline on one screen

```sh
cd scripts

sh redo.sh             # full conversion: lrv_0 -> lrv_1 -> ... -> lrv_5
sh quality_check.sh    # all qc_*.py defect scans, with per-step "ideal" stated
sh redo_revert.sh      # round-trip check: revert 5->4->3->2->1, diff each
                       #   against the real stage file (ideal: empty diffs)

# downstream, from csl-pywork/v02/ (the central display build, not this repo):
sh generate_dict.sh lrv ../../LRVScan/2020
sh xmlchk_xampp.sh lrv
```

⚠️ `redo.sh` **rewrites the tracked `interim/lrv_1..5.txt` files in place.**
Run it only when you intend to regenerate the pipeline (a prep-script fix, a
correction to `lrv_0.txt`); an accidental run shows up as a large tracked
diff — check `git diff --stat interim/` before committing anything.

## 2. Data-flow diagram

```
glacier/LR_Vaidya_Main_proofed_20220920.txt   (proofread OCR source, TSV,
│      received 20-09-2022 "with compounds properly parsed" — see glacier/README.md)
▼  copy (+3 hand-fixes of stray spaces after <b>, issue #4)
interim/lrv_0.txt      TSV: lnum · pc · headword(deva) ·(alt cols)· #-grammar · $--entry · len
│  lrv_prep1.py        line endings \r\n -> \n
▼
interim/lrv_1.txt
│  lrv_prep2.py        build the <L>/<pc>/<k1>/<k2> metaline; keep key2 +
▼                      grammar + entry text; split multi-headword rows
interim/lrv_2.txt
│  lrv_prep3.py        <ls>...</ls> literary-source markup; // -> <P>
▼
interim/lrv_3.txt
│  lrv_prep4.py        Devanagari -> SLP1 ({#...#} Sanskrit, {%...%} italics)
▼
interim/lrv_4.txt
│  lrv_prep5.py        bracketed alternate headwords out of <k1>; every changed
▼                      metaline logged to interim/change_metalines.json
interim/lrv_5.txt      CDSL-ready output (190,412 lines from 43,598 source lines
│                       — growth is markup, not content)
▼  delivered once to
csl-orig/v02/lrv/lrv.txt   (canonical; all later fixes go through the
                            correction workflow, §5 — never re-delivered wholesale)

VERIFICATION LOOPS:
  scripts/qc_*.py + quality_check.sh   — defect scans over the stage files (§4)
  scripts/revert_Nto(N-1).py + redo_revert.sh
      — inverse transforms into interim/reversion/, diffed against the real
        stage files: proves each stage is information-preserving
```

## 3. Step-by-step: the five stages

Each stage is one Python script, `python3 lrv_prepN.py <in> <out>`, run from
`scripts/` (the orchestration is
[scripts/redo.sh](https://github.com/sanskrit-lexicon/LRV/blob/main/scripts/redo.sh);
per-stage change notes of record are
[interim/README.md](https://github.com/sanskrit-lexicon/LRV/blob/main/interim/README.md)):

| Stage | Script | Transform | Notes |
|---|---|---|---|
| 0 | — (copy) | `glacier/LR_Vaidya_Main_proofed_20220920.txt` → `lrv_0.txt` | + 3 hand-corrections ([issue #4](https://github.com/sanskrit-lexicon/LRV/issues/4)). The file is **TSV**: `lnum · pc · headword · … · #-grammar · $--entry · length` — several scripts (incl. QC) parse it with `csv.reader(delimiter='\t')` |
| 1 | [lrv_prep1.py](https://github.com/sanskrit-lexicon/LRV/blob/main/scripts/lrv_prep1.py) | `\r\n` → `\n` | `diff -Z lrv_0.txt lrv_1.txt` must be empty |
| 2 | [lrv_prep2.py](https://github.com/sanskrit-lexicon/LRV/blob/main/scripts/lrv_prep2.py) | metaline `<L>NNNNN<pc>PPP-CC<k1>…<k2>…` + body line + `<LEND>`; strips `<p>`/`<b>`/`<+>`/`#-`/`$--` working markup; splits rows carrying multiple headwords (`aMSa-hara, aMSa-hArin`) | the structural heart of the conversion; headline parsing shared via [parseheadline.py](https://github.com/sanskrit-lexicon/LRV/blob/main/scripts/parseheadline.py) |
| 3 | [lrv_prep3.py](https://github.com/sanskrit-lexicon/LRV/blob/main/scripts/lrv_prep3.py) | `<ls>…</ls>` around literary-source citations (`/K.S./i.32` style); `//` paragraph breaks → `<P>` | |
| 4 | [lrv_prep4.py](https://github.com/sanskrit-lexicon/LRV/blob/main/scripts/lrv_prep4.py) | Devanāgarī → SLP1 | Sanskrit lands in `{#…#}`, italic grammar labels in `{%…%}` |
| 5 | [lrv_prep5.py](https://github.com/sanskrit-lexicon/LRV/blob/main/scripts/lrv_prep5.py) | bracketed alternates removed from `<k1>` (one canonical headword per entry); **every changed metaline logged to [interim/change_metalines.json](https://github.com/sanskrit-lexicon/LRV/blob/main/interim/change_metalines.json)** | that JSON is the input to [scripts/issue12.py](https://github.com/sanskrit-lexicon/LRV/blob/main/scripts/issue12.py) (alternate-headword baseline `lrv_hwextra.txt`) — don't delete it |

**Re-running from a middle stage** is just invoking that stage's script with
the existing predecessor file — the stages have no hidden state. **Extending
the pipeline** = a new `lrv_prep6.py <lrv_5 in> <lrv_6 out>` + a `redo.sh`
line + an `interim/README.md` section + (ideally) a `revert_6to5.py` — the
per-stage README note is not optional; it is the pipeline's only change log.

## 4. Verification — QC scans and the reversion round-trip

### 4.1 `sh quality_check.sh` — defect scans

Each `qc_*.py` targets one defect class; the driver prints the "ideal"
outcome per step:

| Script | Defect class | Ideal |
|---|---|---|
| [qc_duplicate_pc.py](https://github.com/sanskrit-lexicon/LRV/blob/main/scripts/qc_duplicate_pc.py) | duplicate page-column refs in `lrv_0.txt` | no output |
| [qc_duplicate_lnum.py](https://github.com/sanskrit-lexicon/LRV/blob/main/scripts/qc_duplicate_lnum.py) | duplicate `<L>` numbers | no output |
| [qc_unique_headwords.py](https://github.com/sanskrit-lexicon/LRV/blob/main/scripts/qc_unique_headwords.py) | headwords appearing once (typo suspects) → [logs/issue11/unique_headwords.txt](https://github.com/sanskrit-lexicon/LRV/blob/main/logs/issue11/unique_headwords.txt) | manual review list |
| [qc_hw_k2_diff.py](https://github.com/sanskrit-lexicon/LRV/blob/main/scripts/qc_hw_k2_diff.py) | body headword ≠ `<k2>` sort key | no output |
| [qc_missing_compounds.py](https://github.com/sanskrit-lexicon/LRV/blob/main/scripts/qc_missing_compounds.py) | compound cross-references with no target ([issue #14](https://github.com/sanskrit-lexicon/LRV/issues/14)) | no output |
| [qc_alternate_headwords.py](https://github.com/sanskrit-lexicon/LRV/blob/main/scripts/qc_alternate_headwords.py) | alternate-headword consistency (not in the driver — run directly) | no output |

A non-empty result is a *finding*, not a crash — it seeds a GitHub issue and
then a per-issue fix (§5).

### 4.2 `sh redo_revert.sh` — the information-preservation proof

For stages 2–5 there is an inverse script (`revert_5to4.py` … `revert_2to1.py`)
writing into `interim/reversion/`; the driver diffs each reverted file
against the real stage file. **Empty diffs prove no stage silently loses
data.** Run it after any prep-script change — it is the closest thing the
pipeline has to a test suite, and a new stage should come with its inverse.

## 5. Post-conversion corrections — the `issues/issueNNN/` pattern

The pipeline ran once; the canonical text now lives in
[csl-orig/v02/lrv/lrv.txt](https://github.com/sanskrit-lexicon/csl-orig/blob/main/v02/lrv/lrv.txt),
and **new defects are fixed there, not by re-running the pipeline.** Each
fix gets a folder `issues/issueNNN/` (pattern of record, e.g.
[issues/issue25/](https://github.com/sanskrit-lexicon/LRV/tree/main/issues/issue25),
[issues/markup_fix/](https://github.com/sanskrit-lexicon/LRV/tree/main/issues/markup_fix)):

1. pin the input: `git show <commit>:v02/lrv/lrv.txt > temp_lrv_0.txt`
   (issue25's readme records the exact commit hash it started from — do the
   same);
2. transform incrementally (`temp_lrv_1.txt`, …) with a per-issue script,
   keeping an `updateByLine`-style change log;
3. rebuild + validate XML from `csl-pywork/v02/`
   (`sh generate_dict.sh lrv ../../LRVScan/2020` · `sh xmlchk_xampp.sh lrv`);
4. deliver per the canonical
   [correction workflow](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md)
   — org agents park change files in the correction queue for the batched
   PR; **never commit or push to csl-orig directly** (the direct-commit
   history in old issue folders is the upstream-maintainer pattern).
5. helper scripts that graduate to reusable status move to `scripts/`
   (`issue12.py`, `issue19.py`, `issue20.py`), with their outputs under
   `logs/issueNN/` — that is the issues/logs convention: `issues/` holds the
   fix workspace, `logs/` holds durable script outputs keyed by the same
   issue number.

## 6. Environment & prerequisites

- **Python 3** + `sh` (Git Bash on Windows); stdlib only — no pip installs.
- Scripts assume they run **from inside `scripts/`** (all paths are
  `../interim/...`-relative).
- The per-issue workflows additionally expect the maintainer XAMPP layout
  (`csl-orig`, `csl-pywork`, `LRVScan` as siblings under
  `/c/xampp/htdocs/...`) — for the org layout substitute your local clone
  paths; only steps 3–4 of §5 touch them.
- Scans for QC context: the HathiTrust digitized copy
  ([catalog record](https://catalog.hathitrust.org/Record/008693928)); the
  display build uses `LRVScan/2020` page images.

## 7. Symptom → cause → cure

| Symptom | Cause | Cure |
|---|---|---|
| Huge tracked diff under `interim/` after "just looking around" | `redo.sh` was run — it rewrites `lrv_1..5.txt` in place | `git checkout -- interim/` if unintended; re-run deliberately only with a prep-script or `lrv_0` change |
| `redo.sh` output differs from committed `lrv_5.txt` with no script change | Your Python/regex environment differs, or `lrv_0.txt` was touched | Diff stage by stage (`lrv_1` first) to find where divergence starts; the committed stages are the reference |
| `redo_revert.sh` prints diffs | A prep script lost or mutated information its inverse can't recover | Fix the prep script (or its inverse if the inverse is stale) before shipping — empty round-trip diffs are the invariant |
| `qc_*.py` crashes with an index error | It parses `lrv_0.txt` as TSV (`csv.reader`, `delimiter='\t'`) — a row lost a column | Fix the malformed row in `lrv_0.txt`; the TSV column contract is §3 stage 0 |
| Fixing a defect by editing `interim/lrv_5.txt` | Wrong layer — lrv_5 was delivered once; the canonical text is csl-orig's `lrv.txt` | Route through `issues/issueNNN/` + the correction workflow (§5) |
| `generate_dict.sh` / `xmlchk_xampp.sh` not found | They live in `csl-pywork/v02/`, not this repo | Run from that repo with `lrv` as argument (§6 layout note) |
| Deleted `interim/change_metalines.json` "as a temp file" | It is stage 5's durable log and `issue12.py`'s input | Restore from git; treat it as a tracked artifact |
| Mojibake `�` characters in an issue-folder byte count | Old issue readmes note them — encoding damage in a pinned historical copy, already handled downstream | Informational; don't "fix" pinned historical inputs |

## 8. Glossary

| Term | Meaning |
|---|---|
| glacier | The frozen proofread deliveries from the keyboarding vendor (2020/2022) — never edited, only copied from |
| interim | The five staged pipeline outputs; tracked so every transform is diffable |
| metaline | `<L>NNNNN<pc>PPP-CC<k1>…<k2>…` — entry id, page-column of the 1889 print, headword, sort key |
| `pc` | page-column reference (`001-01` = page 1, column 1) linking an entry to its scan page |
| `{#…#}` / `{%…%}` | SLP1 Sanskrit / italic display text — standard CDSL body markup |
| `<ls>` | Literary-source citation markup (`/K.S./i.32` → tagged source ref) |
| `#-` / `$--` | lrv_0's working prefixes for the grammar cell and the entry-body cell of the source TSV |
| alternate headword | A bracketed variant spelling in the source headword; stage 5 moves it out of `<k1>` (log: `change_metalines.json`) |
| reversion | The inverse-transform round-trip (§4.2) proving stages are information-preserving |
| issueNNN pattern | Pinned-input, incremental, XML-validated per-defect fix workspace (§5) |

## 9. Maintainer appendix

- **Invariants:** `glacier/` is read-only history; every stage transform is
  documented in `interim/README.md` in the same change; the reversion
  round-trip stays empty-diff; `change_metalines.json` is a tracked
  artifact; post-delivery fixes never bypass the csl-orig correction
  workflow.
- **Script inventory:** 5 prep + 4 revert + 6 QC + `parseheadline.py`
  (shared metaline parser — the same helper family seen in VCP/csl-inflect)
  + 3 graduated issue scripts + 3 shell drivers. All Python-3 stdlib,
  `codecs`-based UTF-8.
- **Observed quirks** (11-07-2026, while writing this manual): (1) the QC
  scripts hardcode their inputs (`../interim/lrv_0.txt` etc.) rather than
  taking argv like the prep scripts — fine for the driver, surprising when
  run ad hoc from elsewhere; (2) `qc_alternate_headwords.py` is not wired
  into `quality_check.sh` — run it directly; (3) there is no
  `revert_1to0.py` (stage 1 is only a line-ending change; `diff -Z` is its
  check); (4) the issue25 readme carries mojibake byte-count lines — damage
  in a pinned historical note, not in live data.
- **What "extend the pipeline" really means in practice:** post-delivery,
  batch transforms happen against csl-orig's `lrv.txt` in an issue folder
  (the `markup_fix/` folder — a port of PWG issue174's fixer, with synthetic
  tests — is the modern template), NOT as a stage 6; a stage 6 only makes
  sense if the whole dictionary is ever re-delivered from a new proofread
  source.
- **Issue taxonomy:** dictionary-repo taxonomy — see
  [CLAUDE.md](https://github.com/sanskrit-lexicon/LRV/blob/main/CLAUDE.md);
  QC findings become issues, issues become `issues/issueNNN/` folders,
  durable outputs land in `logs/issueNN/`.

---

_Dr. Mārcis Gasūns_
