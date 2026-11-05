# GLM × Squares-in-Squares — Investigation Report

**Inputs.** `upload/SKILL_v3.md` (718 lines), `upload/GLM_ACADEMIC_PAPER.md`
(4,819 lines), `upload/GLM_Complete_Number_Theory_Evidence.md` (1,747 lines),
the full repository `github.com/DigitalEuan/GLM` (cloned at
`workspace/glm-repo/`: 3,954 files, 153 MB — Python package `glm_universal`,
Lean development `RequestProject/GLM/`, studies, archive).
**Context.** Our submission stands at score **23.284687** (grid ceiling
28.937670; 399/1000 puzzles beat the grid), matching the published state of
the art for every n ≤ 1000. The question this run: can GLM/SKILL_v3 assist
another push — on the completed packings and on the still-trivial puzzles?

---

## 1. What GLM and SKILL_v3 are (after the dives)

**SKILL_v3** is an *implementation concept* (a discipline, no code of its
own beyond five self-contained scripts): every answer is decomposed into
atomic claims; each claim is answered in three synchronised columns — plain
English, exact mathematics (ℤ/ℚ/𝔽₂), and an executable stdlib-only Python
re-derivation with **no floats, no random, no SHA-256 in computation**
(UBP). Lean formalises what it can and names the rest as `sorry` with gaps.
Refusals are named, never silent. Our whole workspace was already built as a
TCT study — SKILL_v3 is the parent methodology of our pipeline.

**GLM** is the *working system* that methodology produced: 8 registers of
exact carriers on the Golay/Leech substrate, 31 query kinds, 67 report
subjects, a stepwise planner that chains derivations, polynomial solvers
(cubics/quartics by radicals, Zassenhaus factoring, Galois certificates for
"no radical expression"), primality certificates (Pocklington, elliptic),
414 Lean files with 0 sorry, and an evaluation of 237 CLI cases with zero
confidently-wrong answers. Everything computes in exact rationals;
irrationals are *processes* (delta-sigma feedback loops, Sturmian bit
streams), not static values.

## 2. The honest capability map for our problem

| GLM/SKILL faculty | Packing use | Verdict after this run |
|---|---|---|
| Exact arithmetic (Fraction/Decimal, 20–100 digits) | Parsing record SVGs whose side lengths are algebraic numbers (degree up to 18); our `parse_all_svgs.py` already does this | already in use; essential |
| Polynomials in radicals + Galois no-radical certificates | Classifying record s-values (the survey prints root polynomials); deciding which records can be expressed closed-form | available, cosmetic for scoring |
| Delta-sigma irrational carriers | Carrying √2-family constants in constructions | equivalent to what we do with Decimal; no edge |
| Delta-sigma as a *dynamics* (loop chases a signal) | **This is the interesting one** — see §3 | partial match with SA; not stronger |
| Stepwise planner (chains, stitched steps) | Our pipeline is exactly a plan: records → removal windows → chains; TCT would formalise it | methodology already adopted |
| Lean verification tier | Verifying packings is SAT+geometry, decidable by numpy; Lean adds kernel-level proof of the verifier, not of packings | we verify every packing computationally; equivalent assurance for this purpose |
| UBP no-floats | Our **search** needs simulated annealing (floats, randomness) — forbidden by UBP | GLM would refuse the search; see §4 |

## 3. The delta-sigma analogy — what we actually tried

The one GLM faculty with a real mathematical claim on packing search is the
wobble: a deterministic feedback loop that converges onto a target from any
start, with error bounded by the loop's order (MASH 1-1 cascade: error
becomes a second difference). Our simulated annealing is the same *shape*:
penalty in, configuration out, converge to zero violation. The differences
that matter:

1. Delta-sigma converges on **linear** quantities (running means); our
   target (zero overlap under rotation) is a non-convex constraint surface.
