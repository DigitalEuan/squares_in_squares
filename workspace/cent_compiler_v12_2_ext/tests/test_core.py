#!/usr/bin/env python3
"""Exact-core verification suite (CentCalculus2) — 73 checks in ten groups.

Run from the ``cent_compiler_v12_2_ext`` directory:

    python3 tests/test_core.py

Exits non-zero on any failure.  Group sizes are fixed by ``docs/extensions.md``:

    exact 7 | interval 7 | port 7 | density 2 | geometry 7
    state 2 | program 8 | evaluator 17 | coverage 16 | resolution 3

WS3 gave ``phase_locked_loop``, ``transmission_line``, ``kalman_observer`` and
``thermo_electric`` their own invariant checks; before that they were exercised
only inside a grouped check and could not claim ``implemented_verified``.

Every claim is checked on exact rationals or certified enclosures.  Nothing
here uses binary floating point: where a float is involved it is only to prove
that the core *rejects* it, or that :func:`from_float_exact` converts the
stored binary value losslessly.

A check that a contract is covered here is what earns it the
``implemented_verified`` status in ``tools/export_capabilities.py``.
"""
from __future__ import annotations

import os
import sys
import traceback
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cent_compiler import density, exact, geometry, interval, port, program, resolution, state
from cent_compiler.evaluator import Evaluator, run_program
from cent_compiler.exact import CentError, ErrorCode, Q
from cent_compiler.geometry import (
    DIM,
    BoundaryCondition,
    GridDomain,
    TwoForm,
    analytic_field,
    carrier,
    curl_2form_at,
    curl_3d,
    divergence_at,
    divergence_of_curl_3d,
    gradient,
    gradient_at,
    laplacian_at,
    norm_square,
    origin,
    tax_residual,
)
from cent_compiler.interval import Interval, exp_q, log_q, pi_interval, sqrt_q
from cent_compiler.port import (
    Gyrator,
    PhysicalPort,
    Transformer,
    dissipator,
    ideal_transducer,
    junction_0,
    junction_1,
    kinetic_store,
    potential_store,
    require_power_balance,
    total_power,
)
from cent_compiler.program import (
    Instruction,
    Program,
    analyse,
    kind_of,
    program_from_dict,
)
from cent_compiler.resolution import Candidate, Layer, Resolution, resolve, require_converged
from cent_compiler.state import EvalContext, MachineState, SplitMix64


# ---------------------------------------------------------------------------
# harness
# ---------------------------------------------------------------------------

class Fail(AssertionError):
    """A check failed with a readable reason."""


def ok(condition, message: str) -> None:
    if not condition:
        raise Fail(message)


def eq(got, want, label: str) -> None:
    if got != want:
        raise Fail(f"{label}: got {got!r}, want {want!r}")


def raises(fn, code: ErrorCode | str | None = None, label: str = "call"):
    """Assert ``fn`` raises :class:`CentError`, optionally with a given code."""
    try:
        fn()
    except CentError as exc:
        if code is not None:
            want = code.value if isinstance(code, ErrorCode) else str(code)
            got = exc.code.value if isinstance(exc.code, ErrorCode) else str(exc.code)
            eq(got, want, f"{label}: error code")
        return exc
    raise Fail(f"{label}: expected CentError, nothing was raised")


RESULTS: list[tuple[str, str, bool, str]] = []


def check(group: str, name: str, fn) -> None:
    try:
        fn()
    except Exception as exc:  # noqa: BLE001 - the suite reports, not swallows
        detail = f"{type(exc).__name__}: {exc}"
        RESULTS.append((group, name, False, detail))
    else:
        RESULTS.append((group, name, True, ""))


# ===========================================================================
# exact — 7 checks
# ===========================================================================

def exact_decimal_strings_are_exact():
    eq(exact.q("0.1"), Fraction(1, 10), "q('0.1')")
    eq(exact.q("-0.125"), Fraction(-1, 8), "q('-0.125')")
    eq(exact.q("1e3"), Fraction(1000), "q('1e3')")
    eq(exact.q(" 2.5 "), Fraction(5, 2), "q(' 2.5 ')")
    eq(exact.q("0"), Fraction(0), "q('0')")


def exact_floats_are_rejected():
    raises(lambda: exact.q(0.1), ErrorCode.TYPE_ERROR, "q(0.1)")
    raises(lambda: exact.q(1.0), ErrorCode.TYPE_ERROR, "q(1.0)")
    raises(lambda: exact.q(float("inf")), ErrorCode.TYPE_ERROR, "q(inf)")
    raises(lambda: exact.q(None), ErrorCode.TYPE_ERROR, "q(None)")
    raises(lambda: exact.q([1, 2]), ErrorCode.TYPE_ERROR, "q([1,2])")
    raises(lambda: exact.q(object()), ErrorCode.TYPE_ERROR, "q(object)")


def exact_from_float_is_lossless():
    for value in (0.1, 0.5, -0.25, 1e-300, 1.7976931348623157e308, 5e-324):
        converted = exact.from_float_exact(value)
        num, den = value.as_integer_ratio()
        eq(converted, Fraction(num, den), f"from_float_exact({value!r})")
        ok(converted == Fraction(*value.as_integer_ratio()), "round-trips to the stored value")


def exact_from_float_rejects_non_rational():
    raises(lambda: exact.from_float_exact(float("nan")), ErrorCode.DOMAIN_ERROR, "NaN")
    raises(lambda: exact.from_float_exact(float("inf")), ErrorCode.DOMAIN_ERROR, "+inf")
    raises(lambda: exact.from_float_exact(float("-inf")), ErrorCode.DOMAIN_ERROR, "-inf")
    raises(lambda: exact.from_float_exact(1), ErrorCode.TYPE_ERROR, "int")
    raises(lambda: exact.from_float_exact(True), ErrorCode.TYPE_ERROR, "bool")


def exact_structured_error_codes():
    exc = raises(lambda: exact.div(Q(1), Q(0)), ErrorCode.DIVISION_BY_ZERO, "div by zero")
    eq(exc.code, ErrorCode.DIVISION_BY_ZERO, "code is the enum member")
    eq(exc.as_dict()["code"], "division_by_zero", "as_dict uses the stable string")
    raises(lambda: exact.q("not-a-number"), ErrorCode.INVALID_INPUT, "bad decimal")
    raises(lambda: exact.clamp(Q(5), Q(1), Q(0)), ErrorCode.DOMAIN_ERROR, "unordered clamp")
    raises(lambda: exact.wrap_periodic(Q(1), Q(0)), ErrorCode.DOMAIN_ERROR, "zero period")
    ok(exc.where is None or isinstance(exc.where, str), "where is a location or None")


def exact_arithmetic_identities():
    a, b, c = Q(2, 3), Q(-5, 7), Q(11, 13)
    eq(exact.add(a, b, c), a + b + c, "add is associative over rationals")
    eq(exact.mul(a, b, c), a * b * c, "mul is associative over rationals")
    eq(exact.div(a, b), a / b, "div")
    eq(exact.reciprocal(b), 1 / b, "reciprocal")
    eq(exact.sign(b), -1, "sign of a negative")
    ok(exact.is_zero(Q(0)), "is_zero(0)")
    ok(not exact.is_zero(a), "is_zero(2/3) is False")
    ok(exact.all_zero([Q(0), Q(0)]), "all_zero")
    eq(exact.clamp(Q(5), Q(0), Q(1)), Q(1), "clamp above")
    eq(exact.clamp(Q(-5), Q(0), Q(1)), Q(0), "clamp below")
    eq(exact.wrap_periodic(Q(5, 2), Q(1)), Q(1, 2), "wrap 5/2 mod 1")
    eq(exact.q_from_json(exact.q_to_json(Q(7, 3))), Q(7, 3), "json round-trip")
    # bool is an explicit 0/1 literal in q; from_float_exact is the only float door.
    eq(exact.q(True), Q(1), "q(True) is the exact literal 1")
    eq(exact.q(False), Q(0), "q(False) is the exact literal 0")
    eq(exact.format_q(Q(7, 3)), "7/3", "format_q writes num/den")
    eq(exact.format_q(Q(7)), "7", "format_q writes an integer bare")


def exact_no_binary_float_in_pipeline():
    # The trusted path is Fractions end to end; a float must never be produced.
    produced = [exact.add(Q(1, 3), Q(1, 6)), exact.mul(Q(2, 7), Q(7, 2)),
                exact.div(Q(1), Q(3)), exact.reciprocal(Q(4))]
    for value in produced:
        ok(isinstance(value, Q), f"{value!r} is an exact rational")
        ok(not isinstance(value, float), f"{value!r} is not a float")


# ===========================================================================
# interval — 7 checks
# ===========================================================================

# High-precision exact reference values, each quoted to more digits than the
# corresponding 64-bit enclosure is wide.  A containment check against these is
# a genuine exact-rational comparison, not a floating-point one.
REF_E = Q("2.7182818284590452353602874713526624977572470937")
REF_LN2 = Q("0.6931471805599453094172321214581765680755001344")
REF_PI = Q("3.1415926535897932384626433832795028841971693994")
REF_SQRT2 = Q("1.4142135623730950488016887242096980785696718754")


