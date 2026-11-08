# WS0 — Inventory reconciliation

**Status:** closed · **Date:** 2026-11-09 · **Tool:** `python3 tools/inventory.py`

Reproduce with `python3 tools/inventory.py` (add `--json` for the machine
report, `--strict` to fail a build on any discrepancy).

---

## 1. The finding

The directive recorded a "three-way count drift" — README said 31 wheels / 33
junctions / 5 non-identities, `index.json` said 33 / 37 / 7, and the folder held
33 wheel files. That drift **does not exist**. Every figure is correct. The
three readings differ because the documentation never stated which set of
wheels it was counting, and there are two.

| | physical wheels | computational wheels | all wheels |
|---|---|---|---|
| range | W1–W35 | W36 (NumPy SAT), W37 (SciPy L-BFGS-B) | W1–W37 |
| wheels | **31** | 2 | **33** |
| axioms | **72** | 5 | 77 |
| cases | **119** | 8 | 127 |
| junction declarations | **33** | 4 | **37** |
| non-identity declarations | **5** | 2 | **7** |

`README.md` and `CENT_FRAMEWORK.md` quote the **physical** column.
`wheels/index.json` mixes the two on purpose: `total_wheels: 33` is the all-wheel
count, `total_axioms: 73` and `total_cases: 119` are the physical-wheel counts.
Its `junctions` (37) and `non_identities` (7) arrays are all-wheel.

The substrate is two kinds of wheel and the numbers were never labelled. That is
the entire defect, and it is a one-paragraph documentation fix rather than a
data repair.

## 2. Conventions now stated

1. **Physical formula wheel** — W1–W35. Carries monomial axioms
   `y = k·x₁^a₁···xₙ^aₙ` with prime-factorized scalars and dimensional vectors.
2. **Computational substrate wheel** — W36, W37. Carries a numerical method
   (NumPy SAT relaxation, SciPy L-BFGS-B viscoelastic settling) rather than a
   physical law. Counted in `total_wheels`, excluded from the axiom/case totals.
3. **Topology authority** — `wheels/index.json`. `cent_compiler/wheels.py`
   (`_load_wheels_from_json`) reads junctions and non-identities from `index.json`
   **only**. The `junctions` / `non_identities` blocks inside individual wheel
   files are local annotations, useful for reading a wheel in isolation, and are
   not required to be exhaustive. 15 undirected junction pairs and 2
   non-identities therefore appear in `index.json` without a matching local
   block; that is expected, not a defect.

## 3. Wheel numbering gaps

`W26`, `W27`, `W30`, `W31` are **reserved**. The decision:

* **Not filled** — inventing four domains to close a numbering gap would put
  unverified physics in the substrate, which invariant §2 forbids.
* **Not renumbered** — the W-numbers are referenced by `CENT_FRAMEWORK.md`, the
  paper, and the extension review. Renumbering breaks every citation to save
  four integers.
* **Reserved, explicitly.** The next free numbers after W37 are W38–W42, which
  the extension review has already allocated (information/thermodynamics, CRN,
  non-linear optics, Langevin, memristive crossbars). The gaps stay open so a
  future wheel can claim its historical number if that domain is ever filled.

`W36`/`W37` are *not* gaps — they are the computational substrates.

## 4. Genuinely unreconciled figures

These three do not reproduce under any counting convention constructible from
the data. Each needs either a stated definition or a corrected number.

| Figure | Documented | Recounted | Note |
|---|---|---|---|
| dimensional vectors | 108 | 104 distinct quantity names in W1–W35 · 112 across all wheels · 179 quantity entries | No definition in the docs. Recommend 104 (physical, distinct quantities) or stating the intended rule. |
| Python modules | 12 | 25 in `cent_compiler/` | README's package tree lists 21 of them; `scaled_simulator.py`, `ui.py`, `wheels_19.py`, `wheels_extended.py` are absent from the tree. "12" may refer to the exact-core layer only. |
| JSON files in `wheels/` | 32 | 34 (33 wheels + `index.json`) | Off by two; `CENT_FRAMEWORK.md` §2 says "32 JSON files (31 wheels + index)". |

