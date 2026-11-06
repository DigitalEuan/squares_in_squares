# NEXT_STEPS.md — where the remaining 0.766 lives and how to get it

Companion to `STATUS.md`. Everything below is measured on the delivered
table (**Run 26, score 22.819978**, 454/1000 beat grid) with
`scripts/gap_analysis.py` and the diagonal census; nothing here is
aspirational without a number attached.

---

## 0. Execution status of this plan (updated Run 26, 2026-11-06)

Runs 14–26 executed this plan. Measured outcomes, per item:

| item | status | measured result |
|---|---|---|
| **P1(a)** strip + generalized Göbel (w∈{1,2,3}, two independent staircases) | **CLOSED (Run 25)** | built EXACTLY from a closed-form decode of the imported members (L(a,w)=a+1+w/√2); 88/88 designs finalize-verified; the family is DOMINATED by the table on every row n≤1000 (full-range check: table strictly deeper at 950 rows, equal at the rest, 0 finds); acceptance 44/58/31 FAILS by capacity (ceilings 38/52/27 squares — short by 6/6/4). The community "exact:square-N.svg" rows ARE this family. |
| **P1(b)** two-block / block+slab ((K−2)×(K−1) body + 45° corner block) | **CLOSED (Run 26)** | exact family: 45° m×m corner block, lower-left face on x+y=D, maximal integer-lattice fill; L=(D+(3/2)√2·m)/2, n=m²+\|cells\|; 763 designs enumerated, pointwise DOMINATED by plain grid capacity at the same L (0 designs beat grid, min gap 0 at one tie); acceptance FAILS by capacity (ceilings 36/49/25). |
| **P1(c)** axis-aligned dominant + tilted seams | **CLOSED as a family (Run 26)** | census of all 454 sub-grid rows: 314 strip-45 (P1(a)), 31 Pythagorean-exact, 109 drifted. The blob rows are isostatic hand-polished arrangements on rational lattices (n=50 decoded exactly: L=53/7, angle arctan(3/4), tilted centers on 1/50, axis grid at 2/7 mod 1, 105 contacts, K²+1 signature) — NOT a parametric family. The decode→closed-form→sweep method does not transfer; the follow-up is the blob-regime insertion campaign (P2-bis below). |
| **P2** motif-seeded numerical polish | **DONE (Runs 23–25)** | full designed sweep 52/52 cells (26 rows × 2 targets): 0 hard checks, 0 finds with BOTH random seeds (run 23) and family seeds (runs 24–25). These rows are jammed at their family geometry at targets grid−0.0005/grid−0.002. |
| **P3** source watch | **LIVE (paid this run)** | Run 26: T-263 s(299)≤17.8012385339790622 (jlevy/squares #893, Nov 3 2026; finder Daniel, improver Özden) fetched from the retained packet, exact-rational verify (0 penetration, L=side exactly), APPLIED: row gain 0.0012513. The weekly watch is the highest-EV item in this plan — it produced the only score gain of runs 14–26. |
| **P4** root conversions | **standing** | the T-263 import propagated via cascade3 to n=334, 371 (chain, +0.000273); the chain correctly stops where gobel2 designs are deeper (410, 453, 498). |
| **P5** certification completeness | **open** | unchanged (Lean build, exact replays) |

**P1 is now fully closed** — all three named architectures were built
exactly, measured, and dominated. The remaining paths are: sources (P3),
the blob-regime insertion campaign (P2-bis), and certification (P5).

## 1. The gap, decomposed

| | score | note |
|---|---|---|
| our submission (Run 26) | 22.819978 | 454/1000 beat grid |
| leaderboard best (reported) | 22.0544214515 | |
| gap | **0.765556** | |

Closed since Run 13 (measured):

| push | gain |
|---|---|
| import 76 community best-known packings (n ≤ 324) | 0.050264 |
| chain propagation from those records (33 conversions) | 0.013671 |
| T-263 s(299) import + cascade (Run 26) | 0.003559 |
| **total closed** | **0.067494** |

**Where the remaining ~0.76 must be:** the register now moves above
n=324 too (T-263 is a 299; Deotte's fault-DP seeds s(334) directly) —
the mid-band 325..1000 is no longer beyond the published frontier, it
is at its edge. The tie structure (measured on the Run-26 table):

| band | tied rows | area headroom Σ(K−√n)/√n |
|---|---|---|
| n ≤ 324 | 174 | 4.96 (famous open problems) |
| n > 324 | 372 | 4.06 |
| **total** | **546** | **9.02** |

A uniform depth d\* = 0.028 below grid on every open row matches the
leader (leader uses 8.5% of the theoretical ceiling).

## 2. The frontier is organized in residue diagonals (the leverage map)

Unchanged (the chain law and the diagonal structure stand). The
c=10 diagonal (299, 334, 371, 410, 453, 498 … 993) is now a live
example: T-263 at the root converted 2 members by chain; the tail
(810, 869, 930, 993) is still AT GRID — the deepest untapped chain
reach in the table. A second T-263-class record at any of those four
n converts them all by the chain law.

## 3. Failure → requirement (updated with runs 14–26)

Items 1–7 of the original list stand. Three additions from the
closures:

8. **P1(a)/(b) dominated pointwise** (runs 25–26) → confirmed: any
   single-family architecture with a rigid parametrization is dominated
   by the grid at equal L; the sub-grid records live in the blob regime.
9. **The blob records are isostatic, not parametric** (Run 26 census) →
   the method that closed P1(a) (decode → closed form → sweep) does
   not transfer; blob rows need search seeded from the records
   themselves (insertion at fixed L), or new sources.
10. **Sources move weekly now** (T-258 Oct 26 → T-263 Nov 4) → the
    watch must run weekly; each record is worth ~0.0013/row plus chain.

## 4. Prioritized pushes (updated)

### P1 — CLOSED (see §0). Replaced by:

### P1' — blob-regime insertion campaign (the renamed P2-bis)

The 140 blob rows (31 Pythagorean-exact + 109 drifted) are hand-polished
isostatic arrangements. The record-holders' method (fault-line DP,
refill generations, exact descent — visible in the T-258→T-263 history)
transfers to us as: seed from an existing record state, insert one
square at fixed L, pressure-settle, exact-descent. First targets: the
at-grid c=10 tail (810, 869, 930, 993) seeded from the T-263 state at
L=17.80…+h; acceptance = any row below grid.

### P2 — DONE (52/52 cells, 0 finds; rows jammed at family geometry)

Renewal only if P1' produces a new near-miss map worth polishing.

### P3 — source watch (weekly; the only item that paid in runs 14–26)

- `import_atlas.py` weekly (idempotent).
- The register (jlevy/squares) now moves above n=324: watch issues for
  T-numbers ≥ 263, the `packing/frontier/*.md` files, and the Deotte
  fault-DP line (s(334) seed → 334, 371 …).
- Verified lower bounds (Hosono 2026 etc.) keep pruning the target set.

### P4 — root conversions (standing; mandatory after every table change)

cascade3 + closure_apply to fixpoint, then final_assembly. Run 26's
order is the template: import → cascade3 (2 conversions) →
closure_apply (0) → final_assembly (score 22.819978) → download sync.

### P5 — certification completeness (open; ledger, not score)

Unchanged: Lean `lake build`, exact-algebraic replays of imported
states (T-263 is already exact-rational — replay it in `Fraction`
arithmetic as the community's verifier does), the run-12 Q(√2) family
certificate.

## 5. Value ladder (updated)

| action | score value |
|---|---|
| one imported record at depth d (no cascade) | d/√n |
| one root record at depth d on a diagonal with m tied members | ≈ d · Σ(1/√m) |
| the T-263 import (d=0.0216 at n=299, 2 chain members) | 0.003559 (measured) |
| depth 0.028 uniform over the 546 open rows | **0.765556 (the whole gap)** |
| all open rows at the area bound | 9.02 (theoretical ceiling) |
| the leader's standing | 8.5% of the theoretical ceiling |

## 6. What was executed (runs 14–26), measured

1. **Run 24–25**: NEXT_STEPS P1(a) + P2 executed as designed (see §0).
2. **Run 26**: P1(b) closed by domination; P1(c) closed as a census +
   decode (blob regime); P3 paid: T-263 imported exactly, +0.003559
   with chain; fixpoint confirmed; score 22.823536149 → **22.819978**.

Score 22.823536149 → **22.819978** (−0.003559); beats-grid 454 (new
members 334, 371 are sub-grid); submission.csv rebuilt and round-trip
verified (0 issues, 1000/1000 rows re-verified independently).
