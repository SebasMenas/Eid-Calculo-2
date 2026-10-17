"""Caso de uso para el total descargado y el espacio restante.

Ejemplo:
    ``compute_download_summary(rate, negative_rate, capacity).remaining`` devuelve ``55 MB``.
"""

from dataclasses import dataclass
from fractions import Fraction

from group14_manim.application.compute_net_change import compute_net_change
from group14_manim.domain.rate_function import RateFunction


@dataclass(frozen=True)
class DownloadSummary:
    """Resumen de la descarga en unidades acumuladas.

    Ejemplo:
        ``summary.completion_fraction`` vale ``Fraction(45, 100)``.
    """

    capacity: Fraction
    downloaded: Fraction
    remaining: Fraction
    completion_fraction: Fraction
    completion_percentage: Fraction


def compute_download_summary(
    rate: RateFunction,
    negative_rate: RateFunction,
    capacity: Fraction,
) -> DownloadSummary:
    """Calcula bytes recibidos, porcentaje completado y tamaño restante.

    Parámetros:
        rate: Tasa positiva que describe la descarga.
        negative_rate: Tasa opuesta que describe el espacio restante.
        capacity: Capacidad inicial del archivo.

    Retorno:
        Resumen exacto derivado de las tasas configuradas.

    Ejemplo:
        Con un archivo de ``100 MB`` y la tasa principal, faltan ``55 MB``.
    """
    if capacity <= 0:
        raise ValueError("La capacidad del archivo debe ser positiva.")
    downloaded = compute_net_change(rate, Fraction(0)).change
    remaining = compute_net_change(negative_rate, capacity).final_value
    completion_fraction = downloaded / capacity
    return DownloadSummary(
        capacity,
        downloaded,
        remaining,
        completion_fraction,
        completion_fraction * 100,
    )
