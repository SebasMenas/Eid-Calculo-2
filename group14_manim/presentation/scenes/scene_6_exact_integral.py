"""Escena del valor exacto, porcentaje descargado y cantidad restante.

Ejemplo:
    ``manim -pql group14_manim/presentation/scenes/scene_6_exact_integral.py Scene6ExactIntegral``
"""

from manim import (
    DOWN,
    DL,
    DR,
    Create,
    FadeIn,
    LEFT,
    MathTex,
    Rectangle,
    Scene,
    Text,
    TransformMatchingTex,
    UP,
    WHITE,
    Write,
)

from group14_manim.application.compute_download_summary import compute_download_summary
from group14_manim.application.compute_exact_integral import compute_exact_integral
from group14_manim.application.compute_rate_plot import compute_rate_plot
from group14_manim.config.problem import PROBLEM
from group14_manim.presentation.components.chart import build_rate_axes, build_rate_graph, format_value
from group14_manim.presentation.theme import BACKGROUND_BAR, BODY_SIZE, RESULT_GREEN, TITLE_SIZE


class Scene6ExactIntegral(Scene):
    """3:30–4:00; evalúa la antiderivada y conecta el resultado con el archivo.

    Se ve la integral definida desarrollada, el área neta positiva y el
    porcentaje del archivo recibido; explica el valor inicial más el cambio.

    Ejemplo:
        ``manim -pql scene_6_exact_integral.py Scene6ExactIntegral``.
    """

    def construct(self) -> None:
        """Transforma la integral en su resultado y muestra el estado final.

        Retorno:
            Ninguno; construye la explicación visual del total exacto.

        Ejemplo:
            Manim llama este método al render de la escena.
        """
        rate = PROBLEM.rate
        evaluation = compute_exact_integral(rate)
        summary = compute_download_summary(PROBLEM.rate, PROBLEM.negative_rate, PROBLEM.initial_file_size)
        intercept = format_value(evaluation.intercept)
        quadratic = format_value(evaluation.primitive_quadratic_coefficient)
        start = format_value(evaluation.start)
        end = format_value(evaluation.end)
        first = MathTex(
            rf"\int_{{{start}}}^{{{end}}}({intercept}+{format_value(evaluation.slope)}t)\,dt"
            rf"=\left[{intercept}t+{quadratic}t^2\right]_{{{start}}}^{{{end}}}"
        ).scale(0.82)
        second = MathTex(
            rf"={format_value(evaluation.primitive_at_end)}"
            rf"-({format_value(evaluation.primitive_at_start)})"
        ).scale(0.82)
        third = MathTex(
            rf"={format_value(evaluation.value)}\,\mathrm{{{evaluation.unit}}}",
            color=RESULT_GREEN,
        ).scale(0.95)
        title = Text("La integral da la acumulación exacta", font_size=TITLE_SIZE).to_edge(UP)
        first.next_to(title, DOWN, buff=0.5)
        second.next_to(first, DOWN, buff=0.25)
        third.next_to(second, DOWN, buff=0.25)
        self.play(Write(title), Write(first))
        self.play(TransformMatchingTex(first, second))
        self.play(TransformMatchingTex(second, third))

        axes = build_rate_axes(
            rate,
            float(PROBLEM.positive_axis_min),
            float(PROBLEM.positive_axis_max),
        ).scale(0.42)
        axes.to_corner(DL).shift(UP * 0.45)
        graph = build_rate_graph(axes, compute_rate_plot(rate), rate)
        area = axes.get_area(
            graph,
            x_range=(float(rate.interval.start), float(rate.interval.end)),
            color=RESULT_GREEN,
            opacity=0.65,
        )
        self.play(Create(axes), Create(graph), FadeIn(area))
        bar_width = 5.2
        bar_height = 0.55
        background = Rectangle(
            width=bar_width,
            height=bar_height,
            fill_color=BACKGROUND_BAR,
            fill_opacity=1,
        ).to_corner(DR).shift(UP * 1.35)
        received = Rectangle(
            width=bar_width * float(summary.completion_fraction),
            height=bar_height,
            fill_color=RESULT_GREEN,
            fill_opacity=1,
            stroke_width=0,
        ).align_to(background, LEFT)
        received.move_to([received.get_center()[0], background.get_center()[1], 0])
        bar_label = Text(
            f"{format_value(summary.downloaded)} / {format_value(summary.capacity)} MB",
            font_size=BODY_SIZE,
            color=RESULT_GREEN,
        ).next_to(background, UP)
        percentage_label = Text(
            f"{format_value(summary.completion_percentage)} %",
            font_size=BODY_SIZE,
            color=WHITE,
        ).move_to(received.get_center())
        remaining_label = Text(
            f"Faltan {format_value(summary.remaining)} MB",
            font_size=BODY_SIZE,
        ).next_to(background, DOWN)
        state_equation = MathTex(
            rf"Q({end})=Q({start})+{format_value(summary.downloaded)}\,\mathrm{{{evaluation.unit}}}"
        ).scale(0.72).next_to(remaining_label, DOWN)
        self.play(
            FadeIn(background),
            FadeIn(received),
            FadeIn(bar_label),
            FadeIn(percentage_label),
            FadeIn(remaining_label),
        )
        self.play(Write(state_equation))
        self.wait(0.3)
