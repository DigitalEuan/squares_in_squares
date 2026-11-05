# STATUS.md — Squares in Squares: complete system state (Run 13, 2026-11-05)

This is the "everything in one place" document: what the system is, what has
been done, what works, what fails, and where the frontier actually lies.
Historical detail lives in `workspace/README.md` (run ledger), the run JSONs
in `json/`, and the study series in `workspace/docs/`. The forward-looking
analysis is in `NEXT_STEPS.md`.

---

## 1. The competition and the score mechanics

Pack n unit squares (n = 1..1000) into the smallest axis-aligned square of
side L. Score = Σ (L/√n − 1) over the 1000 puzzles, **lower is better**;
a missing puzzle is charged the trivial grid ceiling L = ⌈√n⌉. The grid
ceiling total is **28.937670** (exact: 28.9376699165…, isqrt-bounded).
Every valid improvement over the grid scores, however small; the score's
density per unit of L is 1/√n, so small n are worth ~30× more per unit of
container than n ≈ 1000.

## 2. Delivered state (verified this session)

| Quantity | Value |
|---|---|
| Submission score | **22.823536** |
| Grid ceiling | 28.937670 |
| Total improvement | −6.114134 |
| Puzzles beating the grid | **454 / 1000** |
| Grid-tied | 546 (of which **94 are proven optimal**, see §5) |
| Certification | 1000/1000 packings SAT-verified (pairwise non-overlap, bbox containment), 12-dp CSV round-trip, 2e-9 clearance |
| Leaderboard best (user-reported 2026-11-05) | 22.0544214515 |
| Gap to leader | **0.769115** |
| Absolute area floor (all open rows at L = √n) | 15.08 (of which 14.24 is already locked in by closed rows) |

Table invariants (all machine-checked by `scripts/gap_analysis.py` and the
round-trip in `scripts/final_assembly.py`):

- **Monotone envelope**: L(n) ≤ L(n+1) for all 999 adjacent pairs — 0
  violations. (Run 12's "deletion lemma": no free improvement exists by
  removal alone; every below-grid value is earned.)
- **Shell law**: L(n + 2⌊L(n)⌋ + 1) ≤ L(n) + 1 — 937 checked, 0 violations.
  The +1 container transfer is a family law, exact on this table.
- **Round-trip**: submission.csv read back from disk, every packing
  re-verified, score recomputed independently.

### Where the improvements come from (source census, 454 rows)

| Source family | Rows | What it is |
|---|---|---|
| `chain3` | 137 | L-extension band chains (base + free-band cells at L+1) |
| `atlas` | 76 | community best-known records imported this session (Run 13) |
| `exact` / `aux` / `removal` | 107 | Ellsworth survey SVGs (parsed at 20–100 digits) + removal windows |
| `closure` | 54 | removal-closure to fixpoint (drop squares from larger m) |
| `gobel2` | 53 | the 4-parameter Göbel family G(a1,a2,b,c) (Run 9) |
| `gobelS` | 18 | Göbel strip / central-square families |
| `gobel3` | 9 | clipped-diamond family G(a1,a2,b,c,t) (Run 10) |
| `grid` | 546 | trivial grid (⌈√n⌉) |

---

## 3. What works (the instruments that produce score)

1. **Sources beat search — by an order of magnitude.** The single biggest
   jump of the project (28.35 → 23.28) came from parsing the survey's 235
   record SVGs, not from an optimizer. This session repeated the lesson:
   the community register (Square Packing Atlas / jlevy/squares) held **76
   best-known packings our table lacked** (autumn-2026 finds by Couzo,
   Chaoweeraprasit/SQUISH, Ostashev, Ryan Xu, de Winter, PingYou, Mishapolk,
   Ellsworth, Daniel, Schadt, Hajba, …), worth 0.050 directly and 0.064
   after chain propagation. The published catalogue (Ellsworth/kingbird) is
   **not** the frontier any more — the community register is.
2. **Analytic construction families.** Göbel strip/central-square (`gobelS`),
   the generalized diamond + staircase G(a1,a2,b,c) (`gobel2`, 17
   beyond-catalogue finds at mid-band n), and the clipped variant
   G(a1,a2,b,c,t) (`gobel3`, 5 more). Families are exact, sweepable, and
   certifiable — and they beat the catalogue on the mid-band where no
   catalogue exists.
3. **Exact propagation.** Two closure laws, both verified to fixpoint:
   - *Removal closure*: removing squares never grows the bbox, so every
     n < m inherits L(m) (prefix-min envelope; `closure_apply.py`).
   - *L-extension chains*: a base (m, L) fills the free L-band at L+1 with
     ⌊L+1⌋+⌊L⌋ cells, partial fills included (`cascade3.py`).
   The residue-family law makes this multiplicative: **one base at
   n₀ = (k₀−1)² + c opens the whole diagonal n = (K−1)² + c for all K ≥ k₀**
   (verified chain arithmetic: m_j = (j+k₀−1)² + c at L₀ + j). This is why
   an imported record at, e.g., n = 308 propagates to 343, 380, 419 …
