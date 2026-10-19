"""Créditos del video y referencias bibliográficas configurables.

Ejemplo:
    ``manim -pql group14_manim/presentation/scenes/scene_9_credits.py Scene9Credits``
"""

from manim import DOWN, LEFT, Scene, Text, VGroup, Write

from group14_manim.config.problem import PROBLEM


class Scene9Credits(Scene):
    """5:15–5:30; cierra con los créditos del grupo y las fuentes.

    Los nombres se editan en ``config/problem.py`` sin modificar la escena.

    Ejemplo:
        ``manim -pql scene_9_credits.py Scene9Credits``.
    """

    def construct(self) -> None:
        """Muestra grupo, integrantes y fuentes configuradas.

        Retorno:
            Ninguno; agrega textos a la escena.

        Ejemplo:
            Manim llama el método para renderizar los créditos.
        """
        title = Text(PROBLEM.group_name, font_size=42)
        contributors = VGroup(
            *(Text(contributor, font_size=25) for contributor in PROBLEM.contributors)
        ).arrange(DOWN, buff=0.16)
        references = VGroup(
            *(
                Text(reference, font_size=15, line_spacing=0.7)
                for reference in PROBLEM.references
            )
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        content = VGroup(title, contributors, references).arrange(DOWN, buff=0.42)
        self.play(Write(content))
        self.wait(5)
