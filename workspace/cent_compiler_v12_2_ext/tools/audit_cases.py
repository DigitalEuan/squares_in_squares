#!/usr/bin/env python3
"""WS0b substrate case audit — the declaration gate for `wheels/*.json`.

Every case in every wheel carries two claims about itself:

    expected_dimensional            "this equation balances dimensionally"
    expected_derivable              "this equation follows from the wheel's axioms"

plus an optional ``expected_dimensional_explicit`` for the eight-axis check.
``cent_compiler.wheels.case_table()`` recomputes all of them.  This tool diffs
the claims against the engine and reports every disagreement.

    python3 tools/audit_cases.py             # human report
    python3 tools/audit_cases.py --json      # machine report
    python3 tools/audit_cases.py --strict    # exit 1 on any disagreement

Which check is authoritative
----------------------------
``expected_dimensional`` is compared against ``dim_reference_si``: the
**seven-axis** reference check (L, M, T, I, H, N, J), which deliberately
ignores the eighth house axis ``A``.  ``expected_dimensional_explicit`` is
compared against the eight-axis ``dim_reference_explicit``.  Using the wrong
one produces phantom mismatches — see ``docs/INVENTORY.md``.

WS1 acceptance: every new wheel must leave this tool reporting zero
disagreements, including its own cases.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from cent_compiler import wheels as W  # noqa: E402


def collect() -> dict:
    rows = W.case_table()
    dim_si, dim_exp, der = [], [], []
    for r in rows:
        if r["dim_reference_si"] != r["expected_dim_si"]:
            dim_si.append(r)
        if r["dim_reference_explicit"] != r["expected_dim_explicit"]:
            dim_exp.append(r)
        if r["derivable"] != r["expected_derivable"]:
            der.append(r)

    # Names referenced by a case but absent from REFERENCE_DIMENSIONS make the
    # dimension check return None.  Those are declaration gaps, not physics.
    undeclared = []
    for r in rows:
        if r["dim_reference_si"] is None or r["dim_reference_explicit"] is None:
            undeclared.append(r)

    # Axioms carry no flags, so nothing was checking them.  Every axiom must
    # balance dimensionally and must parse to an exact rational coefficient:
    # a fractional power over a non-unit rational base yields an irrational
    # coefficient (sqrt(2/314159265)), which the exact RREF solver can never
    # cancel, silently making every case under that axiom underivable.
    axiom_dim, axiom_coeff = [], []
    for w in W.WHEELS:
        for a in w.axioms:
            # Same authority as cases: the seven physical axes.  The eighth
            # house axis 'A' (angle) is not expected to balance -- W13 gives
            # angle an A exponent of +1, so any quantity derived from an
            # angular frequency picks up A while its declaration says A^0.
            ok7 = W._reference_si(a)
            cons8 = W.consistency(a, "reference")
            if not ok7:
                axiom_dim.append({"wheel": w.id, "axiom": a,
                                  "residual": None if cons8 is None else cons8["residual"]})
            for side in W.parse_equation(a):
                c = side.coefficient
                if c.denominator > 10 ** 12 or c.numerator > 10 ** 12:
                    axiom_coeff.append({"wheel": w.id, "axiom": a, "coefficient": str(c)})
                    break

    return {
        "cases": len(rows),
        "rows": rows,
        "dimensional_mismatches": dim_si,
        "dimensional_explicit_mismatches": dim_exp,
        "derivable_mismatches": der,
        "undeclared_names": undeclared,
        "axiom_dimensional_defects": axiom_dim,
        "axiom_irrational_coefficients": axiom_coeff,
    }


def _names_outside_reference(equation: str) -> list[str]:
    import re
    known = set(W.REFERENCE_DIMENSIONS)
    out = []
    for name in re.findall(r"[A-Za-z_][A-Za-z_0-9]*", equation):
        if name in known or name in {"e"}:
            continue
        if name not in out:
            out.append(name)
    return out


def render(report: dict) -> str:
    lines = []
    add = lines.append
    add("wheels/*.json case audit — WS0b declaration gate")
    add("=" * 78)
    add(f"cases checked: {report['cases']}")
    add("")
    add("authoritative checks")
    add("  expected_dimensional         vs dim_reference_si        (7 axes, no 'A')")
    add("  expected_dimensional_explicit vs dim_reference_explicit (8 axes)")
    add("  expected_derivable           vs derivable               (wheel axioms)")
    add("")

    def section(title, rows, declared_key, engine_key):
        add(f"{title}: {len(rows)}")
        add("-" * 78)
        if not rows:
            add("  clean")
            add("")
            return
        for r in rows:
            add(f"  {r['wheel']} {r['case']}  [{r['status']}]")
            add(f"      declared = {r[declared_key]}   engine = {r[engine_key]}")
            add(f"      {r['equation']}")
            extra = _names_outside_reference(r["equation"])
            if r[engine_key] is None and extra:
                add(f"      undeclared names: {', '.join(extra)}")
        add("")

    section("expected_dimensional disagreements", report["dimensional_mismatches"],
            "expected_dim_si", "dim_reference_si")
    section("expected_dimensional_explicit disagreements",
            report["dimensional_explicit_mismatches"],
            "expected_dim_explicit", "dim_reference_explicit")
    section("expected_derivable disagreements", report["derivable_mismatches"],
            "expected_derivable", "derivable")

    add(f"axiom dimensional defects (7 physical axes): "
        f"{len(report['axiom_dimensional_defects'])}")
    add("-" * 78)
    if not report["axiom_dimensional_defects"]:
        add("  clean")
    for a in report["axiom_dimensional_defects"]:
        add(f"  {a['wheel']}: {a['axiom']}")
        add(f"      residual = {a['residual']}")
    add("")

    add(f"axioms with irrational coefficients: "
        f"{len(report['axiom_irrational_coefficients'])}")
    add("-" * 78)
    if not report["axiom_irrational_coefficients"]:
        add("  clean")
    for a in report["axiom_irrational_coefficients"]:
        add(f"  {a['wheel']}: {a['axiom']}")
        add(f"      coefficient = {a['coefficient']}  (float-rounding tell)")
        add("      a fractional power over a non-unit rational base is irrational;")
        add("      rewrite the axiom in powered form so the root disappears.")
    add("")

    total = (len(report["dimensional_mismatches"])
             + len(report["dimensional_explicit_mismatches"])
             + len(report["derivable_mismatches"])
             + len(report["axiom_dimensional_defects"])
             + len(report["axiom_irrational_coefficients"]))
    add("=" * 78)
    add(f"  {total} disagreement(s) across {report['cases']} cases")
    if total:
        add("  WS0b is closed when this reaches 0.")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", action="store_true", help="emit the machine report")
    ap.add_argument("--strict", action="store_true", help="exit 1 on any disagreement")
    args = ap.parse_args()

    report = collect()
    if args.json:
        slim = {k: v for k, v in report.items() if k != "rows"}
        print(json.dumps(slim, indent=2, ensure_ascii=False, default=str))
    else:
        print(render(report))

    total = (len(report["dimensional_mismatches"])
             + len(report["dimensional_explicit_mismatches"])
             + len(report["derivable_mismatches"])
             + len(report["axiom_dimensional_defects"])
             + len(report["axiom_irrational_coefficients"]))
    return 1 if (args.strict and total) else 0


if __name__ == "__main__":
    sys.exit(main())
