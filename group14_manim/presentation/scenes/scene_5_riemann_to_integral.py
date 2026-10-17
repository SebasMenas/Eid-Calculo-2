"""Escena de aproximación por sumas de Riemann y paso al límite.

Ejemplo:
    ``manim -pql group14_manim/presentation/scenes/scene_5_riemann_to_integral.py Scene5RiemannToIntegral``
"""

from manim import (
    DOWN,
    Create,
    FadeIn,
    LEFT,
    MathTex,
    Scene,
    Text,
    Transform,
    UP,
    UR,
    ValueTracker,
    VGroup,
    Write,
    always_redraw,
)

from group14_manim.application.compute_rate_plot import compute_rate_plot
from group14_manim.application.compute_riemann_table import compute_riemann_table
from group14_manim.config.problem import PROBLEM
from group14_manim.presentation.components.chart import (
    build_rate_axes,
    build_rate_graph,
    format_value,
    rate_label,
)
from group14_manim.presentation.theme import RECTANGLE_YELLOW, TITLE_SIZE


class Scene5RiemannToIntegral(Scene):
    """2:20–3:30; compara muestras y hace tender ``Δt`` a cero.

    Se ven rectángulos izquierdos, derechos y centrales, una tabla creciente
    de particiones y la notación de suma que conduce a la integral.

    Ejemplo:
        ``manim -pql scene_5_riemann_to_integral.py Scene5RiemannToIntegral``.
    """

    def construct(self) -> None:
        """Anima las reglas de muestreo y la reducción del tamaño de paso.

        Retorno:
            Ninguno; dibuja gráfica, tabla y límite integral.

        Ejemplo:
            Manim llama este método al renderizar la escena.
        """
        rate = PROBLEM.rate
        table = compute_riemann_table(rate, PROBLEM.partitions)
        axes = build_rate_axes(
            rate,
            float(PROBLEM.positive_axis_min),
            float(PROBLEM.positive_axis_max),
        )
        axes.scale(0.64).shift(LEFT * 3.2 + DOWN * 0.35)
        graph = build_rate_graph(axes, compute_rate_plot(rate), rate)
        title = Text("De los aportes a la suma", font_size=TITLE_SIZE).to_edge(UP)
        formula = MathTex(
            r"\sum_i r(t_i^*)\,\Delta t",
            r"\longrightarrow",
            rf"\int_{{{format_value(rate.interval.start)}}}^{{{format_value(rate.interval.end)}}}r(t)\,dt",
        ).to_edge(UP).shift(DOWN * 0.7)
        function_name = rate_label(rate).scale(0.72).to_corner(UR)
        rectangles = axes.get_riemann_rectangles(
            graph,
            x_range=[float(rate.interval.start), float(rate.interval.end)],
            dx=float(table.rows[0].delta_t),
            input_sample_type="left",
            color=RECTANGLE_YELLOW,
            fill_opacity=0.58,
            stroke_width=0.5,
        )
        dx_tracker = ValueTracker(float(table.rows[0].delta_t))
        self.play(Write(title), Write(formula))
        self.play(Create(axes), Create(graph), Write(function_name))
        self.play(Write(rectangles))

        for method in ("right", "center"):
            target = axes.get_riemann_rectangles(
                graph,
                x_range=[float(rate.interval.start), float(rate.interval.end)],
                dx=float(table.rows[0].delta_t),
                input_sample_type=method,
                color=RECTANGLE_YELLOW,
                fill_opacity=0.58,
                stroke_width=0.5,
            )
            self.play(Transform(rectangles, target), run_time=0.35)

        rows = []
        for result in table.rows:
            rows.append(
                MathTex(
                    f"{result.n}",
                    format_value(result.left),
                    format_value(result.right),
                    format_value(result.midpoint),
                ).scale(0.65)
            )
        headings = Text("n     Izq.     Der.     Medio", font_size=19)
        table_group = VGroup(headings, *rows).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        table_group.to_corner(UR).shift(DOWN * 1.8)
        for row in rows:
            self.play(Write(row), run_time=0.25)
        self.play(FadeIn(headings), run_time=0.25)

        self.remove(rectangles)
        # always_redraw actualiza los rectángulos al animar el cambio de Δt.
        dynamic_rectangles = always_redraw(
            lambda: axes.get_riemann_rectangles(
                graph,
                x_range=[float(rate.interval.start), float(rate.interval.end)],
                dx=dx_tracker.get_value(),
                input_sample_type="center",
                color=RECTANGLE_YELLOW,
                fill_opacity=0.58,
                stroke_width=0.5,
            )
        )
        self.add(dynamic_rectangles)
        self.play(dx_tracker.animate.set_value(float(table.rows[1].delta_t)), run_time=0.45)
        self.play(dx_tracker.animate.set_value(float(table.rows[2].delta_t)), run_time=0.7)
        self.wait(0.3)
