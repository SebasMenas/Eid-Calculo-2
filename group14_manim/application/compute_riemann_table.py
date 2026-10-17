"""Caso de uso para preparar la tabla de aproximaciones del video.

Ejemplo:
    ``compute_riemann_table(PROBLEM.rate, PROBLEM.partitions)`` devuelve tres filas.
"""

from dataclasses import dataclass

from group14_manim.domain.rate_function import RateFunction
from group14_manim.domain.riemann import RiemannSums, compute_riemann_sums


@dataclass(frozen=True)
class RiemannTable:
    """Tabla inmutable de resultados para varios tamaños de partición.

    Ejemplo:
        ``table.rows[0].left`` entrega la primera suma izquierda.
    """

    rows: tuple[RiemannSums, ...]


def compute_riemann_table(rate: RateFunction, partitions: tuple[int, ...]) -> RiemannTable:
    """Construye resultados de Riemann para cada cantidad de subintervalos.

    Parámetros:
        rate: Tasa afín del caso de uso.
        partitions: Cantidades de subintervalos que se desean comparar.

    Retorno:
        Tabla con resultados exactos e inmutables.

    Ejemplo:
        ``compute_riemann_table(rate, (5, 10)).rows`` contiene dos filas.
    """
    if not partitions:
        raise ValueError("La tabla requiere al menos una partición.")
    return RiemannTable(tuple(compute_riemann_sums(rate, n) for n in partitions))
