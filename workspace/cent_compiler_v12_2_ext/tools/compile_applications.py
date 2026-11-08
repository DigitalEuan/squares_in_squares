#!/usr/bin/env python3
"""Compile every application proposal through the real cent pipeline.

The Markdown files remain human-readable proposal records. This tool treats the
first code block under ``£ (Target Relation)`` as their source relation, runs
``cent_compiler.ui.build_report`` for each one, and writes a JSON ledger with the
DAG, ranked implementations, exact-core material, SPICE material, and notes.
It therefore makes proposal validation reproducible instead of accepting static
printed results as evidence.

Usage from the workspace root::

    python3 tools/compile_applications.py
    python3 tools/compile_applications.py --out validation/applications.json --strict
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cent_compiler.ui import build_report  # noqa: E402

RELATION_RE = re.compile(
    r"##\s*£\s*\(Target Relation\)\s*\n\s*```[^\n]*\n(?P<relation>[^\n]+)\n\s*```",
    re.IGNORECASE,
)

def proposal_relation(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = RELATION_RE.search(text)
    if not match:
        raise ValueError("missing `£ (Target Relation)` code block")
    relation = match.group("relation").strip()
    if not relation or "=" not in relation:
        raise ValueError(f"invalid target relation: {relation!r}")
    return relation

def jsonable_report(report) -> dict:
    material = report.material()
    ranked = []
    for impl, cost in report.top:
        ranked.append({
            "domain": impl.substrate_domain,
            "carrier": impl.carrier_type,
            "delta_sigma": bool(impl.is_delta_sigma),
            "components": list(impl.components),
            "cost": cost.total,
        })
    material["ranked"] = ranked
    material["notes"] = list(report.notes)
    material["compiler_status"] = {
        "has_dag": bool(report.ops),
        "has_implementations": report.impl_count > 0,
        "has_ranked_implementation": bool(report.top),
        "has_spice_material": bool(report.template and report.netlist),
        "has_exact_program": report.program is not None,
    }
    return material

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=ROOT / "validation" / "applications.json")
    parser.add_argument("--strict", action="store_true", help="fail if any proposal cannot be compiled")
    args = parser.parse_args()

    rows = []
    failures = []
    for path in sorted((ROOT / "applications").glob("proposal_*.md")):
        row = {"proposal": path.name}
        try:
            relation = proposal_relation(path)
            report = build_report(relation)
            row.update({"relation": relation, "material": jsonable_report(report)})
            status = row["material"]["compiler_status"]
            if not status["has_implementations"] or not status["has_ranked_implementation"]:
                failures.append({"proposal": path.name, "reason": "no ranked implementation"})
        except Exception as exc:  # report every proposal; do not hide one bad input
            row["error"] = f"{type(exc).__name__}: {exc}"
            failures.append({"proposal": path.name, "reason": row["error"]})
        rows.append(row)

    payload = {
        "schema": "cent-application-compilation/1",
        "workspace": str(ROOT.name),
        "proposal_count": len(rows),
        "compiled_count": sum("material" in row for row in rows),
        "failure_count": len(failures),
        "failures": failures,
        "proposals": rows,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    print(f"wrote {args.out}: {payload['compiled_count']}/{payload['proposal_count']} compiled")
    if failures:
        print(json.dumps(failures, indent=2))
    return 1 if args.strict and failures else 0

if __name__ == "__main__":
    raise SystemExit(main())
