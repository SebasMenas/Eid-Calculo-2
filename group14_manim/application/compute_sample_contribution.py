"""Caso de uso para un aporte local de la suma de Riemann.

Ejemplo:
    ``compute_sample_contribution(rate, interval).value`` vale ``9 MB``.
"""

from dataclasses import dataclass
from fractions import Fraction

from group14_manim.domain.rate_function import RateFunction, TimeInterval
from group14_manim.domain.units import Unit


@dataclass(frozen=True)
class SampleContribution:
    """Aporte de una muestra y ancho de subintervalo con sus unidades.

    Ejemplo:
        El intervalo ``[4, 6]`` tiene aporte ``9 MB`` en su punto medio.
    """

    interval: TimeInterval
    sample_time: Fraction
    sample_rate: Fraction
    delta_t: Fraction
    value: Fraction
    rate_unit: Unit
    time_unit: Unit
    accumulated_unit: Unit


def compute_sample_contribution(
    rate: RateFunction,
    interval: TimeInterval,
    sample_time: Fraction | None = None,
) -> SampleContribution:
    """Calcula la contribución ``r(t*) Δt`` en una submuestra.

    Parámetros:
        rate: Tasa que describe el fenómeno.
        interval: Subintervalo donde se acumula.
        sample_time: Instante de evaluación; si se omite, usa el punto medio.

    Retorno:
        Tasa, ancho, producto y unidades asociadas.

    Ejemplo:
        Para ``[4, 6]`` y ``t*=5``, devuelve ``4.5 × 2 = 9 MB``.
    """
    if sample_time is None:
        sample_time = (interval.start + interval.end) / 2
    if interval.start < rate.interval.start or interval.end > rate.interval.end:
        raise ValueError("El subintervalo debe pertenecer al intervalo de la tasa.")
    if not interval.start <= sample_time <= interval.end:
        raise ValueError("La muestra debe pertenecer al subintervalo.")
    sample_rate = rate.value_at(sample_time)
    delta_t = interval.duration
    return SampleContribution(
        interval,
        sample_time,
        sample_rate,
        delta_t,
        sample_rate * delta_t,
        rate.rate_unit,
        rate.variable_unit,
        rate.accumulated_unit,
    )
