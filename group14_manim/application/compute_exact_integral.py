"""Caso de uso que prepara la antiderivada evaluada en los extremos.

Ejemplo:
    ``compute_exact_integral(PROBLEM.rate).value`` devuelve ``Fraction(45)``.
"""

from dataclasses import dataclass
from fractions import Fraction

from group14_manim.domain.integral import antiderivative_at, integral_exact
from group14_manim.domain.rate_function import RateFunction
from group14_manim.domain.units import Unit


@dataclass(frozen=True)
class IntegralEvaluation:
    """Datos exactos para presentar los pasos de una integral definida.

    Ejemplo:
        ``evaluation.value`` entrega el cambio acumulado entre los extremos.
    """

    intercept: Fraction
    slope: Fraction
    primitive_quadratic_coefficient: Fraction
    start: Fraction
    end: Fraction
    primitive_at_start: Fraction
    primitive_at_end: Fraction
    value: Fraction
    unit: Unit


def compute_exact_integral(rate: RateFunction) -> IntegralEvaluation:
    """Evalúa la antiderivada de la tasa en los extremos del intervalo.

    Parámetros:
        rate: Función afín que se desea integrar.

    Retorno:
        Coeficientes, extremos, evaluaciones y resultado con unidad.

    Ejemplo:
        ``compute_exact_integral(rate).primitive_at_end`` devuelve ``45``.
    """
    return IntegralEvaluation(
        intercept=rate.intercept,
        slope=rate.slope,
        primitive_quadratic_coefficient=rate.slope / 2,
        start=rate.interval.start,
        end=rate.interval.end,
        primitive_at_start=antiderivative_at(rate, rate.interval.start),
        primitive_at_end=antiderivative_at(rate, rate.interval.end),
        value=integral_exact(rate),
        unit=rate.accumulated_unit,
    )
