"""Pruebas de matemática pura, unidades y sumas de Riemann.

Ejemplo:
    ``python -m pytest group14_manim/tests/test_domain.py``
"""

from fractions import Fraction

import pytest

from group14_manim.config.problem import ProblemConfig
from group14_manim.domain.integral import integral_exact
from group14_manim.domain.rate_function import RateFunction, TimeInterval
from group14_manim.domain.riemann import RiemannMethod, compute_riemann_sums, riemann_sum


def test_integral_exact_and_rate_endpoints(problem: ProblemConfig) -> None:
    """Comprueba tasa inicial/final e integral exacta en MB.

    Ejemplo:
        El resultado exacto de la tasa del guion es ``45``.
    """
    assert problem.rate.value_at(Fraction(0)) == Fraction(2)
    assert problem.rate.value_at(Fraction(10)) == Fraction(7)
    assert integral_exact(problem.rate) == Fraction(45)


@pytest.mark.parametrize(
    ("n", "left", "right", "midpoint"),
    (
        (5, Fraction(40), Fraction(50), Fraction(45)),
        (10, Fraction(85, 2), Fraction(95, 2), Fraction(45)),
        (100, Fraction(179, 4), Fraction(181, 4), Fraction(45)),
    ),
)
def test_expected_riemann_sums(
    problem: ProblemConfig,
    n: int,
    left: Fraction,
    right: Fraction,
    midpoint: Fraction,
) -> None:
    """Compara las tres reglas con los valores exactos de validación.

    Ejemplo:
        ``n=5`` produce sumas ``40``, ``50`` y ``45``.
    """
    sums = compute_riemann_sums(problem.rate, n)
    assert (sums.left, sums.right, sums.midpoint) == (left, right, midpoint)


def test_left_and_right_errors_decrease_as_partition_grows(problem: ProblemConfig) -> None:
    """Verifica que las cotas laterales convergen a la integral.

    Ejemplo:
        El error de cada extremo es menor con ``n=100`` que con ``n=5``.
    """
    exact = integral_exact(problem.rate)
    coarse = compute_riemann_sums(problem.rate, 5)
    fine = compute_riemann_sums(problem.rate, 100)
    assert coarse.left < exact < coarse.right
    assert abs(exact - fine.left) < abs(exact - coarse.left)
    assert abs(fine.right - exact) < abs(coarse.right - exact)


@pytest.mark.parametrize("n", (1, 2, 5, 10, 100))
def test_midpoint_is_exact_for_affine_rate(problem: ProblemConfig, n: int) -> None:
    """Comprueba la exactitud del punto medio para una función lineal.

    Ejemplo:
        Con cualquier partición uniforme, la suma central vale ``45``.
    """
    assert riemann_sum(problem.rate, n, RiemannMethod.MIDPOINT) == integral_exact(problem.rate)


def test_constant_and_negative_integrals(problem: ProblemConfig) -> None:
    """Comprueba acumulación positiva constante y acumulación firmada negativa.

    Ejemplo:
        ``4 MB/s`` durante el intervalo acumula ``40 MB``.
    """
    assert integral_exact(problem.constant_rate_model) == Fraction(40)
    assert integral_exact(problem.negative_rate) == Fraction(-45)


def test_invalid_interval_and_partition_are_rejected(problem: ProblemConfig) -> None:
    """Rechaza dominios degenerados y particiones no positivas.

    Ejemplo:
        Una suma con ``n=0`` produce ``ValueError`` explícito.
    """
    with pytest.raises(ValueError):
        TimeInterval(Fraction(2), Fraction(2))
    with pytest.raises(ValueError):
        riemann_sum(problem.rate, 0, RiemannMethod.LEFT)


def test_rate_rejects_times_outside_its_interval(problem: ProblemConfig) -> None:
    """Rechaza la evaluación de una tasa fuera del dominio configurado.

    Ejemplo:
        ``t=-1`` no pertenece al intervalo de descarga.
    """
    with pytest.raises(ValueError):
        problem.rate.value_at(Fraction(-1))


def test_affine_rate_requires_exact_fraction_inputs(problem: ProblemConfig) -> None:
    """Construye una entidad afín inmutable con unidades de dominio.

    Ejemplo:
        Una tasa constante modelada con pendiente cero conserva su intervalo.
    """
    rate = RateFunction(
        Fraction(3),
        Fraction(0),
        problem.rate.interval,
        problem.rate.rate_unit,
        problem.rate.variable_unit,
    )
    assert integral_exact(rate) == Fraction(30)
