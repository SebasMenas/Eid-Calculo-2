"""Caso de uso del cambio neto para una tasa constante.

Ejemplo:
    ``compute_constant_rate_change(rate)`` integra una tasa de pendiente nula.
"""

from fractions import Fraction

from group14_manim.domain.rate_function import RateFunction


def compute_constant_rate_change(rate: RateFunction) -> Fraction:
    """Calcula el cambio neto de un modelo de tasa constante.

    Parámetros:
        rate: Modelo cuya pendiente debe ser cero.

    Retorno:
        Integral exacta del modelo constante.

    Ejemplo:
        La tasa de ``4 MB/s`` durante diez segundos acumula ``40 MB``.
    """
    if rate.slope != 0:
        raise ValueError("El modelo debe tener tasa constante.")
    return rate.intercept * rate.interval.duration
