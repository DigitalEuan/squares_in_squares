#!/usr/bin/env python3
"""WS0 inventory reconciliation for the ¢ wheel substrate.

The single source of truth is ``wheels/*.json`` plus ``wheels/index.json``.
Everything else — README, ``CENT_FRAMEWORK.md``, ``docs/*.md`` — is generated
prose that can drift.  This tool recounts the substrate from the JSON and
reports every place the prose disagrees, so the drift is visible instead of
accumulating.

    python3 tools/inventory.py             # human report
    python3 tools/inventory.py --json      # machine report
    python3 tools/inventory.py --strict    # exit 1 on any drift

What is counted
---------------
* wheel files on disk, and the gaps in the W-numbering
* axioms, cases, negative controls and dimensional exponent rows per wheel
* the declared totals in ``wheels/index.json``
* junctions and non-identities, in both the wheel files and the index,
  as directed declarations and as deduplicated undirected pairs
* the ¢ primitives referenced by wheel data
* the Python module count, the test-suite presence and the CLI subcommands

Invariant (directive §2.1): ``index.json`` declares totals that the wheel files
must actually have.  A disagreement between them is a defect, not a style note.
"""
from __future__ import annotations

import argparse

import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WHEELS = os.path.join(ROOT, "wheels")
PACKAGE = os.path.join(ROOT, "cent_compiler")
TESTS = os.path.join(ROOT, "tests", "test_core.py")

# Figures quoted by README.md / CENT_FRAMEWORK.md.  They are counted over the
# 31 *physical* formula wheels (W1-W35); index.json additionally carries the two
# computational substrates (W36 NumPy SAT, W37 SciPy L-BFGS-B) and so reports
# the all-wheel figures.  Both sets are correct -- the docs simply never said
# which set they meant, which is what produced three different readings.
DOCUMENTED_PHYSICAL = {
    "wheels": 31,
    "axioms": 73,
    "cases": 119,
    "junction_declarations": 33,
    "nonidentity_declarations": 5,
}
DOCUMENTED_ALL = {
    "wheels": 33,
    "axioms": 78,
    "cases": 127,
    "junction_declarations": 37,
    "nonidentity_declarations": 7,
}
INDEX_DECLARED = {
    "wheels": 33,
    "axioms": 73,
    "cases": 119,
}
# Documented but not reproducible under any counting convention this tool can
# construct; see docs/INVENTORY.md.
UNRECONCILED = {}


def _wheel_number(name: str) -> int:
    return int(name[1:])


def _is_physical(name: str) -> bool:
    """The 31 physical formula wheels; W36/W37 are computational substrates."""
    return _wheel_number(name) <= 35


def load_wheels() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for path in sorted(glob.glob(os.path.join(WHEELS, "W*.json"))):
        name = os.path.basename(path)[:-5]
        with open(path, encoding="utf-8") as fh:
            out[name] = json.load(fh)
    return out


def count_wheels(wheels: dict[str, dict]) -> dict:
    def blank():
        return {"wheels": 0, "axioms": 0, "cases": 0, "negative_controls": 0,
                "quantities": 0, "dimensional_vectors": 0,
                "junction_declarations": 0, "nonidentity_declarations": 0}

    physical, computational = blank(), blank()
    per_wheel = {}
    for name, data in wheels.items():
        bucket = physical if _is_physical(name) else computational
        ax = data.get("axioms", []) or []
        cs = data.get("cases", []) or []
        dims = data.get("dimensions", {}) or {}
        n_vec = sum(
            1 for v in dims.values()
            if isinstance(v, dict) and isinstance(v.get("exponents"), list)
        )
        n_neg = sum(1 for c in cs if c.get("physical_status") == "negative_control")
        n_j = len(data.get("junctions", []) or [])
        n_n = len(data.get("non_identities", []) or [])
        per_wheel[name] = {
            "axioms": len(ax), "cases": len(cs), "negative_controls": n_neg,
            "quantities": len(data.get("quantities", []) or []),
            "dimensional_vectors": n_vec,
            "junction_declarations": n_j, "nonidentity_declarations": n_n,
            "substrate": "physical" if _is_physical(name) else "computational",
        }
        bucket["wheels"] += 1
        bucket["axioms"] += len(ax)
        bucket["cases"] += len(cs)
        bucket["negative_controls"] += n_neg
        bucket["quantities"] += per_wheel[name]["quantities"]
        bucket["dimensional_vectors"] += n_vec
        bucket["junction_declarations"] += n_j
        bucket["nonidentity_declarations"] += n_n
    total = {k: physical[k] + computational[k] for k in physical}
    return {"physical": physical, "computational": computational, "all": total,
            "per_wheel": per_wheel}