4. **The honest gate.** Every applied state — imported or constructed —
   goes through `packlib.finalize` + SAT verification (pairwise separation
   on 4 axes, bbox containment, 2e-9 contact gap, 12-dp round-trip). The
   pipeline has never shipped a packing that failed re-verification.

## 4. Failure ledger — what fails, and what each failure *literally* says

The project's failures are unusually informative; each one names the thing
that is required to go further.

| # | Failed instrument | Measured failure | What it literally indicates |
|---|---|---|---|
| 1 | Pressure-settling / simulated annealing (Runs 1,2,6,8) | jams at E ~ 1e-2 on every target; **positive control failed**: 0/10 calls reach grid−0.004 at n=5 or n=12 where the optima are famous and simple | the answers are **low-measure crystalline motifs** (n=5 is literally "one 45° square + four corners"): relaxation cannot invent them. Construct motifs analytically; use search only to polish motifs |
| 2 | LP closure over near-states (Run 8) | s\* = (k−L)/(k−1) **exactly** on every target; engine always lands on a rigid grid; zero binding flips ever helped | every local optimum is the grid: leaving it requires a **change of combinatorial type**, not a gradient step. The LP is a finisher, never a finder |
| 3 | Mixed-angle assemblies (Run 8) | mixed 0/45 contact costs 1+√2/2 = 1.2071 vs 1.0 same-angle on every SAT axis | **build in one angle**: compression lives in same-angle 45° strips; mixed interfaces pay a 21% tax |
| 4 | Level escalation (√3 hypothesis, Run 4) | refuted empirically (levels are parallel), constructively (45° is the kink minimum of s(θ); fine sweep 0.05°), and algebraically (certificates) | the jam walls are **real structures**, not a missing higher field. Stay in Q(√2)/45°; 45° is optimal inside the family |
| 5 | Carried forks / wheels (Run 5) | both wheels dead by inequality (tilted-grid capacity {0:593}; mirror-split needs θ ≥ 126.87°); 30/30 branches RIGID_WALL; positive control failed | the crystalline tie is a **LOCK**, not a Golay-type ambiguity: there is nothing to discriminate and no key to supply |
| 6 | Pocket-fill / n-migration (Run 10) | structurally negative: closure fixpoint makes L non-decreasing in n | improvement cannot come from re-packing inside known containers; **only new bases move the front** |
| 7 | θ-family sweep, 7 special angles (Run 5) | 45° strictly best; other angles lose on every n | rotation away from 45° lowers the container diagonal faster than the staircase cost |
| 8 | **G4 asymmetric-staircase sweep (Run 13, today)** | 0 of 503 near-miss targets have ANY representation at design s < grid (complete sweep incl. zero-depth corners) | the tied zone is **not** a parameter-granularity problem: the diamond+staircase architecture has a density ceiling (a 45° diamond is ≤ 50% area-efficient in its bbox). A **new architecture** is required for n = K² − r at small r |

The positive results point the same way as the failures: everything this
project has ever scored came from **structure that already existed as
data** (survey, catalogue, community register) or **structure derived
analytically** (families, closures). No search campaign has ever produced
a single applied improvement. That is the design law of this system.

---

## 5. The frontier map (where the remaining score lives)

### 5.1 Block/residue structure

Let K = ⌈√n⌉ and r = K² − n (distance below the top of the block).
The delivered table has a sharp shape per block:

- **improved window**: n from the block bottom (K−1)²+1 up to about
  K² − (K+5) — fed by L-extension chains from bases below; depths taper
  0.48 → 0.02 across the window;
- **tied zone**: n from about K² − (K+4) up to K² − 3 — **this is where all
  remaining score is**;
- **proven optimal**: r = 0 (perfect squares), r = 1,2 (Nagamochi
  s(k²−2)=s(k²−1)=k), and — new since the 2026 community work — **r = 3**
  (s(m²−3)=m for m ≥ 6, Bentz 2016 + 2026 re-proof) and **r = 4**
  (s(k²−4)=k, Daniel 2026). 94 rows are optimal today; several more are
  claimed-proved but not yet replayed (n=12 sits on the s(k²−4)=k family).

The tied rows form **residue diagonals** n = K² − r = (K−1)² + c with
c = 2K−1−r: one diagonal per c. Chains run *up* a diagonal from its first
record base; the tied part of each diagonal is exactly the *root region*
below the best known base. Consequence (the residue-family law): **an
improvement at any root opens the whole diagonal above it.**

### 5.2 Headroom (from `scripts/gap_analysis.json`)

- Tied, not proven: **~405 rows**, total area headroom Σ(K−√n)/√n ≈ **5.3**.
- The leader's 0.769 gap is **~15% of that headroom**; equivalently a
  uniform depth of **d\* = 0.034** below grid on every open row matches the
  leader exactly.
- Per-puzzle value concentrates at small n: the top headroom rows are
  n=20 (0.118), 30 (0.095), 21 (0.091), 42 (0.080), 31 (0.078), 56 (0.069),
  43 (0.067) … — the classic open problems where the community's best is
  still the grid.
