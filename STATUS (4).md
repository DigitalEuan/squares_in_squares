# STATUS.md — Squares in Squares: complete system state (Run 32, 2026-11-06)

This is the "everything in one place" document. Since run 32 it carries
two things per the standing operations rule:

1. **A duplication of the current README information** (§1) — the
   headline numbers and the score engine, refreshed together with the
   README every run. The README is the source of the wording; this file
   re-states it so the system's state is readable in one place. The
   sync is checked mechanically: `deliverNN.py` fails if the headline
   numbers here disagree with the live table or the README.
2. **The system description** (§2) — how the system operates, and what
   information comes from where: every artifact class in the repository
   named by its producing instrument.

Historical detail lives in `RUN_NOTES.md` + `notes/` (run ledger), the
run JSONs in `workspace/push/`, and the study series in
`workspace/docs/`. The forward-looking analysis is in `NEXT_STEPS.md`.

---

## 1. Headline results and score engine (duplicated from README.md, Run 32)

### 1.1 Headline results (Run 32, 2026-11-06; last score move run 30)

| Quantity | Value |
|---|---|
| Submission score | **22.645991** (grid ceiling 28.937670, improvement −6.291679) |
| Puzzles beating the plain grid | **543 / 1000** |
| Leaderboard best (reported) | 22.0544214515 → gap **0.591569** |
| Certification | 1000/1000 packings SAT-verified + 500,500-row CSV round-trip (0 issues; re-verified run 32) |
| Golay/Leech verification | 28/28 + 14/14 assertions, integer-exact |
| Algebraic certificates | 1169 (7 angle families + surveys + run-11 census) |
| Proven-optimal rows | 156 (152 tied at grid + 4 below-grid: s(5), s(11), s(17), s(19)) |
| Largest single import | **Mishapolk/square-packing-records, 221 rows (run 30)**: 22.819978 → 22.645991 (−0.173983) |

### 1.2 The score engine (what actually produces improvements)

1. **Source integration** — the survey's 235 record SVGs (20–100 digit
   parse), the Ellsworth catalogue, the community register (76 records
   our table lacked, run 13; the T-263 record, run 26), and — the
   largest import of the project — **Mishapolk/square-packing-records**
   (run 30: verified bounds at ALL 1000 n; the band 325..1000 was
   invisible to our atlas; 221 rows imported, −0.173983). *Sources beat
   search: every score move since run 9 has been an import.*
2. **Analytic families** — Göbel strip/central-square, the 4-parameter
   diamond+staircase G(a1,a2,b,c) (17 mid-band finds beyond the catalogue),
   the clipped variant G(a1,a2,b,c,t) (5 more).
3. **Exact propagation** — removal closure (prefix-min envelope) +
   L-extension band chains; the residue-diagonal law multiplies every find
   (one base at n₀ opens its whole diagonal n = (K−1)² + c).
4. **The honest gate** — every state, imported or constructed, is
   packlib-verified (SAT non-overlap, bbox containment, 2e-9 clearance,
   12-dp round-trip). Nothing ships unverified.
5. **The measurement layer (runs 27–31)** — `root_audit.py` (chain-envelope
   fixpoint audit + the aiming map: where a new record pays most; best aim
   c=32 n=356), `sat_review.py` (per-pair SAT margins, contact language,
   Maxwell ratios), `sat_measure.py` (TAX/NRCI regime map: the vacuum is
   exactly the grid rows), `symmetry_audit.py` (D4 census: constructions
   symmetric, records asymmetric). Every campaign is aimed by these
   instruments, never by eyeball.

### 1.3 Score history (measured)

| run | score | event |
|---|---|---|
| 13 | 22.823536 | community register import (76 rows) + propagation |
| 26–27 | 22.819978 | T-263 s(299) import + cascade |
| 30 | **22.645991** | Mishapolk 221-row import + channel (−0.173983) |
| 31–32 | 22.645991 | analysis + campaign nulls; no score move |

---

## 2. How the system operates, and what information comes from where

### 2.1 The operating loop (every run)

```
   upload/ + workspace/sources/          scripts/ (instruments)
   external sources  ─────────────────▶  imports & constructions
        │                                   │
        │                          packlib.verify (SAT, the honest gate)
        │                                   │
        ▼                                   ▼
   workspace/sources/atlas, mishapolk   workspace/submission/table.json
   (fetched clones; git-tracked          (the system of record: 1000 rows,
    register copies)                      n → {L, state, src})
                                              │
                    cascade3 ─ closure_apply ─┤ (the standing channel,
                    final_assembly (round-trip)│  mandatory order)
                                              ▼
                                   submission.csv (500,500 rows) ── score
                                              │
                workspace/push/*.json ◀───────┤ (ledgers: every run's
                RUN_NOTES.md, notes/          │  measured outcomes)
                README/STATUS/NEXT_STEPS/     ▼
                REPRODUCE + download/runNN/      git commit + push to
                (delivery copies)                github (the off-site line)
```

