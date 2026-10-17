"""Adaptador de datos de dominio a una función gráfica sin dependencias Manim.

Ejemplo:
    ``compute_rate_plot(PROBLEM.rate).value_at(5.0)`` devuelve ``4.5`` para dibujar.
"""

from dataclasses import dataclass

from group14_manim.domain.rate_function import RateFunction


@dataclass(frozen=True)
class RatePlot:
    """Curva afín lista para que un adaptador gráfico la dibuje.

    Ejemplo:
        ``plot.value_at(5.0)`` entrega la coordenada vertical para Manim.
    """

    intercept: float
    slope: float
    start_time: float
    end_time: float
    start_value: float
    end_value: float

    def value_at(self, time: float) -> float:
        """Evalúa la curva en coordenadas de pantalla.

        Parámetros:
            time: Coordenada horizontal en segundos.

        Retorno:
            Coordenada vertical de la tasa.

        Ejemplo:
            ``plot.value_at(5.0)`` entrega la tasa central de la escena.
        """
        return self.intercept + self.slope * time


def compute_rate_plot(rate: RateFunction) -> RatePlot:
    """Prepara coeficientes de una tasa para el protocolo de graficación.

    Parámetros:
        rate: Tasa afín del dominio.

    Retorno:
        Curva callable sin importar Manim.

    Ejemplo:
        ``compute_rate_plot(PROBLEM.rate)`` genera la recta principal.
    """
    return RatePlot(
        float(rate.intercept),
        float(rate.slope),
        float(rate.interval.start),
        float(rate.interval.end),
        float(rate.value_at(rate.interval.start)),
        float(rate.value_at(rate.interval.end)),
    )