- At n = 325..1000 the per-puzzle headroom is capped at ~0.026 (area), but
  there are ~310 tied rows there.

### 5.3 What the leaderboard gap tells us (quantified)

Decomposition of the 0.769 gap:

| Component | Score | Evidence |
|---|---|---|
| best-known records we lacked (n ≤ 324) | **0.050 — closed this session** | community register vs table diff (`workspace/push/atlas_import.json`) |
| chain propagation from those records | **0.014 — closed this session** | `cascade3` run, 33 conversions |
| everything else | **~0.70 — beyond the published frontier** | see below |

For n ≤ 324 we are now **exactly at the community's certified frontier**
(76 imports applied, 0 rows where we beat their best.json and 0 where they
beat ours after import). The community tracks only n ≤ 324. Therefore the
leader's remaining ~0.70 must live at **n = 325..1000** — the range where
the catalogue is nearly empty (1 record in 325..1000!) and our own
families/chains are the de-facto state of the art. That is also the range
where nobody in the literature has systematically searched.

Two consistent readings (both point at the same work):

1. *Small depth across many rows*: depth ≈ 0.02–0.03 on a large share of
   the ~310 tied rows at n > 324, or better depths on the improved-window
   rows (ours taper to 0.02 at the window top where the area bound allows
   0.3–0.5).
2. *Root constructions*: a handful of new packings at the roots of the
   residue diagonals (n = 44, 57, 72, 90, 111, …), each of which cascades
   up its diagonal via the chain law.

---

## 6. External source landscape (checked 2026-11-05)

| Source | Status | Use |
|---|---|---|
| Ellsworth catalogue (kingbird.myphotos.cc/packing) | live; 164 records; only **1** in 325..1000 (n=626); **not** updated with the autumn-2026 finds | historical baseline; SVGs in `workspace/svgs/` |
| Square Packing Atlas (evand/square-packing) | live; certified best-known for **n ≤ 324**, exact rational certificates | **imported this session** (`workspace/sources/atlas/lists/`, `scripts/import_atlas.py`) |
| The Squares Project (jlevy/squares → squaremath.org) | live; the community register (frontier survey, verified lower bounds, per-n case files); new records land here weekly | the frontier to watch; **76 records since mid-Sept 2026** |
| Friedman survey (EJC DS#7) | stable | theory: proven values, families, lower bounds |

2026 additions worth knowing (they change the "open" list): s(13)=4 and
s(46)=7 (Bentz 2010), s(22)=5, s(33)=6 (Bentz 2016), s(m²−3)=m for m ≥ 6
and s(k²−4)=k (2026, computer-checked, unrefereed), plus new **verified
lower bounds** (Hosono 2026: s(20) ≥ 4.9125, s(30) ≥ 5.8835, s(31) ≥
5.9775, …) that quantify how much room the classic open problems have.

---

## 7. Run history (1 → 13)

| Run | Theme | Score after | Verdict |
|---|---|---|---|
| 1 | engine + survey integration | 23.19 | sources dominate search |
| 2 | Göbel family sweep, motif zoo | 23.19 | family exhausted; φ is not a generator |
| 3 | closure to fixpoint + live catalogue | 23.173640 | at published frontier; catalogue adds 0 |
| 4 | Leech/Golay layer + √3 escalation test | 23.173640 | lattice logic exact; √3 refuted 3 ways |
| 5 | rotated-block program (7 angles) | 23.173640 | 45° kink minimum; Level-0 negative |
| 6 | residue audit + cent engines | 23.173640 | audit corrected the picture; engines = 0 finds |
| 7 | Lorentz lift + gain tables + plan | 23.173640 | value ladder: mid-band is the prize |
| 8 | LP closure + sweeps + area recalibration | 23.173640 | search cannot produce 0.1-class; construct analytically |
| 9 | gobel2: full G(a1,a2,b,c) | 22.897558 | 17 mid-band finds beyond the catalogue |
| 10 | gobel3: clipped diamond + pocket fill | 22.887471 | 5 finds; pocket-fill structurally negative |
| 11 | precision architecture + certificates | 22.887471 | 1169 certificates; value-scan certification impossible at 4e-9 |
| 12 | lemma-driven table laws | 22.887471 | monotone envelope, shell law, 94 proven rows, new Q(√2) family |
| **13** | **community register import + propagation + G4 architecture test** | **22.823536** | **76 records + 33 chain conversions; G4: architecture ceiling proven by exhaustive sweep** |

---

## 8. Guarantee

Every packing in `submission.csv` is re-verified from the file on disk
(pairwise SAT non-overlap with worst penetration ≤ 0, bbox containment,
per-n counts, id continuity 0..500499, 12-dp round-trip with ~2e-9
clearance). Imported packings carry their finder attribution in `src`.
Every lattice-mathematics claim in the Leech layer is integer-exact
(Λ16's kissing number 7320 is cited, marked as such). Optimality is never
claimed for any packing: the verified statement is always "improved over
the grid ceiling on N puzzles, certified".