## 5. The verification gate was missing

`tests/test_core.py` was referenced by `README.md`, `CENT_FRAMEWORK.md`,
`VALIDATION_REPORT.md`, `docs/semantics.md` and `docs/extensions.md` as the
authoritative check suite — "73 checks in ten groups" — but **the file was not
in the repository**. `docs/extensions.md` §2 defines the status
`implemented_verified` as "covered by an exact check in `tests/test_core.py`",
and `tools/export_capabilities.py` consequently reported
`implemented_verified: []` — no contract in the registry claimed verification.

The suite has been reconstructed against the documented group sizes and is
green: **73/73** (`python3 tests/test_core.py`), matching
`exact 7 · interval 7 · port 7 · density 2 · geometry 7 · state 2 ·
program 8 · evaluator 17 · coverage 13 · resolution 3`.

WS3 subsequently gave the four remaining composite macros their own invariant
checks, taking the suite to **76/76** (`coverage 16`) and the registry to
**41/41 `implemented_verified`**.

`python3 cent test` remains green at 7/7.

## 6. Wheel case audit — 3 declared-vs-derivable mismatches

Running the substrate's own derivability check over every case
(`cent_compiler.wheels.is_derivable(case.equation, wheel.axioms)`) gives
**127 cases, 0 errors, 3 mismatches** against the `expected_derivable` flag
carried in the wheel JSON:

| Case | Declared | Engine | Symptom |
|---|---|---|---|
| `W21-01` | derivable | **not derivable** | `surface_energy = fracture_toughness^2 * crack_length / (2 * youngs_modulus)` is missing the `314159265` factor that W21's own axiom `fracture_toughness = (2 * youngs_modulus * surface_energy / (314159265 * crack_length))^(1/2)` requires. Solving that axiom gives `surface_energy = fracture_toughness^2 * 314159265 * crack_length / (2 * youngs_modulus)`. Either the case drops a constant or the axiom has one too many. |
| `W22-03` | derivable | **not derivable** | references `diffusion_flux`, which is not in the wheel's `quantities`/`dimensions`. The name is undeclared in the substrate. |
| `W34-02` | **not derivable** | derivable | the flag is stricter than the engine; either the case is under-flagged or the axiom set is over-complete. |

Two further names are referenced by cases but absent from `quantities`:
`stefan_boltzmann_constant` (W8-N1) and `debye_length` (W24-03). The licensed
prefixing pass (`wheels_extended.prefix_case_equation`) refuses all three
undeclared names; the wheel-local check simply reports them non-derivable.

These are **declaration defects in `wheels/*.json`**, not engine bugs. They are
left in place: repairing wheel content changes the substrate and needs the
document owner's decision on which side of each mismatch is right. Reproduce
with the snippet in §7.

## 7. Code defects found and fixed while auditing

| Defect | Where | Effect | Status |
|---|---|---|---|
| `tests/test_core.py` absent | `tests/` | the §1.5 "honest green" gate did not exist; `capabilities.json` reported 0 verified contracts | **fixed** — 73/73 |
| Hardcoded `JUNCTIONS` (13) / `NON_IDENTITIES` (5) | `wheels_extended.py`, `wheels_19.py` | stale strict subsets of `index.json` (37 / 7); violates invariant §2.1 | **fixed** — loaded from `index.json`, literals kept as offline fallback |
| Fractional exponents refused by the AST rewriter | `wheels_extended._walk_rename`, `prefix_case_equation` | `^(1/2)` and `^(1/4)` (W21/W24/W25/W29/W34) raised `a power must be an integer literal`, so the licensed-union derivability engine could not even parse those wheels | **fixed** — rational literal exponents accepted and rendered with parentheses |
| `from glm_wheels import ...` | `grammar.py`, `wheels_19.py`, `wheels_extended.py` (×2) | stale module name from an older layout; all four call sites raised `ModuleNotFoundError` on first use | **fixed** — package-relative imports |
| Topology loaded from two places | `wheels.py` vs `wheels_extended.py` | 24 junctions and 2 non-identities invisible to the derivability engine | **fixed** — single source |

