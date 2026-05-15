# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**LRV** converts and corrects the digitization of L.R. Vaidya's *Sanskrit-English Dictionary* (1889) into CDSL format. The canonical output lives in `csl-orig/v02/lrv/lrv.txt`.

## Architecture

| Directory | Purpose |
|---|---|
| `scripts/` | Conversion and quality-check pipeline scripts |
| `issues/` | Per-issue correction workflows (`issueNNN/` pattern) |
| `interim/` | Intermediate data files from pipeline stages |
| `glacier/` | Archived/historical data versions |
| `logs/` | Pipeline execution logs |

### Conversion pipeline (`scripts/`)

Multi-stage pipeline with quality-check gates:
1. `lrv_prep1.py` through `lrv_prep5.py` — incremental conversion stages
2. `parseheadline.py` — parses entry headlines into CDSL markup
3. Quality checks: `qc_alternate_headwords.py`, `qc_duplicate_lnum.py`, `qc_duplicate_pc.py`, `qc_hw_k2_diff.py`, `qc_missing_compounds.py`, `qc_unique_headwords.py`
4. `quality_check.sh` — runs all QC scripts and summarizes results
5. `issue12.py`, `issue19.py`, `issue20.py` — issue-specific correction scripts
6. `redo.sh` — full pipeline orchestration
7. `revert_Nto(N-1).py` scripts — roll back specific pipeline stages

### Issue correction pattern (`issues/issueNNN/`)

Standard workflow: copy `lrv.txt`, apply corrections incrementally, rebuild XML, validate, commit to `csl-orig`.

## Common Commands

### Run full conversion pipeline (from `scripts/`)
```bash
sh redo.sh
```

### Quality check (from `scripts/`)
```bash
sh quality_check.sh
```

### Rebuild and validate XML (from `csl-pywork/v02/`)
```bash
sh generate_dict.sh lrv ../../LRVScan/2020
sh xmlchk_xampp.sh lrv
```

## Dependencies

- **Python 3**
- **lrv.txt** — in `$BASE/cologne/csl-orig/v02/lrv/lrv.txt`
