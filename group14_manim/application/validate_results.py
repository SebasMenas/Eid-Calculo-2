"""Validación ejecutable de resultados exactos del problema.

Ejemplo:
    ``validate_results(...)`` devuelve una colección vacía cuando todo coincide.
"""

from dataclasses import dataclass
from fractions import Fraction

from group14_manim.application.compute_net_change import compute_net_change
from group14_manim.application.compute_riemann_table import compute_riemann_table
from group14_manim.domain.integral import integral_exact
from group14_manim.domain.rate_function import RateFunction
from group14_manim.domain.riemann import RiemannMethod, riemann_sum


@dataclass(frozen=True)
class ValidationIssue:
    """Diferencia entre un resultado esperado y uno calculado.

    Ejemplo:
        ``issue.description`` explica el control que no coincidió.
    """

    description: str
    expected: Fraction
    calculated: Fraction


@dataclass(frozen=True)
class ValidationExpectations:
    """Valores de referencia externos para el control exacto del caso.

    Ejemplo:
        ``ValidationExpectations(...).exact_integral`` fija el total esperado.
    """

    riemann_rows: tuple[tuple[int, Fraction, Fraction, Fraction], ...]
    exact_integral: Fraction
    constant_integral: Fraction
    negative_integral: Fraction
    downloaded: Fraction
    remaining: Fraction


def validate_results(
    rate: RateFunction,
    partitions: tuple[int, ...],
    constant_rate: RateFunction,
    negative_rate: RateFunction,
    initial_capacity: Fraction,
    expectations: ValidationExpectations,
) -> tuple[ValidationIssue, ...]:
    """Compara con aritmética exacta todos los resultados del guion.

    Parámetros:
        rate: Tasa principal que se valida.
        partitions: Particiones usadas en la tabla.
        constant_rate: Modelo constante del ejemplo geométrico.
        negative_rate: Modelo de signo negativo.
        initial_capacity: Capacidad original del archivo.
        expectations: Contrato de valores esperados.

    Retorno:
        Tupla vacía si los resultados esperados coinciden.

    Ejemplo:
        ``validate_results(...) == ()`` confirma los valores del video.
    """
    issues: list[ValidationIssue] = []
    table = compute_riemann_table(rate, partitions)
    actual_rows = tuple((row.n, row.left, row.right, row.midpoint) for row in table.rows)
    for actual, expected in zip(actual_rows, expectations.riemann_rows, strict=True):
        for method_name, calculated, target in zip(
            ("izquierda", "derecha", "punto medio"),
            actual[1:],
            expected[1:],
            strict=True,
        ):
            if calculated != target:
                issues.append(ValidationIssue(f"Riemann n={actual[0]} {method_name}", target, calculated))

    exact_expected = expectations.exact_integral
    exact_actual = integral_exact(rate)
    if exact_actual != exact_expected:
        issues.append(ValidationIssue("Integral exacta", exact_expected, exact_actual))

    constant_expected = expectations.constant_integral
    constant_actual = integral_exact(constant_rate)
    if constant_actual != constant_expected:
        issues.append(ValidationIssue("Tasa constante", constant_expected, constant_actual))

    negative_expected = expectations.negative_integral
    negative_actual = integral_exact(negative_rate)
    if negative_actual != negative_expected:
        issues.append(ValidationIssue("Integral negativa", negative_expected, negative_actual))

    downloaded = compute_net_change(rate, Fraction(0)).change
    downloaded_expected = expectations.downloaded
    if downloaded != downloaded_expected:
        issues.append(ValidationIssue("Cantidad descargada", downloaded_expected, downloaded))

    remaining = compute_net_change(negative_rate, initial_capacity).final_value
    remaining_expected = expectations.remaining
    if remaining != remaining_expected:
        issues.append(ValidationIssue("Espacio restante", remaining_expected, remaining))

    left_5 = riemann_sum(rate, 5, RiemannMethod.LEFT)
    right_5 = riemann_sum(rate, 5, RiemannMethod.RIGHT)
    midpoint_5 = riemann_sum(rate, 5, RiemannMethod.MIDPOINT)
    if not left_5 < exact_actual < right_5:
        issues.append(ValidationIssue("Orden creciente izquierda < integral < derecha", exact_actual, (left_5 + right_5) / 2))
    if midpoint_5 != exact_actual:
        issues.append(ValidationIssue("Punto medio exacto para función lineal", exact_actual, midpoint_5))
    return tuple(issues)


def require_valid_results(
    rate: RateFunction,
    partitions: tuple[int, ...],
    constant_rate: RateFunction,
    negative_rate: RateFunction,
    initial_capacity: Fraction,
    expectations: ValidationExpectations,
) -> None:
    """Falla explícitamente si un resultado central del guion no coincide.

    Retorno:
        Ninguno si la validación pasó.

    Ejemplo:
        ``require_valid_results(...)`` puede usarse al iniciar el render general.
    """
    issues = validate_results(rate, partitions, constant_rate, negative_rate, initial_capacity, expectations)
    if issues:
        details = "; ".join(
            f"{issue.description}: esperado {issue.expected}, calculado {issue.calculated}"
            for issue in issues
        )
        raise ArithmeticError(details)
