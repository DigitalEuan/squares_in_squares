# NEXT_STEPS.md — where the remaining 0.766 lives and how to get it

Companion to `STATUS.md`. Everything below is measured on the delivered
table (**Run 27, score 22.819978**, 454/1000 beat grid; fixpoint
re-confirmed this run) with `scripts/gap_analysis.py`,
`scripts/root_audit.py` (new, run 27) and the diagonal census; nothing
here is aspirational without a number attached.

---

## 0. Execution status of this plan (updated Run 27, 2026-11-06)

Runs 14–27 executed this plan. Measured outcomes, per item:

| item | status | measured result |
|---|---|---|
| **P1(a)** strip + generalized Göbel | **CLOSED (Run 25)** | exact closed-form family (L(a,w)=a+1+w/√2); 88/88 designs verified; dominated by the table on every row (0 finds); acceptance 44/58/31 fails by capacity (ceilings 38/52/27). |
| **P1(b)** two-block / block+slab | **CLOSED (Run 26)** | 45° m×m corner block + integer-lattice fill, L=(D+(3/2)√2·m)/2; 763 designs, pointwise grid-dominated (0 beat grid at equal L); acceptance fails by capacity (36/49/25). |
| **P1(c)** axis-aligned dominant + tilted seams | **CLOSED as a family (Run 26)** | census: 314 strip-45, 31 Pythagorean-exact, 109 drifted; n=50 decoded exactly (L=53/7, arctan(3/4), 1/50 lattice, 105 contacts, K²+1). The blob rows are isostatic hand-polished, not parametric; follow-up = P1'. |
| **P2** motif-seeded numerical polish | **DONE (Runs 23–25)** | 52/52 cells swept, 0 finds (random + family seeds); rows jammed at family geometry. Renew only if P1' yields a new near-miss map. |
| **P3** source watch | **LIVE (paid runs 22+26)** | Run 26: T-263 s(299)≤17.8012385339790622 imported exactly (+0.003559 with chain). Run 27: register re-checked — no new records; **4 optimality theorems + individual proofs absorbed into the instrument** (see §2). |
| **P4** root conversions | **INSTRUMENTED (Run 27)** | standing channel re-run (cascade 0, closure 0 — fixpoint true); `scripts/root_audit.py` built and run: the leverage map, corrected (below). Two documentation errors from run 26 fixed (§2). |
| **P5** certification completeness | **open** | unchanged (Lean build, exact replays). |

## 1. The gap, decomposed

| | score | note |
|---|---|---|
| our submission (Run 27) | 22.819978 | 454/1000 beat grid |
| leaderboard best (reported) | 22.0544214515 | |
| gap | **0.765556** | |

Closed since Run 13 (measured):

| push | gain |
|---|---|
| import 76 community best-known packings (n ≤ 324) | 0.050264 |
| chain propagation from those records (33 conversions) | 0.013671 |
| T-263 s(299) import + cascade (Run 26) | 0.003559 |
| **total closed** | **0.067494** |

**Where the remaining 0.766 lives (measured, run 27):** the register's
entire result set spans n = 5..308 — **zero upper bounds exist above
n = 324** (the run-26 statement "the register now moves above n=324"
was wrong: T-263 is a 299, inside the classic range). The mid-band
325..1000 remains beyond the published frontier; the watch must keep
probing for it.

The tie structure, corrected by the proven-floor split:

| | rows | note |
|---|---|---|
| tied rows (L = grid) | 546 | |
| — of which **proven floors** (can never improve) | 152 | perfect squares (area bound), s(k²−1)=k [T-084], s(k²−2)=k [T-086], s(k²−3)=k [T-064], s(k²−4)=k [T-081], plus individuals: s(11), s(12)=4, s(13)=4, s(21)=5, s(32)=6, s(44)=7 [T-252], s(45)=7, s(46)=7, s(59)=8, s(60)=8, s(61)=8, s(76)=9, s(77)=s(78)=9, s(95)=s(96)=10, s(2..5) |
| — **open rows** (the attackable set) | **394** | all at r = 2K−1−c ≥ 5; area room 6.662 |