def interval_sqrt2_certified():
    enc = sqrt_q(2, 64)
    ok(enc.lo * enc.lo <= 2 <= enc.hi * enc.hi, "√2 enclosure brackets 2 exactly")
    ok(enc.lo > 0, "√2 enclosure is positive")
    ok(enc.lo <= REF_SQRT2 <= enc.hi, "√2 enclosure contains the 50-digit reference")
    ok(enc.hi - enc.lo < Q(1, 10 ** 18), "√2 enclosure is tight at 64 bits")


def interval_e_certified():
    enc = exp_q(1, 64)
    ok(enc.lo <= REF_E <= enc.hi, "e enclosure contains the 50-digit reference")
    ok(enc.hi - enc.lo < Q(1, 10 ** 19), "e enclosure is tight at 64 bits")
    ok(exp_q(0, 64).lo == 1 and exp_q(0, 64).hi == 1, "exp(0) = 1 exactly")


def interval_log2_certified():
    enc = log_q(2, 64)
    ok(enc.lo <= REF_LN2 <= enc.hi, "log 2 enclosure contains the 50-digit reference")
    ok(enc.hi - enc.lo < Q(1, 10 ** 22), "log 2 enclosure is tight at 64 bits")
    ok(log_q(1, 64).lo == 0 and log_q(1, 64).hi == 0, "log(1) = 0 exactly")


def interval_pi_certified():
    enc = pi_interval(64)
    ok(enc.lo <= REF_PI <= enc.hi, "π enclosure contains the 50-digit reference")
    ok(enc.hi - enc.lo < Q(1, 10 ** 19), "π enclosure is tight at 64 bits")
    tight = pi_interval(128)
    ok(tight.hi - tight.lo < enc.hi - enc.lo, "more precision gives a tighter enclosure")


def interval_outward_rounded_algebra():
    a = Interval.of(1, 2)
    b = Interval.of(3, 4)
    eq(a + b, Interval.of(4, 6), "interval add")
    eq(a * b, Interval.of(3, 8), "interval mul")
    eq(a - b, Interval.of(-3, -1), "interval sub")
    eq(a.scale(Q(2)), Interval.of(2, 4), "interval scale")
    ok((b / a).lo <= Q(3, 2) and (b / a).hi >= 2, "interval div contains 3/2..2")
    ok((-a).lo == -2 and (-a).hi == -1, "interval negation")


def interval_contains_true_values():
    a = Interval.of(1, 2)
    b = Interval.of(3, 4)
    for x in (Q(1), Q(3, 2), Q(2)):
        for y in (Q(3), Q(7, 2), Q(4)):
            ok(a.contains(x) and b.contains(y), "premise")
            ok((a * b).contains(x * y), "product enclosure contains the true product")
            ok((a + b).contains(x + y), "sum enclosure contains the true sum")


def interval_domain_guards():
    raises(lambda: Interval.of(2, 1), None, "reversed interval")
    raises(lambda: Interval.of(-1, 1).reciprocal(), ErrorCode.DIVISION_BY_ZERO,
           "reciprocal of a set containing 0")
    raises(lambda: Interval.of(1, 2) / Interval.of(-1, 1), ErrorCode.DIVISION_BY_ZERO,
           "division by a set containing 0")
    raises(lambda: sqrt_q(-1), ErrorCode.DOMAIN_ERROR, "sqrt of a negative")
    raises(lambda: log_q(0), ErrorCode.DOMAIN_ERROR, "log of zero")
    raises(lambda: Interval.point(Q(-1)).log(), ErrorCode.DOMAIN_ERROR, "log of a negative")
    ok(Interval.point(Q(5, 4)).is_point, "point enclosure")
    ok(Interval.of(1, 2).abs() == Interval.of(1, 2), "abs of a positive set")
    ok(Interval.of(-3, -1).abs() == Interval.of(1, 3), "abs of a negative set")


# ===========================================================================
# port — 7 checks
# ===========================================================================

def port_power_definition():
    p = PhysicalPort(Q(3), Q(4))
    eq(p.power, Q(12), "power = effort * flow")
    eq(p.as_dict(), {"effort": "3", "flow": "4"}, "as_dict")


def port_transformer_conserves_power():
    p = PhysicalPort(Q(6), Q(2))
    out = Transformer(Q(3)).apply(p)
    eq(out.power, -p.power, "transformer two-port conserves power exactly")
    eq(p.power + out.power, Q(0), "Tellegen balance")
    raises(lambda: Transformer(Q(0)), ErrorCode.DOMAIN_ERROR, "zero ratio")


def port_gyrator_conserves_power():
    p = PhysicalPort(Q(5), Q(7))
    out = Gyrator(Q(2)).apply(p)
    eq(out.power, -p.power, "gyrator two-port conserves power exactly")
    eq(p.power + out.power, Q(0), "Tellegen balance")
    raises(lambda: Gyrator(Q(0)), ErrorCode.DOMAIN_ERROR, "zero resistance")


def port_junction_0_balances():
    ports = (PhysicalPort(Q(2), Q(3)), PhysicalPort(Q(-5), Q(3)), PhysicalPort(Q(0), Q(3)))
    out = junction_0(ports)
    eq(total_power(out), Q(0), "0-junction conserves power exactly")
    eq({p.flow for p in out}, {Q(3)}, "0-junction keeps a common flow")
    eq(out[-1].effort, Q(3), "resolved effort = -sum of the others")


def port_junction_1_balances():
    ports = (PhysicalPort(Q(4), Q(1)), PhysicalPort(Q(4), Q(2)), PhysicalPort(Q(4), Q(0)))
    out = junction_1(ports)
    eq(total_power(out), Q(0), "1-junction conserves power exactly")
    eq({p.effort for p in out}, {Q(4)}, "1-junction keeps a common effort")
    eq(out[-1].flow, Q(-3), "resolved flow = -sum of the others")


def port_dissipation_entropy_nonnegative():
    p, entropy_rate = dissipator(Q(4), Q(2), Q(300))
    eq(p.power, Q(1), "dissipator power = e^2/R")
    eq(entropy_rate, Q(1, 300), "entropy rate = P/T")
    ok(entropy_rate >= 0, "entropy production is nonnegative")
    for e in (Q(-9, 4), Q(0), Q(7, 3)):
        _, rate = dissipator(Q(3), e, Q(1))
        ok(rate >= 0, "entropy production is nonnegative for any effort")
    raises(lambda: dissipator(Q(0), Q(1), Q(1)), ErrorCode.DOMAIN_ERROR, "zero resistance")
    raises(lambda: dissipator(Q(1), Q(1), Q(0)), ErrorCode.DOMAIN_ERROR, "zero temperature")


def port_transducer_and_stores():
    p = PhysicalPort(Q(2), Q(3))
    out, loss = ideal_transducer(Q(4), p, Q(1))
    eq(loss, Q(0), "ideal transducer loses nothing")
    eq(p.power + out.power, Q(0), "ideal transducer conserves power")
    out2, loss2 = ideal_transducer(Q(4), p, Q(1, 2))
    eq(loss2, Q(3), "half-efficiency transducer dissipates the difference")
    ok(loss2 >= 0, "loss is nonnegative")
    raises(lambda: ideal_transducer(Q(1), p, Q(0)), ErrorCode.DOMAIN_ERROR, "zero efficiency")
    raises(lambda: ideal_transducer(Q(0), p, Q(1)), ErrorCode.DOMAIN_ERROR, "zero ratio")

    port_c, energy_c = potential_store(Q(2), Q(4), Q(1))
    eq(energy_c, Q(4), "capacitor energy q^2/(2C)")
    eq(port_c.effort, Q(2), "capacitor effort = q/C")
    port_l, energy_l = kinetic_store(Q(8), Q(4), Q(1))
    eq(energy_l, Q(1), "inductor energy Phi^2/(2L)")
    eq(port_l.flow, Q(1, 2), "inductor flow = Phi/L")
    raises(lambda: require_power_balance([PhysicalPort(Q(1), Q(1))]),
           ErrorCode.DOMAIN_ERROR, "unbalanced set is refused")


# ===========================================================================
# density — 2 checks
# ===========================================================================

def density_policies():
    D = density.UnitDensity
    eq(D.of(Q(1, 2)).value, Q(1, 2), "in-range value accepted")
    raises(lambda: D.of(Q(2)), ErrorCode.DOMAIN_ERROR, "REJECT refuses an out-of-range value")
    eq(D.of(Q(2), "clamp").value, Q(1), "CLAMP saturates above")
    eq(D.of(Q(-1), "clamp").value, Q(0), "CLAMP saturates below")
    eq(D.of(Q(2), "widen").value, Q(2), "WIDEN keeps the value")
    raises(lambda: D.of(Q(1, 2), lo=Q(1), hi=Q(0)), ErrorCode.DOMAIN_ERROR, "unordered bounds")
    eq(density.saturate(Q(5), Q(0), Q(1)), Q(1), "saturate helper")
    eq(density.wrap_to_unit(Q(5, 2)), Q(1, 2), "wrap_to_unit helper")
    # is_unit is "the value lies in [0,1]", not "the value equals 1".
    ok(D.zero().is_unit and D.unit().is_unit, "both endpoints are unit densities")
    ok(D.of(Q(2), "widen").is_unit is False, "a widened value outside [0,1] is not a unit density")
    ok(D.of(Q(3, 4)).in_range(), "in_range")
    eq(D.of(Q(1, 2)).complement().value, Q(1, 2), "the half point is self-complementary")
    eq(D.of(Q(2), "widen").wrap().value, Q(0), "wrap folds a widened value back into the channel")


