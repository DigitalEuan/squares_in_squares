# NEXT_STEPS.md — where the remaining 0.592 lives and how to get it

Companion to `STATUS.md`. Everything below is measured on the delivered
table (**Run 30, score 22.645991**, 543/1000 beat grid; the Mishapolk
import landed that run; run 31 reviewed the table — §2c — and closed
P1' by null without changing it) with `scripts/gap_analysis.py`,
`scripts/root_audit.py` (run 27; refreshed run 30),
`scripts/sat_review.py` (run 28), `scripts/sat_measure.py` (run 29)
and `scripts/symmetry_audit.py` (run 31); nothing here is aspirational
without a number attached.

---

## 0. Execution status of this plan (updated Run 31, 2026-11-06)

Runs 14–31 executed this plan. Measured outcomes, per item:

| item | status | measured result |
|---|---|---|
| **P1(a)** strip + generalized Göbel | **CLOSED (Run 25)** | exact closed-form family (L(a,w)=a+1+w/√2); 88/88 designs verified; dominated by the table on every row (0 finds); acceptance 44/58/31 fails by capacity (ceilings 38/52/27). |
| **P1(b)** two-block / block+slab | **CLOSED (Run 26)** | 45° m×m corner block + integer-lattice fill, L=(D+(3/2)√2·m)/2; 763 designs, pointwise grid-dominated (0 beat grid at equal L); acceptance fails by capacity (36/49/25). |
| **P1(c)** axis-aligned dominant + tilted seams | **CLOSED as a family (Run 26)** | census: 314 strip-45, 31 Pythagorean-exact, 109 drifted; n=50 decoded exactly (L=53/7, arctan(3/4), 1/50 lattice, 105 contacts, K²+1). The blob rows are isostatic hand-polished, not parametric; follow-up = P1'. |
| **P2** motif-seeded numerical polish | **CLOSED (Runs 23–25, 30)** | runs 23–25: 52/52 cells 0 finds. Run 30 renewal for the T-263 family (the SAT review's exception: 41 floaters at ratio 0.68): 12/12 cells (299/334/371 × ladder 0.002/0.005/0.01), 0 finds, 0 hard hops, soft extents pinned 0.4–2.5e-3 above L_t — the floaters do not settle deeper by contact-graph re-breaking. P2 is closed for good. |
| **P3** source watch | **LIVE (paid runs 22, 26, 30)** | Run 30 (the largest since run 22): the weekly atlas check was unchanged, but probing beyond it found **Mishapolk/square-packing-records** — `upper_bounds.json` carries verified bounds at ALL 1000 n, including 676 in the band 325..1000 our atlas never showed us. 221 rows imported (exact certificates, center-basis t=tan(θ/2)): score 22.819978 → 22.645991. Also read: Karimi two-strip (n≥1184, above our range) + window theorem. |
| **P4** root conversions | **INSTRUMENTED (Run 27)** | standing channel re-run (cascade 0, closure 0 — fixpoint true); `scripts/root_audit.py` built and run: the leverage map, corrected. Two documentation errors from run 26 fixed (§2). |
| **SAT data review** | **DONE (Run 28, user input)** | `scripts/sat_review.py` over all 1000 packings: contact language 99% parallel (run18-frontier 8% generic outlier); T-263 family 41 floaters at 0.68 (most slack); grid nearest-gap exactly 1.0; n=50 decode cross-validated (105 contacts). §2a. |
| **SAT measure (TAX/NRCI)** | **DONE (Run 29, user input)** | `scripts/sat_measure.py`: the tie test is the SAT data's binary layer (3.3-decade gap); SAT-TAX = g·Q, SAT-NRCI with GLM's constants and regime map. Vacuum = exactly the 546 grid rows; only off-vacuum provable rows = the 4 hand-proved packings (5/11/17/19); depth anti-correlates with genericity (frontier −0.61; chain3 deepest yet nearly vacuum) — run-28 P1' reading corrected. §2b. |
| **Symmetry review (D4 census)** | **DONE (Run 31, user input)** | `scripts/symmetry_audit.py` over all 1000 rows: constructions are majority-symmetric (gobel2/gobelS 100%, chain3 76%, exact 71%, closure 72%) but every record class is asymmetric (mishapolk 0%, run18-frontier 5%, register C1); tied-vs-sub asymmetry is a storage artifact; G~depth +0.31 / G~C/n +0.32 (present but weak). The P1' campaign built on it (symmetric canonical seeds + record-seeded insertion) closed by null at 356/395/355 — the Mishapolk records' voids are a thin seam (no axis-aligned +1 insertion; first candidate overlaps +0.257), not +1-voided grids. §2c. |
| **P5** certification completeness | **open** | unchanged (Lean build, exact replays); the tier-1 report's "s(6)=3 theorem" line retracted (register: restricted-optimality only). |

## 1. The gap, decomposed

| | score | note |
|---|---|---|
| our submission (Run 30) | 22.645991 | 543/1000 beat grid |
| leaderboard best (reported) | 22.0544214515 | |
| gap | **0.591569** | |

Closed since Run 13 (measured):

| push | gain |
|---|---|
| import 76 community best-known packings (n ≤ 324) | 0.050264 |
| chain propagation from those records (33 conversions) | 0.013671 |
| T-263 s(299) import + cascade (Run 26) | 0.003559 |
| **Mishapolk 221-row import + channel (Run 30)** | **0.173983** |
| **total closed** | **0.241477** |

**The mid-band 325..1000 is no longer empty upstream.** The run-27
statement "zero upper bounds exist above n = 324" was true of our
atlas (squaremath.org covers 1..324 only). Mishapolk's
`upper_bounds.json` (fetched run 30) has verified bounds at every n
in 1..1000; the ones that beat our table were imported, and the rest
of the band is now ours. The frontier moved: our watch must keep
probing Mishapolk, Couzo and Karimi for anything below our new rows.

The tie structure on the new table:

| | rows | note |
|---|---|---|
| tied rows (L = grid) | 457 | |
| — of which **proven floors** (can never improve) | 152 | perfect squares (area bound), s(k²−1)=k [T-084], s(k²−2)=k [T-086], s(k²−3)=k [T-064], s(k²−4)=k [T-081], plus individuals: s(11), s(12)=4, s(13)=4, s(21)=5, s(32)=6, s(44)=7 [T-252], s(45)=7, s(46)=7, s(59)=8, s(60)=8, s(61)=8, s(76)=9, s(77)=s(78)=9, s(95)=s(96)=10, s(2..5) |
| — **open rows** (the attackable set) | **305** | measured by root_audit run 30 |

A uniform depth d\* = 0.0365 (0.591569 over Σ(1/√m) = 16.198) on the
305 open rows matches the leader. The leader's standing as a share of
the open rows' area ceiling (5.005): 11.8%.

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

**Fixpoint audit (refreshed Run 30):** 0 rows above the chain envelope
(fixpoint true after the import — the channel absorbed it); 305 open
rows; 0 fully-open diagonals remain (the four optimality theorems
prove every diagonal's head).

**Top aims by value** (one Mishapolk-depth record, ~0.002/√n at the
aim, converting every later member of its diagonal to min(current,
chain from the aim) — root_audit run 30):

| c | best aim (first open row) | K | converts | window | value |
|---|---|---|---|---|---|
| 32 | 356 | 19 | 14 | 0.132038 | 0.011102 |
| 34 | 395 | 20 | 13 | 0.125393 | 0.010656 |
| 31 | 355 | 19 | 13 | 0.158556 | 0.010527 |
| 28 | 284 | 17 | 11 | 0.147700 | 0.010418 |
| 30 | 319 | 18 | 13 | 0.139429 | 0.010378 |
| 26 | 251 | 16 | 11 | 0.157020 | 0.010296 |
| 33 | 394 | 20 | 13 | 0.150567 | 0.010229 |
| 36 | 436 | 21 | 12 | 0.119387 | 0.009958 |
| 24 | 220 | 15 | 10 | 0.167603 | 0.009886 |
| 35 | 435 | 21 | 12 | 0.143346 | 0.009667 |

**Aggregate:** one Mishapolk-depth record at every diagonal's first
open aim = **0.375304** (63.4% of the whole gap); at depth 0.01,
0.167187. All top aims sit at grid today — the rows 356/395/355/284/
319/251/394/436/220/435 are open and tied; every one of them is a
legal P1' insertion target with measured conversion reach.

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
   never been polish-seeded. **RESOLVED (Run 30): the bounded P2
   re-run (12/12 cells, ladder 0.002/0.005/0.01 below row L,
   settle→anneal→re-harden, finalize gate) found nothing — 0 finds,
   0 hard hops, soft extents pinned 0.4–2.5e-3 above L_t.** The
   floaters do not settle deeper by contact-graph re-breaking; the
   record's depth is not floaters waiting to close. P2 closed for
   good.
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

### 2c. The symmetry review (Run 31, user input: "many optimal grids are
symmetrical and efficient")

`scripts/symmetry_audit.py`: a D4 point-group census over all 1000
delivered packings — 8 elements about the bbox center (rotations leave
θ invariant mod π/2; every reflection maps θ → −θ); an element holds
iff the mapped multiset of (center, θ) matches within 1e-6. Joined
per row with the SAT measures (C, g, φ, NRCI recomputed), depth, class
and status. Ledger `workspace/push/symmetry_audit31.json`.

1. **The input is true of the construction classes, not of the
   records.** gobel2/gobelS are 100% symmetric (D2/D4), chain3 76%
   (C2/Cs), exact 71%, closure 72% — but every record class is
   asymmetric: mishapolk 0% symmetric (209/209 C1, distance-to-symmetry
   ≥ 0.1), run18-frontier 5%, register (T-263) C1. The deepest known
   rows are lattice-tied AND symmetric; the imported frontier is
   neither.
2. **The tied/sub asymmetry split is a storage artifact.** Stored tied
   states are 15.3% symmetric vs sub 37.6% — but tied rows are stored
   as tail-drop grids (canonical asymmetric); a symmetric arrangement
   exists for every tied row, and the census note says so. Read
   nothing into the split.
3. **Efficiency (C/n) tracks the contact language, not symmetry.**
   Mean C/n: grid 3.600 (corner contacts included; validated at n=356:
   C=1313 = 674 edge + 639 corner), construction classes 3.1–3.6,
   records ~1.9–2.8. G_size~C/n = +0.32 and G_size~depth = +0.31 are
   present but weak — both are carried by the class structure (item
   1), not by within-class variation. Depth~φ +0.14: deeper rows are
   slightly MORE generic on this table (the Mishapolk import put
   asymmetric deep rows in the mid-band; run-29's −0.61 was measured
   on run18-frontier alone).
4. **The falsifiable turn: the P1' campaign at the top aims
   (356/395/355) built on the census — and closed by null.**
   - Arm A (symmetric canonical seeds, 14/14 cells: 7 hole-orbit
     patterns across the three aims × 2 deltas): D4/D2/Cs hole
     orbits in the K×K lattice, ramp_settle pressure + 3 anneal cycles,
     finalize gate. Every seed's group confirmed in-ledger by the
     census; every cell an honest null (0 hard hops, soft extents
     pinned ~2e-3 above L_t — the run-30 signature).
   - Arm B (record-seeded greedy insertion, 3/3 cells): the deepest
     sub-K record below each aim (344@18.9927 for 356/355;
     382@19.9876 for 395), greedy max-clearance axis-aligned
     insertion at L(seed) on the 0.25-lattice. Result: **zero
     insertions everywhere** — the best first candidate overlaps by
     +0.257. The Mishapolk records' free area (16.7 units² at n=344)
     is a thin seam fragmented across 51 orientations, not +1-voided
     grids like the gobel rows. This is the structural reason
     mid-band +1 insertion at fixed L has no purchase, and matches
     Karimi's observation that his next-K strip jumps +8 squares —
     there is no +1 route.
   - Three arm-B bugs were found and fixed by synthetic sanity tests
     before the null was trusted (seed rule: smallest-L record over
     all m; tangency: pen=0 rejected; container: centers at 0.25 put
     edges outside [0, L] by 0.25). Each fix is a run-31 lesson: the
     greedy is only trustworthy after it recovers a known answer.
5. **What the null leaves standing.** The aims stay open (356/395/355
   at grid, Mishapolk's best there = integer grid too — checked
   upstream). The next legal language at the aims is Karimi's
   two-strip class (wall strips at small angles) — which is exactly
   what Mishapolk's rows already are, and their voids are seams. So
   the aiming map's values (§2) remain live but unclaimed by this
   run's instruments; the honest statement is: **symmetry does not
   buy depth at the aims — it is the signature of the parametric
   classes that already sit below the frontier.**

## 3. Failure → requirement (updated with runs 14–31)

Items 1–13 stand (see run-26/27/28 revisions). Two additions:

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

14. **A greedy is only trustworthy after it recovers a known answer**
    (run 31): arm B returned 0 insertions three times for three
    different bugs (seed rule; tangency sign; container bounds) — and
    each looked like an honest null. The synthetic sanity test (a
    grid with known holes; the greedy must find exactly those holes)
    is what caught all three. Requirement: every new search heuristic
    ships with a synthetic recovery test in the ledger; a null from
    an untested heuristic is not a result.
15. **Correlations recomputed on a changed table can flip sign**
    (run 31): run-29's depth~φ = −0.61 (frontier-only) became +0.14
    on the run-30 table — the Mishapolk import added asymmetric deep
    rows to the mid-band. Requirement: every published correlation
    carries its row set; re-state it after each import, never carry
    it across a table change.

## 4. Prioritized pushes (updated Run 31)

### P1' — CLOSED BY NULL (runs 30–31)

Run 30: the aiming map moved to 356/395/355 with the Mishapolk
import. Run 31 built the campaign the census informed and closed it:
arm A (symmetric canonical seeds) 14/14 null; arm B (record-seeded
insertion) 3/3 null — the Mishapolk records' voids are a thin seam,
not +1 space (§2c.4). The aims remain open upstream (Mishapolk's best
there = integer grid). The two-phase picture stands untested at the
aims: no improvement was found to measure φ on. Numerical insertion
and squeeze at the aims are dead in this landscape; the next legal
language there is the two-strip class, and its voids are seams too —
which is why the aiming map's values stay unclaimed. If anything
moves at the aims it will be an imported record (P3), not a
construction we can parametrize or a settle we can run.

### P2 — CLOSED FOR GOOD (runs 23–25, 30)

Runs 23–25: 52/52 cells, 0 finds. Run 30: the T-263 renewal (§2a.2)
returned an honest null in all 12 cells — the 41 floaters at Maxwell
ratio 0.68 do not settle deeper by contact-graph re-breaking. The
run-29 falsifiable prediction (φ down / NRCI up on any improvement)
stands untested: there was no improvement to measure. Numerical
polish is dead in this landscape; every future gain must come from
constructions or imports (P1', P3).

### P3 — source watch (weekly; the only item that has paid)

- `import_atlas.py` weekly (idempotent) — unchanged this week
  (324 entries, 0 new; 319 rejected no-beat).
- **Add Mishapolk to the weekly loop** (`fetch_mishapolk.py` +
  `import_mishapolk.py`, idempotent + resumable): it paid 0.173983 on
  its first run. Watch `upper_bounds.json` for rows that beat our new
  table; watch for certificates at the 528 construction-only entries
  (only n=261 has gain > 1e-5: 16.678780 vs our 16.682927).
- Karimi (read run 30): two-strip packings live at n ≥ 1184 —
  outside our range — but the **window theorem** (for every integer
  K ≥ 16, s(n) < K whenever n ≤ K² − 8√K − 19; exponent 3/5 → 1/2
  over Bui/McClenagan) is the certificate shape for our mid-band
  rows: it proves sub-grid existence for n up to K²−8√K−19 whenever
  such a record lands. At K=19: n ≤ 303. If his preprint ever
  optimizes the construction below 1184, import directly.

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
| one Mishapolk-depth record at 356 / 395 / 284 | 0.011102 / 0.010656 / 0.010418 |
| the Mishapolk import (measured, run 30) | 0.173983 |
| one Mishapolk-depth record at every diagonal's first open aim | **0.375304 (63.4% of the gap)** |
| uniform depth matching the leader over the 305 open rows | **0.591569 (the whole gap; d\* = 0.0365)** |
| all open rows at the area bound | 5.005 (theoretical ceiling) |

## 6. What was executed (runs 14–30), measured

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
6. **Run 30 (this run; continue NEXT_STEPS)**: three parts.
   **(a) P2 closed for good** — the T-263 renewal (§2a.2): 12/12
   cells (299/334/371 × ladder 0.002/0.005/0.01 below row L,
   settle→anneal→re-harden hops, finalize gate), 0 finds, 0 hard
   hops, soft extents pinned 0.4–2.5e-3 above L_t. The 41 floaters
   do not settle deeper by re-breaking.
   **(b) P3 paid the largest import since run 22** — the weekly
   atlas check was unchanged, but the Karimi lead (issue #799, read
   via browser; preprints.org blocks plain fetchers) pointed past
   our sources: **Mishapolk/square-packing-records**
   `upper_bounds.json` has verified bounds at ALL 1000 n — the band
   325..1000 our atlas (1..324 only) never showed us. Imported 221
   rows (exact certificates, center-basis t=tan(θ/2); two
   invocations after a verify-tolerance fix for exact-tangency float
   noise and a dry-run ledger bug): score 22.819977568 →
   **22.645990613**, beats-grid 454 → 543. Standing channel run
   (cascade 9, closure 3, assembly round-trip 0 issues); root_audit
   refreshed: fixpoint true, 305 open rows, aggregate 0.375304;
   best aim moved to c=32 n=356 (0.011102, 14 conversions).
   **(c) Karimi read**: two-strip packings at n ≥ 1184 (outside our
   range) + the window theorem (K ≥ 16: s(n) < K whenever
   n ≤ K² − 8√K − 19, exponent 3/5 → 1/2 over Bui/McClenagan) —
   the certificate shape for our mid-band rows.
7. **Run 31 (user input: "many optimal grids are symmetrical and
   efficient")**: the input became a measured hypothesis, not an
   assumption. `scripts/symmetry_audit.py`: D4 census over all 1000
   rows joined with recomputed SAT measures (§2c). Headline: the
   construction classes are majority-symmetric (gobel2/gobelS 100%,
   chain3 76%) but every record class is asymmetric (mishapolk 0%,
   209/209 C1, distance-to-symmetry ≥ 0.1); tied-vs-sub 15.3%/37.6%
   is a storage artifact (tail-drop grids); G~depth +0.31 / G~C/n
   +0.32 present but weak; grid C validated as edge+corner contacts
   (n=356: 1313 = 674 + 639). The P1' campaign built on the census
   closed by null at the top aims 356/395/355: arm A (canonical
   symmetric seeds, 14/14) and arm B (record-seeded greedy insertion,
   3/3 after three bug fixes each caught by a synthetic sanity test —
   §3.14). Arm B's null is structural: the Mishapolk records' free
   area is a thin seam (best first-candidate overlap +0.257 at
   n=344), not +1-voided grids — mid-band +1 insertion at fixed L has
   no purchase, matching Karimi's +8-per-K jumps. P1' closed by null;
   the aims stay open. Score unchanged 22.645990613.

Score 22.823536149 → 22.819977568 (runs 26–27) → **22.645990613**
(run 30); beats-grid 543; run 31 unchanged (analysis + campaign null);
submission.csv rebuilt and round-trip verified.
