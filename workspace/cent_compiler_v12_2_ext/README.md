# cent_compiler v2.0 — The £ → ¢ → ∆ Physical Compiler

A cross-domain physical compiler with a **living knowledge base**. Takes any abstract operation £, decomposes it into atomic ¢ steps, enumerates all valid physical ∆ implementations, escalates through 5 fidelity layers, and emits a SPICE netlist for the chosen ∆.

**Delta-sigma is the canonical carrier for irrational numbers** — one valid ∆ among many, recognized via a composed-loop predicate (not a property of any single substrate).

---

## Quick Start

```bash
cd cent_compiler_v12_2_ext

# Compile a £ through the full pipeline
python3 cent compile "velocity = (2 * energy / mass)^(1/2)"

# Interactive console: enter a £, read ¢ primitives, ∆ ranking and material
python3 cent ui

# One-shot report; --save writes the material bundle, netlist and report
python3 cent report "velocity = (2 * energy / mass)^(1/2)" --save cent_out

# Run the generated exact-core program
python3 cent eval cent_out/velocity.material.json --set energy=8 --set mass=1

# Run the delta-sigma flagship showcase
python3 cent showcase

# Run all tests
python3 cent test

# Emit a SPICE netlist (writes .cir to disk)
python3 cent spice "y = sqrt(5)"

# Enumerate all ∆ for a £
python3 cent enumerate "y = sqrt(5)"
```

---

## System Statistics (v2.0)

**Counting convention.** The substrate holds two kinds of wheel. *Physical
formula wheels* (W1–W35) carry monomial axioms and dimensional vectors;
*computational substrate wheels* (W36 NumPy SAT, W37 SciPy L-BFGS-B) carry a
numerical method instead of a law. The table below counts the **31 physical
wheels**; `wheels/index.json` additionally reports the 33-wheel totals. Both
are correct — see `docs/INVENTORY.md` for the full reconciliation and
`python3 tools/inventory.py` to re-derive it.