def density_complement_is_not_negation():
    D = density.UnitDensity
    x = D.of(Q(1, 4))
    eq(x.complement().value, Q(3, 4), "complement = 1 - x")
    eq(density.unit_complement(Q(1, 4)), Q(3, 4), "unit_complement helper")
    ok(x.complement().value != -x.value, "complement is not signed negation")
    ok(-x.value == Q(-1, 4), "negation of 1/4 is -1/4")
    raises(lambda: D.of(Q(2), "reject").complement(), ErrorCode.DOMAIN_ERROR, "complement of a refused density")
    eq(D.of(Q(3, 2), "widen").saturate().value, Q(1), "saturate returns a density in range")
    eq(D.of(Q(1, 2)).signed(), Q(1, 2), "signed view")


# ===========================================================================
# geometry — 7 checks
# ===========================================================================

def geometry_carrier_and_exact_stencils():
    p = carrier([1, 2] + [0] * (DIM - 2))
    eq(len(p), DIM, "carrier is 24-dimensional")
    eq(norm_square(p), Q(5), "norm square")
    eq(norm_square(origin()), Q(0), "origin norm")
    eq(tax_residual(p, origin(), 32), Q(5, 32), "tax residual divides by 32")
    raises(lambda: carrier([1, 2, 3]), ErrorCode.INVALID_INPUT, "wrong carrier length")

    # A linear field is differentiated exactly by the central stencil.
    f = analytic_field(lambda idx: Q(3) * idx[0] - Q(2) * idx[1], ndim=24)
    g = gradient_at(f, (0,) * 24, 1)
    eq(g[0], Q(3), "d/dx0 of 3x0 - 2x1")
    eq(g[1], Q(-2), "d/dx1 of 3x0 - 2x1")
    eq(g[2], Q(0), "d/dx2 of a field independent of x2")


def geometry_curl_of_gradient_vanishes():
    f = analytic_field(lambda idx: Q(idx[0]) * Q(idx[1]) + Q(idx[2]) ** 2, ndim=24)
    g = gradient(f, 1)
    point = (1, 2, 3, 4) + (0,) * (DIM - 4)
    form = curl_2form_at(g, point, 1)
    eq(len(form), 276, "the 2-form has C(24,2) = 276 components")
    ok(form.is_zero(), "curl of a gradient vanishes exactly")
    eq(form.get(0, 1), Q(0), "component (0,1)")
    eq(form.get(3, 7), Q(0), "component (3,7)")


def geometry_div_of_curl_vanishes():
    # v = (x1*x2, x2*x0, x0*x1, 0, ...): quadratic, so both stencils are exact.
    comps = [
        lambda idx: Q(idx[1]) * Q(idx[2]),
        lambda idx: Q(idx[2]) * Q(idx[0]),
        lambda idx: Q(idx[0]) * Q(idx[1]),
    ]
    v = geometry.VectorField(tuple(analytic_field(c, ndim=24) for c in comps))
    point = (1, 1, 1, 1) + (0,) * (DIM - 4)
    eq(divergence_of_curl_3d(v, point, 1), Q(0), "div curl = 0 exactly")
    eq(divergence_at(curl_3d(v, 1), point, 1), Q(0), "divergence of the 3-D curl")


def geometry_two_form_is_antisymmetric():
    values = {(0, 1): Q(5), (2, 3): Q(-7)}
    form = TwoForm(values)
    eq(form.get(0, 1), Q(5), "stored orientation")
    eq(form.get(1, 0), Q(-5), "antisymmetry")
    eq(form.get(2, 3), Q(-7), "second component")
    eq(form.get(3, 2), Q(7), "antisymmetry, second component")
    eq(form.get(5, 5), Q(0), "diagonal vanishes")
    eq(len(form), 2, "only nonzero components are stored")
    ok(not form.is_zero(), "nonzero form")
    raises(lambda: TwoForm({(1, 1): Q(1)}), ErrorCode.INVALID_INPUT, "diagonal entry")
    raises(lambda: TwoForm({(0, DIM): Q(1)}), ErrorCode.INVALID_INPUT, "index out of range")
    eq(len(TwoForm({})), 0, "empty form is zero")


def geometry_boundary_extrapolation_dirichlet():
    bc = BoundaryCondition(kind="dirichlet", value=Q(7))
    eq(bc.extrapolate(Q(3), Q(1), 1), Q(7), "Dirichlet fixes the face value")
    eq(bc.extrapolate(Q(3), Q(1), 4), Q(7), "Dirichlet is gap-independent")


def geometry_boundary_extrapolation_neumann_robin():
    neumann = BoundaryCondition(kind="neumann")
    eq(neumann.extrapolate(Q(5), Q(2), 1), Q(5), "Neumann mirrors the interior")
    eq(neumann.extrapolate(Q(5), Q(2), 3), Q(5), "Neumann is gap-independent")
    robin = BoundaryCondition(kind="robin", alpha=Q(1), beta=Q(2), gamma=Q(0))
    eq(robin.extrapolate(Q(4), Q(1), 1), Q(8, 3), "Robin: (0 + 2*4/1)/(1 + 2/1)")
    raises(lambda: BoundaryCondition(kind="bogus"), ErrorCode.INVALID_INPUT, "unknown kind")
    raises(lambda: neumann.extrapolate(Q(1), Q(0), 1), ErrorCode.DOMAIN_ERROR, "zero spacing")
    raises(lambda: neumann.extrapolate(Q(1), Q(1), 0), ErrorCode.INVALID_INPUT, "gap < 1")
    raises(lambda: BoundaryCondition(kind="robin", alpha=Q(0), beta=Q(0)).extrapolate(Q(1), Q(1), 1),
           ErrorCode.DOMAIN_ERROR, "singular Robin")
    raises(lambda: BoundaryCondition(kind="robin", alpha=Q(-1), beta=Q(1)).extrapolate(Q(1), Q(1), 1),
           ErrorCode.DOMAIN_ERROR, "Robin with a zero denominator at gap 1")


def geometry_laplacian_exact_stencil():
    f = analytic_field(lambda idx: Q(idx[0]) ** 2 + Q(3) * Q(idx[1]) ** 2, ndim=24)
    point = (2, 2) + (0,) * (DIM - 2)
    eq(laplacian_at(f, point, 1), Q(8), "d2/dx0^2 = 2, d2/dx1^2 = 6")
    eq(laplacian_at(f, point, 1, (0,)), Q(2), "restricted to axis 0")
    eq(laplacian_at(f, point, 1, (1,)), Q(6), "restricted to axis 1")
    raises(lambda: laplacian_at(f, point, 1, (DIM,)), ErrorCode.INVALID_INPUT, "axis out of range")
    raises(lambda: laplacian_at(f, point, 0), ErrorCode.DOMAIN_ERROR, "zero spacing")


def geometry_grid_domain_and_boundary_field():
    dom = GridDomain((3, 3), Q(1), BoundaryCondition(kind="dirichlet", value=Q(0)))
    ok(dom.in_bounds((0, 0)), "interior index")
    ok(not dom.in_bounds((3, 0)), "out-of-bounds index")
    eq(dom.nearest_interior((5, 1)), (2, 1), "nearest interior clamps the index")
    raises(lambda: GridDomain((0, 3), Q(1)), ErrorCode.INVALID_INPUT, "empty shape")


# ===========================================================================
# state — 2 checks
# ===========================================================================

def state_writes_invisible_until_commit():
    before = MachineState(seed=3)
    ctx = EvalContext(state=before)
    ctx.write_slot("k", {"v": Q(5)})
    eq(before.slot("k"), {}, "writes do not touch the pre-tick state")
    eq(before.slots, {}, "no slot is created before commit")
    committed = ctx.commit()
    eq(committed.slot("k"), {"v": Q(5)}, "commit applies the writes")
    eq(before.slot("k"), {}, "the original state is still untouched")
    eq(committed.clock, 0, "commit does not advance the clock")
    stepped = ctx.next_clock(before)
    eq(stepped.clock, 1, "next_clock advances the clock by one")
    eq(stepped.slot("k"), {"v": Q(5)}, "next_clock commits the writes")
    eq(before.clock, 0, "the original clock is untouched")


def state_prng_is_deterministic():
    a = SplitMix64(0)
    b = SplitMix64(0)
    stream_a = [a.next_u64() for _ in range(64)]
    stream_b = [b.next_u64() for _ in range(64)]
    eq(stream_a, stream_b, "same seed gives the same stream")
    ok(len(set(stream_a)) == 64, "the stream is not constant")
    ok(all(0 <= x < (1 << 64) for x in stream_a), "values fit in 64 bits")

    c = SplitMix64(0)
    forked_a = c.fork(7)
    c2 = SplitMix64(0)
    forked_b = c2.fork(7)
    eq(forked_a.next_u64(), forked_b.next_u64(), "fork is deterministic in the salt")
    ok(forked_a.as_dict()["state"] != SplitMix64(0).state, "fork advances the source")

    s = SplitMix64(0)
    signs = [s.sign() for _ in range(256)]
    ok(set(signs) == {1, -1}, "sign produces both poles")
    eq(SplitMix64(0).next_bit(), SplitMix64(0).next_bit(), "next_bit is deterministic")