A uniform depth **d\* = 0.0382** below grid on the 394 open rows
matches the leader (equivalently 0.028 over all 546 tied rows — but 152
of those are proven floors that can never move). The leader's standing
is 11.5% of the open rows' theoretical ceiling.

## 2. The leverage map (corrected + instrumented, Run 27)

Two errors in the run-26 edit of this section are corrected here:
(1) the "c=10 live example" listed 453, 498, 810, 869, 930, 993 as
c=10 members — diagonal membership must be computed, not eyeballed;
453 = 21²+12 and 498 = 22²+14 are c=12/c=14, and 810, 869, 930, 993
are members of the fully-open-head diagonals c=26/28/30/32;
(2) "the tail (810…) is the deepest untapped chain reach" — wrong on
both ends: T-263 binds only 299..539 (the chain stops at 410/451 where
gobel2 is deeper), and the far c=10 tail 586..971 is bound by the
community record at 586 (ρ = 1/√2−1 ≈ −0.2929). The corrected c=10
picture: fully sub-grid, 11 roots in a staircase (35, 110, 131, 154,
179, 206, 235, 266, 299, 410, 586), ρ descending 0 → −0.2929.

The instrument (`scripts/root_audit.py`, ledger
`workspace/push/root_audit27.json`) recomputes the whole map from the
table. Its outputs, cross-validated against an independent
reimplementation (totals agree to 1e-6):

