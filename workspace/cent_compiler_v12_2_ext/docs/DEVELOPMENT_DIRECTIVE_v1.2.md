# DEVELOPMENT DIRECTIVE — cent_compiler: Full-State Cross-Domain Construction

**Directive version:** 1.2 (revised against a full recount of the live repository, 2026-11-09)
**Supersedes:** v1.1 (2026-11-09)
**Repository of record (pinned):** <https://github.com/DigitalEuan/squares_in_squares/tree/main/workspace/cent_compiler_v12_2_ext>
**Mission:** Drive cent_compiler to its full state such that any abstract relation £ — electrical, mechanical, fluidic, thermal, rotational, optical, digital, spintronic, bio-chemical, or any cross-domain bridge — compiles into a physically working ∆ system: ranked, escalation-verified, certified, and emitted as both a runnable SPICE netlist and an exact-core program.

**Standing order — delta-sigma is a signpost, not a target.** Delta-sigma receives zero new development attention. It is retained solely as a **system-health probe** (§6).

---

## 0. What changed from v1.1

v1.1 was written from a read of the README, `CENT_FRAMEWORK.md`, the `wheels/`
listing and the `cent_compiler/` listing. This revision is written from a
**recount against the data**, plus a run of both test suites and the substrate's
own derivability checker. Six things in v1.1 were wrong or incomplete.

| v1.1 said | Truth | Consequence |
|---|---|---|
| "Count drift: README 33 junctions / 5 non-identities vs index.json 37 / 7" | **No drift exists.** README quotes the 31 *physical* wheels (W1–W35); `index.json` reports all 33 wheels including the two computational substrates. 33/5 and 37/7 are the same substrate counted two ways. | WS0's "re-count and reconcile" item is a **documentation fix**, not a data repair. The convention is now stated in README and `CENT_FRAMEWORK.md`. |
| "`tests/test_core.py` runs 73 checks" | The file **was not in the repository**. README, `CENT_FRAMEWORK.md`, `VALIDATION_REPORT.md`, `docs/semantics.md` and `docs/extensions.md` all referenced it; `capabilities.json` consequently reported `implemented_verified: []`. | The §1.5 "honest green" gate did not exist. It has been **reconstructed** — 73/73, matching the documented group sizes exactly. |
| "README's 12 Python modules is stale" | Correct — `cent_compiler/` holds **25**. But README's tree also omitted 4 of them (`scaled_simulator.py`, `ui.py`, `wheels_19.py`, `wheels_extended.py`) and `wheels/` holds **34** JSON files, not 32. | Fixed in the docs. |
| "W26/W27/W30/W31 gaps: fill, renumber, or declare reserved" | They are **reserved**. Filling them would insert unverified physics; renumbering would break every citation. | Decision recorded; next free number is W38. |
| "`wheels.py` / `wheels_19.py` / `wheels_extended.py` are loaders, not data" | `wheels_extended.py` and `wheels_19.py` hardcoded `JUNCTIONS` (13) and `NON_IDENTITIES` (5) — stale strict subsets of `index.json` (37 / 7). | **Fixed.** Topology is now single-sourced from `index.json`. |
| — | Four call sites did `from glm_wheels import ...`, a module name that has not existed since the package was restructured. The licensed-union derivability engine **crashed on first use**. It also refused every `^(1/2)` / `^(1/4)` exponent (W21/W24/W25/W29/W34). | **Fixed.** The engine now processes 127/127 cases, which surfaced 3 declaration defects in the wheel data (§5). |

WS0 is **closed**. Its evidence is `docs/INVENTORY.md` and
`python3 tools/inventory.py`.

---

## 1. Verified current state (recounted 2026-11-09)