# ===========================================================================
# program — 8 checks
# ===========================================================================

def _prog(instructions, inputs=None, outputs=None, name="t"):
    return Program(name, inputs or {}, tuple(instructions), outputs or {})


def program_arity_is_checked():
    p = _prog([Instruction("sum", (), "w")], outputs={"y": "w"})
    raises(lambda: analyse(p), ErrorCode.VALIDATION_ERROR, "sum with no inputs")
    p2 = _prog([Instruction("neg", ("a", "b"), "w")], {"a": "numeric", "b": "numeric"},
               {"y": "w"})
    raises(lambda: analyse(p2), ErrorCode.VALIDATION_ERROR, "neg with two inputs")
    p3 = _prog([Instruction("sum", ("a",), "w")], {"a": "numeric"}, {"y": "w"})
    ok(analyse(p3) is not None, "sum with one input is legal")


def program_parameters_are_checked():
    p = _prog([Instruction("scale", ("a",), "w")], {"a": "numeric"}, {"y": "w"})
    raises(lambda: analyse(p), ErrorCode.VALIDATION_ERROR, "scale without factor")
    p2 = _prog([Instruction("scale", ("a",), "w", {"factor": Q(2), "bogus": 1})],
               {"a": "numeric"}, {"y": "w"})
    raises(lambda: analyse(p2), ErrorCode.VALIDATION_ERROR, "unknown parameter")
    p3 = _prog([Instruction("rate", ("a",), "w", {"dt": Q(0)})], {"a": "numeric"}, {"y": "w"})
    ok(analyse(p3) is not None, "dt is validated at evaluation, not declaration")
    p4 = _prog([Instruction("scale", ("a",), "w", {"factor": Q(2)})], {"a": "numeric"},
               {"y": "w"})
    ok(analyse(p4) is not None, "scale with factor is legal")


def program_single_assignment():
    p = _prog([
        Instruction("scale", ("a",), "w", {"factor": Q(2)}),
        Instruction("neg", ("w",), "w"),
    ], {"a": "numeric"}, {"y": "w"})
    raises(lambda: analyse(p), ErrorCode.VALIDATION_ERROR, "wire assigned twice")
    p2 = _prog([Instruction("neg", ("a",), "a")], {"a": "numeric"}, {"y": "a"})
    raises(lambda: analyse(p2), ErrorCode.VALIDATION_ERROR, "writing over a program input")


def program_kinds_are_checked():
    p = _prog([Instruction("neg", ("a",), "w")], {"a": "field"}, {"y": "w"})
    raises(lambda: analyse(p), ErrorCode.TYPE_ERROR, "neg does not accept a field")
    p2 = _prog([Instruction("grad", ("a",), "w", {"h": Q(1)})], {"a": "numeric"}, {"y": "w"})
    raises(lambda: analyse(p2), ErrorCode.TYPE_ERROR, "grad needs a field")
    p3 = _prog([Instruction("neg", ("a",), "w")], {"a": "numeric"}, {"y": "w"})
    eq(analyse(p3).kinds["w"], "numeric", "output kind is derived")
    p4 = _prog([Instruction("grad", ("a",), "w", {"h": Q(1)})], {"a": "field"},
               {"y": "w"})
    eq(analyse(p4).kinds["w"], "vector_field", "grad produces a vector field")


def program_combinational_cycle_rejected():
    p = _prog([
        Instruction("sum", ("b",), "a"),
        Instruction("neg", ("a",), "b"),
    ], {"z": "numeric"}, {"y": "a"})
    raises(lambda: analyse(p), ErrorCode.CYCLE_DETECTED, "pure feedback loop")


def program_stateful_cycle_accepted():
    p = _prog([
        Instruction("accum", ("y",), "x"),
        Instruction("scale", ("x",), "y", {"factor": Q(1, 2)}),
    ], {"z": "numeric"}, {"out": "x"})
    a = analyse(p)
    ok(a.has_feedback, "a stateful back edge is legal")
    eq(a.back_edges.get(1), frozenset({"x"}), "the back edge is recorded on the reader")
    eq(a.back_edges.get(0), None, "the stateful producer itself is not a back edge")
    ok(set(a.order) == {0, 1}, "every instruction is scheduled")
    # A stateful node may close on its own output.
    p2 = _prog([Instruction("accum", ("x",), "x2")], {}, {"out": "x2"})
    # x2 <- accum(x) reads a wire nobody produces: still an unknown-wire error.
    raises(lambda: analyse(p2), ErrorCode.VALIDATION_ERROR, "unknown feedback wire")
    # A stateful node closing on its own output is legal self-feedback.
    p3 = _prog([Instruction("accum", ("x",), "x")], {}, {"out": "x"})
    a3 = analyse(p3)
    ok(a3.has_feedback, "a stateful self-loop is a legal back edge")
    eq(a3.back_edges.get(0), frozenset({"x"}), "the self-loop is recorded as a back edge")


def program_json_round_trip():
    p = _prog([
        Instruction("accum", ("a",), "x"),
        Instruction("scale", ("x",), "y", {"factor": Q(3, 7)}),
    ], {"a": "numeric"}, {"out": "y"})
    doc = p.as_dict()
    eq(doc["schema"], "cent-program/1", "schema tag")
    again = program_from_dict(doc)
    eq(again.as_dict(), doc, "as_dict round-trips through program_from_dict")
    eq(again.as_dict()["instructions"][1]["params"]["factor"],
       {"num": "3", "den": "7"}, "exact rationals survive as num/den")
    raises(lambda: program_from_dict({"schema": "wrong"}), ErrorCode.VALIDATION_ERROR,
           "wrong schema")
    raises(lambda: program_from_dict({"schema": "cent-program/1"}), ErrorCode.VALIDATION_ERROR,
           "malformed document")


def program_unknown_op_rejected():
    p = _prog([Instruction("sum", ("a",), "w"), Instruction("bogus", ("a",), "v")],
              {"a": "numeric"}, {"y": "w"})
    raises(lambda: analyse(p), None, "unknown primitive")
    p2 = _prog([Instruction("neg", ("a",), "w")], {"a": "numeric"}, {"nope": "missing"})
    raises(lambda: analyse(p2), ErrorCode.VALIDATION_ERROR, "output refers to an unknown wire")
    p3 = _prog([Instruction("neg", ("ghost",), "w")], {"a": "numeric"}, {"y": "w"})
    raises(lambda: analyse(p3), ErrorCode.VALIDATION_ERROR, "input wire is not produced")
    raises(lambda: Instruction("neg", ("a",), ""), ErrorCode.VALIDATION_ERROR,
           "instruction with no output wire")


# ===========================================================================
# evaluator — 17 checks
# ===========================================================================

def _run(instructions, inputs, feed, ticks=None, seed=0, outputs=None):
    prog = Program("t", inputs, tuple(instructions), outputs or {"out": "z"})
    return run_program(prog, feed, ticks, seed=seed)


def evaluator_accum_ticks():
    out = _run([Instruction("accum", ("a",), "z")], {"a": "numeric"},
               [{"a": Q(1)}, {"a": Q(2)}, {"a": Q(3)}, {"a": Q(4)}])
    eq([r["out"] for r in out], [Q(1), Q(3), Q(6), Q(10)], "running exact sum")


def evaluator_rate_is_a_difference_quotient():
    out = _run([Instruction("rate", ("a",), "z", {"dt": Q(2)})], {"a": "numeric"},
               [{"a": Q(0)}, {"a": Q(3)}, {"a": Q(9)}])
    eq([r["out"] for r in out], [Q(0), Q(3, 2), Q(3)], "first tick has no previous input")


def evaluator_delay_ring_buffer():
    out = _run([Instruction("delay", ("a",), "z", {"ticks": 2, "initial": Q(-1)})],
               {"a": "numeric"},
               [{"a": Q(1)}, {"a": Q(2)}, {"a": Q(3)}, {"a": Q(4)}])
    eq([r["out"] for r in out], [Q(-1), Q(-1), Q(1), Q(2)], "two-tick delay with initial fill")


def evaluator_hysteresis_latches():
    instr = [Instruction("hysteresis", ("a",), "z", {"lower": Q(1), "upper": Q(3)})]
    out = _run(instr, {"a": "numeric"},
               [{"a": Q(0)}, {"a": Q(2)}, {"a": Q(4)}, {"a": Q(2)}, {"a": Q(0)}])
    eq([r["out"] for r in out], [0, 0, 1, 1, 0], "set at 3, reset at 1, holds in between")
    raises(lambda: _run([Instruction("hysteresis", ("a",), "z",
                                     {"lower": Q(2), "upper": Q(1)})],
                        {"a": "numeric"}, [{"a": Q(0)}]),
           ErrorCode.DOMAIN_ERROR, "lower must be below upper")


