# NEXT_STEPS.md — where the remaining 0.769 lives and how to get it

Companion to `STATUS.md`. Everything below is measured on the delivered
table (Run 13, score 22.823536) with `scripts/gap_analysis.py` and the
diagonal census; nothing here is aspirational without a number attached.

---

## 1. The gap, decomposed

| | score | note |
|---|---|---|
| our submission (Run 13) | 22.823536 | 454/1000 beat grid |
| leaderboard best (reported) | 22.0544214515 | |
| gap | **0.769115** | |

Closed this session (measured):

| push | gain |
|---|---|
| import 76 community best-known packings (n ≤ 324) | 0.050264 |
| chain propagation from those records (33 conversions) | 0.013671 |
| **total closed** | **0.063935** |

**Where the remaining ~0.70 must be:** for n ≤ 324 we are now *exactly* at
the community's certified frontier (`best.json` vs table: 0 rows either
way). The community tracks only n ≤ 324. The Ellsworth catalogue has **one**
record in 325..1000. So the remaining score lives at **n = 325..1000**,
plus the classic open problems at small n — in both cases beyond the
published frontier.

Concretely (area headroom of the tied, non-proven rows):

| band | tied rows | area headroom Σ(K−√n)/√n | leader needs |
|---|---|---|---|
| n ≤ 324 | ~150 | 2.82 (much of it in famous open problems) | some |
| n > 324 | ~255 | 4.02 (per-row cap ≈ 0.026) | most of the 0.769 |
| **total** | **~405** | **6.82** | **11.3% of it** |

Equivalent statement: a uniform depth of **d\* = 0.034** below grid on every
open row matches the leader. That is a small, systematic edge — consistent
with either (a) many modest new packings in the un-searched mid-band, or
(b) better depths on the improved-window rows where our chain tails sit at
0.02–0.05 while the area bound allows 0.3–0.5.

## 2. The frontier is organized in residue diagonals (the leverage map)

Write K = ⌈√n⌉, c = n − (K−1)². The tied rows lie on **54 diagonals**
n = (K−1)² + c; each diagonal is one cascade family. The chain law
(`cascade3`) walks *up* a diagonal from its first construction, at constant
depth. So **a single construction at a diagonal's root converts every tied
member above it** — and the 2026 proofs (s(k²−3)=k, s(k²−4)=k) have cut off
the shallow part of each diagonal, leaving the roots exactly where the open
problems are.

Top diagonals by total headroom (`scripts/gap_analysis.py`, extend with the
diagonal census below):

| c | open members | total headroom | root (K, r) | root headroom |
|---|---|---|---|---|
| 26 | 16 (251 … 926) | 0.274 | 251 (K=16, r=5) | 0.0099 |
| 25 | 15 (250 … 866) | 0.272 | 250 (K=16, r=6) | 0.0119 |
| 22 | 13 (191 … 647) | 0.265 | 191 (K=14, r=5) | 0.0130 |
| 21 | 12 (190 … 597) | 0.261 | 190 (K=14, r=6) | 0.0157 |
| 28 | 16 (284 … 989) | 0.251 | 284 (K=17, r=5) | 0.0088 |
| 8 | 3 (44, 57, 72) | 0.176 | 44 (K=7, r=5) | **0.0553** |
| 3 | 1 (12) | 0.155 | 12 (K=4, r=4) | 0.1547 |
| 9 | 3 (58, 73, 90) | 0.158 | 58 (K=8, r=6) | 0.0505 |
| 6 | 2 (31, 42) | 0.158 | 31 (K=6, r=5) | **0.0776** |
| 12 | 4 (76 … 133) | 0.149 | 76 (K=9, r=5) | 0.0324 |
| 13 | 4 (94 … 157) | 0.140 | 94 (K=10, r=6) | 0.0314 |

Reading of the table:

- The **master keys** are the r = 5/6 rows (n = K²−5, K²−6): they are the
  roots of the long diagonals (c = 2K−1−r). A depth-d construction at a
  root is worth ≈ d × Σ(1/√m) over its diagonal — e.g. n=251 at depth 0.01
  converts 16 rows and is worth ≈ 0.005; n=44 at depth 0.05 converts 3 rows
  *and* deepens 89, 108, 129 … where it beats the current chain values,
  worth ≈ 0.025.
- The **deepest roots** (best d for the effort) are the small ones:
  n=31 (0.078 area), n=44 (0.055), n=58 (0.050), n=76 (0.032), n=94 (0.031).
  These are also the honest open problems of the literature.
- The long diagonals' roots (250, 251, 283, 284 …) have little area room
  (0.007–0.016) but huge reach — small depths are still worth having
  because the chain multiplies them.

## 3. Failure → requirement (the failures name the next design)

This is the analytic core of "what is required to push further":

1. **Relaxation/SA jams at E ~ 1e-2 and fails the positive control even at
   n=5** (whose answer is literally a picture: one 45° square + four
   corners) → required: **motif-level constructions**. Search may only
   polish constructions, never find them.
2. **LP always lands on a rigid grid (s\* = (k−L)/(k−1) exactly)** →
   required: **change of combinatorial type**. No local move crosses the
   wall; the design space must be new shapes, not new starting points.
3. **Mixed 0/45 contacts cost 1+√2/2** → required: **single-angle
   assemblies** (45° blocks and axis-aligned blocks, meeting along clean
   faces).
4. **45° is the kink minimum of s(θ); √3 escalation refuted** → required:
   stay in **Q(√2)/45°** geometry; the walls are structure, not fields.
5. **Pocket-fill is structurally negative (L is monotone in n)** →
   required: **new bases**; the front moves only by construction.
