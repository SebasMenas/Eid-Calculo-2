"""Caso de uso para obtener ejemplos de unidades acumuladas.

Ejemplo:
    ``compute_unit_examples(examples)[0].accumulated_unit`` representa megabytes.
"""

from group14_manim.domain.units import UnitExample


def compute_unit_examples(examples: tuple[UnitExample, ...]) -> tuple[UnitExample, ...]:
    """Devuelve ejemplos configurados de tasas con unidades distintas.

    Parámetros:
        examples: Ejemplos dimensionales configurados por el adaptador externo.

    Retorno:
        Tupla inmutable de ejemplos para presentar.

    Ejemplo:
        ``len(compute_unit_examples(examples))`` devuelve la cantidad de contextos.
    """
    if not examples:
        raise ValueError("Se requiere al menos un ejemplo de unidades.")
    return examples
