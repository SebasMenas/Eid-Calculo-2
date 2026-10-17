"""Fixtures compartidas para comprobar el problema configurado.

Ejemplo:
    La fixture ``problem`` entrega la configuración inmutable central.
"""

import pytest

from group14_manim.config.problem import PROBLEM, ProblemConfig


@pytest.fixture
def problem() -> ProblemConfig:
    """Entrega los parámetros compartidos del caso de descarga.

    Retorno:
        Configuración de tasa, intervalo y unidades.

    Ejemplo:
        ``def test_rate(problem): ...`` recibe ``PROBLEM``.
    """
    return PROBLEM
