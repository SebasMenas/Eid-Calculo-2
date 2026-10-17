"""Integración exacta de tasas afines mediante su antiderivada.

Ejemplo:
    ``integral_exact(rate)`` devuelve ``Fraction(45)`` para los datos del video.
"""

from fractions import Fraction

from group14_manim.domain.rate_function import RateFunction


def antiderivative_at(rate: RateFunction, time: Fraction) -> Fraction:
    """Evalúa la antiderivada ``a*t + b*t²/2`` en un instante.

    Parámetros:
        rate: Tasa afín ``a + b*t``.
        time: Instante donde evaluar.

    Retorno:
        Valor exacto de la antiderivada, con referencia fijada en cero.

    Ejemplo:
        Para la tasa del video, ``antiderivative_at(rate, 10)`` vale ``45``.
    """
    return rate.intercept * time + rate.slope * time**2 / 2


def integral_exact(rate: RateFunction) -> Fraction:
    """Integra exactamente una tasa afín sobre su intervalo.

    Parámetros:
        rate: Tasa y extremos de integración.

    Retorno:
        Cambio neto exacto entre los extremos.

    Ejemplo:
        ``integral_exact(rate)`` vale ``45 MB`` en el problema principal.
    """
    return antiderivative_at(rate, rate.interval.end) - antiderivative_at(rate, rate.interval.start)
