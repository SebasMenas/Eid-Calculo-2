"""Constructores visuales para ejes, curvas y formato numérico.

Ejemplo:
    ``axes = build_rate_axes(PROBLEM.rate, y_min=0, y_max=8)``
"""

from fractions import Fraction

from manim import Axes, MathTex, ParametricFunction

from group14_manim.application.compute_rate_plot import RatePlot
from group14_manim.domain.rate_function import RateFunction
from group14_manim.domain.units import Unit
from group14_manim.presentation.theme import RATE_BLUE


def format_value(value: Fraction | float) -> str:
    """Formatea una magnitud para rótulos y fórmulas.

    Parámetros:
        value: Resultado numérico exacto o coordenada gráfica.

    Retorno:
        Cadena decimal compacta sin ceros innecesarios.

    Ejemplo:
        ``format_value(Fraction(45))`` devuelve ``"45"``.
    """
    return f"{float(value):g}"


def build_rate_axes(rate: RateFunction, y_min: float, y_max: float) -> Axes:
    """Crea ejes rotulados desde las unidades y el intervalo del dominio.

    Parámetros:
        rate: Tasa cuyas unidades y extremos definen los ejes.
        y_min: Mínimo vertical visual.
        y_max: Máximo vertical visual.

    Retorno:
        Ejes Manim listos para una escena.

    Ejemplo:
        ``build_rate_axes(rate, 0, 8)`` dibuja la escala de la tasa de descarga.
    """
    start = float(rate.interval.start)
    end = float(rate.interval.end)
    axes = Axes(
        x_range=[start, end, (end - start) / 5],
        y_range=[y_min, y_max, (y_max - y_min) / 4],
        x_length=9,
        y_length=4.5,
        axis_config={"include_numbers": True, "font_size": 18},
        tips=True,
    ).add_coordinates()
    axis_labels = axes.get_axis_labels(
        x_label=MathTex(rf"t\,({unit_expression(rate.variable_unit)})"),
        y_label=MathTex(rf"r\,({unit_expression(rate.rate_unit)})"),
    )
    axes.add(axis_labels)
    return axes


def build_rate_graph(
    axes: Axes,
    plot: RatePlot,
    rate: RateFunction,
    color: str = RATE_BLUE,
) -> ParametricFunction:
    """Dibuja la función gráfica preparada por la capa de aplicación.

    Parámetros:
        axes: Ejes donde se representa la curva.
        plot: Callable de coordenadas creado por el caso de uso.
        rate: Tasa que determina el dominio visible.
        color: Color Manim de la curva.

    Retorno:
        Curva parametrizada compatible con los rectángulos de Riemann.

    Ejemplo:
        ``build_rate_graph(axes, compute_rate_plot(rate), rate)`` dibuja ``r(t)``.
    """
    return axes.plot(
        plot.value_at,
        x_range=[float(rate.interval.start), float(rate.interval.end)],
        color=color,
        stroke_width=4,
    )


def rate_label(rate: RateFunction, name: str = "r") -> MathTex:
    """Construye la fórmula de una tasa afín usando sus coeficientes.

    Parámetros:
        rate: Tasa a describir.
        name: Nombre simbólico de la función.

    Retorno:
        Fórmula MathTex con intercepto y pendiente configurados.

    Ejemplo:
        ``rate_label(PROBLEM.rate)`` genera la fórmula del caso principal.
    """
    intercept = format_value(rate.intercept)
    slope = format_value(abs(rate.slope))
    sign = "+" if rate.slope >= 0 else "-"
    variable = "t"
    return MathTex(
        rf"{name}(t)={intercept}{sign}{slope}{variable}",
        color=RATE_BLUE,
    )


def unit_expression(unit: Unit) -> str:
    """Convierte las dimensiones del dominio en una expresión MathTex.

    Parámetros:
        unit: Unidad del álgebra dimensional.

    Retorno:
        Cadena LaTeX con unidades en numerador y denominador.

    Ejemplo:
        ``unit_expression(MEGABYTE_PER_SECOND)`` produce una fracción MB/s.
    """
    if str(unit) == "J":
        return r"\mathrm{J}"
    numerator = [f"\\mathrm{{{symbol}}}" if power == 1 else f"\\mathrm{{{symbol}}}^{{{power}}}"
                 for symbol, power in unit.dimensions if power > 0]
    denominator = [f"\\mathrm{{{symbol}}}" if power == -1 else f"\\mathrm{{{symbol}}}^{{{-power}}}"
                   for symbol, power in unit.dimensions if power < 0]
    top = r"\cdot".join(numerator) or "1"
    bottom = r"\cdot".join(denominator)
    return rf"\frac{{{top}}}{{{bottom}}}" if denominator else top