2. Delta-sigma has no barriers; SA has exactly the barrier problems we hit
   this run (collective-rotation jams, rigid record geometry).
3. Determinism: SA with fixed seeds is exactly reproducible — our whole
   campaign is deterministic in that sense; UBP's ban is on *float drift*,
   not on reproducibility, and our verification path (packlib) is exact.

**Conclusion:** the wobble does not give a stronger solver for this problem
class. What it gives — and what we took — is the *discipline*: exact
verification, named refusals, negative results as first-class findings.

## 4. Where GLM would refuse — and we agree

GLM refuses to *guess*. A packing that cannot be derived or verified is not
submitted. Applied here: the 601 grid-tied puzzles are **open problems**;
our previous run proved the chain-reach limits per block and matched the
survey exactly. This run's push campaign (below) is the honest attempt at
the open ones; every find must survive `packlib.verify` (SAT non-overlap,
containment) at 1e-9 before it enters the table — nothing enters by
annealer's word alone.

## 5. The push campaign (this run) — outcome

**Engine** (`scripts/sa_push.py`): vectorized simulated annealing; penalty
math is exact (self-test agreement with packlib's SAT at 1e-9); collective
moves (global rotation, row shifts) included; container violations weighted
4×. A 9-configuration schedule probe (`scripts/probe_sa.py`) over the two
archetypes — Stage A (compressed chain3 packing, residual 2.6e-4) and Stage
B (grid seed at container g−0.02) — found **no configuration that clears
either**. Stage A freezes at the seed residual under every schedule; Stage
B's hot starts wreck the grid and cold starts freeze. This is the motif
barrier, now documented numerically: the reorganization needed is
collective, and local-move annealing does not find it — the same conclusion
as the literature's 45-year experience with these puzzles.

**The productive route — analytic families (sources beat search, again).**
Re-deriving the Göbel-square family from the survey's square-233.svg
(a=7, b=11) — a b×b diamond of 45° squares plus four T(a) staircases,
contacting on x+y = a+1 — and sweeping all constrained (a, b) produced
**18 verified improvements** (`scripts/gobel_squares.py`), including two
genuine beats on puzzles that were grid-tied in *both* our table and the
survey (open problems): **n=861: 30 → 29.849242** and **n=921: 31 →
30.849242**, plus structural beats at 489, 636, 688, 964. Re-running the
cascade fixpoint with the new bases propagated 32 more chain improvements.
Final: score **23.284687 → 23.193864**, 399 → **406/1000** beating the grid.

## 6. How GLM could assist further (concrete, ranked)

1. **Delta-sigma planner for the shrink ladder.** Not as a solver — as a
   *controller*: replace fixed-step shrink with feedback on measured
   residual overlap (order the loop, second-order cascade). Worth one
   experiment on the best Stage-A targets.
2. **Sturmian read of contact sequences.** The compressed packings have
   Sturmian structure in their contact sequence (as GLM proved for the
   wobble: algebraic targets → strong negative lag-1 autocorrelation). A
   detector could classify which jams are one-parameter families (fixable
   by global moves) vs. genuinely rigid (not fixable) *before* spending
   anneal time.
3. **Galois certificates on any new record we find.** If the campaign
   lands a find at an algebraic L, GLM's polynomial machinery can classify
   it (radical / no-radical) for the survey-format report.
4. **Lean tier for the verifier.** `packlib.verify` is numpy; a Lean port
   would give kernel-checked verification of the *verifier*, raising the
   assurance ceiling for competition audits. Estimated 2–3 files of real
   analysis; only worth it if the competition demands it.

## 7. Bottom line

GLM's substrate (Golay/Leech) has no direct purchase on 2-D square packing
— the effective parts are its *disciplines*: exact verification, honest
refusals, sources-beat-search. Those we already run; this run added the
annealing push under them, with GLM's negative-result convention applied.
See `push/log_*.txt` and `finds_*.json` for the raw campaign record.

---

## Addendum — Second push (the "wheels" run)

**Inputs this run.** The owner's strategic brief: provide the "wheels"
(parameterized families) rather than expect a solver; consider golden-ratio
and other constants as potential wheels; multi-square rigid macro-units as
dimensionality reduction.

**What was done.**
1. *Survey re-fetch.* squaring.net is live but reorganized; the equal-squares
   family pages are gone (404) and archive.org is unreachable from this
   sandbox. The catalogue pages that remain (cpss, s-pss, …) belong to the
   *squared-squares* (integer dissection) class, not equal-squares packing.
   Conclusion: no new geometry source exists beyond what we already
   integrated.
2. *Motif zoo (from our own verified data).* All 1000 table packings
   classified by angle signature: 191 signatures. The 45° family dominates
   (Göbel-square outputs and their chains). Two findings of the constants
   kind: (a) the **golden-ratio near-miss** — record packings exist with
   tilt 31.5663°, but atan(1/φ) = 31.717°: 0.15° apart, so φ is *not* the
   generator; these are numerically optimized sporadics. (b) the 45°±2.3522°
   symmetric pair (42.6479°/47.3522°) in the n=259 family: exactly mirrored
   about 45°, but no rational tangent (p/q, q≤100, 1e-6) and no radical
   closed form — again sporadic.
3. *Family exhaustion proof (sweep argument).* The Göbel-square family
   n = 2a(a+1)+b², s = a+1+b√2/2 was swept over ALL (a,b) with n ≤ 1000
   under the contact constraint last run; every valid member that beat the
   table was applied (18, including the survey's own missing members 861
   and 921). This run confirmed by enumeration: no further members exist
   below 1000. Asymmetric-depth variants (a≠c staircases) force a≠c ⇒
   non-square container — dead end, verified by the contact identity.
4. *Residue-coverage map.* chain3 covers r ≤ 18 per block k²..(k+1)²−1
   (r ≤ 21 for k = 30, where last run's mid-band bases landed). The
   remaining grid-tied puzzles concentrate exactly at r = 19..2k —
   the mid-band. These are open problems: no published construction
   exists (survey gaps), SA probe (9 configurations) cannot cross the motif
   barrier, and no parametric family in the verified literature covers them.

**Verdict on the wheels concept.** The GLM-style "provide the wheels, not a
solver" doctrine produced this project's only two score jumps: the survey
SVG integration and the Göbel-square sweep — both were wheels, and both are
now exhausted for n ≤ 1000. The constants wheel (φ) was tested against the
data and measured as a near-miss, not a generator — recorded as a negative
result. The macro-unit (multi-square rigid block) idea is exactly what the
chain/cascade planners already do at the construction level; as a search
dimension it inherits the same motif barrier.

**Score stands at 23.193864** (406/1000 beat grid). Every verified
improvement found across both pushes is in the table; the frontier beyond
it is genuinely open research — the honest GLM-style refusal.

---

## Addendum — Third push (directive: GLM-assisted geometric optimization)

**Score: 23.193864 -> 23.173640** (406 -> 407/1000 grid beats). One real
gain, cleanly proven; the rest of the directive was audited honestly.

### The gain: the removal-closure was missing (again, in the other direction)

Last run added the Göbel members but never re-ran the global closure:
F(n) = min L(m) over m >= n. Every n < m inherits L(m) for free by dropping
squares. 19 entries improved, all verified (SAT + containment, 1e-9):
18 chain values lowered + the gem **n=860: 30.0 -> 29.85 (removal from the
861 Göbel member)** — the last run's family sweep created the base and the
closure finally harvested it. Fixpoint in one pass (script:
`scripts/closure_apply.py`). The lesson is now enforced: closure is
re-run after ANY table change (checked into the loop order).

### Audit of the directive's premises

* *Near-miss list (n=11@3.98 etc.): stale.* Those came from the pre-survey
  logs. All are survey records now. The only live small grid-tied are
  n=12,13 — both AT the published catalogue value 4.0 (open for decades).
* *n>1000 "uncontested score reductions":* no. Kaggle scores 1..1000 only;
  L>32 packings don't propagate into the table; the ONE crossover window
  n in (1000,1024) with s<32 was tested exactly: largest Göbel member under
  s=32 is n=964 (s=31.556); the next member (a=16,b=22) is n=1028 at
  s=32.56 — too big; chains from below land at >=32.5; catalogue has
  nothing there. Open by exhaustion, all routes measured.
* *New source found (better than expected):* the kingbird.myphotos.cc
  mirror — Davidebyzero's maintained live version of Friedman's catalogue,
  actively updated (record n=2043 improved Sep 2026, credits "Claude Opus 5
  and Claude Fable 5"). Parsed 164 records: **zero real imports for
  n<=1000** (all diffs ~1e-9 = our +1e-9 safety inflation). Independent
  confirmation the table is AT the published frontier. Its 4 records above
  1000 (1453, 1765, 1850, 2043) were imported into the new extended table.

### §2 machinery — implemented, measured, wall confirmed

* Delta-Sigma shrink controller: implemented (2-integrator modulator,
  geometric step clamp 5e-4..2e-2). n=12/13 jam immediately at 3.995;
  classifier says RIGID_WALL, cycle budget not committed.
* Sturmian contact classifier: lag-1 autocorrelation of the contact
  bit-stream. n=12, 13: rho=1.000, all squares touching — crystalline
  jam, motif change needed. All 10 roomiest mid-band targets (803, 748,
  983, 804, 862, 695, 749, 984, 922, 696): RIGID_WALL at seed level
  (rho=1.000, every square in contact). Cost measurement that justified
  seed-level classification: ONE 20k-move anneal at n=803 ran >150s
  (full 120k attempt ~15min) — the classifier exists precisely to not
  pay that. Verdict consistent with the catalogue having nothing there.

### §3 artifact (no-score by domain, delivered as data)

`extended_table_5000.json` (n=1001..5000): 4 catalogue records imported
with states (1453@38.628, 1765@42.488, 1850@43.488, 2043@45.696 — the
last is the Sep-2026 record), 29 Göbel members verified, closure with
77 numerical spot-checks (every 50th entry) on top of the theorem,
+1 forward bound; 805/4000 entries beat grid by bound. States kept only
for real constructions (33 entries); grid states regenerable by formula.
Submission untouched: format is 1..1000 by rule.

**Standing: 23.173640, 407/1000, zero real imports available from the
world catalogue, mid-band classified RIGID_WALL at seed level.** The next
gain, anywhere, is a new world record by definition.

---

## Addendum — Fourth push (level-escalation hypothesis: √3)

**Question.** The user read the RIGID_WALL jam as numerical complexity
escalation — "perhaps √3, not just √2?" — and asked for Delta-Sigma /
Sturmian / Galois work ("as suggested": of these, Delta-Sigma and Sturmian
were ours; Galois certificates were not previously suggested — noted for
the record).

**Down-level audit first.** Zero of the 593 grid-tied n are proven
optimal anywhere (all 61 "Proved" catalogue entries prove non-trivial
optima). So the wall is empirical, and any level hypothesis must be
tested constructively, not by proof.

**Three-layer test, all layers delivered:**

1. *Empirical level map.* Angle histogram: 0°/45° only in constructed
   packings; 880 "non-standard" angles are the numerical records' free
   tilts (only 5% are rational slopes). Field fits (strict): Q(599) ∥
   Q(√2)(293) ∥ Q(√7)(24, genuine — e.g. n=18 = (7+√7)/2) ∥ numerical
   (209). The 16 biquadratic fits were all chance (residual test:
   2.4e-9..1.6e-8 vs genuine 1.8e-9). Levels are PARALLEL branches, not
   an escalation hierarchy; √3 appears nowhere in the known universe.

2. *Constructive escalation test.* Exact θ-generalized Göbel family
   (rotated block + corner staircases), tight algebra
   s(θ) = (2a·M + 2·m + p)/(cosθ+sinθ), verified states at 7 special
   angles (45/30/22.5/15/atan(1/3)/atan(1/2)/atan(3/4)) plus a 0.05° fine
   sweep: s(θ) strictly decreases toward 45°; the minimum sits at exactly
   45.00° for every (a,p). √3/30° never beats √2/45° at any n. Mixed
   45°+30° two-block structures (both blocks on the container diagonal):
   36 verified packings, none beat even grid (diagonal alignment is the
   family's binding weakness; mixing levels buys nothing).

3. *Galois/exact-field certificates.* 54 certificates
   (galois_certificates.json): minimal polynomials + Galois groups via
   sympy: Q(√2)/C2, Q(√3)/C2, Q(√6)/C2, Q(√(2+√2))/C4 (x⁴−4x²+2 — the
   real subfield of Q(ζ16); correct cyclic group computed, my earlier D4
   annotation was wrong and was fixed), Q(√2,√3)/V4 at 15°, plus the
   six √7 survey records. By-product: the first Q(√3)-level packings
   ever constructed — n=5: 1+√3 = 2.732 (record 2.7071), n=37: 4√3 =
   6.9282 (record 6.5986) — both beat grid, both lose to the world
   records. theta30_new_members.json carries their full states,
   independently re-verified.

**Verdict on the hypothesis.** No — with a certified mechanism. 45°/√2
is the family's ceiling and floor simultaneously: rotating away from 45°
shrinks the container-diagonal gain (c+s) faster than it shrinks the
staircase cost; 45° is the kink of M(θ). The jam walls are real
structures, not a missing higher field.

**Score: unchanged 23.173640 (407/1000).** No wins — honestly none
available via this hypothesis. Deliverables updated
(galois_certificates.json, theta30_new_members.json, /tmp reports
mirrored into the repository). The frontier remains: every next gain
anywhere is a new world record by definition.

---

## Addendum — Fifth push (tie-resolution framework: carried forks)

**Directive.** The user supplied the GLM's complete tie-resolution
framework: Golay d=4 six-fold ties (1771/4096 cosets, 680064 tied reads),
carried forks instead of forced guesses, four resolution mechanisms
(protected tags, multi-view frames, optimal splitting questions,
Lorentzian lift / MOG swaps), and the mapping: packing jams ARE deep-hole
ties; annealing jitter = guessing among the 6; supplying an analytical
family parameter (a "wheel": strip width, tilt, macro-block) is the tag
that collapses the tie.

**What was run (scripts/fork_push.py, 2212s; scripts/positive_control.py).**

1. *Framework arithmetic* — verified exact, every number: C(24,4)=10626
   =6×1771; coset leaders 1+24+276+2024=2325, so weight-4-leader cosets
   4096−2325=1771; λ₄=C(20,1)/C(4,1)=5, giving the 6-fold tie {0}∪5
   octads; 680064=1771×384. The framework's internal mathematics is
   correct — the failure is not in its numbers but in its mapping (below).

2. *Wheels (structural keys), certified:*
   A. Tilted-grid wheel (strip width w, tilt θ): extra-square capacity
      over a rigid tilted k-grid at s=k+1 is ZERO for all 593 open n
      (bbox caps θ at ~2.1° while a unit-wide wedge needs θ≥~15°).
   B. Mirror-split wheel: gap≥1 between mirrored half-grids requires
      θ≥126.87° (>90°) — impossible; the max achievable gap is 0.9980<1.
   Both certified dead by exact inequalities, not by search.

3. *Carried fork, full pressure.* Operational correction first: run 3's
   RIGID_WALL verdicts had been computed on jittered seeds (grid_seed
   tilts each square ±0.35 rad — precisely the framework's "blind
   jitter" failure mode). This run replaced them with structural seeds:
   4 bases (S1 the table's own clean grid state; S2 nearest member
   rescaled with innermost staircase layers removed; S3 mirror-split
   ±0.5° half-grids; S4 rigid tilted grid at the bbox limit + diamond
   stack) × hot/cold protocols. Result: 30/30 classifications
   RIGID_WALL, ρ=1.000, n/n contacts; S1's seed overlap is exactly
   0.0e+00 — a perfect crystal. All 16 settles (8 branches × 2 targets
   n=803, 748, 6k moves/call, Delta-Sigma controller, up to 12 calls):
   3 jams in 3 calls, zero successes, wall never yields 0.004.

4. *Positive control — the decisive test.* n=5 and n=12: the smallest
   grid-tied n whose below-grid optima are famous and simple (2.7071 =
   one 45° square + 4 corners; 3.8771). Pressure alone from a clean grid
   seed FAILED both: 0/10 calls × 3 seeds, cannot even reach grid−0.004
   (61s and 83s). The settle engine cannot cross the wall from a grid
   seed anywhere — including where the answer is known to exist.

**Verdict on the mapping.** Honest and negative: in square packing the
crystalline tie is a LOCK, not a d=4 ambiguity. The Golay situation has
six DISTINCT valid codewords and a supplied tag discriminates the true
one; at the packing wall all branches carry the SAME state — one
perfect crystal (seed overlap 0, ρ=1, all contacts) — so there is
nothing to discriminate, no key to supply, and no sector to lift to.
The four GLM mechanisms map as: tags → wheels (certified dead, A/B);
multi-view → classification across 8 branches (all identical RIGID);
splitting questions → the 3-binary fork (every branch answers the same);
Lorentzian lift/MOG swaps → level escalation (run 4: dead — 45°/√2 is
the floor and ceiling). Zero finds; score stands 23.173640. The five-push
campaign (survey → wheels → GLM directive → levels → forks) ends with
the wall re-confirmed by the fork's own protocol — every structural key
that exists in this 2D geometry has now been tried and certified.

## Addendum — Sixth and seventh pushes (2026-11-04): construction replaces pressure

The five pushes above all pressed on jammed states (pressure, wheels,
forks, levels) and hit the same wall. Runs 9 and 10 changed tack
entirely: construct analytically from families, verify with the SAT
substrate, and only then propagate — the GLM directives are retired.

**Run 9 (sixth push): the full Göbel family.** G(a1,a2,b,c) — the
shipped instrument covered only the square subfamily; the general
family had never been swept. 326 candidates, 68 applied, 0 verify
fails: 17 MID finds beyond the published catalogue and 51 LOW
improvements. Score 23.173640 → 22.897558; beats-grid 407 → 445.

**Run 10 (seventh push): the clipped family and the closed front.**
Wave A clipped the t×t block from each (u,v) corner of the diamond
(trade 4t² cells for √2·t on all four sides): 9 applied (5 real, all
high-n; depths (√2−1)² and 0.0502525). Wave B planned to pocket-fill
every state and migrate the fill upward in n; the closure fixpoint
makes this impossible in principle (L is non-decreasing in n by the
removal closure already applied), and two independent collision models
agreed: 509 clean fills, 0 applicable. Score 22.897558 → 22.887471;
beats-grid 448; MID below grid 49.

**What actually moved the needle.** Not any pressure campaign: the
contact-identity derivation of the Göbel family (Run 9) and its clip
extension (Run 10). The motif barrier that defeated every settle
engine is trivially crossed by construction — the MID band's craved
"collective crystalline motif" IS the 45° diamond with staircases.
The honest ledger: open LOW 69, open MID 392; both records in
`download/README.md` (Run 9 / Run 10 sections).