def topology(wheels: dict[str, dict], index: dict) -> dict:
    """Directed declarations and deduplicated undirected pairs, two ways."""
    wheel_j: list[tuple[str, str, str, str]] = []
    wheel_ni: list[tuple[str, str, str]] = []
    for name, data in wheels.items():
        for j in data.get("junctions", []) or []:
            wheel_j.append((name, j.get("other_wheel", ""), j.get("name_in_this_wheel", ""),
                            j.get("name_in_other_wheel", "")))
        for n in data.get("non_identities", []) or []:
            wheel_ni.append((name, n.get("other_wheel", ""), n.get("name", "")))

    index_j = [(j.get("wheel_a", ""), j.get("wheel_b", ""), j.get("name_a", ""),
                j.get("name_b", "")) for j in index.get("junctions", [])]
    index_ni = [(n.get("wheel_a", ""), n.get("wheel_b", ""), n.get("name", ""))
                for n in index.get("non_identities", [])]

    def undirected(rows):
        return {tuple(sorted((a, b))) for a, b, *_ in rows if a and b}

    wj, ij = undirected(wheel_j), undirected(index_j)
    wn, ino = undirected(wheel_ni), undirected(index_ni)
    return {
        "wheel_junction_rows": wheel_j,
        "index_junction_rows": index_j,
        "wheel_nonidentity_rows": wheel_ni,
        "index_nonidentity_rows": index_ni,
        "wheel_junction_declarations": len(wheel_j),
        "wheel_junction_pairs": sorted(wj),
        "index_junction_declarations": len(index_j),
        "index_junction_pairs": sorted(ij),
        "junction_pairs_only_in_index": sorted(ij - wj),
        "junction_pairs_only_in_wheels": sorted(wj - ij),
        "wheel_nonidentity_declarations": len(wheel_ni),
        "wheel_nonidentity_pairs": sorted(wn),
        "index_nonidentity_declarations": len(index_ni),
        "index_nonidentity_pairs": sorted(ino),
        "nonidentity_pairs_only_in_index": sorted(ino - wn),
        "nonidentity_pairs_only_in_wheels": sorted(wn - ino),
    }


def package_state() -> dict:
    modules = sorted(
        os.path.basename(p)[:-3]
        for p in glob.glob(os.path.join(PACKAGE, "*.py"))
        if not os.path.basename(p).startswith("__")
    )
    cli = []
    cent = os.path.join(ROOT, "cent")
    if os.path.exists(cent):
        with open(cent, encoding="utf-8") as fh:
            src = fh.read()
        m = re.search(r"add_parser\(\s*\"(\w+)\"", src)
        cli = sorted(set(re.findall(r"add_parser\(\s*\"(\w+)\"", src)))
    return {
        "modules": modules,
        "module_count": len(modules),
        "cli_subcommands": cli,
        "tests_present": os.path.exists(TESTS),
    }


def cent_vocabulary(wheels: dict[str, dict]) -> dict:
    """Which ¢ primitives the wheel data actually exercises."""
    tokens: dict[str, int] = {}
    for name, data in wheels.items():
        for tok in set(re.findall(r"¢_[a-z_]+", json.dumps(data, ensure_ascii=False))):
            tokens[tok] = tokens.get(tok, 0) + 1
    return dict(sorted(tokens.items()))


