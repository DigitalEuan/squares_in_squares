# NEXT_STEPS.md — where the remaining 0.766 lives and how to get it

Companion to `STATUS.md`. Everything below is measured on the delivered
table (**Run 29, score 22.819978**, 454/1000 beat grid; the SAT data
reviewed run 28 and measured run 29) with `scripts/gap_analysis.py`,
`scripts/root_audit.py` (run 27), `scripts/sat_review.py` (run 28) and
`scripts/sat_measure.py` (run 29); nothing here is aspirational
without a number attached.

---

## 0. Execution status of this plan (updated Run 28, 2026-11-06)

Runs 14–28 executed this plan. Measured outcomes, per item:

| item | status | measured result |
|---|---|---|
| **P1(a)** strip + generalized Göbel | **CLOSED (Run 25)** | exact closed-form family (L(a,w)=a+1+w/√2); 88/88 designs verified; dominated by the table on every row (0 finds); acceptance 44/58/31 fails by capacity (ceilings 38/52/27). |
| **P1(b)** two-block / block+slab | **CLOSED (Run 26)** | 45° m×m corner block + integer-lattice fill, L=(D+(3/2)√2·m)/2; 763 designs, pointwise grid-dominated (0 beat grid at equal L); acceptance fails by capacity (36/49/25). |
| **P1(c)** axis-aligned dominant + tilted seams | **CLOSED as a family (Run 26)** | census: 314 strip-45, 31 Pythagorean-exact, 109 drifted; n=50 decoded exactly (L=53/7, arctan(3/4), 1/50 lattice, 105 contacts, K²+1). The blob rows are isostatic hand-polished, not parametric; follow-up = P1'. |
| **P2** motif-seeded numerical polish | **DONE (23–25) → RENEWED (Run 28)** | 52/52 cells 0 finds originally; the SAT review found the T-263 family (299/334/371) with 41 floaters at ratio 0.68, imported after the campaign — one bounded re-run aimed there (§2a.2). |
| **P3** source watch | **LIVE (paid runs 22+26)** | Run 26: T-263 s(299) imported exactly (+0.003559 with chain). Run 27: 4 optimality theorems + individuals absorbed into the instrument. Run 28: T-083 rectangle bound checked against every row (0 violations, no new floors); register best-known still grid at every top aim. |
| **P4** root conversions | **INSTRUMENTED (Run 27)** | standing channel re-run (cascade 0, closure 0 — fixpoint true); `scripts/root_audit.py` built and run: the leverage map, corrected. Two documentation errors from run 26 fixed (§2). |
| **SAT data review** | **DONE (Run 28, user input)** | `scripts/sat_review.py` over all 1000 packings: contact language 99% parallel (run18-frontier 8% generic outlier); T-263 family 41 floaters at 0.68 (most slack); grid nearest-gap exactly 1.0; n=50 decode cross-validated (105 contacts). §2a. |
| **SAT measure (TAX/NRCI)** | **DONE (Run 29, user input)** | `scripts/sat_measure.py`: the tie test is the SAT data's binary layer (3.3-decade gap); SAT-TAX = g·Q, SAT-NRCI with GLM's constants and regime map. Vacuum = exactly the 546 grid rows; only off-vacuum provable rows = the 4 hand-proved packings (5/11/17/19); depth anti-correlates with genericity (frontier −0.61; chain3 deepest yet nearly vacuum) — run-28 P1' reading corrected. §2b. |
| **P5** certification completeness | **open** | unchanged (Lean build, exact replays); the tier-1 report's "s(6)=3 theorem" line retracted (register: restricted-optimality only). |

## 1. The gap, decomposed

