"""Caso de uso para comunicar cambio neto y cantidad final.

Ejemplo:
    ``compute_net_change(rate, Fraction(0)).final_value`` devuelve ``45``.
"""

from dataclasses import dataclass
from fractions import Fraction

from group14_manim.domain.rate_function import RateFunction
from group14_manim.domain.integral import integral_exact
from group14_manim.domain.units import Unit


@dataclass(frozen=True)
class NetChange:
    """Cambio neto, estado inicial y estado final con unidad acumulada.

    Ejemplo:
        ``result.change`` es ``-45`` para una tasa negativa simétrica.
    """

    initial_value: Fraction
    change: Fraction
    final_value: Fraction
    unit: Unit


def compute_net_change(rate: RateFunction, initial_value: Fraction) -> NetChange:
    """Integra una tasa y suma el cambio neto al estado inicial.

    Parámetros:
        rate: Tasa que describe el cambio del estado.
        initial_value: Valor inicial en la unidad acumulada.

    Retorno:
        Estado inicial, cambio neto y estado final.

    Ejemplo:
        Un archivo inicialmente de ``100 MB`` termina con ``45 MB`` restantes
        si la tasa modela el espacio libre perdido al descargar.
    """
    change = integral_exact(rate)
    return NetChange(initial_value, change, initial_value + change, rate.accumulated_unit)
