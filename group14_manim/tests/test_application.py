"""Pruebas de los casos de uso que consumen el dominio matemático.

Ejemplo:
    ``python -m pytest group14_manim/tests/test_application.py``
"""

from fractions import Fraction

import pytest

from group14_manim.application.compute_download_summary import compute_download_summary
from group14_manim.application.compute_exact_integral import compute_exact_integral
from group14_manim.application.compute_net_change import compute_net_change
from group14_manim.application.compute_riemann_table import compute_riemann_table
from group14_manim.application.compute_sample_contribution import compute_sample_contribution
from group14_manim.application.compute_unit_examples import compute_unit_examples
from group14_manim.application.validate_results import require_valid_results, validate_results
from group14_manim.config.problem import EXPECTED_RESULTS, PROBLEM, UNIT_EXAMPLES, ProblemConfig
from group14_manim.domain.rate_function import TimeInterval
from group14_manim.domain.units import Unit


def test_table_use_case_has_all_configured_partitions(problem: ProblemConfig) -> None:
    """Comprueba filas, anchuras y sumas generadas para la tabla animada.

    Ejemplo:
        La tabla contiene particiones ``5``, ``10`` y ``100``.
    """
    table = compute_riemann_table(problem.rate, problem.partitions)
    assert tuple(row.n for row in table.rows) == problem.partitions
    assert tuple(row.midpoint for row in table.rows) == (Fraction(45),) * 3
    assert tuple(row.delta_t for row in table.rows) == (Fraction(2), Fraction(1), Fraction(1, 10))


def test_download_summary_and_net_change(problem: ProblemConfig) -> None:
    """Verifica megabytes recibidos, capacidad, avance y espacio restante.

    Ejemplo:
        De un archivo de ``100 MB``, llegan ``45 MB`` y faltan ``55 MB``.
    """
    summary = compute_download_summary(problem.rate, problem.negative_rate, problem.initial_file_size)
    assert summary.capacity == Fraction(100)
    assert summary.downloaded == Fraction(45)
    assert summary.remaining == Fraction(55)
    assert summary.completion_fraction == Fraction(45, 100)
    assert summary.completion_percentage == Fraction(45)
    assert compute_net_change(problem.negative_rate, problem.initial_file_size).final_value == Fraction(55)


def test_local_contribution_uses_the_sample_and_interval(problem: ProblemConfig) -> None:
    """Calcula el aporte del punto medio del intervalo configurado.

    Ejemplo:
        ``4.5 MB/s × 2 s`` corresponde a ``9 MB``.
    """
    result = compute_sample_contribution(problem.rate, problem.sample_interval)
    assert result.sample_time == Fraction(5)
    assert result.sample_rate == Fraction(9, 2)
    assert result.delta_t == Fraction(2)
    assert result.value == Fraction(9)
    assert str(result.accumulated_unit) == "MB"


def test_unit_products_simplify_download_energy_and_requests() -> None:
    """Comprueba cancelación de segundos y alias dimensionales.

    Ejemplo:
        ``W·s`` se presenta como joules y peticiones/s·s como peticiones.
    """
    assert str(Unit((("MB", 1), ("s", -1))) * Unit.base("s")) == "MB"
    assert str(Unit.base("W") * Unit.base("s")) == "J"
    request_rate = Unit((("peticiones", 1), ("s", -1)))
    assert str(request_rate * Unit.base("s")) == "peticiones"
    assert tuple(example.accumulated_unit for example in compute_unit_examples(UNIT_EXAMPLES)) == (
        Unit.base("MB"),
        Unit.base("W") * Unit.base("s"),
        Unit.base("peticiones"),
    )


def test_exact_integral_use_case_exposes_antiderivative_values(problem: ProblemConfig) -> None:
    """Verifica los pasos exactos que alimentan la escena de la integral.

    Ejemplo:
        La antiderivada evaluada al final vale ``45``.
    """
    evaluation = compute_exact_integral(problem.rate)
    assert evaluation.primitive_quadratic_coefficient == Fraction(1, 4)
    assert evaluation.primitive_at_start == 0
    assert evaluation.primitive_at_end == 45
    assert evaluation.value == 45


def test_validation_use_case_reports_no_mismatches() -> None:
    """Confirma todos los valores y propiedades pedagógicas configurados.

    Ejemplo:
        ``validate_results(...)`` devuelve ``()`` para el guion correcto.
    """
    parameters = (
        PROBLEM.rate,
        PROBLEM.partitions,
        PROBLEM.constant_rate_model,
        PROBLEM.negative_rate,
        PROBLEM.initial_file_size,
        EXPECTED_RESULTS,
    )
    assert validate_results(*parameters) == ()
    require_valid_results(*parameters)


def test_sample_must_belong_to_subinterval(problem: ProblemConfig) -> None:
    """Rechaza muestras que no correspondan al rectángulo local.

    Ejemplo:
        Una muestra anterior al intervalo no puede producir un aporte.
    """
    with pytest.raises(ValueError):
        compute_sample_contribution(
            problem.rate,
            TimeInterval(Fraction(4), Fraction(6)),
            Fraction(3),
        )


def test_subinterval_must_belong_to_rate_domain(problem: ProblemConfig) -> None:
    """Rechaza un rectángulo que se extienda fuera del dominio de integración.

    Ejemplo:
        Un subintervalo cuyo extremo sobrepasa el final de la tasa es inválido.
    """
    with pytest.raises(ValueError):
        compute_sample_contribution(
            problem.rate,
            TimeInterval(Fraction(9), Fraction(11)),
            Fraction(10),
        )