**Fixpoint audit:** 0 rows above the chain envelope (no unexploited
conversions — the cascade is at a true fixpoint); 968 rows at/below
envelope; 0 fully-open diagonals remain (the four optimality theorems
prove every diagonal's head).

**Top diagonals by open-row headroom** (identical to the Run-13 table,
now instrument-verified — that table was right all along):

| c | open rows | headroom | best aim (first open row) |
|---|---|---|---|
| 26 | 16 (251 … 926) | 0.274 | 251 (K=16, r=5) |
| 25 | 15 (250 … 866) | 0.272 | 250 (K=16, r=6) |
| 22 | 13 (191 … 647) | 0.265 | 191 (K=14, r=5) |
| 21 | 12 (190 … 597) | 0.261 | 190 (K=14, r=6) |
| 28 | 16 (284 … 989) | 0.251 | 284 (K=17, r=5) |
| 27 | 15 (283 … 988) | 0.249 | 283 (K=17, r=6) |
| 24 | 13 (220 … 985) | 0.239 | 220 (K=15, r=6) |
| 23 | 12 (219 … 984) | 0.235 | 219 (K=15, r=7) |
| 29 | 15 (318 … 990) | 0.229 | 318 (K=18, r=7) |
| 30 | 15 (319 … 991) | 0.215 | 319 (K=18, r=8) |

**Aiming map** (value of one T-263-class record, depth 0.0216, at the
best open row of each diagonal — a record at row m converts every
later member of its diagonal to min(current, chain from m)):

| aim n | K | converts | value |
|---|---|---|---|
| 251 | 16 | 16 rows (251…926) | 0.015569 |
| 250 | 16 | 15 rows (250…866) | 0.014877 |
| 284 | 17 | 16 rows (284…989) | 0.014863 |
| 191 | 14 | 13 rows (191…647) | 0.014854 |
| 283 | 17 | 15 rows (283…988) | 0.014191 |
| 220 | 15 | 13 rows | 0.014069 |
| 190 | 14 | 12 rows | 0.014027 |
| 318 | 18 | 15 rows | 0.013568 |

**Aggregate:** one T-263-class record at every diagonal's best open
aim = **0.4334** (56.6% of the whole gap); at depth 0.01, 0.1989.
Σ(1/√m) over all convertible open rows = 20.07, so d\* = 0.765556 /
20.07 = **0.0382** uniform matches the leader.

The **master keys** remain the r = 5/6 roots (n = K²−5, K²−6): c = 2K−1−r
puts c=26 at r=5 (K=16) and c=25 at r=6 — the same pair the original
plan named, now with the conversions measured. The deepest-root small
open problems (n = 6, 43, 57, 58, 74, 75 …) are single-row diagonals —
worth their d/√n only, no chain reach (values 0.002–0.009).

## 3. Failure → requirement (updated with runs 14–27)

Items 1–10 stand (see run-26 revision). Two additions:

11. **Documentation arithmetic is a failure mode too** (run 27): the
run-26 §2 edit eyeballed diagonal memberships and chain extents, and
got them wrong — 6 rows mislabeled, 1 binding root misattributed, and
a register-range claim invented. Requirement: **every structural claim
in this document must come from a script** (root_audit.py is now that
instrument; rerun it after every table change, like gap_analysis.py).
12. **Proven floors gate the aiming** (run 27): without the four
optimality theorems in the floor set, the instrument aimed at perfect
squares (provably dead) and overcounted the aggregate by 70% (0.736 vs
the true 0.433). Requirement: absorb every new optimality result into
PROVEN_FLOOR immediately — a wrong aiming map wastes the whole
campaign.

## 4. Prioritized pushes (updated Run 27)

### P1' — blob-regime insertion campaign (unchanged; new lead)

Seed from record states, insert one square at fixed L, pressure-settle;
first targets the aiming map's top rows (251, 250, 284, 191 — the
r=5/6 roots of the two biggest diagonals). New lead to read first:
"Structure-Guided Search for Packing Unit Squares in a Square"
(preprints.org, 2026-11-03, registration requests jlevy/squares #799)
— the community's current method paper; it names the structures that
found the recent records.

### P2 — DONE (renew only on a new near-miss map from P1')

### P3 — source watch (weekly; the only item that has paid)

- `import_atlas.py` weekly (idempotent); register frontier files for
  T ≥ 264; the mid-band 325..1000 is still empty upstream — a single
  record there (e.g. at 251/250/284) is worth 0.015 by the map.
- Absorb new **optimality** results into root_audit's PROVEN_FLOOR the
  day they land (they re-cut the aiming map; see §3.12).

### P4 — root conversions (INSTRUMENTED, Run 27; standing)

The original requirement stands and is now enforced by tooling:
whatever produces constructions, aim it at the measured best rows
(§2 aiming map); after any table change re-run the loop
cascade3 → closure_apply → final_assembly (mandatory order), then
`root_audit.py` to refresh the map and check the fixpoint (0 rows
above envelope required). Run 27 state: fixpoint true, score
22.819977568 unchanged, map refreshed, two documentation errors
corrected.

### P5 — certification completeness (open; ledger, not score)

Unchanged: Lean `lake build` (close `cascade_count_symbolic`,
`verification_margin_soundness`); exact Fraction replays of imported
states (T-263 already exact-rational); the run-12 Q(√2) family
certificate.

## 5. Value ladder (updated, measured)

| action | score value |
|---|---|
| one imported record at depth d (no cascade) | d/√n |
| one T-263-class record at 251 / 250 / 284 / 191 | 0.0156 / 0.0149 / 0.0149 / 0.0149 |
| the T-263 import (measured, runs 26) | 0.003559 |
| one T-263-class record at every diagonal's best open aim | **0.4334 (56.6% of the gap)** |
| depth 0.0382 uniform over the 394 open rows | **0.765556 (the whole gap)** |
| all open rows at the area bound | 6.662 (theoretical ceiling) |
| the leader's standing | 11.5% of the theoretical ceiling |

## 6. What was executed (runs 14–27), measured

1. **Runs 14–25**: P2 finished; P1(a) closed by domination; the
   deliverable-name fix (run 25).
2. **Run 26**: P1(b) closed by domination; P1(c) closed as a census +
   decode (blob regime); P3 paid: T-263 imported exactly, +0.003559
   with chain (334, 371); score 22.823536149 → 22.819977568.
3. **Run 27 (this run)**: P4 executed — the standing channel re-run to
   fixpoint (cascade 0, closure 0, score unchanged 22.819977568;
   submission.csv round-trip 0 issues); `root_audit.py` built and run
   (chain-envelope audit: 0 above envelope; proven floors: 156 rows;
   aiming map: 54 diagonals, 394 open rows); two run-26 documentation
   errors found and corrected (§2); the four optimality theorems +
   individual proofs absorbed into the instrument; the register
   re-checked (no new records; max n = 308, zero bounds > 324); the
   aggregate measured (0.4334 at T-263 depth; d\* = 0.0382).

Score 22.823536149 → **22.819977568** (runs 26–27); beats-grid 454;
submission.csv rebuilt and round-trip verified.
