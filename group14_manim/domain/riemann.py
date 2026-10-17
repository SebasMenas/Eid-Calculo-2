"""Sumas de Riemann exactas para tasas afines.

Ejemplo:
    ``riemann_sum(rate, 5, RiemannMethod.LEFT)`` devuelve ``Fraction(40)``.
"""

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction

from group14_manim.domain.rate_function import RateFunction


class RiemannMethod(Enum):
    """Regla de muestreo de una suma de Riemann.

    Ejemplo:
        ``RiemannMethod.MIDPOINT`` selecciona el punto medio de cada subintervalo.
    """

    LEFT = "left"
    RIGHT = "right"
    MIDPOINT = "center"


@dataclass(frozen=True)
class RiemannSums:
    """Resultados de las tres reglas para una partición dada.

    Parámetros:
        n: Cantidad de subintervalos.
        delta_t: Ancho exacto de cada subintervalo.
        left: Suma por extremo izquierdo.
        right: Suma por extremo derecho.
        midpoint: Suma por punto medio.

    Ejemplo:
        ``compute_riemann_sums(rate, 5).midpoint`` devuelve ``Fraction(45)``.
    """

    n: int
    delta_t: Fraction
    left: Fraction
    right: Fraction
    midpoint: Fraction


def riemann_sum(rate: RateFunction, n: int, method: RiemannMethod) -> Fraction:
    """Calcula una suma de Riemann exacta.

    Parámetros:
        rate: Tasa afín y dominio.
        n: Número positivo de subintervalos.
        method: Regla de muestreo.

    Retorno:
        Aproximación exacta de la cantidad acumulada.

    Ejemplo:
        Para ``n=5``, la suma izquierda de la tasa del video es ``40 MB``.
    """
    if n <= 0:
        raise ValueError("La cantidad de subintervalos debe ser positiva.")
    delta_t = rate.interval.duration / n
    total = Fraction(0)
    for index in range(n):
        left = rate.interval.start + index * delta_t
        if method is RiemannMethod.LEFT:
            sample = left
        elif method is RiemannMethod.RIGHT:
            sample = left + delta_t
        else:
            sample = left + delta_t / 2
        total += rate.value_at(sample) * delta_t
    return total


def compute_riemann_sums(rate: RateFunction, n: int) -> RiemannSums:
    """Calcula izquierda, derecha y punto medio para la misma partición.

    Parámetros:
        rate: Tasa a integrar.
        n: Número positivo de subintervalos.

    Retorno:
        Sumas exactas y tamaño de paso.

    Ejemplo:
        ``compute_riemann_sums(rate, 10).left`` devuelve ``Fraction(85, 2)``.
    """
    if n <= 0:
        raise ValueError("La cantidad de subintervalos debe ser positiva.")
    return RiemannSums(
        n=n,
        delta_t=rate.interval.duration / n,
        left=riemann_sum(rate, n, RiemannMethod.LEFT),
        right=riemann_sum(rate, n, RiemannMethod.RIGHT),
        midpoint=riemann_sum(rate, n, RiemannMethod.MIDPOINT),
    )