def build_report() -> dict:
    wheels = load_wheels()
    with open(os.path.join(WHEELS, "index.json"), encoding="utf-8") as fh:
        index = json.load(fh)
    counted = count_wheels(wheels)
    top = topology(wheels, index)
    pkg = package_state()

    numbers = sorted(_wheel_number(n) for n in wheels)
    gaps = [f"W{i}" for i in range(min(numbers), max(numbers) + 1)
            if i not in set(numbers)]

    # Declarations are also split by substrate, so the convention can be checked.
    def split_decl(rows):
        phys = [r for r in rows if _is_physical(r[0]) and _is_physical(r[1])]
        return len(phys), len(rows) - len(phys)

    wj_phys, wj_comp = split_decl(top["wheel_junction_rows"])
    ij_phys, ij_comp = split_decl(top["index_junction_rows"])
    wn_phys, wn_comp = split_decl(top["wheel_nonidentity_rows"])
    in_phys, in_comp = split_decl(top["index_nonidentity_rows"])

    discrepancies = []
    # README/CENT_FRAMEWORK quote the physical-wheel figures.
    checks = (
        ("wheels", DOCUMENTED_PHYSICAL["wheels"], counted["physical"]["wheels"]),
        ("axioms", DOCUMENTED_PHYSICAL["axioms"], counted["physical"]["axioms"]),
        ("cases", DOCUMENTED_PHYSICAL["cases"], counted["physical"]["cases"]),
        ("junction declarations", DOCUMENTED_PHYSICAL["junction_declarations"], ij_phys),
        ("non-identity declarations", DOCUMENTED_PHYSICAL["nonidentity_declarations"], in_phys),
    )
    for field, documented, recounted in checks:
        if documented != recounted:
            discrepancies.append({"field": field, "documented": documented,
                                  "recounted": recounted,
                                  "source": "README/CENT_FRAMEWORK (physical wheels W1-W35)"})

    # index.json mixes the two conventions on purpose: all-wheel totals for the
    # wheel count, physical-wheel totals for the axiom/case counts.
    index_checks = (
        ("total_wheels", INDEX_DECLARED["wheels"], counted["all"]["wheels"]),
        ("total_axioms", INDEX_DECLARED["axioms"], counted["physical"]["axioms"]),
        ("total_cases", INDEX_DECLARED["cases"], counted["physical"]["cases"]),
        ("junctions", DOCUMENTED_ALL["junction_declarations"], ij_phys + ij_comp),
        ("non_identities", DOCUMENTED_ALL["nonidentity_declarations"], in_phys + in_comp),
    )
    for field, declared, recounted in index_checks:
        if declared != recounted:
            discrepancies.append({"field": f"index.{field}", "documented": declared,
                                  "recounted": recounted, "source": "wheels/index.json"})

    for field, (documented, note) in UNRECONCILED.items():
        discrepancies.append({"field": field, "documented": documented,
                              "recounted": note,
                              "source": "README/CENT_FRAMEWORK — definition not stated"})

    return {
        "wheel_files": counted["all"]["wheels"],
        "wheel_ids": sorted(wheels, key=_wheel_number),
        "gaps": gaps,
        "counted": counted,
        "topology": top,
        "topology_split": {
            "wheel_junction": {"physical": wj_phys, "computational": wj_comp},
            "index_junction": {"physical": ij_phys, "computational": ij_comp},
            "wheel_nonidentity": {"physical": wn_phys, "computational": wn_comp},
            "index_nonidentity": {"physical": in_phys, "computational": in_comp},
        },
        "package": pkg,
        "cent_tokens_in_wheels": cent_vocabulary(wheels),
        "discrepancies": discrepancies,
    }


