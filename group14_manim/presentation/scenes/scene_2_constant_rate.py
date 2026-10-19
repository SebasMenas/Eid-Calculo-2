"""Escena de referencia geométrica para una tasa constante.

Ejemplo:
    ``manim -pql group14_manim/presentation/scenes/scene_2_constant_rate.py Scene2ConstantRate``
"""

from manim import (
    Brace,
    Create,
    DOWN,
    FadeIn,
    Line,
    MathTex,
    Rectangle,
    RIGHT,
    Scene,
    Text,
    UP,
    Write,
)

from group14_manim.application.compute_constant_rate_change import compute_constant_rate_change
from group14_manim.application.compute_rate_plot import compute_rate_plot
from group14_manim.config.problem import PROBLEM
from group14_manim.presentation.components.chart import (
    build_rate_axes,
    build_rate_graph,
    format_value,
    unit_expression,
)
from group14_manim.presentation.theme import RECTANGLE_YELLOW, RESULT_GREEN, TITLE_SIZE


class Scene2ConstantRate(Scene):
    """0:30–1:00; representa una tasa constante como rectángulo.

    Se ve el producto de tasa por duración y se simplifican visualmente los
    segundos. Explica la interpretación geométrica para una tasa constante.

    Ejemplo:
        ``manim -pql scene_2_constant_rate.py Scene2ConstantRate``.
    """

    def construct(self) -> None:
        """Dibuja el rectángulo de acumulación y las unidades.

        Retorno:
            Ninguno; agrega la animación de la escena.

        Ejemplo:
            Manim llama este método al renderizar ``Scene2ConstantRate``.
        """
        model = PROBLEM.constant_rate_model
        duration = model.interval.duration
        amount = compute_constant_rate_change(model)
        axes = build_rate_axes(
            model,
            float(PROBLEM.positive_axis_min),
            float(PROBLEM.positive_axis_max),
        ).scale(0.7).shift(UP * 0.25)
        graph = build_rate_graph(axes, compute_rate_plot(model), model)
        rectangle_start = axes.c2p(float(model.interval.start), 0)
        rectangle_end = axes.c2p(float(duration), float(model.intercept))
        rectangle = Rectangle(
            width=rectangle_end[0] - rectangle_start[0],
            height=rectangle_end[1] - rectangle_start[1],
            stroke_color=RECTANGLE_YELLOW,
            fill_color=RECTANGLE_YELLOW,
            fill_opacity=0.55,
        )
        rectangle.move_to(axes.c2p(float(duration) / 2, float(model.intercept) / 2))
        title = Text("Una tasa constante sí forma un rectángulo", font_size=TITLE_SIZE).to_edge(UP)
        self.play(Write(title), Create(axes), Create(graph))
        self.play(FadeIn(rectangle))

        horizontal = Line(axes.c2p(float(model.interval.start), 0), axes.c2p(float(model.interval.end), 0))
        horizontal_brace = Brace(horizontal, DOWN)
        horizontal_label = horizontal_brace.get_tex(f"{format_value(duration)}\\,\\mathrm{{{model.variable_unit}}}")
        vertical = Line(axes.c2p(float(duration), 0), axes.c2p(float(duration), float(model.intercept)))
        vertical_brace = Brace(vertical, RIGHT).shift(RIGHT * 0.5)
        vertical_label = vertical_brace.get_tex(
            f"{format_value(model.intercept)}\\,\\mathrm{{{model.rate_unit}}}"
        ).shift(UP * 0.25)
        self.play(Create(horizontal_brace), FadeIn(horizontal_label), Create(vertical_brace), FadeIn(vertical_label))

        equation = MathTex(
            format_value(model.intercept),
            unit_expression(model.rate_unit),
            r"\cdot",
            format_value(duration),
            unit_expression(model.variable_unit),
            "=",
            format_value(amount),
            unit_expression(model.accumulated_unit),
            color=RESULT_GREEN,
        ).scale(0.86).to_edge(DOWN)
        self.play(Write(equation))
        # La línea sobre la s final representa la cancelación de unidades.
        second = equation[4]
        cancellation = Line(second.get_left(), second.get_right(), color=RESULT_GREEN, stroke_width=4)
        self.play(Create(cancellation))
        self.wait(2)