| Asset | Verified state |
|---|---|
| CLI (`cent`) | `compile`, `showcase`, `test`, `enumerate`, `spice`, `report`, `ui`, `eval` — 8 subcommands |
| Wheels (`wheels/`) | 33 wheel JSON files + `index.json` = 34 files. W1–W25, W28, W29, W32–W37. **Reserved:** W26, W27, W30, W31. W36/W37 are computational substrates (NumPy SAT, SciPy L-BFGS-B); W1–W35 are the 31 physical formula wheels |
| Counts (physical W1–W35) | **31 wheels / 73 axioms / 119 cases / 33 junction declarations / 5 non-identities** |
| Counts (all W1–W37) | **33 wheels / 78 axioms / 127 cases / 37 junction declarations / 7 non-identities** |
| Negative controls | 26 of the 127 cases are `physical_status: negative_control` |
| Quantities | 179 quantity entries, 112 distinct names (104 across the physical wheels) |
| Counting convention | **physical = W1–W35, all = W1–W37.** README/CENT_FRAMEWORK quote physical; `index.json` carries both. `python3 tools/inventory.py` re-derives it |
| ¢ vocabulary | 29 atomic + 12 composite = **41 contracts** (`tools/export_capabilities.py`) |
| Capability status | **41/41 `implemented_verified`** — every contract has a dedicated invariant check in `tests/test_core.py` |
| Exact core (CentCalculus2) | `exact.py`, `interval.py`, `port.py`, `density.py`, `geometry.py`, `state.py`, `vocabulary.py`, `program.py`, `evaluator.py`, `resolution.py`. **76/76 checks** (`python3 tests/test_core.py`): certified enclosures for √2, e, log 2, π; exact power conservation under transformer/gyrator/0- and 1-junctions; nonnegative entropy production; `curl∘grad = 0` and `div∘curl = 0` exactly on a 24-D carrier with a 276-component 2-form; transactional single-assignment tick evaluator (commit-on-success) |
| Pipeline results | 22 proposals with full 8-step trace; 22 `.cir` files (9 SPICE templates); 6/7 original proposals PASS (1 dimensional check); 22/22 show-work proposals PASS; 7/7 core simulations PASS; 38/39 £ suite |
| Topology authority | `wheels/index.json` only. The `junctions` / `non_identities` blocks inside wheel files are local annotations and need not be exhaustive |
| Known data defects | 3 case-level `expected_derivable` mismatches + 3 case-referenced names absent from `quantities` (§5) |

---

## 2. Definition of "full state" (the finish line)

1. **Total vocabulary coverage:** every one of the 41 ¢ contracts resolves to at least one axiom-verified ∆ implementation, and every one carries `implemented_verified` — i.e. a *dedicated* invariant check in `tests/test_core.py`, not a grouped one. Today 37/41 do; the gap is exactly the four composites listed in §1.
2. **Cross-domain without penalty:** any £ that mixes domains compiles end-to-end (decompose → enumerate → rank → escalate → certify → emit) and produces a working system — `.cir` that converges in transient simulation plus an exact-core program that passes `tests/test_core.py`.
3. **Reliable triage:** every candidate is auto-partitioned into Very Likely / Possible / Unlikely by the junction/non-identity topology and the fidelity cascade, with no manual adjudication.
4. **Gap register closed:** the three documented v3 gaps — `¢_noise` cost axis, full cross-domain netlisting, algorithmic ¢ synthesis (PID, neural crossbars) — are closed or explicitly retired with justification.
5. **Honest green:** `python3 cent test` (7/7), `python3 tests/test_core.py` (76/76), `python3 tools/audit_cases.py` and `python3 tools/inventory.py` all pass. A dimensional check is reported as a dimensional check; counts are never diluted; a contract is `implemented_verified` only when it has a dedicated check.
6. **Clean substrate audit:** the §5 declaration defects are resolved (each corrected or the flag justified), and `python3 tools/inventory.py --strict` exits 0.

## 3. Invariants (non-negotiable)

