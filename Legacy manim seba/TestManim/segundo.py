
from manim import *


class Presentacion(Scene):
    def construct(self):

        # 1. Crear el título principal.
        titulo = Text(
            "Hola cauros que se cuentan...",
            font_size=40,
            weight=BOLD,
            color=BLUE_C
        )

        # 2. Crear un subtítulo debajo del título.
        subtitulo = Text(
            "digan algo cabrones",
            font_size=25,
            color=WHITE
        )

        subtitulo.next_to(titulo, DOWN, buff=0.4)

        # 3. Crear una línea decorativa bajo el subtítulo.
        linea = Line(
            LEFT * 2,
            RIGHT * 2,
            color=YELLOW,
            stroke_width=4
        )

        linea.next_to(subtitulo, DOWN, buff=0.5)

        # 4. Agrupar todos los elementos.
        presentacion = VGroup(
            titulo,
            subtitulo,
            linea
        )

        # 5. Centrar el conjunto en la pantalla.
        presentacion.move_to(ORIGIN)

        # 6. Animar la aparición de los elementos.
        self.play(Write(titulo), run_time=2)
        self.play(FadeIn(subtitulo, shift=UP * 0.3))
        self.play(Create(linea))

        # 7. Mantener la presentación visible.
        self.wait(3)

        # 8. Despedir la escena suavemente.
        self.play(FadeOut(presentacion), run_time=1.5)
