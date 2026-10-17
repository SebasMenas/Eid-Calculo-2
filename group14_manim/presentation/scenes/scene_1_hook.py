"""Gancho visual inicial sobre la descarga y la pregunta de acumulación.

Ejemplo:
    ``manim -pql group14_manim/presentation/scenes/scene_1_hook.py Scene1Hook``
"""

from manim import (
    DOWN,
    LEFT,
    UP,
    Rectangle,
    Scene,
    Text,
    ValueTracker,
    Write,
    FadeIn,
    always_redraw,
)

from group14_manim.application.compute_download_summary import compute_download_summary
from group14_manim.application.compute_rate_plot import compute_rate_plot
from group14_manim.config.problem import PROBLEM
from group14_manim.presentation.theme import BACKGROUND_BAR, BODY_SIZE, RATE_BLUE, RESULT_GREEN, TITLE_SIZE


class Scene1Hook(Scene):
    """0:00–0:30; muestra la descarga y pregunta cuánto se acumula.

    Se ve una barra que se llena mientras cambia la tasa instantánea.
    Explica que la pregunta trata de la cantidad acumulada, no de una altura.

    Ejemplo:
        Renderiza con ``manim -pql scene_1_hook.py Scene1Hook``.
    """

    def construct(self) -> None:
        """Anima el gancho, la tasa y la cantidad que llega.

        Retorno:
            Ninguno; agrega animaciones a la escena.

        Ejemplo:
            Manim llama este método al renderizar ``Scene1Hook``.
        """
        summary = compute_download_summary(PROBLEM.rate, PROBLEM.negative_rate, PROBLEM.initial_file_size)
        rate = PROBLEM.rate
        title = Text("La integral más allá del área", font_size=TITLE_SIZE)
        title.to_edge(UP)
        question = Text(
            f"¿Cuántos {rate.accumulated_unit} llegaron en {float(rate.interval.duration):g} s?",
            font_size=BODY_SIZE,
        )
        question.to_edge(DOWN)
        bar_width = 6.4
        bar_height = 0.62
        background = Rectangle(width=bar_width, height=bar_height, fill_color=BACKGROUND_BAR, fill_opacity=1)
        downloaded = ValueTracker(0)
        progress_bar = always_redraw(
            lambda: Rectangle(
                width=max(0.01, bar_width * downloaded.get_value()),
                height=bar_height,
                fill_color=RESULT_GREEN,
                fill_opacity=1,
                stroke_width=0,
            ).align_to(background, DOWN).align_to(background, LEFT)
        )
        rate_plot = compute_rate_plot(rate)
        rate_tracker = ValueTracker(rate_plot.start_value)
        rate_display = always_redraw(
            lambda: Text(
                f"{rate_tracker.get_value():.1f} {rate.rate_unit}",
                font_size=BODY_SIZE,
                color=RATE_BLUE,
            ).next_to(background, UP)
        )
        total_label = Text(
            f"{float(summary.downloaded):g} / {float(summary.capacity):g} {rate.accumulated_unit}",
            font_size=BODY_SIZE,
            color=RESULT_GREEN,
        ).next_to(background, DOWN, buff=0.55)
        background.move_to([0, 0.6, 0])
        progress_bar.update(0)
        rate_display.update(0)
        self.play(Write(title))
        self.play(FadeIn(question), FadeIn(background), FadeIn(total_label), FadeIn(rate_display), FadeIn(progress_bar))
        self.play(
            downloaded.animate.set_value(float(summary.completion_fraction)),
            rate_tracker.animate.set_value(rate_plot.end_value),
            run_time=1.5,
        )
        self.wait(0.3)