| | score | note |
|---|---|---|
| our submission (Run 28) | 22.819978 | 454/1000 beat grid |
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
worth their d/√n only, no chain reach (values 0.002–0.009). NOTE (run
28): the tier-1 verification report's old "theorem s(6)=3" line is NOT
backed by the register — n = 6 appears there only in
restricted-optimality rows (T-261/T-124, local-minima searches, C1/C0),
never as an optimality result. s(6) = 3 remains a conjecture by our
classification; n = 6 stays a legal (if low-value) aim.

### 2a. The SAT data reviewed (Run 28, `scripts/sat_review.py`)

Per-pair separating-axis data over all 1000 delivered packings
(margins, contact normals, contact types, binding-wall touches, free
squares, Maxwell counting ratio). Ledger
`workspace/push/sat_review28.json`. What it says:

1. **The table's contact language is 99% parallel.** Of 1,806,403 pair
   contacts, 51.5% have exactly 2 tight SAT axes (parallel edge or
   non-parallel corner) and 47.5% have 4 (parallel corner); only 1.0%
   are generic single-tight edge/vertex contacts, and 3-tight is
   structurally empty. The classes differ sharply: grid/chain/closure/
   gobel are ≥ 99% parallel (2- or 4-tight), while run18-frontier —
   the record class — carries 8% generic contacts (ratio median
   1.057 vs 1.2+ everywhere else). READING CORRECTED BY RUN 29 (§2b):
   the class-level contrast is real but the prescription is not
   "seek generic contacts" — within the record class, deeper rows are
   LESS generic (φ-vs-depth −0.61), and the deepest class in the
   table (chain3) is nearly at the vacuum. Genericity marks the
   small-n provable regime and shallow records, not depth.
2. **The T-263 family floats 41 squares.** n = 299/334/371 each have
   41 free squares (no pair contact, no wall touch) at Maxwell ratio
   0.68 — the most slack in the table (next: 0.71 at 334). The 41 are
   the same squares in all three (chain children inherit them),
   quasi-contacting at median gap 0.0035 with wall distance up to 6.46.
   These rows were imported AFTER the P2 polish campaign; they have
   never been polish-seeded. **Renew P2 for exactly this family** —
   it is the one place where the record-holder's engine and our
   finisher could meet: 41 floaters at ratio 0.68 is a near-miss map
   of size 3.
3. **The grid is provably rigid at the pair level.** The 546 grid rows
   have nearest non-contact gap exactly 1.0 (a full empty cell) — the
   P2 0-finds there are now a measured statement, not an anecdote.
4. **Karakuş's rectangle bound (T-083) was checked against every row.**
   s(N) ≥ 1/2 + √(N − ⌊√N⌋ + 1/4) for nonsquare 8..324: 0 violations
   of our sub-grid L; it implies grid-optimality only on the c = 1
   diagonal (k²−1, already covered by T-084) — no new proven floors
   for us, but it is the right certificate shape for the mid-band:
   if it ever extends past 324 it cuts the aiming set directly.
5. **The register's best-known is still grid at every top aim**
   (250/251/284/191/190: side "16.0/17.0/14.0", finder "-"). Nobody
   upstream has beaten grid in the mid-band either; the 325..1000
   emptiness and these rows are the same frontier.

### 2b. The SAT measure: TAX/NRCI on the SAT data (Run 29, `scripts/sat_measure.py`)

User input asked for a measure on the SAT data in the GLM's currency
(TAX, NRCI — github.com/DigitalEuan/GLM, the parent system; definitions
in upload/GLM_Complete_Number_Theory_Evidence.md §1.1–1.3). The answer
is yes, and the SAT data has its own binary layer to carry it:

- **The binary layer is the symmetry tie.** A contact pair is *tied*
  when the two axis families see the same two directions
  (multiset{pen_u0, pen_v0} = multiset{pen_u1, pen_v1}); tied contacts
  have even weight (2 or 4 tight axes — the parity law of run 28).
  Measured: the tie residual is sharply bimodal — tied population
  ≤ 5e-12 (float noise of exact constructions), generic continuum
  ≥ 1.1e-8, a 3.3-decade empty gap between. "Parallel" is a measured
  property of the data, not a tolerance choice.