| Metric | Value |
|--------|-------|
| Wheels | 31 physical (W1–W35) + 2 computational (W36, W37) = 33 files |
| Axioms | 73 physical (78 including the computational substrates) |
| Cases | 119 physical (127 including the computational substrates) |
| ¢ primitives | 29 atomic + 12 composite = 41 contracts |
| ∆ substrate expansions | ~38 |
| TIER 3 transducers | 7 |
| Cross-domain junctions | 33 physical (37 including the computational substrates) |
| Non-identities | 5 physical (7 including the computational substrates) |
| Escalation layers | 5 (ideal → parasitic → thermal → quantum → fabricated) |
| Knowledge states | 5 (KNOWS / THINKS-TRUE / DOESN'T-KNOW / NEEDS / LANGUAGE) |
| Python modules | 25 in `cent_compiler/` |
| Exact-core checks | 76/76 (`python3 tests/test_core.py`) |
| Simulation checks | 7/7 (`python3 cent test`) |
| Package exports | 49 |
| £ test cases | 38/39 (1 dimensional check, honestly classified) |

---

## Key Results

- **33 wheels** loaded from JSON (31 physical formula wheels + 2 computational substrates; single source of truth in `wheels/` folder)
- **22 ¢ primitives** (v1.0's 12 + v2.0's 10 new: exp, log, sat, hysteresis, grad, div_spatial, curl, delay, translinear, state_space)
- **22 proposals** with full 8-step pipeline trace (7 original + 3 v2.0 primitives + 12 expanded wheels)
- **22 .cir files** written to disk (one per proposal, 9 SPICE templates)
- **7 TIER 3 transducers** (Paynter, rotational-linear, C-L duality, electromechanical, thermoelectric, optoelectronic, electro-hydrodynamic)
- **Delta-sigma flagship**: √2 carried as bitstream, 36.9 dB noise suppression, NTF slope 28.0 dB/dec
- **Hypothesis bridge**: Cent Wheel knowledge state management, 5-layer escalation, conjecture loop, parametric ledger
- **6 of 7** original application proposals pass validation (1 honestly classified as DIMENSIONAL CHECK)
- **22 of 22** show-work proposals pass the full pipeline (decompose → enumerate → escalate → emit .cir)
- **7 of 7** core simulations pass

---

## Exact core (v2.1) — `CentCalculus2`

The v2.0 compiler above is a floating-point pipeline: it decomposes, enumerates, escalates and emits SPICE. The exact core is a second, independent execution layer in the same package. It has no binary floating point at all.

```bash
# 76 checks over exact arithmetic, enclosures, ports, fields, programs
python3 tests/test_core.py

# machine-readable capability registry (29 atomic + 12 composite)
python3 tools/export_capabilities.py --out capabilities.json
```

| Metric | Value |
|--------|-------|
| Atomic ¢ primitives | 29 across 4 tiers |
| Composite macros | 12 |
| Contracts in the registry | 41 |
| Core verification | 76/76 checks |
| Documentation | `docs/semantics.md`, `docs/extensions.md` |

What the exact core adds:

- **Exact scalars** — every numeric wire is a `fractions.Fraction`; floats are rejected unless converted explicitly (`from_float_exact`), and failures are structured `CentError` codes rather than sentinel values.
- **Certified enclosures** — `√2`, `e`, `log 2` and `π` are bracketed by exact rational endpoints proved by construction (integer square root, Taylor with Lagrange remainder, `atanh` series, Machin's formula).
- **Conservative ports** — effort/flow pairs, power-conserving 0/1 junctions, gyrator, transformer, and dissipation with entropy production.
- **Spatial carriers** — exact central stencils on the 24-D carrier, a 276-component 2-form curl, and Dirichlet/Neumann/Robin boundaries.
- **A transactional tick evaluator** — a single-assignment ¢ program IR with static arity, parameter, kind and cycle checking; state is committed only on success.
- **Layered resolution** — `ideal → parasitic → thermal → quantum → fabricated` with every failure preserved in the trace.

---

## Package Layout

```
cent_compiler_v12_2_ext/
├── README.md                    # this file
├── CENT_FRAMEWORK.md            # canonical documentation
├── DELTA_SIGMA_DEMO.md           # standalone flagship demo
├── VALIDATION_REPORT.md         # 6 PASS + 1 dimensional check (honest)
├── cent                         # CLI tool (8 subcommands)
├── cent_compiler/               # Python package (25 modules)
│   ├── grammar.py               # 41 ¢ contracts + AST decomposer
│   ├── wheels.py                # 33 wheels loaded from JSON (topology from index.json)
│   ├── wheels_19.py             # W16-W19 extension layer
│   ├── wheels_extended.py       # licensed-union derivability helpers
│   ├── substrate_library.py     # ~38 ∆ expansion rules
│   ├── pattern_matcher.py       # 3-pattern clustering
│   ├── cost_function.py         # 6-axis ¢_cost + pruning
│   ├── isomorphism_gate.py      # 3-tier gate + ∆Σ classifier + 7 transducers
│   ├── simulator.py             # 7 verified simulations
│   ├── scaled_simulator.py      # unit-scaled simulation layer
│   ├── spice_emitter.py         # SPICE netlist + .cir file output
│   ├── delta_sigma.py           # ∆Σ engine + flagship demonstration
│   ├── pound_suite.py           # £ test cases
│   ├── hypothesis_bridge.py     # Cent Wheel + escalation + conjecture loop + ledger
│   └── ui.py                    # cent ui / report / eval console
├── applications/                # 22 source application proposals
├── expansion/                   # roadmap + Hypothesis Engine reference
├── tests/                       # test_core.py — 73 exact-core checks
├── wheels/                      # 34 JSON files (33 wheels + index.json) — single source of truth
└── examples/                    # 5 .cir files + demo output
```

### Exact-core additions

```
cent_compiler/
├── exact.py            # exact rationals, structured error taxonomy
├── interval.py         # certified sqrt/exp/log/pi enclosures
├── port.py             # conjugate ports, junctions, two-ports
├── density.py          # unit-density channel policies
├── geometry.py         # carrier, fields, stencils, boundaries
├── state.py            # machine state, transactional context, PRNG
├── vocabulary.py       # 29 atomic + 12 composite contracts
├── program.py          # program IR, static checker, feedback analysis
├── evaluator.py        # exact tick evaluator
└── resolution.py       # layered fallback with a preserved failure trace

docs/
├── semantics.md        # the conventions the exact core checks
└── extensions.md       # 29/23 reconciliation, statuses, limitations

tools/
├── export_capabilities.py   # renders the contract registry
└── inventory.py             # WS0 recount + counting-convention reconciliation

tests/
└── test_core.py        # 76 core checks in ten groups
```

Run both suites:

```bash
python3 tests/test_core.py   # 76/76 exact-core checks
python3 cent test            # 7/7 physical simulations
python3 tools/inventory.py   # substrate recount (see docs/INVENTORY.md)
```

---

## The Delta-Sigma Flagship

> Delta-Sigma modulation is the physical process that carries irrational numbers without storing them.

```bash
python3 cent showcase
```

Output: √2 carried as a 100,000-sample bitstream at OSR=64×. Running average converges to 1.414213562373095 (exact). FFT shows 36.9 dB in-band noise suppression vs unshaped quantizer. NTF slope = 28.0 dB/decade (first-order high-pass).

---

## Expansion Roadmap

The `expansion/` folder contains three roadmap documents:

1. **01_Expanding_Computational_Depth.md** — new ¢ primitives, ∆ substrates, TIER 3 transducers (IMPLEMENTED in v2.0)
2. **02_Expanding_Wheels.md** — W20-W35 new domain wheels (IMPLEMENTED in v2.0)
3. **03_Expanding_Beyond.md** — 10-axis cost engine, multi-format output, native solver integration, algorithmic £ synthesis (deferred to v3)

Plus Hypothesis Engine reference files for the knowledge state management architecture.

---

## License

Open source. Built on the GLM wheel system (github.com/DigitalEuan/GLM).

### Compiler-backed application proposals

The 22 Markdown files in `applications/` are source proposal records, not test
output. Their target relations can be compiled and audited against the live
compiler with:

```bash
python3 tools/compile_applications.py --out validation/applications.json --strict
```

The command writes a machine-readable ledger containing each proposal's parsed
¢ DAG, implementation count and ranking, exact-core material, SPICE material,
and compiler notes. It exits non-zero if a proposal cannot be compiled or has no
ranked implementation.
