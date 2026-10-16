
from manim import *


class PruebaManim(Scene):
    def construct(self):

        # ------------------------------------------------
        # 1. PRESENTACIÓN
        # ------------------------------------------------

        titulo = Text(
            "Esto es una prueba de Manim",
            font_size=36
        )

        subtitulo = Text(
            "Animaciones matemáticas con Python",
            font_size=24
        )

        subtitulo.next_to(titulo, DOWN, buff=0.4)

        # Escribe el título y muestra el subtítulo.
        self.play(Write(titulo))
        self.play(FadeIn(subtitulo))
        self.wait(2)

        # Limpia la pantalla antes de continuar.
        self.play(
            FadeOut(titulo),
            FadeOut(subtitulo)
        )

        # ------------------------------------------------
        # 2. EXPLICAR QUÉ ES UNA FUNCIÓN
        # ------------------------------------------------

        texto = Text(
            "Una función relaciona una entrada con una salida.",
            font_size=27
        )

        formula = MathTex(
            r"y = f(x)"
        ).scale(1.5)

        formula.next_to(texto, DOWN, buff=0.6)

        self.play(Write(texto))
        self.play(Write(formula))
        self.wait(2)

        self.play(
            FadeOut(texto),
            FadeOut(formula)
        )

        # ------------------------------------------------
        # 3. MOSTRAR UNA FUNCIÓN LINEAL
        # ------------------------------------------------

        titulo_lineal = Text(
            "Primera función: una recta",
            font_size=30
        ).to_edge(UP)

        # Creamos los ejes del gráfico.
        ejes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=4,
            axis_config={
                "include_numbers": True,
                "font_size": 20
            },
            tips=True
        )

        etiquetas = ejes.get_axis_labels(
            x_label="x",
            y_label="y"
        )

        # Definimos la función y = x.
        grafico_lineal = ejes.plot(
            lambda x: x,
            x_range=[-3, 3],
            color=BLUE
        )

        formula_lineal = MathTex(
            r"f(x) = x",
            color=BLUE
        ).to_corner(UR).shift(DOWN * 0.8)

        self.play(Write(titulo_lineal))
        self.play(Create(ejes))
        self.play(Write(etiquetas))
        self.play(Create(grafico_lineal))
        self.play(Write(formula_lineal))
        self.wait(2)

        # Quitamos los elementos de esta escena.
        self.play(
            FadeOut(titulo_lineal),
            FadeOut(ejes),
            FadeOut(etiquetas),
            FadeOut(grafico_lineal),
            FadeOut(formula_lineal)
        )

        # ------------------------------------------------
        # 4. MOSTRAR UNA FUNCIÓN CUADRÁTICA
        # ------------------------------------------------

        titulo_cuadratica = Text(
            "Segunda función: una parábola",
            font_size=30
        ).to_edge(UP)

        ejes2 = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 9, 2],
            x_length=6,
            y_length=4,
            axis_config={
                "include_numbers": True,
                "font_size": 20
            },
            tips=True
        )

        etiquetas2 = ejes2.get_axis_labels(
            x_label="x",
            y_label="y"
        )

        # Definimos la función y = x².
        grafico_cuadratico = ejes2.plot(
            lambda x: x**2,
            x_range=[-3, 3],
            color=YELLOW
        )

        formula_cuadratica = MathTex(
            r"f(x) = x^2",
            color=YELLOW
        ).to_corner(UR).shift(DOWN * 0.8)

        self.play(Write(titulo_cuadratica))
        self.play(Create(ejes2))
        self.play(Write(etiquetas2))
        self.play(Create(grafico_cuadratico))
        self.play(Write(formula_cuadratica))
        self.wait(2)

        # Limpiamos antes de la última parte.
        self.play(
            FadeOut(titulo_cuadratica),
            FadeOut(ejes2),
            FadeOut(etiquetas2),
            FadeOut(grafico_cuadratico),
            FadeOut(formula_cuadratica)
        )

        # ------------------------------------------------
        # 5. MOSTRAR UNA FUNCIÓN CONSTANTE
        # ------------------------------------------------

        titulo_constante = Text(
            "Tercera función: una constante",
            font_size=30
        ).to_edge(UP)

        ejes3 = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 5, 1],
            x_length=6,
            y_length=4,
            axis_config={
                "include_numbers": True,
                "font_size": 20
            },
            tips=True
        )

        etiquetas3 = ejes3.get_axis_labels(
            x_label="x",
            y_label="y"
        )

        # Definimos la función y = 3.
        grafico_constante = ejes3.plot(
            lambda x: 3,
            x_range=[-3, 3],
            color=GREEN
        )

        formula_constante = MathTex(
            r"f(x) = 3",
            color=GREEN
        ).to_corner(UR).shift(DOWN * 0.8)

        self.play(Write(titulo_constante))
        self.play(Create(ejes3))
        self.play(Write(etiquetas3))
        self.play(Create(grafico_constante))
        self.play(Write(formula_constante))
        self.wait(2)

        # ------------------------------------------------
        # 6. CONCLUSIÓN
        # ------------------------------------------------

        self.play(
            FadeOut(titulo_constante),
            FadeOut(ejes3),
            FadeOut(etiquetas3),
            FadeOut(grafico_constante),
            FadeOut(formula_constante)
        )

        conclusion = VGroup(
            Text(
                "¡Esta fue una prueba de Manim!",
                font_size=34,
                color=BLUE_C
            ),
            Text(
                "Podemos crear gráficos y animaciones",
                font_size=25
            ),
            Text(
                "matemáticas usando código Python.",
                font_size=25
            )
        ).arrange(DOWN, buff=0.35)

        self.play(Write(conclusion))
        self.wait(3)
        self.play(FadeOut(conclusion))