- **The measure** (the carrier is the packing's contact word; 1-bits =
  generic contacts, g of them): SAT-TAX = g·Q with the GLM's Q =
  Y+1/8 (Y = 1/(π+2/π)); SAT-NRCI = 10/(10+SAT-TAX) ∈ (0,1];
  GLM regime map at integer cutoffs g ≤ 6/25/59 (exact under the
  proved Y bounds). Validated on the n=50 decode row (C=105, g=10,
  the ten weight-1 contacts of run 26/28).
- **What it says about the landscape:**
  1. The vacuum (NRCI = 1 exactly) is precisely the 546 grid rows.
     The GLM theorem NRCI=1 ⟺ v=0 lands here as: no generic contacts
     ⟺ grid.
  2. The only off-vacuum **provable** rows in the whole table are the
     four hand-proved packings — Göbel 5 (φ=1.00: all four contacts
     generic), Ahmed 11, Overbeck 17, Fitzharding 19 (NRCI 0.70–0.87).
     The provable frontier off the vacuum is exactly the generic
     language at small n; everything else (450 sub rows, NRCI median
     0.39, 55 subcoherent) is unproven territory.
  3. **Depth is not bought with genericity.** Within run18-frontier,
     φ-vs-depth = −0.61 (shallow third φ 0.138, deep third 0.048);
     the deepest class, chain3 (our large-n constructions, d/√n
     median 0.0123), sits nearly at the vacuum (φ 0.015). The
     landscape is two-phase: a **vacuum phase** (grid/lattice-tied,
     depth by chain arithmetic at large n) and a **generic phase**
     (small n, hand-proved, where every known proof lives). This
     corrects run 28's P1' reading: do not chase generic contacts
     for depth; genericity is the signature of the small-n provable
     regime.
  4. The register row (T-263, n=299) is the most generic per contact
     in the table (φ 0.101). **Falsifiable prediction for the P2
     re-run:** if settling the 41 floaters improves L on that family,
     the improved packing should move toward the tied language (φ
     down, NRCI up) — the deep mid-band is vacuum-like. If instead
     the improved packing has φ up, the two-phase picture is wrong
     and the P1' search should be re-aimed at the generic language.
- Ledger: `workspace/push/sat_measure29.json` (per-row g, φ, TAX,
  NRCI, regime, census, walls; class and status aggregates).

## 3. Failure → requirement (updated with runs 14–28)

Items 1–10 stand (see run-26 revision). Three additions:

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
13. **A "theorem" cited without the register row is a claim, not a
floor** (run 28): the tier-1 verification report carries "engine
refuses 6@2.9 = theorem s(6)=3", but the register has no optimality
row for n = 6 — only restricted-optimality searches (T-261/T-124,
local-minima assertions, C1/C0). We keep n = 6 as a legal aim and
retract the floor. Requirement: PROVEN_FLOOR entries must cite a
register row (or a published theorem we have read), and old claims
get audited when the register is re-checked — the same retraction
discipline as failure 11, applied backwards in time.

## 4. Prioritized pushes (updated Run 28)

### P1' — blob-regime insertion campaign (updated Run 29)