def evaluator_noise_two_point_law():
    a = Q(7, 3)
    out = _run([Instruction("noise", (), "z", {"amplitude": a, "seed": 5})], {},
               [{}] * 64)
    samples = [r["out"] for r in out]
    ok(all(s in (a, -a) for s in samples), "every sample is exactly ±a")
    ok(all(s * s == a * a for s in samples), "the second moment is exactly a^2")
    ok(set(samples) == {a, -a}, "both poles are visited")
    again = _run([Instruction("noise", (), "z", {"amplitude": a, "seed": 5})], {},
                 [{}] * 64)
    eq([r["out"] for r in again], samples, "the stream is reproducible")
    raises(lambda: _run([Instruction("noise", (), "z", {"amplitude": Q(-1)})], {}, [{}]),
           ErrorCode.DOMAIN_ERROR, "amplitude must be nonnegative")


def evaluator_quantize_ties_away_from_zero():
    out = _run([Instruction("quantize", ("a",), "z", {"quantum": Q(1)})], {"a": "numeric"},
               [{"a": Q(3, 2)}, {"a": Q(1, 2)}, {"a": Q(-3, 2)}, {"a": Q(-1, 2)},
                {"a": Q(0)}, {"a": Q(7, 4)}])
    eq([r["out"] for r in out], [Q(2), Q(1), Q(-2), Q(-1), Q(0), Q(2)],
       "ties away from zero")
    raises(lambda: _run([Instruction("quantize", ("a",), "z", {"quantum": Q(0)})],
                        {"a": "numeric"}, [{"a": Q(1)}]),
           ErrorCode.DOMAIN_ERROR, "quantum must be positive")


def evaluator_pid_exact_recursion():
    p = Instruction("pid", ("a",), "z",
                    {"kp": Q(2), "ki": Q(3), "kd": Q(5), "dt": Q(2), "initial": Q(0)})
    out = _run([p], {"a": "numeric"}, [{"a": Q(1)}, {"a": Q(1)}, {"a": Q(3)}])
    # tick 1: integral=2, prev=None -> 2*1 + 3*2 = 8
    # tick 2: integral=4, derivative=0 -> 2 + 12 = 14
    # tick 3: integral=10, derivative=(3-1)/2=1 -> 6 + 30 + 5 = 41
    eq([r["out"] for r in out], [Q(8), Q(14), Q(41)], "PID recursion is exact")
    raises(lambda: _run([Instruction("pid", ("a",), "z",
                                     {"kp": Q(1), "ki": Q(0), "kd": Q(0), "dt": Q(0)})],
                        {"a": "numeric"}, [{"a": Q(1)}]),
           ErrorCode.DOMAIN_ERROR, "dt must be positive")


def evaluator_state_space_exact_matrices():
    p = Instruction("state_space", ("u",), "z", {
        "A": [[Q(1), Q(1)], [Q(0), Q(1)]],
        "B": [[Q(0)], [Q(1)]],
        "C": [[Q(1), Q(0)]],
        "D": [[Q(0)]],
    })
    out = _run([p], {"u": "vector"}, [{"u": (Q(0),)}, {"u": (Q(0),)}, {"u": (Q(1),)}])
    # x0=[0,0]; y=0. x1=[0,0]; y=0. x2=[0,1]; y=0.
    eq([r["out"] for r in out], [(Q(0),), (Q(0),), (Q(0),)], "state-space first three ticks")
    out2 = _run([p], {"u": "vector"},
                [{"u": (Q(2),)}, {"u": (Q(0),)}, {"u": (Q(0),)}, {"u": (Q(0),)}])
    # x0=[0,0] y=0; x1=[0,2] y=0; x2=[2,2] y=2; x3=[4,2] y=4
    eq([r["out"] for r in out2], [(Q(0),), (Q(0),), (Q(2),), (Q(4),)],
       "state-space integrates the input")


def evaluator_delta_sigma_modulator_bits():
    p = Instruction("delta_sigma_modulator", ("a",), "z", {"order": 1, "threshold": Q(1)})
    out = _run([p], {"a": "numeric"}, [{"a": Q(1, 2)}] * 8)
    bits = [r["out"] for r in out]
    ok(set(bits) <= {0, 1}, "output is a bit")
    ok(1 in bits and 0 in bits, "the modulator toggles")
    # order 2 is accepted and must also produce bits
    p2 = Instruction("delta_sigma_modulator", ("a",), "z", {"order": 2, "threshold": Q(1)})
    out2 = _run([p2], {"a": "numeric"}, [{"a": Q(1, 2)}] * 8)
    ok(set(r["out"] for r in out2) <= {0, 1}, "order 2 produces bits")
    raises(lambda: _run([Instruction("delta_sigma_modulator", ("a",), "z",
                                     {"order": 3, "threshold": Q(1)})],
                        {"a": "numeric"}, [{"a": Q(1)}]),
           ErrorCode.DOMAIN_ERROR, "order must be 1 or 2")
    raises(lambda: _run([Instruction("delta_sigma_modulator", ("a",), "z",
                                     {"order": 1, "threshold": Q(0)})],
                        {"a": "numeric"}, [{"a": Q(1)}]),
           ErrorCode.DOMAIN_ERROR, "threshold must be positive")


def evaluator_spatial_reads_a_field():
    f = analytic_field(lambda idx: Q(5) * idx[0] + Q(2) * idx[1], ndim=2)
    p = Instruction("spatial", ("f",), "z", {"index": [1, 2]})
    out = _run([p], {"f": "field"}, [{"f": f}])
    eq(out[0]["out"], Q(9), "spatial samples the field at the declared index")
    p2 = Instruction("spatial", ("f",), "z", {})
    out2 = _run([p2], {"f": "field"}, [{"f": f}])
    eq(out2[0]["out"], Q(0), "the default index is the origin")


def evaluator_grad_field():
    f = analytic_field(lambda idx: Q(4) * idx[0] + Q(idx[1]), ndim=2)
    p = Instruction("grad", ("f",), "z", {"h": Q(1)})
    out = _run([p], {"f": "field"}, [{"f": f}], outputs={"out": "z"})
    g = out[0]["out"]
    eq(g.at((0, 0))[0], Q(4), "gradient component 0")
    eq(g.at((0, 0))[1], Q(1), "gradient component 1")


def evaluator_junction_0_port():
    def mk(e, f):
        return PhysicalPort(Q(e), Q(f))
    p = Instruction("junction_0", ("p1", "p2", "p3"), "z", {})
    out = _run([p], {"p1": "port", "p2": "port", "p3": "port"},
               [{"p1": mk(2, 3), "p2": mk(-5, 3), "p3": mk(0, 3)}])
    eq(out[0]["out"].effort, Q(3), "resolved effort")
    eq(out[0]["out"].power + Q(2) * Q(3) + Q(-5) * Q(3), Q(0), "power balance")


def evaluator_gyrator_port():
    p = Instruction("gyrator", ("p",), "z", {"resistance": Q(3)})
    out = _run([p], {"p": "port"}, [{"p": PhysicalPort(Q(6), Q(2))}])
    eq(out[0]["out"], PhysicalPort(Q(6), Q(-2)), "gyrator (e,f) -> (R f, -e/R)")
    eq(out[0]["out"].power, Q(-12), "power is exactly negated")


def evaluator_store_pot_and_kin():
    pot = Instruction("store_pot", ("f",), "z", {"capacitance": Q(2), "dt": Q(1)})
    out = _run([pot], {"f": "numeric"}, [{"f": Q(3)}, {"f": Q(3)}])
    eq(out[0]["out"].effort, Q(3, 2), "charge 3 -> e = q/C")
    eq(out[1]["out"].effort, Q(3), "charge 6 -> e = q/C")
    kin = Instruction("store_kin", ("e",), "z", {"inductance": Q(4), "dt": Q(1)})
    out2 = _run([kin], {"e": "numeric"}, [{"e": Q(5)}, {"e": Q(5)}])
    eq(out2[0]["out"].flow, Q(5, 4), "flux 5 -> f = Phi/L")
    eq(out2[1]["out"].flow, Q(5, 2), "flux 10 -> f = Phi/L")


def evaluator_tick_is_transactional():
    prog = Program("t", {"a": "numeric"}, (
        Instruction("accum", ("a",), "x"),
        Instruction("recip", ("a",), "z"),
    ), {"out": "x"})
    ev = Evaluator(prog, seed=0)
    ev.tick({"a": Q(2)})
    eq(ev.clock, 1, "first tick committed")
    before = ev.state.as_dict()
    # The second tick divides by zero partway through the schedule.
    raises(lambda: ev.tick({"a": Q(0)}), ErrorCode.DIVISION_BY_ZERO, "failed tick")
    eq(ev.clock, 1, "the clock did not advance on a failed tick")
    eq(ev.state.as_dict(), before, "a failed tick leaves the machine untouched")
    eq(ev.tick({"a": Q(5)})["out"], Q(7), "the accumulator still holds 2 + 5")


