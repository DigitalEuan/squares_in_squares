# Squares in Squares — Verified Constructions, Leech-Lattice Analysis, and the Rotated-Block Program

This repository is the complete, reproducible working state of a
Kaggle *Squares in Squares* project (pack n unit squares into a minimal
square container; 1000 puzzles, n = 1..1000; score = Σ(L/√n − 1), lower
is better), extended with a machine-verified Leech-lattice layer and a
fully enumerated rotated-block family program.

## Headline results (Last score move run 13, 2026-11-05)

| Quantity | Value |
|---|---|
| Submission score | **22.823536** (grid ceiling 28.937670, improvement −6.114134) |
| Puzzles beating the plain grid | **454 / 1000** |
| Leaderboard best (reported) | 22.0544214515 → gap **0.769115** |
| Certification | 1000/1000 packings SAT-verified + 500,500-row CSV round-trip (0 issues) |
| Golay/Leech verification | 28/28 + 14/14 assertions, integer-exact |
| Algebraic certificates | 1169 (7 angle families + surveys + run-11 census) |
| Proven-optimal rows | 94 (squares, Nagamochi, + 2026 s(k²−3)=k / s(k²−4)=k families) |

## The score engine (what actually produces improvements)

1. **Source integration** — the survey's 235 record SVGs (20–100 digit
   parse), the Ellsworth catalogue, and — this session — the community's
   certified best-known register (76 records our table lacked; 0.050
   directly, 0.064 with propagation). *Sources beat search, three runs in a
   row.*
2. **Analytic families** — Göbel strip/central-square, the 4-parameter
   diamond+staircase G(a1,a2,b,c) (17 mid-band finds beyond the catalogue),
   the clipped variant G(a1,a2,b,c,t) (5 more).
3. **Exact propagation** — removal closure (prefix-min envelope) +
   L-extension band chains; the residue-diagonal law multiplies every find
   (one base at n₀ opens its whole diagonal n = (K−1)² + c).
4. **The honest gate** — every state, imported or constructed, is
   packlib-verified (SAT non-overlap, bbox containment, 2e-9 clearance,
   12-dp round-trip). Nothing ships unverified.


## Reproducing

See **REPRODUCE.md** for the exact command chain, expected outputs, and
the list of steps that need network access (live catalogue mirrors) or
transient /tmp files.

## Operations 
Each run, update top-level README.md, STATUS.md, NEXT_STEPS.md and REPRODUCE.md all need updating. If possible GLM_INVESTIGATION.md should be upkeep as an overview of the whole study.

## Guarantee

Every packing shipped in submission.csv was re-verified from the file as
written on disk (pairwise SAT non-overlap with worst penetration ≤ 0,
bounding-box containment, per-n counts, id continuity 0..500499, 12-dp
round-trip stability with ~2e-9 clearance). Every mathematical claim in
the Leech layer is machine-verified with exact integer computation; no
floats anywhere in the lattice math. Λ16's kissing number 7320 is cited
(SPLAG), not verified — marked as such everywhere it appears.