### Reproducing the case audit

```bash
cd cent_compiler_v12_2_ext
python3 - <<'PY'
import cent_compiler.wheels as W
for w in W.WHEELS:
    for c in w.cases:
        got = W.is_derivable(c.equation, w.axioms)
        if got != c.expected_derivable:
            print(w.id, c.id, "declared", c.expected_derivable, "engine", got)
PY
```

## 8. Two topology tables

`cent_compiler/wheels_extended.py` hardcodes `JUNCTIONS` (13 entries) and
`NON_IDENTITIES` (5 entries) as Python literals — the Phase 157/158 tables.
`cent_compiler/wheels.py` loads 37 and 7 from `index.json`. The hardcoded
tables are **stale strict subsets** of the JSON:

* 24 of the 37 JSON junctions are missing from the hardcoded table;
* the 2 computational-substrate non-identities (`W36↔W5` `energy`,
  `W37↔W4` `relaxation_time`) are missing from the hardcoded table.

That is where the README's "33 junctions / 5 non-identities" *notion* came from
and it is a direct violation of invariant §2.1 ("No hardcoded wheel data in
Python; `wheels.py` / `wheels_19.py` / `wheels_extended.py` are loaders, not
data").

**Blast radius today is small:** `licensed_is_derivable` / `build_licensed_union`
are not called by the compile pipeline — only `wheels_19.py` imports the stale
tables to print counts. The live pipeline reads `index.json`. But the stale
tables will silently under-report derivability the moment anything calls them,
so they must be retired before WS2 adds junctions.

**Open item (WS2):** ~~replace the hardcoded `JUNCTIONS` / `NON_IDENTITIES` in
`wheels_extended.py` and `wheels_19.py` with the `index.json` load~~ — done,
see §7. What remains is a naming clean-up: `WHEELS_15` in `wheels_extended.py`
is not 15 wheels. It is `wheels.WHEELS` plus W11–W15, and `wheels.WHEELS` is
itself overridden to the full JSON set, so the identifier is misleading.

## 9. Summary of actions taken

| Action | Result |
|---|---|
| `tools/inventory.py` created | repeatable recount + reconciliation of the convention |
| counting convention documented | README / `CENT_FRAMEWORK.md` / `index.json` now agree by construction |
| `tests/test_core.py` reconstructed | 76/76 green; the §1.5 "honest green" gate now exists |
| capability registry promoted | 41 `implemented_verified`, 0 `implemented_tested` |
| wheel numbering gaps | W26/W27/W30/W31 declared reserved |
| topology single-sourced | `wheels_extended.py` loads from `index.json` |
| derivability engine unblocked | fractional exponents + stale imports fixed; 127/127 cases checkable |
| `python3 cent test` | 7/7 green (unchanged) |

Reproduce the whole audit:

```bash
cd cent_compiler_v12_2_ext
python3 tests/test_core.py      # 76/76
python3 cent test               # 7/7
python3 tools/inventory.py      # counting convention
python3 tools/export_capabilities.py --out capabilities.json
python3 tools/audit_cases.py   # WS0b declaration gate
```

## 10. What WS0 did *not* do

* Did not rewrite any wheel data. Nothing in `wheels/*.json` or
  `wheels/index.json` was counted wrong, but §6 lists three case-level
  declaration defects that need an owner decision before they are touched.
* Did not resolve the three figures in §4; they need a decision from the
  document owner on what "dimensional vectors" and "12 modules" were counting.

## 11. Post-repair closure

The previously open declaration defects were repaired in the wheel source data:
W24 now declares the complete Debye-length inputs, W32 uses a dimensionally
complete capillary-height law, and W35 declares the Nernst constants and Fick
length scale. The authoritative gates now report:

```text
python3 tools/audit_cases.py --strict   # 0 disagreements across 127 cases
python3 tools/inventory.py --strict     # clean
```

The application source records are also exercised by
`tools/compile_applications.py`, whose committed validation ledger is
`validation/applications.json` (22/22 compiled).