Each run: read `NEXT_STEPS.md` (the map) → execute the highest-priority
open item with a script → every claim lands in a `workspace/push/`
ledger JSON with measured numbers → the channel (cascade3 →
closure_apply → final_assembly) and root_audit.py re-run after any
table change → documents updated (README, STATUS.md, NEXT_STEPS.md,
REPRODUCE.md, RUN_NOTES.md, notes/runNN_NOTES.md) → `deliverNN.py`
copies the state to `download/runNN/` → commit and push. Nothing is
ever claimed without a number from a ledger; failures 11–15 in
NEXT_STEPS §3 exist because that discipline was learned the hard way.

### 2.2 What information comes from where (artifact provenance)

| Information / artifact | Producer | Where it lives |
|---|---|---|
| Competition definition, baseline data, user's papers | the task (`upload/Squares in Squares.txt`, `sample_submission.csv`) | `upload/` (inputs; never modified) |
| Community record packings (SVGs, atlas lists) | `fetch_atlas.py`, survey parse | `workspace/sources/atlas/`, `workspace/svgs/` |
| Verified bounds at all 1000 n (the run-30 source) | `fetch_mishapolk.py` (clone; only `upper_bounds.json` git-tracked — the clone is 5.3 GB) | `workspace/sources/mishapolk/` |
| Göbel-family constructions | `gobel2/3/5/6.py`, engine scripts | applied straight into `table.json` rows (`src: gobel*:…`) |
| L-extension chain conversions | `cascade3.py` | row `src: chain3`; ledger in stdout + `download/runNN/outcomes` |
| Removal-closure rows | `closure_apply.py` | row `src: closure:…` |
| Imported records (atlas, T-263, Mishapolk) | `import_atlas.py`, `import_s299.py`, `import_mishapolk.py` | row `src: atlas / run18-frontier / mishapolk` + import ledgers |
| The system of record (states + L + src per n) | channel scripts | `workspace/submission/table.json` |
| The deliverable + independent score check | `final_assembly.py` (12-dp CSV + round-trip re-verification) | `workspace/submission/submission.csv` |
| Per-run measured outcomes (every claim) | each run's instrument script | `workspace/push/<name>NN.json` |
| Fixpoint + aiming map (where new records pay) | `root_audit.py` (refreshed after every table change) | `workspace/push/root_auditNN.json` |
| SAT margins / contact language | `sat_review.py` (run 28) | `workspace/push/sat_review28.json` |
| TAX/NRCI measures | `sat_measure.py` (run 29) | `workspace/push/sat_measure29.json` |
| D4 symmetry census | `symmetry_audit.py` (run 31) | `workspace/push/symmetry_audit31.json` |
| Run ledger (one section per run) | the agent, from the ledgers | `RUN_NOTES.md` + `notes/runNN_NOTES.md` |
| The forward map (remaining gap, priorities) | the agent, from root_audit + gap_analysis | `NEXT_STEPS.md` (3 synced copies incl. `download/`) |
| Reproduction commands per run | the agent | `REPRODUCE.md` (append-only `A<NN>` sections) |
| Delivery copies for the user | `deliverNN.py` | `download/runNN/` + `download/table.json`, `submission.csv` |
| Off-site durability | `git push origin main` | github.com/DigitalEuan/squares_in_squares |

### 2.3 Where the score comes from (source census of the run-32 table)

Script-computed (`gap_analysis.py` class census, startswith on `src`):

| Source class | All 1000 | Beats grid (543) | What it is |
|---|---|---|---|
| `grid` | 457 | 0 (tied) | the trivial ⌈√n⌉ grid — the ceiling every other class beats |
| `mishapolk` | 209 | 209 | run-30 import (221 rows applied; 12 were re-earned deeper by the channel and re-labeled — cascade 9, closure 3): verified bounds, exact certificates, centre-basis t = tan(θ/2) |
| `chain3` | 87 | 87 | L-extension band chains (base + free-band cells at L+1) |
| `exact` | 78 | 78 | Ellsworth survey SVGs (20–100 digit parse) |
| `run18-frontier` | 75 | 75 | community register import (run 18, the 76-record set) |
| göbel families (2/3/S) | 54 | 54 | G(a1,a2,b,c), clipped t-variant, strips |
| `removal` | 18 | 18 | removal windows from survey packings |
| `closure` | 18 | 18 | removal-closure to fixpoint (drop squares from larger m) |
| `aux` | 3 | 3 | auxiliary survey constructions |
| `register:T-263` | 1 | 1 | the run-26 exact import s(299) ≤ 17.8012385 |