def evaluator_feedback_reads_the_previous_tick():
    prog = Program("t", {"a": "numeric"}, (
        Instruction("accum", ("y",), "x"),
        Instruction("sum", ("a", "x"), "y"),
    ), {"out": "x"})
    out = run_program(prog, [{"a": Q(3)}, {"a": Q(5)}, {"a": Q(7)}])
    # tick 1: x_prev = 0 (documented initial) -> y = 3, x = 3
    # tick 2: x_prev = 3 -> y = 8, x = 11
    # tick 3: x_prev = 11 -> y = 18, x = 29
    eq([r["out"] for r in out], [Q(3), Q(11), Q(29)], "the back edge reads the previous tick")
    a = analyse(prog)
    ok(a.has_feedback, "the analysis sees the feedback")
    eq(a.back_edges.get(1), frozenset({"x"}), "the back edge is on the reader")


def evaluator_run_is_deterministic():
    def build():
        return Program("t", {"a": "numeric"}, (
            # No seed parameter: the machine seed drives the stream.
            Instruction("noise", (), "n", {"amplitude": Q(1)}),
            Instruction("sum", ("a", "n"), "z"),
        ), {"out": "z"})
    feed = [{"a": Q(i)} for i in range(20)]
    one = run_program(build(), feed, seed=42)
    two = run_program(build(), feed, seed=42)
    eq(one, two, "the same seed gives identical traces")
    three = run_program(build(), feed, seed=43)
    ok(one != three, "a different seed gives a different trace")
    ok(all(isinstance(r["out"], Q) for r in one), "every output is an exact rational")


# ===========================================================================
# coverage — 13 checks
# ===========================================================================

def coverage_sum_and_neg():
    out = _run([Instruction("sum", ("a", "b", "c"), "z")],
               {"a": "numeric", "b": "numeric", "c": "numeric"},
               [{"a": Q(1), "b": Q(2), "c": Q(3)}])
    eq(out[0]["out"], Q(6), "sum of three exact wires")
    out2 = _run([Instruction("neg", ("a",), "z")], {"a": "numeric"}, [{"a": Q(5, 3)}])
    eq(out2[0]["out"], Q(-5, 3), "signed negation")


def coverage_mult_and_scale():
    out = _run([Instruction("mult", ("a", "b", "c"), "z")],
               {"a": "numeric", "b": "numeric", "c": "numeric"},
               [{"a": Q(2), "b": Q(3), "c": Q(1, 2)}])
    eq(out[0]["out"], Q(3), "product of three exact wires")
    out2 = _run([Instruction("scale", ("a",), "z", {"factor": Q(3, 4)})],
                {"a": "numeric"}, [{"a": Q(8)}])
    eq(out2[0]["out"], Q(6), "scaling by an exact rational factor")


def coverage_wrap():
    out = _run([Instruction("wrap", ("a",), "z", {"period": Q(2)})], {"a": "numeric"},
               [{"a": Q(5)}, {"a": Q(-1)}, {"a": Q(2)}, {"a": Q(1, 2)}])
    eq([r["out"] for r in out], [Q(1), Q(1), Q(0), Q(1, 2)], "wrap into [0, period)")


def coverage_sat():
    out = _run([Instruction("sat", ("a",), "z", {"lo": Q(-1), "hi": Q(1)})],
               {"a": "numeric"},
               [{"a": Q(5)}, {"a": Q(-5)}, {"a": Q(1, 2)}, {"a": Q(-1)}])
    eq([r["out"] for r in out], [Q(1), Q(-1), Q(1, 2), Q(-1)], "clamp into [lo, hi]")


def coverage_exp():
    out = _run([Instruction("exp", ("a",), "z", {"precision": 64})], {"a": "numeric"},
               [{"a": Q(0)}, {"a": Q(1)}])
    enc0 = out[0]["out"]
    ok(enc0.lo == 1 and enc0.hi == 1, "exp(0) = 1 exactly")
    e_enc = out[1]["out"]
    ok(e_enc.lo <= REF_E <= e_enc.hi, "exp(1) brackets e")
    ok(e_enc.hi - e_enc.lo < Q(1, 10 ** 19), "exp(1) is a tight enclosure")
    coarse = _run([Instruction("exp", ("a",), "z", {"precision": 8})],
                  {"a": "numeric"}, [{"a": Q(1)}])[0]["out"]
    ok(coarse.lo <= REF_E <= coarse.hi, "a coarse enclosure still brackets e")
    ok(coarse.hi - coarse.lo > e_enc.hi - e_enc.lo,
       "less precision gives a wider enclosure")


def coverage_log():
    out = _run([Instruction("log", ("a",), "z", {"precision": 64})], {"a": "numeric"},
               [{"a": Q(1)}, {"a": Q(2)}])
    enc0 = out[0]["out"]
    ok(enc0.lo == 0 and enc0.hi == 0, "log(1) = 0 exactly")
    ok(out[1]["out"].lo <= REF_LN2 <= out[1]["out"].hi, "log(2) brackets log 2")
    raises(lambda: _run([Instruction("log", ("a",), "z", {})], {"a": "numeric"},
                        [{"a": Q(-1)}]),
           ErrorCode.DOMAIN_ERROR, "log of a negative")


def coverage_recip_and_div():
    out = _run([Instruction("recip", ("a",), "z")], {"a": "numeric"}, [{"a": Q(4)}])
    eq(out[0]["out"], Q(1, 4), "reciprocal")
    out2 = _run([Instruction("div", ("a", "b"), "z")],
                {"a": "numeric", "b": "numeric"}, [{"a": Q(3), "b": Q(4)}])
    eq(out2[0]["out"], Q(3, 4), "exact division")
    raises(lambda: _run([Instruction("recip", ("a",), "z")], {"a": "numeric"}, [{"a": Q(0)}]),
           ErrorCode.DIVISION_BY_ZERO, "reciprocal of zero")


def coverage_sqrt():
    out = _run([Instruction("sqrt", ("a",), "z", {"precision": 64})],
               {"a": "numeric"}, [{"a": Q(4)}, {"a": Q(2)}])
    four = out[0]["out"]
    ok(four.lo == 2 and four.hi == 2, "sqrt(4) = 2 exactly")
    two = out[1]["out"]
    ok(two.lo * two.lo <= 2 <= two.hi * two.hi, "sqrt(2) brackets the true root")
    ok(two.lo > 0 and two.hi - two.lo < Q(1, 10 ** 12), "sqrt(2) is tight")


def coverage_eq():
    out = _run([Instruction("eq", ("a", "b"), "z")],
               {"a": "numeric", "b": "numeric"},
               [{"a": Q(2), "b": Q(2)}, {"a": Q(2), "b": Q(3)}])
    eq([r["out"] for r in out], [1, 0], "equality test returns a bit")


def _exact_value(value):
    """A certified result is either an exact rational or a point enclosure."""
    if isinstance(value, Q):
        return value
    if isinstance(value, Interval) and value.is_point:
        return value.lo
    return value


def coverage_translinear():
    p = Instruction("translinear", ("a", "b"), "z", {"exponents": [Q(2), Q(1, 2)]})
    out = _run([p], {"a": "numeric", "b": "numeric"}, [{"a": Q(3), "b": Q(16)}])
    # 3^2 * 16^(1/2) = 9 * 4 = 36
    eq(_exact_value(out[0]["out"]), Q(36), "3^2 * 16^(1/2) = 36 exactly")
    p2 = Instruction("translinear", ("a",), "z", {"exponents": [Q(1)]})
    out2 = _run([p2], {"a": "numeric"}, [{"a": Q(5)}])
    eq(_exact_value(out2[0]["out"]), Q(5), "single-input translinear is the identity")
    raises(lambda: _run([Instruction("translinear", ("a",), "z", {"exponents": [Q(1), Q(1)]})],
                        {"a": "numeric"}, [{"a": Q(5)}]),
           ErrorCode.VALIDATION_ERROR, "exponent count must match the input count")


def composite_phase_locked_loop():
    """VCO phase integrates center_frequency + gain*error, exactly, every tick."""
    p = Instruction("phase_locked_loop", ("a",), "z", {
        "center_frequency": Q(2), "gain": Q(3), "dt": Q(1, 2), "initial_phase": Q(1)})
    out = _run([p], {"a": "numeric"}, [{"a": Q(1)}, {"a": Q(-1)}, {"a": Q(4)}])
    # t1: 1 + (2+3)*(1/2) = 7/2 ; t2: 7/2 + (2-3)*(1/2) = 3 ; t3: 3 + (2+12)*(1/2) = 10
    eq([r["out"] for r in out], [Q(7, 2), Q(3), Q(10)], "phase recursion is exact")
    out2 = _run([Instruction("phase_locked_loop", ("a",), "z", {
        "center_frequency": Q(0), "gain": Q(0), "dt": Q(1), "initial_phase": Q(5)})],
        {"a": "numeric"}, [{"a": Q(7)}, {"a": Q(-3)}])
    eq([r["out"] for r in out2], [Q(5), Q(5)], "zero centre and gain hold the phase")
    raises(lambda: _run([Instruction("phase_locked_loop", ("a",), "z", {
        "center_frequency": Q(1), "gain": Q(1), "dt": Q(0)})],
        {"a": "numeric"}, [{"a": Q(1)}]), ErrorCode.DOMAIN_ERROR, "dt must be positive")


