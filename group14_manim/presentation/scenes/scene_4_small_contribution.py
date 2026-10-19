"""Escena que identifica el aporte ``r(t*) Δt`` en un solo subintervalo.

Ejemplo:
    ``manim -pql group14_manim/presentation/scenes/scene_4_small_contribution.py Scene4SmallContribution``
"""

from manim import (
    Brace,
    Create,
    DashedLine,
    DOWN,
    FadeIn,
    MathTex,
    Rectangle,
    Scene,
    Text,
    UP,
    UR,
    Write,
)

from group14_manim.application.compute_sample_contribution import compute_sample_contribution
from group14_manim.application.compute_rate_plot import compute_rate_plot
from group14_manim.config.problem import PROBLEM
from group14_manim.presentation.components.chart import (
    build_rate_axes,
    build_rate_graph,
    format_value,
    unit_expression,
)
from group14_manim.presentation.theme import BODY_SIZE, RATE_BLUE, RECTANGLE_YELLOW, RESULT_GREEN, TITLE_SIZE


class Scene4SmallContribution(Scene):
    """1:30–2:20; amplía una contribución local de la suma.

    Se ve el intervalo elegido, la altura de su punto medio y el producto con
    el ancho. Explica por qué el rectángulo corresponde a megabytes aportados.

    Ejemplo:
        ``manim -pql scene_4_small_contribution.py Scene4SmallContribution``.
    """

    def construct(self) -> None:
        """Dibuja una muestra, su ancho temporal y sus unidades.

        Retorno:
            Ninguno; agrega los elementos de Manim.

        Ejemplo:
            Manim llama este método al render de la escena.
        """
        rate = PROBLEM.rate
        sample_interval = PROBLEM.sample_interval
        contribution = compute_sample_contribution(rate, sample_interval)
        axes = build_rate_axes(
            rate,
            float(PROBLEM.positive_axis_min),
            float(PROBLEM.positive_axis_max),
        ).scale(0.7).shift(UP * 0.25)
        graph = build_rate_graph(axes, compute_rate_plot(rate), rate)
        start = float(sample_interval.start)
        end = float(sample_interval.end)
        sample = float(contribution.sample_time)
        sample_rate = float(contribution.sample_rate)
        rectangle_start = axes.c2p(start, 0)
        rectangle_end = axes.c2p(end, sample_rate)
        rectangle = Rectangle(
            width=rectangle_end[0] - rectangle_start[0],
            height=rectangle_end[1] - rectangle_start[1],
            stroke_color=RECTANGLE_YELLOW,
            fill_color=RECTANGLE_YELLOW,
            fill_opacity=0.6,
        ).move_to(axes.c2p(sample, sample_rate / 2))
        title = Text("Un pequeño aporte", font_size=TITLE_SIZE).to_edge(UP)
        sample_line = DashedLine(
            axes.c2p(sample, 0),
            axes.c2p(sample, sample_rate),
            color=RECTANGLE_YELLOW,
        )
        horizontal_line = DashedLine(
            axes.c2p(0, sample_rate),
            axes.c2p(sample, sample_rate),
            color=RATE_BLUE,
        )
        interval_line = DashedLine(axes.c2p(start, 0), axes.c2p(end, 0), color=RECTANGLE_YELLOW)
        brace = Brace(interval_line, DOWN, color=RECTANGLE_YELLOW)
        brace_label = brace.get_tex(r"\Delta t")
        amount_formula = MathTex(
            rf"r({format_value(contribution.sample_time)})\,\Delta t"
            rf"={format_value(contribution.sample_rate)}\cdot{format_value(contribution.delta_t)}"
            rf"={format_value(contribution.value)}\,\mathrm{{{contribution.accumulated_unit}}}",
            color=RESULT_GREEN,
        ).scale(0.85).to_corner(UR).shift(DOWN * 0.95)
        units = MathTex(
            rf"\left({unit_expression(contribution.rate_unit)}\right)"
            rf"\left({unit_expression(contribution.time_unit)}\right)"
            rf"=\mathrm{{{contribution.accumulated_unit}}}"
        ).scale(0.82).to_edge(DOWN)
        message = Text(
            f"El rectángulo aporta {contribution.accumulated_unit}.",
            font_size=22,
            color=RESULT_GREEN,
        ).move_to([3.9, 0, 0])
        self.play(Write(title), Create(axes), Create(graph))
        self.play(FadeIn(rectangle), Create(sample_line), Create(horizontal_line))
        self.play(Create(interval_line), Create(brace), FadeIn(brace_label))
        self.play(Write(amount_formula), Write(units), FadeIn(message))
        self.wait(2)