---

## 3. Delivered state (verified Run 32)

| Quantity | Value |
|---|---|
| Submission score | **22.645991** |
| Grid ceiling | 28.937670 |
| Total improvement | −6.291679 |
| Puzzles beating the grid | **543 / 1000** |
| Grid-tied | 457 (of which **152 are proven floors** — see §1.1) |
| Open rows (attackable set) | **305** (measured by root_audit run 32) |
| Certification | 1000/1000 packings SAT-verified (pairwise non-overlap, bbox containment), 12-dp CSV round-trip, 2e-9 clearance |
| Leaderboard best (user-reported 2026-11-05) | 22.0544214515 |
| Gap to leader | **0.591569** |

Table invariants (all machine-checked by `scripts/gap_analysis.py`,
`scripts/root_audit.py`, and the round-trip in
`scripts/final_assembly.py` — re-verified this run on the recovered
tree: cascade 0 applied, closure fixpoint, assembly 0 issues, table
bit-identical):

- **Chain-envelope fixpoint**: 0 rows above the chain envelope (the
  root_audit audit; a hit would be a missed cascade conversion).
- **Monotone envelope**: L(n) ≤ L(n+1) for all 999 adjacent pairs — 0
  violations. (Run 12's "deletion lemma": no free improvement exists by
  removal alone; every below-grid value is earned.)
- **Shell law**: L(n + 2⌊L(n)⌋ + 1) ≤ L(n) + 1 — 937 checked, 0 violations.
- **Round-trip**: submission.csv read back from disk, every packing
  re-verified, score recomputed independently (run 32: 0 issues).

---

## 4. What works (the instruments that produce score)

1. **Sources beat search — by an order of magnitude.** The single biggest
   jump of the project (28.35 → 23.28) came from parsing the survey's 235
   record SVGs, not from an optimizer. Every score move since has been an
   import: the community register (run 18: 76 records, 0.050 + 0.064
   propagated), the T-263 record (run 26: +0.003559), and Mishapolk
   (run 30: 221 rows, −0.173983 — the largest single import of the
   project). The published catalogue (Ellsworth/kingbird) is **not** the
   frontier; the community register and Mishapolk's verifier-bounds file
   are.
2. **Analytic construction families.** Göbel strip/central-square
   (`gobelS`), the generalized diamond + staircase G(a1,a2,b,c)
   (`gobel2`, 17 beyond-catalogue finds at mid-band n), and the clipped
   variant G(a1,a2,b,c,t) (`gobel3`, 5 more). Families are exact,
   sweepable, and certifiable — and they beat the catalogue on the
   mid-band where no catalogue exists.
3. **Exact propagation.** Two closure laws, both verified to fixpoint:
   - *Removal closure*: removing squares never grows the bbox, so every
     n < m inherits L(m) (prefix-min envelope; `closure_apply.py`).
   - *L-extension chains*: a base (m, L) fills the free L-band at L+1
     with ⌊L+1⌋+⌊L⌋ cells, partial fills included (`cascade3.py`).
   The residue-family law makes this multiplicative: **one base at
   n₀ = (k₀−1)² + c opens the whole diagonal n = (K−1)² + c for all
   K ≥ k₀** (verified chain arithmetic: m_j = (j+k₀−1)² + c at L₀ + j).
   The channel absorbed the entire Mishapolk import (221 rows) with 12
   deeper re-earnings and 0 fixpoint violations.
4. **The honest gate.** Every applied state — imported or constructed —
   goes through `packlib.finalize` + SAT verification (pairwise separation
   on 4 axes, bbox containment, 2e-9 contact gap, 12-dp round-trip). The
   pipeline has never shipped a packing that failed re-verification.
5. **The measurement layer (runs 27–31).** The table is now inspected the
   way the physics is inspected: `root_audit.py` (fixpoint + aiming map),
   `sat_review.py` (contact language: 99% parallel; the T-263 family's 41
   floaters at Maxwell ratio 0.68), `sat_measure.py` (the SAT-TAX/NRCI
   regime map: the vacuum is exactly the grid rows), `symmetry_audit.py`
   (constructions symmetric, records asymmetric; G~depth +0.31 but weak).
   These instruments closed P1/P1'/P2 as measured nulls and point every
   future campaign at the aiming map's top rows.