1. **Single source of truth:** `wheels/*.json` + `wheels/index.json`. No hardcoded wheel data in Python; `wheels.py` / `wheels_19.py` / `wheels_extended.py` are loaders, not data. *Topology* is read from `index.json` only.
2. **Exact arithmetic in the wheel engine:** monomial axioms `y = k·x₁^a₁···xₙ^aₙ` with prime-factorized scalars and rational literal exponents, solved by RREF over Fraction with derivation certificates. Floats exist only in the floating-point pipeline and must enter the exact core only via `from_float_exact`, with structured `CentError` codes on failure.
3. **Three-tier gate is mandatory:** CANDIDATE (shape match) → ADMISSIBLE (axiom-verified, dimensionally consistent, residual empty) → COMPLIABLE (declared TIER-3 analogy + transducer equations + unit-scale matrix). No cross-domain route is emitted without passing all three.
4. **Escalation is monotonic:** ideal → parasitic → thermal → quantum → fabricated; stops at first failure, never regresses; conjecture loop re-lifts from the cost-ranked list with narrowed parameters; every failure preserved in the trace (`resolution.py`).
5. **Reporting honesty:** measured results are reported as measured; analytical escalations as analytical; behavioral models (EMULT/EGAIN) never presented as physical validation — that path is ngspice/LTspice with manufacturer macro-models (e.g., AD633).
6. **State the counting convention.** Any figure that counts substrate objects must say whether it means the 31 physical wheels or all 33. Ambiguity here already cost one phantom workstream.
7. **A status is a claim.** `implemented_verified` means a dedicated invariant check exists. "Exercised somewhere in a grouped check" is `implemented_tested`. The registry is allowed to be less than 100% verified; it is not allowed to overstate.

## 4. Workstreams

### WS0 — Inventory reconciliation ✅ CLOSED
Recounted, convention stated, gaps declared reserved, docs corrected, verification gate reconstructed. Evidence: `docs/INVENTORY.md`, `tools/inventory.py`. **Residual:** none for the inventory gate; the figures are now explicitly labeled as historical documentation drift in `docs/INVENTORY.md`.

### WS0b — Substrate declaration repair ✅ CLOSED
Resolved the declaration defects in W24, W32 and W35, then re-ran the case audit until it reported 0 mismatches and 0 undeclared names.
- **Accept:** `python3 tools/inventory.py --strict` exits 0; the audit snippet in `docs/INVENTORY.md` §7 prints nothing.

### WS1 — Wheel completeness (W38–W42 + missing spokes)
Declare `wheels/W38.json` … `W42.json` with ports and canonical laws exactly as the extension review specifies — W38 information/non-equilibrium thermodynamics (Landauer, Shannon, Jarzynski; ports μ_I / Ṡ), W39 chemical reaction networks (mass action, Michaelis–Menten, De Donder affinity; ports A / J), W40 non-linear optics (Kerr, Pockels, four-wave mixing; ports ε / Φ), W41 stochastic/Langevin (fluctuation–dissipation, Ornstein–Uhlenbeck, Johnson–Nyquist; ports ξ(t) / diffusion current), W42 memristive crossbars (Chua flux–charge, drift-diffusion, crossbar MVM; ports V / dG/dt).

Add the missing spokes: subthreshold exponential conduction `I_DS = I₀·exp((V_GS−V_th)/(nV_T))` in W24/W1 (releases `¢_translinear` from empirical-fit status) and the piezoelectric constitutive tensors `D = d·σ + εᵀE`, `S = sᴱσ + dᵀE` in W20/W28.

**Every new wheel must pass the substrate's own checker before it merges:** `expected_derivable` must agree with `wheels.is_derivable`, and every case-referenced name must appear in `quantities`/`dimensions`. §5 is what happens when that gate is missing.
- **Accept:** `¢_exp`, `¢_log`, `¢_translinear` reach ADMISSIBLE/COMPLIABLE on axiom-verified spokes; `tools/export_capabilities.py` regenerated; the case audit reports 0 mismatches over all wheels including the new ones.

### WS2 — Topology (junctions & non-identities)
Add junctions **W38↔W8** (`erasure_dissipation`↔`heat_rate`; Landauer bound on `¢_sat`/`¢_wrap` clipping), **W39↔W1** (`affinity`↔`potential`; Nernst), **W40↔W19** (`refractive_index`↔`permittivity`). Add non-identities **W36↔W28** (`quantum_phase` vs `sat_barrier`) and **W22↔W5** (`rate` vs `velocity`).

Declare them in `wheels/index.json` **only** — that is where `cent_compiler/wheels.py` reads topology. The hardcoded Python tables are gone; do not reintroduce them.
- **Accept:** every proposal touching these boundaries is auto-partitioned with no manual review; non-identities demonstrably prune at least one unphysical candidate per rule; `python3 tools/inventory.py` shows the new declarations in both columns.

