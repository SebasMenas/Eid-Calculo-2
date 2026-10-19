"""Escena de álgebra dimensional para tres interpretaciones de la integral.

Ejemplo:
    ``manim -pql group14_manim/presentation/scenes/scene_7_units.py Scene7Units``
"""

from manim import (
    AnimationGroup,
    DOWN,
    Arrow,
    Create,
    FadeIn,
    LaggedStart,
    LEFT,
    Line,
    MathTex,
    Rectangle,
    RoundedRectangle,
    RIGHT,
    Scene,
    Square,
    Text,
    UP,
    VGroup,
    Write,
)

from group14_manim.application.compute_exact_integral import compute_exact_integral
from group14_manim.application.compute_unit_examples import compute_unit_examples
from group14_manim.config.problem import PROBLEM, UNIT_EXAMPLES
from group14_manim.presentation.components.chart import unit_expression
from group14_manim.presentation.theme import BODY_SIZE, RATE_BLUE, RESULT_GREEN, TITLE_SIZE


def make_context_icon(context: str) -> VGroup:
    """Dibuja un pictograma simple para cada contexto de unidades.

    Parámetros:
        context: Nombre del ejemplo configurado.

    Retorno:
        Grupo Manim construido con figuras geométricas básicas.

    Ejemplo:
        ``make_context_icon("Procesador")`` devuelve un chip esquemático.
    """
    if context == "Descarga":
        page = Rectangle(width=0.42, height=0.5, color=RATE_BLUE)
        arrow = Arrow(UP * 0.17, DOWN * 0.15, buff=0, color=RATE_BLUE)
        return VGroup(page, arrow)
    if context == "Procesador":
        chip = Square(side_length=0.42, color=RATE_BLUE)
        pins = VGroup(
            Line(UP * 0.31, UP * 0.42, color=RATE_BLUE),
            Line(DOWN * 0.31, DOWN * 0.42, color=RATE_BLUE),
            Line(LEFT * 0.31, LEFT * 0.42, color=RATE_BLUE),
            Line(RIGHT * 0.31, RIGHT * 0.42, color=RATE_BLUE),
        )
        return VGroup(chip, pins)
    if context == "Servidor":
        boxes = VGroup(
            *(RoundedRectangle(width=0.5, height=0.17, corner_radius=0.03, color=RATE_BLUE) for _ in range(3))
        ).arrange(DOWN, buff=0.07)
        return boxes
    raise ValueError(f"No existe un icono configurado para {context!r}.")


class Scene7Units(Scene):
    """4:00–4:45; compara descarga, procesador y servidor por sus unidades.

    Se ve cómo tasa por tiempo produce MB, J o peticiones. Explica que la
    integral conserva el significado dimensional de las magnitudes.

    Ejemplo:
        ``manim -pql scene_7_units.py Scene7Units``.
    """

    def construct(self) -> None:
        """Presenta los productos de unidades y destaca la cancelación.

        Retorno:
            Ninguno; dibuja la tabla dimensional.

        Ejemplo:
            Manim llama este método al renderizar esta escena.
        """
        examples = compute_unit_examples(UNIT_EXAMPLES)
        title = Text("El significado está en las unidades", font_size=TITLE_SIZE).to_edge(UP)
        result_value = format(float(compute_exact_integral(PROBLEM.rate).value), "g")
        headings = VGroup(
            Text("Contexto", font_size=20),
            Text("Unidades de la tasa", font_size=20),
            Text("Tiempo", font_size=20),
            Text("Resultado", font_size=20),
        )
        column_x = (-4.55, -1.15, 2.0, 5.0)
        for heading, x in zip(headings, column_x):
            heading.move_to([x, 1.85, 0])

        rows = []
        row_animations = []
        for index, example in enumerate(examples):
            rate_unit = MathTex(
                unit_expression(example.rate_unit),
                substrings_to_isolate=[r"\mathrm{s}"],
            )
            time_unit = MathTex(unit_expression(example.variable_unit))
            context = VGroup(
                make_context_icon(example.context),
                Text(example.context, font_size=BODY_SIZE, color=RATE_BLUE),
            ).arrange(RIGHT, buff=0.12).move_to([column_x[0], 0.85 - index * 1.05, 0])
            row = VGroup(
                context,
                rate_unit.move_to([column_x[1], 0.85 - index * 1.05, 0]),
                time_unit.move_to([column_x[2], 0.85 - index * 1.05, 0]),
                MathTex(
                    rf"{result_value}\,\mathrm{{{example.accumulated_unit}}}",
                    color=RESULT_GREEN,
                ).move_to([column_x[3], 0.85 - index * 1.05, 0]),
            )
            rows.append(row)
            row_parts = [FadeIn(row)]
            if any(symbol == "s" and power < 0 for symbol, power in example.rate_unit.dimensions):
                seconds = rate_unit.get_part_by_tex(r"\mathrm{s}")
                row_parts.append(
                    Create(
                        Line(
                            seconds.get_left(),
                            seconds.get_right(),
                            color=RESULT_GREEN,
                            stroke_width=3,
                        )
                    )
                )
            row_animations.append(AnimationGroup(*row_parts, lag_ratio=0.2))
        formula = MathTex(
            r"\text{Integral}=\text{tasa}\times\text{tiempo}",
            color=RESULT_GREEN,
        ).scale(0.9).to_edge(DOWN, buff=0.45)
        self.play(Write(title))
        self.play(FadeIn(headings))
        self.play(
            LaggedStart(
                *row_animations,
                lag_ratio=0.65,
            )
        )
        self.play(Write(formula))
        self.wait(2)