The positive results point the same way as the failures (§5): everything
this project has ever scored came from **structure that already existed
as data** (survey, catalogue, community register, Mishapolk) or
**structure derived analytically** (families, closures). No search
campaign has ever produced a single applied improvement. That is the
design law of this system.

---

## 5. Failure ledger — what fails, and what each failure *literally* says

The project's failures are unusually informative; each one names the
thing that is required to go further. The ledger now lives in
**NEXT_STEPS.md §3** (failures 1–16, updated with runs 14–32): 1–8 are
the campaign failures of runs 1–13 (pressure-settling jams, LP closure,
mixed angles, level escalation, wheels, pocket-fill, θ-sweep, the G4
architecture ceiling); 9–15 are the discipline failures learned since
(documentation arithmetic, proven floors gating the aiming, retracted
theorems, untested greedies, correlations flipped by the Mishapolk
import). Failure 16 (run 32) is the third sandbox rollback of the
project (run 17 lost 9–16, run 19's chapter B lost the campaign files,
run 32 lost 28–31 locally): every time, recovery came from the GitHub
remote plus idempotent imports — and each incident surfaced something
durable (run 17: import idempotence; run 32: this STATUS rewrite). The
standing rules: *check the remote before reconstructing*, and *push
every run*.

---

## 6. The frontier map (where the remaining 0.592 lives)

### 6.1 Shape of the open set

The delivered table has a sharp shape per block (K = ⌈√n⌉, r = K²−n):

- **improved window**: n from the block bottom (K−1)²+1 up to about
  K² − (K+5) — fed by L-extension chains from bases below; depths taper
  0.48 → 0.02 across the window;
- **tied zone**: n from about K² − (K+4) up to K² − 3 — where all
  remaining score lives. **305 open rows** (root_audit run 32: 0 above
  envelope; 152 of the 457 tied rows are proven floors, so the attackable
  set is the 305);
- **proven optimal**: r = 0 (perfect squares), r = 1..4 (s(k²−1..4) = k,
  T-084/086/064/081), plus the individuals s(2..5), s(11), s(12), s(13),
  s(17), s(19), s(21), s(32), s(44..46), s(59..61), s(76..78),
  s(95..96) — 156 floors total in `root_audit.py`'s PROVEN_FLOOR.

The tied rows form **residue diagonals** n = (K−1)² + c, one per c; the
chain law converts within a diagonal, so **an improvement at any
diagonal's first open row opens the whole diagonal above it** — that is
the aiming map (per-diagonal best aim, aggregate 0.375304 at T-263
depth; best single aim c=32 n=356, value 0.011102, 14 conversions).

### 6.2 The gap decomposition (measured)

| | score | note |
|---|---|---|
| our submission (run 32) | 22.645991 | 543/1000 beat grid |
| leaderboard best (reported) | 22.0544214515 | |
| gap | **0.591569** | |

Closed since run 13: register import 0.050264 + propagation 0.013671 +
T-263 0.003559 + **Mishapolk 0.173983** = **0.241477**. A uniform depth
d\* = 0.0365 on the 305 open rows matches the leader exactly; the
leader's standing as a share of the open rows' area ceiling (5.005) is
11.8%. The aiming map says where a single record pays most: 0.375304
(63.4% of the gap) for one T-263-class record at every diagonal's first
open aim.

### 6.3 The two readings of the gap (unchanged in kind)

1. *Imports*: the band 325..1000 is no longer empty upstream (Mishapolk
   covers all 1000 n) — but our table now matches or beats Mishapolk
   everywhere, so the next move must be a **new** record landing
   upstream (P3 weekly watch: atlas + Mishapolk + Couzo + Karimi).
2. *Constructions at the roots*: the aiming map's top rows (356, 395,
   355 — every one at grid today). P1' closed these by null (runs 30–31:
   symmetric seeds 14/14, record-seeded insertion 3/3; the records' voids
   are a thin seam, not +1 space). If anything moves at the aims it will
   be an imported record (P3), not a construction or a settle.

---

## 7. External source landscape (checked 2026-11-06)