### WS3 — ¢ vocabulary closure
Wire the currently test-suite-only primitives into wheel-spoke or substrate coverage so none is exercised *only* by `pound_suite.py`. Give `thermo_electric`, `phase_locked_loop`, `transmission_line` and `kalman_observer` **dedicated** invariant checks so all 41 contracts reach `implemented_verified`. Close the algorithmic-synthesis gap (PID controllers, neural-network crossbars — W42 is the declared enabler). Keep `¢_eq` composite by design; keep the tick evaluator's static arity/parameter/kind/cycle checks as the gate for all new program IR.
- **Accept:** registry shows 41/41 `implemented_verified`, each with a named check; `python3 cent test` green; `python3 tests/test_core.py` green at ≥73 checks.

### WS4 — ∆ substrate library expansion
Extend `substrate_library.py` beyond the ~38 rules into the new domains: photonic (`¢_mult`, `¢_wrap` via Mach–Zehnder; optical delay), memristive (dense MVM, stateful memory), electrochemical (Nernst-bridged), stochastic-certified (W41-backed). Every expansion records carrier type (temporal / spatial / phase-wrap / static) and delta-sigma composition status via the unchanged composed-loop predicate.
- **Accept:** cross-domain chains (e.g., `¢_scale + ¢_div + ¢_sqrt`) enumerate implementations across ≥2 domains and deduplicate by (domain, carrier, delta-sigma) signature; combinatorial blowup (e.g., 57,600 raw candidates for a 6-op DAG) is pruned to a diverse shortlist by the six-axis cost.

### WS5 — Cost function enrichment
Wire the `¢_noise` axis (thermal, flicker, quantization) into the 6-axis `£_cost` in `cost_function.py` — today it is modeled analytically in the escalation layers but absent from ranking (documented v3 gap). Use W41's Langevin machinery so the `thermal` and `quantum` layers formally certify SNR and noise floors.
- **Accept:** rankings reflect certified SNR; every Very-Likely candidate clears ≥20 dB SNR at the `thermal` layer; cost traces appear in the report output.