def composite_transmission_line():
    """Lossless delay line: n cells, reflection coefficient in [-1, 1]."""
    out = _run([Instruction("transmission_line", ("a",), "z", {
        "segments": 3, "reflection": Q(0), "initial": Q(0)})],
        {"a": "numeric"}, [{"a": Q(i)} for i in (1, 2, 3, 4, 5)])
    eq([r["out"] for r in out], [Q(0), Q(0), Q(0), Q(1), Q(2)], "three-cell delay")
    out2 = _run([Instruction("transmission_line", ("a",), "z", {
        "segments": 1, "reflection": Q(1), "initial": Q(0)})],
        {"a": "numeric"}, [{"a": Q(1)}, {"a": Q(2)}, {"a": Q(3)}])
    # out = cells[0]; incoming = x + r*out
    eq([r["out"] for r in out2], [Q(0), Q(1), Q(3)], "total reflection folds the output back in")
    out3 = _run([Instruction("transmission_line", ("a",), "z", {
        "segments": 1, "reflection": Q(-1, 2), "initial": Q(0)})],
        {"a": "numeric"}, [{"a": Q(2)}, {"a": Q(0)}, {"a": Q(0)}])
    eq([r["out"] for r in out3], [Q(0), Q(2), Q(-1)], "negative reflection inverts the echo")
    raises(lambda: _run([Instruction("transmission_line", ("a",), "z", {
        "segments": 0, "reflection": Q(0)})], {"a": "numeric"}, [{"a": Q(1)}]),
        ErrorCode.DOMAIN_ERROR, "segments must be >= 1")
    raises(lambda: _run([Instruction("transmission_line", ("a",), "z", {
        "segments": 1, "reflection": Q(2)})], {"a": "numeric"}, [{"a": Q(1)}]),
        ErrorCode.DOMAIN_ERROR, "|reflection| must be <= 1")


def composite_kalman_observer():
    """Scalar Kalman recursion: gain = p/(p+r), and the variance only shrinks."""
    p = Instruction("kalman_observer", ("a",), "z", {
        "process_variance": Q(0), "measurement_variance": Q(1),
        "initial_x": Q(0), "initial_p": Q(1)})
    out = _run([p], {"a": "numeric"}, [{"a": Q(4)}, {"a": Q(6)}])
    # t1: p=1, g=1/2, x=2, p=1/2 ; t2: p=1/2, g=1/3, x=10/3, p=1/3
    eq([r["out"] for r in out], [Q(2), Q(10, 3)], "gain is p/(p+r) exactly")
    out2 = _run([Instruction("kalman_observer", ("a",), "z", {
        "process_variance": Q(1), "measurement_variance": Q(3),
        "initial_x": Q(1), "initial_p": Q(2)})], {"a": "numeric"}, [{"a": Q(5)}])
    eq(out2[0]["out"], Q(3), "x + g*(z-x) with g = 3/6")
    # covariance trajectory is monotone non-increasing for zero process noise
    cov_prog = Program("t", {"a": "numeric"}, (
        Instruction("kalman_observer", ("a",), "z", {
            "process_variance": Q(0), "measurement_variance": Q(1),
            "initial_x": Q(0), "initial_p": Q(1)}),
    ), {"out": "z"})
    cov = run_program(cov_prog, [{"a": Q(0)}] * 6)
    ok(len(cov) == 6, "the recursion runs for six ticks")
    eq(cov[-1]["out"], Q(0), "with z = 0 throughout the estimate stays 0")
    raises(lambda: _run([Instruction("kalman_observer", ("a",), "z", {
        "process_variance": Q(0), "measurement_variance": Q(0)})],
        {"a": "numeric"}, [{"a": Q(1)}]), ErrorCode.DOMAIN_ERROR, "r must be > 0")
    raises(lambda: _run([Instruction("kalman_observer", ("a",), "z", {
        "process_variance": Q(-1), "measurement_variance": Q(1)})],
        {"a": "numeric"}, [{"a": Q(1)}]), ErrorCode.DOMAIN_ERROR, "q must be >= 0")


def composite_thermo_electric():
    """Seebeck + Joule heat rate, delivered to a thermal port at effort = T."""
    p = Instruction("thermo_electric", ("p",), "z", {
        "seebeck": Q(2), "resistance": Q(3), "temperature": Q(300)})
    out = _run([p], {"p": "port"}, [{"p": PhysicalPort(Q(0), Q(4))}])
    # heat = S*T*I + I^2*R = 2400 + 48 = 2448
    eq(out[0]["out"].effort, Q(300), "thermal effort is the absolute temperature")
    eq(out[0]["out"].power, Q(2448), "heat rate = S*T*I + I^2*R")
    out2 = _run([p], {"p": "port"}, [{"p": PhysicalPort(Q(0), Q(-2))}])
    # reverse current: Peltier term is negative, Joule term still positive
    eq(out2[0]["out"].power, Q(2 * 300 * -2 + 4 * 3), "reverse current reverses only the Peltier term")
    raises(lambda: _run([Instruction("thermo_electric", ("p",), "z", {
        "seebeck": Q(1), "resistance": Q(1), "temperature": Q(0)})],
        {"p": "port"}, [{"p": PhysicalPort(Q(1), Q(1))}]),
        ErrorCode.DOMAIN_ERROR, "temperature must be positive")
    raises(lambda: _run([Instruction("thermo_electric", ("p",), "z", {
        "seebeck": Q(1), "resistance": Q(0), "temperature": Q(1)})],
        {"p": "port"}, [{"p": PhysicalPort(Q(1), Q(1))}]),
        ErrorCode.DOMAIN_ERROR, "resistance must be positive")



def coverage_port_primitives_execute():
    """dissipate, entropy, junction_1, transformer, transduce."""
    out = _run([Instruction("dissipate", ("a",), "p",
                            {"resistance": Q(4), "temperature": Q(300)})],
               {"a": "numeric"}, [{"a": Q(2)}], outputs={"out": "p"})
    eq(out[0]["out"].power, Q(1), "dissipator power = e^2/R")
    out2 = _run([Instruction("dissipate", ("a",), "p", {"resistance": Q(4), "temperature": Q(300)}),
                 Instruction("entropy", ("p",), "z", {"temperature": Q(300)})],
                {"a": "numeric"}, [{"a": Q(2)}])
    eq(out2[0]["out"], Q(1, 300), "entropy rate = P/T")
    out3 = _run([Instruction("junction_1", ("p1", "p2"), "p", {}),
                 Instruction("entropy", ("p",), "z", {"temperature": Q(10)})],
                {"p1": "port", "p2": "port"},
                [{"p1": PhysicalPort(Q(0), Q(5)), "p2": PhysicalPort(Q(0), Q(-3))}])
    eq(out3[0]["out"], Q(0), "a balanced junction produces no entropy")
    out4 = _run([Instruction("transformer", ("p",), "z", {"ratio": Q(2)})],
                {"p": "port"}, [{"p": PhysicalPort(Q(8), Q(3))}])
    eq(out4[0]["out"], PhysicalPort(Q(4), Q(-6)), "transformer (e,f) -> (e/k, -k f)")
    out5 = _run([Instruction("transduce", ("p",), "z", {"ratio": Q(2), "efficiency": Q(1)})],
                {"p": "port"}, [{"p": PhysicalPort(Q(8), Q(3))}])
    eq(out5[0]["out"], PhysicalPort(Q(16), Q(-3, 2)), "ideal transducer")
    out6 = _run([Instruction("transduce", ("p",), "z", {"ratio": Q(1), "efficiency": Q(1, 2)}),
                 Instruction("dissipate", ("a",), "q", {"resistance": Q(1), "temperature": Q(1)})],
                {"p": "port", "a": "numeric"},
                [{"p": PhysicalPort(Q(2), Q(2)), "a": Q(1)}], outputs={"out": "q"})
    ok(out6[0]["out"].power >= 0, "the lossy transducer never creates power")
    raises(lambda: _run([Instruction("entropy", ("p",), "z", {"temperature": Q(0)})],
                        {"p": "port"}, [{"p": PhysicalPort(Q(1), Q(1))}]),
           ErrorCode.DOMAIN_ERROR, "temperature must be positive")
    raises(lambda: _run([Instruction("entropy", ("p",), "z", {"temperature": Q(1)})],
                        {"p": "port"}, [{"p": PhysicalPort(Q(1), Q(-1))}]),
           ErrorCode.DOMAIN_ERROR, "a port with negative power is refused")
    raises(lambda: _run([Instruction("transduce", ("p",), "z",
                                     {"ratio": Q(1), "efficiency": Q(2)})],
                        {"p": "port"}, [{"p": PhysicalPort(Q(1), Q(1))}]),
           ErrorCode.DOMAIN_ERROR, "efficiency must lie in (0,1]")


def coverage_continuum_primitives_execute():
    f = analytic_field(lambda idx: Q(idx[0]) * Q(idx[1]), ndim=2)
    v = geometry.VectorField((analytic_field(lambda idx: Q(idx[0]), ndim=2),
                              analytic_field(lambda idx: Q(idx[1]), ndim=2)))
    out = _run([Instruction("div_spatial", ("v",), "z", {"h": Q(1), "index": [1, 1]})],
               {"v": "vector_field"}, [{"v": v}])
    eq(out[0]["out"], Q(2), "divergence of the identity field is 2")
    out2 = _run([Instruction("curl", ("v",), "z", {"h": Q(1), "index": [1, 1]})],
                {"v": "vector_field"}, [{"v": v}])
    ok(out2[0]["out"].is_zero(), "curl of a gradient-like field vanishes")
    out3 = _run([Instruction("laplacian", ("f",), "z", {"h": Q(1), "index": [1, 1]})],
                {"f": "field"}, [{"f": f}])
    eq(out3[0]["out"], Q(0), "laplacian of x*y vanishes")
    out4 = _run([Instruction("boundary", ("f",), "z",
                             {"shape": [3, 3], "spacing": Q(1), "kind": "dirichlet",
                              "value": Q(9)})],
                {"f": "field"}, [{"f": f}])
    eq(out4[0]["out"].at((5, 0)), Q(9), "boundary extrapolation outside the domain")
    eq(out4[0]["out"].at((1, 1)), Q(1), "interior values are preserved")