| Source | Status | Use |
|---|---|---|
| Ellsworth catalogue (kingbird) | live; 164 records; only 1 in 325..1000; not updated with autumn-2026 | historical baseline; SVGs in `workspace/svgs/` |
| Square Packing Atlas (evand) | live; certified best-known for n ≤ 324, exact rational certificates | `workspace/sources/atlas/`, `scripts/import_atlas.py` (weekly) |
| The Squares Project (jlevy/squares → squaremath.org) | live; the community register | the frontier to watch; paid runs 18, 26 |
| **Mishapolk/square-packing-records** | live; **verified bounds at ALL 1000 n** (upper_bounds.json) | paid 0.173983 (run 30); in the weekly loop (`fetch_mishapolk.py` + `import_mishapolk.py`) |
| Karimi preprint (read run 30) | two-strip packings at n ≥ 1184 (outside our range) + the **window theorem** (K ≥ 16: s(n) < K whenever n ≤ K² − 8√K − 19) | the certificate shape for our mid-band rows; watch for its construction moving below 1184 |
| Friedman survey (EJC DS#7) | stable | theory: proven values, families, lower bounds |

---

## 8. Run history (1 → 32)

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
| 13 | community register import + propagation + G4 test | 22.823536 | 76 records + 33 chain conversions; G4 architecture ceiling proven |
| 14–16 | (lost in the first sandbox rollback — see run 17) | — | no ledgers survive; re-covered at run 17 |
| 17 | **rollback recovery #1**: sandbox recycle rolled the filesystem back to the Nov-2 snapshot; runs 9–16 lost. Frontier re-recovered (22.823536, 454/1000): register re-fetch, import re-run **idempotent across the recycle** (76 applied, gain 0.050264 identical), gobel2 re-implemented from spec | 22.823536 | the recovery pattern is born: GitHub + idempotent imports |
| 18 | GitHub snapshot as system of record; cent_compiler v12_2 extension (W36/W37, 41 wheels); pressure-settle v2 (honest negative) | 22.823536 | 454/1000; sources re-verified twice |
| 19 | oracle study (E1 basin 0/10, E2 cold restarts) + 23-root campaign (0 finds, honest zeroes); **rollback #2** mid-campaign (recovered from GitHub); revalidation extras | 22.823536 | the settle-in channel cannot even hold a known solution |
| 20 | double-check verdict (run-19 "0 applicable finds"); the stall law (p ≈ 0.45–0.88·d); 132 template attempts, 0 finds | 22.823536 | infeasibility-proof program proposed |
| 21 | boundary demo, wheels census, clue ledger | 22.823536 | nulls; ledgers kept |
| 22 | soft relaxation — the pass-through channel (v1 SA 0/16 incl. controls; v2 hybrid: n=5 tight 4/16 hard hops, verified 2.708107 below grid; gap-throttled) | 22.823536 | named; needs a tight target to re-harden |
| 23 | submission audit + tightest ladder sweep | 22.823536 | P2 cells 0 finds |
| 24 | NEXT_STEPS.md execution | 22.823536 | map execution |
| 25 | P1 strip scan rerun + P2 remainder (52/52 cells) | 22.823536149 | both closed by null/capacity |
| 26 | P1(b) two-block, P1(c) census; T-263 import | 22.819978 | +0.003559; P1 closed |
| 27 | P4: root_audit.py instrument | 22.819978 | fixpoint true; aiming map born; 2 doc errors fixed |
| 28 | SAT data review (user input) | 22.819978 | contact language 99% parallel; T-263 floaters |
| 29 | SAT measure: TAX/NRCI (user input) | 22.819978 | vacuum = the grid rows; depth~φ |
| 30 | P2 renewal null + **Mishapolk import** | **22.645991** | −0.173983; 543 beat grid; root_audit refreshed |
| 31 | symmetry census (user input); P1' null | 22.645991 | constructions symmetric, records asymmetric |
| **32** | **recovery + documentation**: sandbox rollback found (runs 28–31 lost locally), recovered from the GitHub remote; channel + fixpoint re-verified (0 issues, table bit-identical); root_audit fixed (hardcoded run-27 gap printed 0.7656 stale); README/STATUS/NEXT_STEPS/RUN_NOTES/REPRODUCE to run-32 state; **STATUS.md now duplicates the README + system map (this file)** | **22.645991** | the remote is the durability line: push every run |

---

## 9. Guarantee

Every packing in `submission.csv` is re-verified from the file on disk
(pairwise SAT non-overlap with worst penetration ≤ 0, bbox containment,
per-n counts, id continuity 0..500499, 12-dp round-trip with ~2e-9
clearance). Imported packings carry their finder attribution in `src`.
Every lattice-mathematics claim in the Leech layer is integer-exact
(Λ16's kissing number 7320 is cited, marked as such). Optimality is never
claimed for any packing: the verified statement is always "improved over
the grid ceiling on N puzzles, certified". Every number in this file
comes from a script-computed ledger (§2.2); the sync between this file,
the README, and the live table is checked by `deliverNN.py` every run.