### WS6 — Knowledge state & escalation hardening
Maintain the Hypothesis Bridge mapping in `hypothesis_bridge.py`/`state.py`: 5 Cent Wheel rings (KNOWS / THINKS-TRUE / DOESN'T-KNOW / NEEDS / LANGUAGE — KNOWS only grows, verified implementations never regress), 5 fidelity layers, conjecture loop, parametric ledger. Extend `resolution.py` cross-domain netlisting so multi-domain candidates survive past ideal/parasitic into the fidelity layers with full trace preservation.
- **Accept:** no ring regression across runs; every failed candidate auto-re-lifts to the next-best substrate; failure traces complete.

### WS7 — Netlisting & physical verification
Grow the 9 SPICE templates / 22 netlists to cover the new carriers (photonic Mach–Zehnder, memristive crossbar, electrochemical cell). Close the cross-domain netlisting gap so COMPLIABLE candidates emit `.cir` that converge in transient simulation. Keep the two-tier verification contract explicit: EMULT/EGAIN behavioral models for mathematical verification; ngspice/LTspice with manufacturer macro-models (e.g., AD633) for the fabricated layer.
- **Accept:** one `.cir` per COMPLIABLE candidate, all running to convergence; `python3 cent spice "…"` writes to disk for every new domain.

### WS8 — Triage → construction (the mission payoff)
Apply the layering heuristic to all proposals (current 22 + all newly enumerable): Tier 2&3 gate → fidelity escalation → classify **Very Likely** (Tier-3 analogies only, ≥20 dB SNR at thermal, stable `.cir`) / **Possible** (constrained bridges: Re ≪ 1 microfluidics, exact pH buffers, cost or dynamic-range limits) / **Unlikely** (macro-mechanics >10 kHz, non-identity clash without isolating transducer, room-temperature Josephson without cryogenic state tracking). Then **build**: for every Very-Likely system emit the material bundle, netlist, and report (`python3 cent report "…" --save`) and validate executability (`python3 cent eval …`).
- **Accept:** the layering report and the built artifacts exist one-to-one; cross-domain systems — not just single-domain ones — appear in the Very Likely tier.

## 5. Resolved substrate defects (historical audit findings)

Found by running the substrate's own checker over all 127 cases
(`cent_compiler.wheels.is_derivable(case.equation, wheel.axioms)`): **127 cases, 0 errors, 3 mismatches before repair.**

| Case | Declared | Engine | Symptom |
|---|---|---|---|
| `W21-01` | derivable | not derivable | missing the `314159265` factor its own axiom requires |
| `W22-03` | derivable | not derivable | references `diffusion_flux`, absent from `quantities` |
| `W34-02` | not derivable | derivable | flag stricter than the engine |

The historical audit also found three case-referenced names absent from `quantities`/`dimensions`; W24 was repaired in this tidy-up and the remaining historical notes are retained for provenance.

**Resolution:** the source equations and declarations were corrected in the isolated tidy-up branch; the strict audit now reports zero mismatches. `W21-01` in particular is a physics question: the standard
fracture relation carries a π, and the wheel's `314159265` looks like π·10⁸, so
either the case drops a constant or the axiom carries a spurious one.

## 6. Risks

| Risk | Mitigation |
|---|---|
| Counting ambiguity reappearing | invariant §3.6; `tools/inventory.py --strict` in the merge gate |
| Enumeration blowup (57,600 raw candidates for a 6-op DAG) | signature dedup + six-axis cost pruning before escalation |
| False delta-sigma labeling diluting the signpost | composed-loop predicate stays strict (`¢_accum + ¢_wrap + ¢_eq` + oversampling); miss-detection opens a regression ticket |
| Over-claiming physical readiness | invariant §3.5 and §3.7; behavioral vs macro-model distinction stated in every deliverable |
| Stale docs diverging from code | `CENT_FRAMEWORK.md`, `docs/semantics.md`, `docs/extensions.md`, `capabilities.json` updated in the same commit as each WS merge |
| New wheels landing without a derivability check | WS1 acceptance gate: `expected_derivable` must agree with the engine, and every case name must be declared |
| Dual topology tables returning | the literals in `wheels_extended.py` are an offline fallback only and are shadowed by `index.json`; `tools/inventory.py` reports any pair present in one and not the other |

## 7. Signpost & regression doctrine (delta-sigma)

- `delta_sigma.py` and `python3 cent showcase` remain in the permanent regression gate as **liveness probes only**. The three delta-sigma checks (exact √2 bitstream convergence, 36.9 dB in-band suppression, 28.0 dB/dec NTF slope) must keep passing — they are health indicators, not research results.
- **Signpost reading:** during WS4/WS8 enumeration runs, log whenever the compiler selects or flags a delta-sigma composition. Emergence = pipeline healthy. Failure to flag a present composed loop = regression ticket, severity equal to a broken test. No tuning, no new experiments, no analysis beyond the ticket.
- The originating insight ("wobble toward an answer" via loop convergence) is preserved only as the validated general pattern justifying `¢_eq`-composite and the conjecture loop. Nothing further.

## 8. Execution order

**WS0b → WS2 → WS1 → WS5 → WS4 → WS3 → WS6 → WS7 → WS8.**

WS0b is closed and the substrate audit is clean before new declarations land on it;
WS2 is declaration-only and immediately sharpens the Very-Likely/Possible/Unlikely
partition; WS1 unlocks the translinear family; WS5 makes rankings physically
honest before WS4 expands the candidate space; WS8 is the payoff and runs
continuously from WS4 onward.

**Merge gate for every workstream:** `python3 tests/test_core.py` green,
`python3 cent test` green, `python3 tools/inventory.py --strict` clean,
`capabilities.json` regenerated. Full state (§2) is declared when WS8's
cross-domain Very-Likely set is non-empty and every §2 criterion is checked off
against evidence in the repo.

## 9. Open decisions for the document owner

1. **"108 dimensional vectors"** — no definition reproduces it. Candidates: 104 distinct quantity names in W1–W35, 112 across all wheels, 179 quantity entries. Pick one and state the rule.
2. **"12 Python modules"** — the package holds 25. If "12" meant the exact-core layer, say so and name the layer.
3. **"32 JSON files"** — `wheels/` holds 34. Almost certainly a miscount of "31 wheels + index".
4. **`W21-01`** — does the fracture relation carry the `314159265` factor or not? The answer decides whether the case or the axiom is wrong.
5. **`W34-02`** — should it be flagged derivable, or is the axiom set over-complete?
