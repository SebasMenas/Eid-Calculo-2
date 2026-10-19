"""Escena donde la tasa horizontal se transforma en una tasa creciente.

Ejemplo:
    ``manim -pql group14_manim/presentation/scenes/scene_3_variable_rate.py Scene3VariableRate``
"""

from manim import (
    Create,
    DOWN,
    Dot,
    FadeIn,
    MathTex,
    Scene,
    Text,
    Transform,
    UP,
    Write,
)

from group14_manim.application.compute_rate_plot import compute_rate_plot
from group14_manim.config.problem import PROBLEM
from group14_manim.presentation.components.chart import build_rate_axes, build_rate_graph, format_value, rate_label
from group14_manim.presentation.theme import RATE_BLUE, TITLE_SIZE


class Scene3VariableRate(Scene):
    """1:00–1:30; transforma la tasa constante en ``r(t)`` creciente.

    Se ven los extremos de la tasa y su expresión en una gráfica.
    Explica que ahora las alturas de los rectángulos cambian con el tiempo.

    Ejemplo:
        ``manim -pql scene_3_variable_rate.py Scene3VariableRate``.
    """

    def construct(self) -> None:
        """Anima la transformación de las dos curvas.

        Retorno:
            Ninguno; agrega objetos a la escena.

        Ejemplo:
            Manim llama el método durante el render de esta escena.
        """
        rate = PROBLEM.rate
        start = rate.interval.start
        end = rate.interval.end
        axes = build_rate_axes(
            rate,
            float(PROBLEM.positive_axis_min),
            float(PROBLEM.positive_axis_max),
        )
        constant = PROBLEM.constant_rate_model
        old_graph = build_rate_graph(axes, compute_rate_plot(constant), constant)
        graph = build_rate_graph(axes, compute_rate_plot(rate), rate)
        title = Text("Ahora la tasa cambia con el tiempo", font_size=TITLE_SIZE).to_edge(UP)
        formula = rate_label(rate).next_to(title, DOWN, buff=0.25)
        rate_plot = compute_rate_plot(rate)
        initial = Dot(axes.c2p(rate_plot.start_time, rate_plot.start_value), color=RATE_BLUE)
        final = Dot(axes.c2p(rate_plot.end_time, rate_plot.end_value), color=RATE_BLUE)
        labels = (
            MathTex(
                rf"({format_value(start)},{format_value(rate_plot.start_value)})",
                color=RATE_BLUE,
            ).next_to(initial, UP),
            MathTex(
                rf"({format_value(end)},{format_value(rate_plot.end_value)})",
                color=RATE_BLUE,
            ).next_to(final, UP),
        )
        self.play(Write(title), Create(axes), Create(old_graph))
        self.play(Transform(old_graph, graph), FadeIn(formula), FadeIn(initial), FadeIn(final))
        self.play(FadeIn(labels[0]), FadeIn(labels[1]))
        self.wait(2)