6. **G4 asymmetric-staircase sweep: 0/503 near-miss targets representable
   at s < grid** (Run 13) → required: **a new architecture**. The
   diamond+staircase family is *count-exhausted* in the tied zone: the
   whole class — symmetric or not, clipped or not — cannot express these n
   below the grid. The binding geometry is the staircase-hypotenuse ↔
   diamond-edge contact (they are parallel 45° lines) and the diamond's
   ≤50% area efficiency in its bbox. Anything that wins must have a higher
   density ceiling: e.g. a mostly-axis-aligned body with tilted seams, or
   an attached-strip (Göbel-strip) geometry, not a central diamond.
7. **Sources beat search (three times now: survey SVGs, catalogue, and this
   session's 76-record register import)** → required: **keep the source
   pipeline warm**; the register moves weekly.

## 4. Prioritized pushes

### P1 — New architecture for the tied zone (the named requirement)

The diamond+staircase class is closed (Run 13). Build and sweep a family
with a higher density ceiling. Concrete candidates, in order of promise:

- **(a) staircase + attached 45° strip** (generalized Göbel strip): the
  Göbel strip family already packs n = ⌊a²+a+3+(a−1)√2⌋ at a+1+1/√2 — a
  **depth 0.293** family, far deeper than anything in the tied zone.
  Generalize to strip width w ∈ {1,2,3} and two independent end
  staircases; sweep for n = K²−r, r ∈ [5, K+4]. This is the closest known
  structure to the deep records (n=27, 38, 52, 67, 84 … are all strip
  members).
- **(b) two-block / block + slab**: an axis-aligned (K−2)×(K−1) body plus a
  45° corner block — the mix the diamond family cannot make.
- **(c) axis-aligned dominant + tilted seams**: for r ≤ 8 the packing must
  be ~97% dense; the only known way is axis-aligned rows with tilted
  squares in the seams (this is what the 2026 community records at
  n ≈ 250–308 look like).

Acceptance test (cheap and decisive): beat grid at **n = 44, 58, 31** — the
deepest roots. A single hit is worth 0.02–0.03 with its diagonal.

### P2 — Motif-seeded numerical polish

The record-holders' engine (GPU SA from structured seeds; Schadt/Ellsworth)
is the only tool known to find packings in this regime. Our LP/annealer is
a *finisher* — but it has never been run **seeded from family states near
the wall** (the near-miss map: gaps 0.0208 / 0.0416 / 0.071 at 503 tied
rows, `workspace/push/gobel4_results.json` + the symmetric near-miss scan).
One bounded campaign: take the top-50 near-misses, seed with the family
state at s = grid + gap, and run contact-graph re-settling (break one
contact cluster at a time). This is the one place where search has a
chance: the state is already 99.9% of the way there.

### P3 — Source watch (proven EV, near-zero cost)

- Re-run `scripts/import_atlas.py` against a refreshed
  `workspace/sources/atlas/lists/` (or the jlevy/squares register) weekly;
  it is idempotent and packlib-gated. 76 records appeared in ~7 weeks; the
  next batch will cover more of the mid-band.
- Watch the register's **verified lower bounds** (Hosono 2026 etc.): they
  tell us which tied rows are worth attacking and which are near-proven
  optimal.

### P4 — Root conversions (amplified by the cascade)

Whatever produces constructions (P1/P2/P3), aim them at the diagonal roots
first (§2 table). The cascade then converts the rest of the diagonal for
free via `cascade3` + `closure_apply` — always re-run both to fixpoint
after any table change (the loop order is mandatory; Run 3/9/10 all earned
score from the propagation pass, not the find itself).

### P5 — Certification completeness (ledger, not score)

- Lean `lake build` completion; close `cascade_count_symbolic` and
  `verification_margin_soundness` (both have candidate proofs written).
- Exact-algebraic re-verification of the imported atlas states (their
  certs are exact rationals in t = tan(θ/2); a replay in `Fraction`
  arithmetic is cheap and matches the community's standard).
- The run-12 Q(√2) family L(k²+1) = k + 5√2/2 − 3: certificate + replay.

## 5. Value ladder (what a unit of effort is worth)

| action | score value |
|---|---|
| one imported record at depth d on n ≤ 324 (no cascade) | d/√n |
| one root construction at depth d on a diagonal with m tied members | ≈ d · Σ(1/√m) ≈ d · (0.4…0.5) |
| depth 0.01 uniform over the 405 open rows | 0.045 |
| depth 0.034 uniform over the open rows | **0.769 (the whole gap)** |
| all open rows at the area bound | 6.82 (theoretical ceiling) |
| the leader's standing | 11.3% of the theoretical ceiling |

## 6. What was executed in this session (Run 13), measured

1. **Path portability fix** — 62 scripts now resolve paths from the repo
   root (they were hard-wired to one machine's home directory); the
   pipeline runs anywhere.
2. **Community register import** (`scripts/import_atlas.py`): 76 certified
   best-known packings applied, 244 equal-to-current correctly skipped, 0
   verify-fails; direct gain 0.050264; attribution preserved per row.
3. **Propagation to fixpoint** (`cascade3`, `closure_apply`): 33 chain
   conversions (gain 0.013671); closure clean at fixpoint (monotone
   envelope preserved, 0 violations).
4. **Architecture test** (`scripts/gobel4.py`): the asymmetric 4-staircase
   generalization swept completely over 503 near-miss targets — **0
   representations below grid**; the negative is now a theorem-grade
   statement about the diamond+staircase class, and it *names* what the
   next architecture must be (P1).
5. **Instrument** (`scripts/gap_analysis.py`): block/residue census, leader
   calibration (d\* = 0.034), headroom decomposition — rerunnable after
   every table change.

Score 22.887471 → **22.823536** (−0.063935); beats-grid 448 → 454;
submission.csv rebuilt and round-trip verified.
