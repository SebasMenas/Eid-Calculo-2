"""Escena de signo negativo y síntesis del significado de la integral.

Ejemplo:
    ``manim -pql group14_manim/presentation/scenes/scene_8_sign_and_closing.py Scene8SignAndClosing``
"""

from manim import (
    Create,
    DOWN,
    FadeIn,
    FadeOut,
    LEFT,
    MathTex,
    RIGHT,
    Scene,
    Text,
    Transform,
    UP,
    VGroup,
    Write,
)

from group14_manim.application.compute_exact_integral import compute_exact_integral
from group14_manim.application.compute_rate_plot import compute_rate_plot
from group14_manim.application.compute_riemann_table import compute_riemann_table
from group14_manim.config.problem import PROBLEM
from group14_manim.presentation.components.chart import build_rate_axes, build_rate_graph, format_value
from group14_manim.presentation.theme import NEGATIVE_RED, RATE_BLUE, RESULT_GREEN, TITLE_SIZE


class Scene8SignAndClosing(Scene):
    """4:45–5:15; interpreta una acumulación negativa y resume la idea.

    Se ve la gráfica reflejada debajo del eje y una región roja firmada.
    Explica que una integral puede representar espacio libre perdido y cierra
    con aportes, límite y magnitudes con unidades.

    Ejemplo:
        ``manim -pql scene_8_sign_and_closing.py Scene8SignAndClosing``.
    """

    def construct(self) -> None:
        """Anima la tasa negativa y luego presenta las tres conclusiones.

        Retorno:
            Ninguno; agrega ambas partes de la escena.

        Ejemplo:
            Manim llama este método al renderizar la escena.
        """
        rate = PROBLEM.negative_rate
        evaluation = compute_exact_integral(rate)
        axes = build_rate_axes(
            rate,
            float(PROBLEM.negative_axis_min),
            float(PROBLEM.positive_axis_min),
        ).scale(0.62).shift(LEFT * 2.5 + DOWN * 0.35)
        graph = build_rate_graph(axes, compute_rate_plot(rate), rate, color=NEGATIVE_RED)
        rectangles = axes.get_riemann_rectangles(
            graph,
            x_range=[float(rate.interval.start), float(rate.interval.end)],
            dx=float(compute_riemann_table(rate, (PROBLEM.partitions[0],)).rows[0].delta_t),
            input_sample_type="center",
            color=NEGATIVE_RED,
            fill_opacity=0.48,
            show_signed_area=False,
        )
        title = Text("El signo también importa", font_size=TITLE_SIZE).to_edge(UP)
        rate_formula = MathTex(
            rf"r(t)=-({format_value(abs(rate.intercept))}"
            rf"+{format_value(abs(rate.slope))}t)",
            color=NEGATIVE_RED,
        ).to_edge(RIGHT, buff=0.55).shift(UP * 0.75)
        integral_formula = MathTex(
            rf"\int_{{{format_value(evaluation.start)}}}^{{{format_value(evaluation.end)}}}"
            rf"-({format_value(abs(rate.intercept))}"
            rf"+{format_value(abs(rate.slope))}t)\,dt"
            rf"={format_value(evaluation.value)}\,\mathrm{{{evaluation.unit}}}",
            color=NEGATIVE_RED,
        ).scale(0.72).next_to(rate_formula, DOWN, buff=0.7).align_to(rate_formula, RIGHT)
        caption = Text(
            "Cambio neto del espacio libre del disco durante la descarga",
            font_size=23,
        ).to_edge(DOWN)
        closing = VGroup(
            MathTex(r"\text{Aportes pequeños: }r(t_i^*)\,\Delta t", font_size=28, color=RATE_BLUE),
            Text("Suma y límite: la integral", font_size=28, color=RESULT_GREEN),
            Text("Significado: magnitudes y unidades", font_size=28),
        ).arrange(DOWN, buff=0.45)
        thanks = Text("¡Gracias por ver nuestro video!", font_size=32).to_edge(DOWN)
        self.play(Write(title), Create(axes), Create(graph))
        self.play(FadeIn(rectangles), Write(rate_formula), Write(integral_formula), FadeIn(caption))
        self.wait(1.5)
        self.play(
            FadeOut(axes),
            FadeOut(graph),
            FadeOut(rectangles),
            FadeOut(rate_formula),
            FadeOut(integral_formula),
            FadeOut(caption),
        )
        self.play(Transform(title, Text("La integral más allá del área", font_size=TITLE_SIZE).to_edge(UP)))
        for idea in closing:
            self.play(Write(idea))
            self.wait(0.45)
        self.play(Write(thanks))
        self.wait(2)
