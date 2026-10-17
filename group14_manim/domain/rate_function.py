"""Entidades inmutables para tasas afines y sus intervalos.

Ejemplo:
    ``rate = RateFunction(Fraction(2), Fraction(1, 2), interval, MB_PER_SECOND, SECOND)``
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from group14_manim.domain.units import Unit


@dataclass(frozen=True)
class TimeInterval:
    """Intervalo cerrado de integración con extremo final mayor al inicial.

    Parámetros:
        start: Inicio del intervalo.
        end: Fin del intervalo.

    Ejemplo:
        ``TimeInterval(Fraction(0), Fraction(10))`` modela diez segundos.
    """

    start: Fraction
    end: Fraction

    def __post_init__(self) -> None:
        """Rechaza intervalos vacíos o invertidos.

        Ejemplo:
            Un intervalo con ``end <= start`` produce ``ValueError``.
        """
        if self.end <= self.start:
            raise ValueError("El extremo final debe ser mayor que el inicial.")

    @property
    def duration(self) -> Fraction:
        """Devuelve la duración exacta del intervalo.

        Retorno:
            Diferencia ``end - start`` como fracción exacta.

        Ejemplo:
            La duración de ``[0, 10]`` es ``Fraction(10)``.
        """
        return self.end - self.start


@dataclass(frozen=True)
class RateFunction:
    """Tasa afín ``intercept + slope*t`` con magnitudes y unidades.

    Parámetros:
        intercept: Valor de la tasa en ``t=0``.
        slope: Cambio de tasa por unidad de tiempo.
        interval: Dominio de integración.
        rate_unit: Unidad de la tasa.
        variable_unit: Unidad de la variable independiente.

    Ejemplo:
        ``rate.value_at(Fraction(10))`` devuelve ``Fraction(7)`` para la tasa del video.
    """

    intercept: Fraction
    slope: Fraction
    interval: TimeInterval
    rate_unit: Unit
    variable_unit: Unit

    def value_at(self, time: Fraction) -> Fraction:
        """Evalúa la tasa en un instante.

        Parámetros:
            time: Instante dentro del intervalo.

        Retorno:
            Tasa exacta en ese instante.

        Ejemplo:
            La tasa ``2 + t/2`` vale ``Fraction(4)`` en ``t=4``.
        """
        if not self.interval.start <= time <= self.interval.end:
            raise ValueError("El instante debe pertenecer al intervalo de la tasa.")
        return self.intercept + self.slope * time

    @property
    def accumulated_unit(self) -> Unit:
        """Devuelve la unidad de la cantidad acumulada.

        Retorno:
            Producto entre unidad de tasa y unidad de tiempo.

        Ejemplo:
            ``MB/s`` por ``s`` se simplifica a ``MB``.
        """
        return self.rate_unit * self.variable_unit