Seed from record states, insert one square at fixed L, pressure-settle;
first targets the aiming map's top rows (251, 250, 284, 191 — the
r=5/6 roots of the two biggest diagonals). New lead to read first:
"Structure-Guided Search for Packing Unit Squares in a Square"
(preprints.org, 2026-11-03, registration requests jlevy/squares #799)
— the community's current method paper; it names the structures that
found the recent records. Run-29 guidance (§2b.3): depth at large n
is vacuum-like — the mid-band target rows will resemble chain3
(lattice-tied, φ ≈ 0.015), not the generic language; genericity is
the small-n provable regime. Read the preprint against that
prediction.

### P2 — RENEWED for the T-263 family (Runs 28–29; see §2a.2, §2b.4)

Originally closed (runs 23–25: 52/52 cells, 0 finds). The SAT review
found the exception the closure was waiting for: n = 299/334/371 carry
41 free squares each at Maxwell ratio 0.68 — imported after the
polish campaign, never seeded. One bounded re-run: seed the LP/
annealer from the register states (exact coordinates in
lists/certs/n-299), floaters free, settle with contact-graph
re-breaking. Value if it converts: the family's rows are already
sub-grid, so any find is direct d/√n on top of 0.68-ratio states.
Run-29 addition: log SAT-NRCI before/after — the two-phase picture
(§2b.3) predicts any improved packing comes with φ down (more tied);
φ up falsifies it and re-aims P1' at the generic language.

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

## 6. What was executed (runs 14–29), measured

1. **Runs 14–25**: P2 finished; P1(a) closed by domination; the
   deliverable-name fix (run 25).
2. **Run 26**: P1(b) closed by domination; P1(c) closed as a census +
   decode (blob regime); P3 paid: T-263 imported exactly, +0.003559
   with chain (334, 371); score 22.823536149 → 22.819977568.
3. **Run 27**: P4 executed — the standing channel re-run to
   fixpoint (cascade 0, closure 0, score unchanged 22.819977568;
   submission.csv round-trip 0 issues); `root_audit.py` built and run
   (chain-envelope audit: 0 above envelope; proven floors: 156 rows;
   aiming map: 54 diagonals, 394 open rows); two run-26 documentation
   errors found and corrected (§2); the four optimality theorems +
   individual proofs absorbed into the instrument; the register
   re-checked (no new records; max n = 308, zero bounds > 324); the
   aggregate measured (0.4334 at T-263 depth; d\* = 0.0382).
4. **Run 28 (user input: review the SAT data for insight)**:
   `scripts/sat_review.py` built and run over all 1000 packings —
   per-pair SAT margins, contact normals, contact types, binding
   walls, free squares, Maxwell ratios. Validated against the run-26
   n=50 decode (105 contacts, exact). Findings in §2a; headline:
   the contact language is 99% parallel with run18-frontier the
   8%-generic outlier; the T-263 family floats 41 squares at ratio
   0.68 (most slack in the table, never polish-seeded → P2 renewed
   for that family); the grid's nearest non-contact gap is exactly
   1.0 (P2's 0-finds there now measured); Karakuş's T-083 rectangle
   bound checked against every row (0 violations, no new floors —
   c=1 only); the register's best-known is still grid at every top
   aim; the old "s(6)=3 theorem" claim retracted (register has only
   restricted-optimality there). Score unchanged 22.819977568.
5. **Run 29 (this run; user input: a TAX/NRCI-style measure on the
   SAT data)**: definitions extracted from the GLM papers (the repo
   is the parent system); `scripts/sat_measure.py` built and run —
   the tie test is the SAT data's binary layer (residual bimodal,
   3.3-decade gap: tied ≤ 5e-12, generic ≥ 1.1e-8); SAT-TAX = g·Q,
   SAT-NRCI = 10/(10+TAX), GLM regime map at integer cutoffs.
   Validated on n=50 (C=105, g=10). Findings in §2b; headline: the
   vacuum (NRCI=1) is exactly the 546 grid rows; the only off-vacuum
   provable rows are the four hand-proved packings (5, 11, 17, 19);
   depth anti-correlates with genericity (frontier φ-vs-depth −0.61;
   deepest class chain3 nearly at the vacuum) — run 28's P1'
   "seek generic contacts" reading corrected in §2a.1; falsifiable
   P2 prediction recorded (any T-263 improvement should come with
   φ down). Score unchanged 22.819977568.

Score 22.823536149 → **22.819977568** (runs 26–27); beats-grid 454;
submission.csv rebuilt and round-trip verified.