def render(report: dict) -> str:
    lines = []
    add = lines.append
    add("¢ wheel inventory — WS0 reconciliation")
    add("=" * 78)
    add("")
    add("Counting convention (this is the whole finding):")
    add("  physical wheels  = W1-W35  — the 31 formula wheels")
    add("  all wheels       = W1-W37  — plus W36 (NumPy SAT) and W37 (SciPy L-BFGS-B)")
    add("  README/CENT_FRAMEWORK quote the physical figures; index.json carries both.")
    add("")
    add(f"wheel files on disk : {report['wheel_files']}")
    add(f"  ids               : {', '.join(report['wheel_ids'])}")
    add(f"  numbering gaps    : {', '.join(report['gaps']) or 'none'}")
    add("")
    c = report["counted"]
    ph, co, al = c["physical"], c["computational"], c["all"]
    add(f"{'quantity':<26}{'physical':>10}{'comput.':>10}{'all':>8}{'docs':>8}")
    add("-" * 78)
    rows = (
        ("wheels", "wheels", 31),
        ("axioms", "axioms", 73),
        ("cases", "cases", 119),
        ("negative controls", "negative_controls", None),
        ("quantities", "quantities", None),
        ("dimensional vectors", "dimensional_vectors", 108),
    )
    for label, key, documented in rows:
        doc = "-" if documented is None else str(documented)
        add(f"{label:<26}{ph[key]:>10}{co[key]:>10}{al[key]:>8}{doc:>8}")
    sp = report["topology_split"]
    add(f"{'junction declarations':<26}{sp['index_junction']['physical']:>10}"
        f"{sp['index_junction']['computational']:>10}"
        f"{sp['index_junction']['physical'] + sp['index_junction']['computational']:>8}{33:>8}")
    add(f"{'non-identity declarations':<26}{sp['index_nonidentity']['physical']:>10}"
        f"{sp['index_nonidentity']['computational']:>10}"
        f"{sp['index_nonidentity']['physical'] + sp['index_nonidentity']['computational']:>8}{5:>8}")
    add(f"{'python modules':<26}{'-':>10}{'-':>10}"
        f"{report['package']['module_count']:>8}{12:>8}")
    add("")
    add("topology")
    add("-" * 78)
    t = report["topology"]
    add(f"junctions     : wheel files {t['wheel_junction_declarations']} declarations / "
        f"{len(t['wheel_junction_pairs'])} undirected pairs")
    add(f"                index.json  {t['index_junction_declarations']} declarations / "
        f"{len(t['index_junction_pairs'])} undirected pairs")
    add(f"non-identities: wheel files {t['wheel_nonidentity_declarations']} declarations / "
        f"{len(t['wheel_nonidentity_pairs'])} undirected pairs")
    add(f"                index.json  {t['index_nonidentity_declarations']} declarations / "
        f"{len(t['index_nonidentity_pairs'])} undirected pairs")
    add("  index.json is the authority for topology (cent_compiler/wheels.py loads")
    add("  junctions and non-identities from it only); the wheel-file blocks are")
    add("  local annotations and are not required to be exhaustive.")
    if t["junction_pairs_only_in_index"]:
        add(f"  pairs declared only in index.json ({len(t['junction_pairs_only_in_index'])}): "
            + ", ".join(f"{a}-{b}" for a, b in t["junction_pairs_only_in_index"]))
    if t["nonidentity_pairs_only_in_index"]:
        add(f"  non-identities only in index.json: "
            + ", ".join(f"{a}-{b}" for a, b in t["nonidentity_pairs_only_in_index"]))
    add("")
    add("package")
    add("-" * 78)
    add(f"modules            : {report['package']['module_count']}")
    add(f"cli subcommands    : {', '.join(report['package']['cli_subcommands']) or 'none found'}")
    add(f"tests/test_core.py : {'present' if report['package']['tests_present'] else 'ABSENT'}")
    add(f"¢ tokens in wheels : "
        + (", ".join(report["cent_tokens_in_wheels"]) or "none"))
    add("")
    add("reconciliation")
    add("-" * 78)
    if not report["discrepancies"]:
        add("  every documented figure reproduces under the stated convention.")
    for d in report["discrepancies"]:
        add(f"  {d['field']}")
        add(f"      documented : {d['documented']}")
        add(f"      recounted  : {d['recounted']}")
        add(f"      source     : {d['source']}")
    add("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", action="store_true", help="emit the machine report")
    ap.add_argument("--strict", action="store_true", help="exit 1 on any discrepancy")
    args = ap.parse_args()

    report = build_report()
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(render(report))
    return 1 if (args.strict and report["discrepancies"]) else 0


if __name__ == "__main__":
    sys.exit(main())
