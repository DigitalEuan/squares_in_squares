# REPRODUCE.md — exact reproduction guide

Everything runs from the repository root (`my-project/`). Python 3.12
with numpy + sympy; node (or bun) with the `docx` package for the report
step. Total time for the offline verification chain: ~15 minutes.

## A. Verify the delivered state (offline, deterministic)

These commands re-verify every shipped artifact exactly as it stands.
Nothing is rebuilt; every check must pass.

```bash
# 0. verifier self-tests (SAT engine, grid packings, overlap detection)
python3 scripts/packlib.py
#    -> "self-tests passed"

# 1. submission.csv round-trip: 500500 rows, ids 0..500499, every packing
#    re-verified from the file on disk, independent score recomputation
python3 scripts/final_assembly.py        # re-reads table, re-writes + re-verifies
python3 scripts/score_submission.py
#    -> SCORE = 22.887471, grid ceiling = 28.937670, overlap failures: none
#    (frontier as of run 10: 448/1000 beat grid; reproduce runs 9+10 first —
#     scripts/gobel2.py then scripts/gobel3.py + propagation (cascade3,
#     closure_apply) + final_assembly — to regenerate that frontier)

# 2. Golay code + Leech lattice: 28 assertions, integer-exact (~4 min)
python3 scripts/leech_core.py
#    -> "SUMMARY: 28/28 VERIFIED"; writes download/leech_core.json

# 3. octad calculus: 14 assertions (~1 min)
python3 scripts/octad_moves.py
#    -> "SUMMARY: 14/14 VERIFIED"; writes download/octad_moves.json

# 4. grid → number-field → laminated-tower mapping (needs 1-3's outputs)
python3 scripts/leech_map.py
#    -> coverage 870/1000 = 87.0%; spearman(level, improvement) = +0.79

# 5. rotated-block program: full 7-angle sweep + certificate census
python3 scripts/theta225_push.py
#    -> 271 verified members; certificates 54 -> 280;
#       Level-0: 130 puzzles, 10 reachable by the family, 0 converted;
#       extended range: 29 candidates past the bound gate, 0 improvements
#    writes download/run5_push.json, theta_quartic_members.json

# 6. figures (English labels)
python3 scripts/figures.py     # -> "ALL 5 FIGURES OK", download/fig/*.png
```

Expected invariant: steps 1 and 5 leave `table.json`, `submission.csv`
and the score unchanged (22.887471, the run-10 frontier) — the pipeline
is idempotent at the delivered frontier. To rebuild the frontier itself
(not just re-verify it), run in order after the self-tests:
scripts/gobel2.py (run 9), scripts/gobel3.py (run 10 wave A),
scripts/cascade3.py + scripts/closure_apply.py (propagation to
fixpoint), then final_assembly.py again.

## A2. Run 11 precision architecture (map + certificates)

```bash
python3 scripts/leech_map.py          # re-architected map on the frontier
python3 scripts/angle_first.py        # Stage-A angle inventory + controls
python3 scripts/cert_extend.py        # 889 new certificates (idempotent-safe:
                                      # truncate galois_certificates.json to
                                      # 280 first if re-running)
# Lean (the reverse direction; resumable, incremental):
cd workspace/lean/tct_squares && /home/z/.elan/bin/lake build
python3 scripts/cert_repro.py         # uploaded certificate reproduction
```

`## B. Rebuild the mathematical layers from scratch (offline)`

The lattice layer needs nothing but the scripts:

```bash
python3 scripts/leech_core.py     # QR factor search -> Golay -> Leech:
                                  # kissing 196560 = 1104+97152+98304,
                                  # det 1 via |L_raw/8Z^24| = 2^36,
                                  # tower 2/6/12/24/240 (7320 cited),
                                  # projection law (759 octads = the only
                                  # defect locus, d=8)
python3 scripts/octad_moves.py    # Steiner 253/77/21/5/1, octad calculus
                                  # 30/448/280, dist-8 graph (diameter 3),
                                  # covering radius exactly 4
```

Both scripts recompute everything from first principles (no lookup
tables); run them twice and the outputs are byte-identical.

## C. Rebuild the packing pipeline (mostly offline; two web steps)

Historical order (the delivered workspace already contains the outputs
of every step; re-running applies the same idempotent updates):

```bash
python3 scripts/parse_all_svgs.py   # survey SVGs (workspace/svgs) -> records
python3 scripts/parse_kingbird.py   # WEB: live catalogue mirror; needs
                                    # network; caches /tmp/kingbird.json
python3 scripts/level_audit.py      # needs /tmp/kingbird.json from above;
                                    # writes /tmp/level_report.json
python3 scripts/build_table.py      # stores -> table.json
python3 scripts/gobel_squares.py    # Göbel 45° family sweep + apply
python3 scripts/galois_certs.py     # certificates + theta-30 members
                                    # (needs /tmp/level_report.json)
python3 scripts/cascade3.py         # chain3 family (see script header)
python3 scripts/closure_apply.py    # removal closure to fixpoint
python3 scripts/theta_family.py    # 7-angle feasibility map + 45° minimum
python3 scripts/theta225_push.py    # Run 5 final sweep + certificates
python3 scripts/final_assembly.py   # table -> submission.csv + round-trip
```

Notes and honest caveats:

- `parse_kingbird.py` fetches the *live* maintained catalogue mirror; the
  web copy drifts over time. The repo ships the parsed values that were
  current at archive time (4 records with states, embedded in
  extended_table_5000.json as `catalogue:kingbird`).
- `level_audit.py` / `galois_certs.py` have a transient `/tmp` dependency
  (kingbird.json, level_report.json). For a cold start, run them in the
  order shown in section C.
- `scripts/theta225_push.py` reads `download/leech_map.json` (step A.4)
  for the Level-0 list — run leech_map.py first.

## D. The report (English, Run 5 edition)

```bash
python3 scripts/figures.py                 # figures (English labels)
node scripts/gen_report_en.js              # docx (needs `docx` npm package)
python3 skills/docx/scripts/add_toc_placeholders.py \
        "download/Leech_Lattice_and_Square_Packing_Report.docx" --auto
python3 scripts/patch_footers.py           # Roman/arabic footer field patch*
```

\* patch_footers.py targets the Chinese Run-4 edition by default; for the
English report, apply the same PAGE-field patch to
Leech_Lattice_and_Square_Packing_Report.docx (ROMAN front matter, arabic
body) — the shipped PDF already has it.

(The docx skill lives under skills/docx/; if you repackage without it,
skip the add_toc_placeholders step — the TOC then has no placeholder
entries until Word updates the field. scripts/gen_report.js is the
Run-4 Chinese edition, kept for the historical record.)