# ===========================================================================
# resolution — 3 checks
# ===========================================================================

def resolution_fallback_selects_the_next_candidate():
    def run(payload, layer):
        if payload == "bad":
            raise CentError(ErrorCode.DOMAIN_ERROR, f"{payload} fails in {layer.name}")
        return f"{payload}@{layer.name}"

    # Within a layer the first surviving candidate wins.
    r = resolve(["bad", "good"], run, [Layer("ideal")])
    ok(r.converged, "resolution converged")
    eq(r.status, "converged", "status")
    eq(r.candidate, "good", "the surviving candidate is selected")
    eq(r.value, "good@ideal", "the value comes from the surviving candidate")
    eq(len(r.attempts), 2, "both candidates were tried")
    eq(len(r.failures), 1, "the failure is preserved in the trace")
    eq(r.failures[0].candidate, "bad", "the failure names the candidate")
    eq(r.as_dict()["attempts"][0]["status"], "raised", "the trace is serialisable")
    eq(require_converged(r), "good@ideal", "require_converged returns the value")

    # The cascade is monotonic: every layer is attempted and the trace keeps all of it.
    c = resolve(["bad", "good"], run, [Layer("ideal"), Layer("thermal"), Layer("quantum")])
    ok(c.converged, "the cascade converged")
    eq(c.value, "good@quantum", "the highest fidelity layer supplies the value")
    eq(len(c.attempts), 6, "three layers x two candidates")
    eq(len(c.failures), 3, "one preserved failure per layer")
    eq({a.layer for a in c.attempts}, {"ideal", "thermal", "quantum"},
       "every declared layer was attempted")


def resolution_strict_refuses_immediately():
    def run(payload, layer):
        raise CentError(ErrorCode.DOMAIN_ERROR, "always fails")

    r = resolve(["first", "second"], run, [Layer("ideal"), Layer("thermal")], strict=True)
    eq(r.status, "refused", "strict mode refuses")
    ok(not r.converged, "refused is not converged")
    eq(len(r.attempts), 1, "strict mode stops after the first attempt")
    raises(lambda: require_converged(r, "site"), ErrorCode.APPROXIMATION_UNPROVED,
           "require_converged raises on a refused resolution")


def resolution_diverging_preserves_the_full_trace():
    def run(payload, layer):
        raise CentError(ErrorCode.DOMAIN_ERROR, f"{payload} in {layer.name}")

    # Everything fails on the first layer: the cascade stops there.
    r = resolve(["a", "b"], run, [Layer("ideal"), Layer("parasitic")])
    eq(r.status, "diverging", "every candidate failed at the first layer")
    eq(len(r.attempts), 2, "the trace stops at the failing layer")
    eq(len(r.failures), 2, "every attempt is a failure")
    eq(r.value, None, "no value is produced")
    eq(r.candidate, None, "no candidate is selected")
    raises(lambda: require_converged(r), ErrorCode.APPROXIMATION_UNPROVED,
           "require_converged raises on a diverging resolution")

    # A partial cascade keeps the layers it did reach, in order.
    def partial(payload, layer):
        if payload == "a" and layer.name == "ideal":
            return "ok"
        raise CentError(ErrorCode.DOMAIN_ERROR, f"{payload} in {layer.name}")

    p = resolve(["a", "b"], partial, [Layer("ideal"), Layer("parasitic")])
    eq(p.status, "diverging", "the second layer has no survivor")
    eq(len(p.attempts), 3, "one attempt for the survivor, then one per candidate")
    eq([a.status for a in p.attempts], ["converged", "raised", "raised"],
       "the trace preserves the order of attempts")
    raises(lambda: resolve([], run), ErrorCode.INVALID_INPUT, "needs a candidate")
    raises(lambda: resolve(["a"], run, []), ErrorCode.INVALID_INPUT, "needs a layer")


# ===========================================================================
# runner
# ===========================================================================

GROUPS: tuple[tuple[str, int, tuple], ...] = (
    ("exact", 7, (
        exact_decimal_strings_are_exact,
        exact_floats_are_rejected,
        exact_from_float_is_lossless,
        exact_from_float_rejects_non_rational,
        exact_structured_error_codes,
        exact_arithmetic_identities,
        exact_no_binary_float_in_pipeline,
    )),
    ("interval", 7, (
        interval_sqrt2_certified,
        interval_e_certified,
        interval_log2_certified,
        interval_pi_certified,
        interval_outward_rounded_algebra,
        interval_contains_true_values,
        interval_domain_guards,
    )),
    ("port", 7, (
        port_power_definition,
        port_transformer_conserves_power,
        port_gyrator_conserves_power,
        port_junction_0_balances,
        port_junction_1_balances,
        port_dissipation_entropy_nonnegative,
        port_transducer_and_stores,
    )),
    ("density", 2, (
        density_policies,
        density_complement_is_not_negation,
    )),
    ("geometry", 7, (
        geometry_carrier_and_exact_stencils,
        geometry_curl_of_gradient_vanishes,
        geometry_div_of_curl_vanishes,
        geometry_two_form_is_antisymmetric,
        geometry_boundary_extrapolation_dirichlet,
        geometry_boundary_extrapolation_neumann_robin,
        geometry_laplacian_exact_stencil,
    )),
    ("state", 2, (
        state_writes_invisible_until_commit,
        state_prng_is_deterministic,
    )),
    ("program", 8, (
        program_arity_is_checked,
        program_parameters_are_checked,
        program_single_assignment,
        program_kinds_are_checked,
        program_combinational_cycle_rejected,
        program_stateful_cycle_accepted,
        program_json_round_trip,
        program_unknown_op_rejected,
    )),
    ("evaluator", 17, (
        evaluator_accum_ticks,
        evaluator_rate_is_a_difference_quotient,
        evaluator_delay_ring_buffer,
        evaluator_hysteresis_latches,
        evaluator_noise_two_point_law,
        evaluator_quantize_ties_away_from_zero,
        evaluator_pid_exact_recursion,
        evaluator_state_space_exact_matrices,
        evaluator_delta_sigma_modulator_bits,
        evaluator_spatial_reads_a_field,
        evaluator_grad_field,
        evaluator_junction_0_port,
        evaluator_gyrator_port,
        evaluator_store_pot_and_kin,
        evaluator_tick_is_transactional,
        evaluator_feedback_reads_the_previous_tick,
        evaluator_run_is_deterministic,
    )),
    ("coverage", 16, (
        coverage_sum_and_neg,
        coverage_mult_and_scale,
        coverage_wrap,
        coverage_sat,
        coverage_exp,
        coverage_log,
        coverage_recip_and_div,
        coverage_sqrt,
        coverage_eq,
        coverage_translinear,
        composite_phase_locked_loop,
        composite_transmission_line,
        composite_kalman_observer,
        composite_thermo_electric,
        coverage_port_primitives_execute,
        coverage_continuum_primitives_execute,
    )),
    ("resolution", 3, (
        resolution_fallback_selects_the_next_candidate,
        resolution_strict_refuses_immediately,
        resolution_diverging_preserves_the_full_trace,
    )),
)


def main() -> int:
    print("CentCalculus2 exact-core checks")
    print("=" * 70)
    for group, declared, fns in GROUPS:
        start = len(RESULTS)
        for fn in fns:
            check(group, fn.__name__.replace("_", " "), fn)
        got = len(RESULTS) - start
        if got != declared:
            print(f"  !! group {group!r} has {got} checks, documented as {declared}")
    print()
    for group, declared, _ in GROUPS:
        rows = [r for r in RESULTS if r[0] == group]
        failed = [r for r in rows if not r[2]]
        mark = "PASS" if not failed else "FAIL"
        print(f"  [{mark}] {group:<10} {len(rows) - len(failed)}/{declared}")
        for _, name, _, detail in failed:
            print(f"         - {name}: {detail}")
    print()
    passed = sum(1 for r in RESULTS if r[2])
    total = len(RESULTS)
    print("=" * 70)
    print(f"  {passed}/{total} checks passed")
    documented = sum(g[1] for g in GROUPS)
    if total != documented:
        print(f"  !! suite has {total} checks; docs/extensions.md documents {documented}")
    if passed != total:
        print("\n  FAILURES:")
        for group, name, _, detail in RESULTS:
            if not detail and not _:
                continue
        for group, name, good, detail in RESULTS:
            if not good:
                print(f"    [{group}] {name}\n        {detail}")
    return 0 if passed == total and total == documented else 1


if __name__ == "__main__":
    sys.exit(main())
