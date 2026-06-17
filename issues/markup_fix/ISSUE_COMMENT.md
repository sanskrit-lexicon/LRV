### Location

Counterpart of https://github.com/sanskrit-lexicon/PWG/issues/175 (PWG) and https://github.com/sanskrit-lexicon/PWK/issues/113 (PWK) for `lrv.txt`.

I ran the same two-job recipe over `csl-orig/v02/lrv/lrv.txt`: auto-fix the few things with a single safe resolution; audit everything else with line refs. Added `08_markup_fix.py` plus outputs to a new `issues/markup_fix/` folder on the branch `markup-fix-audit`.

@funderburkjim @Andhrabharati — please review the findings listed below.

## Markup fixer + audit for `lrv.txt`

### What it auto-fixes

| Pattern | Result |
|---|---|
| `<ab><ab>X</ab> Y</ab>` | `<ab>X Y</ab>` |
| `<ls> word </ls>` | `<ls>word</ls>` |
| `<i> word </i>` | `<i>word</i>` |

Whitespace trimming applies to all 2 paired tag(s) in `lrv.txt`: `<ls>`, `<i>`. The original file is never modified — output goes to `lrv_fixed.txt`, with the full diff in `markup_fix_changes.txt` (updateByLine format). **Output is byte-identical to source** (no auto-fixes triggered).

### Closing-tag inventory in current `lrv.txt`

| Tag | Count |
|---|---:|
| `</ls>` | 16 |
| `</650)>` | ? |
| `</i>` | 2 |
| `</707)>` | ? |

### What it found in current `lrv.txt`

- 0 whitespace trims — byte-identical to source.
- 10 `{#…#}` closing braces immediately followed by `<ab>` or `<ls>` — likely missing space after `#}`. Each is a potential markup boundary collision. Listed in `markup_audit.txt` with line refs.
- 0 adjacent `</ab> <ab>` — no `<ab>` tag in lrv.txt.
- 23 `{{old → new || …}}` correction records present.

### Usage

```
cd issues/markup_fix
python 08_markup_fix.py                        # uses csl-orig/v02/lrv/lrv.txt by default
python 08_markup_fix.py IN.txt OUT.txt         # custom paths
```

Outputs: `lrv_fixed.txt`, `markup_fix_changes.txt`, `markup_audit.txt`.

### Summary

10 {#...#}<ab|ls> boundary collisions — the notable finding.

### Severity

`minor`
