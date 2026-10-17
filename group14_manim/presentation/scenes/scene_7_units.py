"""Escena de álgebra dimensional para tres interpretaciones de la integral.

Ejemplo:
    ``manim -pql group14_manim/presentation/scenes/scene_7_units.py Scene7Units``
"""

from manim import (
    DOWN,
    Arrow,
    FadeIn,
    Indicate,
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
    UP,
    VGroup,
    Write,
)

from group14_manim.application.compute_unit_examples import compute_unit_examples
from group14_manim.config.problem import UNIT_EXAMPLES
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
        rows = []
        cancellations = []
        for example in examples:
            context = VGroup(
                make_context_icon(example.context),
                Text(example.context, font_size=BODY_SIZE, color=RATE_BLUE),
            ).arrange(RIGHT, buff=0.12)
            rate_unit = MathTex(unit_expression(example.rate_unit))
            time_unit = MathTex(unit_expression(example.variable_unit))
            result_unit = MathTex(unit_expression(example.accumulated_unit), color=RESULT_GREEN)
            product = MathTex(r"\cdot")
            equals = MathTex("=")
            row = VGroup(context, rate_unit, product, time_unit, equals, result_unit).arrange(RIGHT, buff=0.28)
            rows.append(row)
            if any(symbol == "s" and power < 0 for symbol, power in example.rate_unit.dimensions):
                seconds = rate_unit.get_part_by_tex(r"\mathrm{s}")
                cancellations.append(seconds)
        VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([0, 0.35, 0])
        formula = MathTex(
            r"[\text{integral}]=[\text{tasa}]\times[\text{variable}]",
            color=RESULT_GREEN,
        ).scale(0.82).to_edge(DOWN)
        self.play(Write(title))
        self.play(*[FadeIn(row) for row in rows], lag_ratio=0.25)
        for seconds in cancellations:
            self.play(Indicate(seconds, color=RESULT_GREEN), run_time=0.45)
        self.play(Write(formula))
        self.wait(0.3)
