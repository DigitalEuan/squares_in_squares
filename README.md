# Squares in Squares — Verified Constructions, Leech-Lattice Analysis, and the Rotated-Block Program

This repository is the complete, reproducible working state of a
Kaggle *Squares in Squares* project (pack n unit squares into a minimal
square container; 1000 puzzles, n = 1..1000; score = Σ(L/√n − 1), lower
is better), extended with a machine-verified Leech-lattice layer and a
fully enumerated rotated-block family program.

## Headline results

| Quantity | Value |
|---|---|
| Submission score | **22.887471** (grid ceiling 28.937670, improvement −6.050199) |
| Puzzles beating the plain grid | 448 / 1000 |
| Certification | 1000/1000 packings SAT-verified + full CSV round-trip |
| Golay/Leech verification | 28/28 + 14/14 assertions, integer-exact (leech_core.py, octad_moves.py) |
| Grid → Leech-level mapping | 87% exact number-field coverage (leech_map.py) |
| Algebraic certificates | 280 (7 angle families × full (a,p) sweeps + survey records) |

## Repository layout

```
scripts/            All pipeline code (Python; one module = one stage).
  packlib.py          THE verifier: SAT non-overlap, bbox, CSV I/O, finalize.
  theta_family.py     Rotated-block family: exact s(θ) formula, feasibility,
                      sweep machinery (7 special angles).
  theta225_push.py    Run 5: full 7-angle re-sweep, certificate collection
                      build (54 → 280), Level-0 gap analysis, extended-range
                      sweep 1001..5000.
  gobel_squares.py    Göbel 45° family (historical entry point).
  galois_certs.py     Galois certificates for construction levels.
  build_table.py, final_assembly.py, score_submission.py
                      Table assembly, submission.csv + round-trip, scoring.
  leech_core.py       Golay code + Leech lattice, tower, projection law
                      (28 verified assertions, exact integer computation).
  octad_moves.py      Octad calculus: Steiner ladder, intersections,
                      distance-8 graph, covering radius (14 assertions).
  leech_map.py        1000 grids → number fields → laminated-tower levels.
  level_audit.py      The audited field-identification standard (2e-8).
  figures.py          The 5 report figures (English labels).
  gen_report.js, patch_footers.py  Report docx generation + post-processing.
workspace/          Data: submission/ (table.json, submission.csv,
  galois_certificates.json, extended_table_5000.json, ...),
  svgs/ (survey SVGs), ledgers, docs, tools. (glm-repo/ is a reference
  clone excluded from the archive.)
download/           Deliverables: submission.csv, table.json, reports,
  figures, verification JSONs. See download/README.md.
```

## The five runs (history)

1. **Engine + survey integration** — cascade search, 235 survey SVGs
   parsed with the survey's own parser, removal windows, partial-fill
   chains: score 28.35 → 23.19.
2. **Göbel families** — full (a,b) sweep applied 18 verified improvements;
   family proven exhausted for n ≤ 1000.
3. **Closure + chains** — removal-closure to fixpoint, chain3 family:
   score 23.173640 (final), 407/1000 beat grid; live-catalogue check
   confirmed we are at the published frontier for n ≤ 1000.
4. **Leech layer** (leech_core.py, octad_moves.py, leech_map.py) — the
   logic of the Golay/Leech system verified exactly; the 1000 grids
   mapped to laminated-tower levels by number field (87% exact);
   Q(√2) alone carries 70% of the total improvement.
5. **Rotated-block program completion** (theta225_push.py) — all 7
   special angles swept over the full (a,p) range: 271 verified members,
   certificates 54 → 280 (including 38 in the nested quartic field
   Q(√(2+√2)) with cyclic C4 Galois group). The hoped-for conversion of
   Level-0 puzzles did NOT materialize: of the 130 unresolved grids, the
   family reaches only 10, and loses to the numeric optimum on every one
   (closest gap 0.004 at n=28). The 45° kink-minimum (proven by sweep)
   and the exhaustion result of Run 2 explain why. No table or score
   change; the deliverable of Run 5 is the certificate collection plus
   the honest negative result.

## Reproducing

See **REPRODUCE.md** for the exact command chain, expected outputs, and
the list of steps that need network access (live catalogue mirrors) or
transient /tmp files.

## Guarantee

Every packing shipped in submission.csv was re-verified from the file as
written on disk (pairwise SAT non-overlap with worst penetration ≤ 0,
bounding-box containment, per-n counts, id continuity 0..500499, 12-dp
round-trip stability with ~2e-9 clearance). Every mathematical claim in
the Leech layer is machine-verified with exact integer computation; no
floats anywhere in the lattice math. Λ16's kissing number 7320 is cited
(SPLAG), not verified — marked as such everywhere it appears.
