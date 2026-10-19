"""Parámetros centrales del problema y de sus ejemplos dimensionales.

Ejemplo:
    ``PROBLEM.rate.value_at(Fraction(10))`` devuelve la tasa final de descarga.
"""

from dataclasses import dataclass
from fractions import Fraction

from group14_manim.application.validate_results import ValidationExpectations
from group14_manim.domain.rate_function import RateFunction, TimeInterval
from group14_manim.domain.units import Unit, UnitExample


SECOND = Unit.base("s")
MEGABYTE_PER_SECOND = Unit((("MB", 1), ("s", -1)))
WATT = Unit.base("W")
REQUEST_PER_SECOND = Unit((("peticiones", 1), ("s", -1)))
MEGABYTE = Unit.base("MB")
WATT_SECOND = WATT * SECOND
REQUEST = REQUEST_PER_SECOND * SECOND


@dataclass(frozen=True)
class ProblemConfig:
    """Datos inmutables del caso de descarga del archivo.

    Ejemplo:
        ``PROBLEM.rate.interval.duration`` devuelve los diez segundos del modelo.
    """

    rate: RateFunction
    initial_file_size: Fraction
    partitions: tuple[int, ...]
    sample_interval: TimeInterval
    constant_rate_model: RateFunction
    positive_axis_min: Fraction
    positive_axis_max: Fraction
    negative_axis_min: Fraction
    negative_rate: RateFunction
    group_name: str
    contributors: tuple[str, ...]
    references: tuple[str, ...]

PROBLEM = ProblemConfig(
    rate=RateFunction(
        intercept=Fraction(2),
        slope=Fraction(1, 2),
        interval=TimeInterval(Fraction(0), Fraction(10)),
        rate_unit=MEGABYTE_PER_SECOND,
        variable_unit=SECOND,
    ),
    initial_file_size=Fraction(100),
    partitions=(5, 10, 100),
    sample_interval=TimeInterval(Fraction(4), Fraction(6)),
    constant_rate_model=RateFunction(
        intercept=Fraction(4),
        slope=Fraction(0),
        interval=TimeInterval(Fraction(0), Fraction(10)),
        rate_unit=MEGABYTE_PER_SECOND,
        variable_unit=SECOND,
    ),
    positive_axis_min=Fraction(0),
    positive_axis_max=Fraction(8),
    negative_axis_min=Fraction(-8),
    negative_rate=RateFunction(
        intercept=Fraction(-2),
        slope=Fraction(-1, 2),
        interval=TimeInterval(Fraction(0), Fraction(10)),
        rate_unit=MEGABYTE_PER_SECOND,
        variable_unit=SECOND,
    ),
    group_name="Grupo 14",
    contributors=(
        "NICOLÁS FELIPE ARRIAGADA RÍOS",
        "CRISTIAN EMMANUEL CÁCERES ESCARE",
        "SEBASTIÁN ESTEBAN MENA FUENTEALBA",
    ),
    references=(
        "Larson, R., & Edwards, B. H. (2016). Cálculo: Tomo I (10.ª ed.). Cengage Learning.\n"
        "Sección 4.3, “Sumas de Riemann e integrales definidas”, pp. 266–276 (inicio: p. 266).\n"
        "Cita en texto: (Larson & Edwards, 2016, p. 266).",
        "Thomas, G. B., Weir, M. D., & Hass, J. (2010). Cálculo: Una variable (12.ª ed.). Pearson Educación.\n"
        "Sección 5.2, “Notación sigma y límites de sumas finitas”, p. 309; sección 5.3, “La integral definida”, p. 316 (ed. en inglés).\n"
        "Cita en texto: (Thomas et al., 2010, p. 309).",
    ),
)

UNIT_EXAMPLES = (
    UnitExample("Descarga", "r(t)", MEGABYTE_PER_SECOND, SECOND, MEGABYTE_PER_SECOND * SECOND),
    UnitExample("Procesador", "P(t)", WATT, SECOND, WATT_SECOND),
    UnitExample("Servidor", "λ(t)", REQUEST_PER_SECOND, SECOND, REQUEST),
)

EXPECTED_RESULTS = ValidationExpectations(
    riemann_rows=(
        (5, Fraction(40), Fraction(50), Fraction(45)),
        (10, Fraction(85, 2), Fraction(95, 2), Fraction(45)),
        (100, Fraction(179, 4), Fraction(181, 4), Fraction(45)),
    ),
    exact_integral=Fraction(45),
    constant_integral=Fraction(40),
    negative_integral=Fraction(-45),
    downloaded=Fraction(45),
    remaining=Fraction(55),
)
