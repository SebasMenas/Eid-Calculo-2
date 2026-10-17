"""Álgebra mínima de unidades para tasas y cantidades acumuladas.

Ejemplo:
    ``Unit.base("MB/s") * Unit.base("s")`` produce la unidad ``MB``.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Unit:
    """Unidad dimensional representada por potencias enteras de símbolos.

    Parámetros:
        dimensions: Potencias de las unidades base, en orden estable.

    Ejemplo:
        ``Unit.base("W") * Unit.base("s")`` representa un joule.
    """

    dimensions: tuple[tuple[str, int], ...]

    def __post_init__(self) -> None:
        """Normaliza dimensiones y descarta potencias nulas.

        Ejemplo:
            ``Unit((("s", 1), ("s", -1)))`` se normaliza a unidad adimensional.
        """
        combined: dict[str, int] = {}
        for symbol, power in self.dimensions:
            combined[symbol] = combined.get(symbol, 0) + power
        normalized = tuple(sorted((symbol, power) for symbol, power in combined.items() if power))
        object.__setattr__(self, "dimensions", normalized)

    @classmethod
    def base(cls, symbol: str) -> Unit:
        """Crea una unidad atómica.

        Parámetros:
            symbol: Símbolo, por ejemplo ``"MB"`` o ``"s"``.

        Retorno:
            Unidad con potencia uno.

        Ejemplo:
            ``Unit.base("s")`` crea segundos.
        """
        return cls(((symbol, 1),))

    def __mul__(self, other: Unit) -> Unit:
        """Multiplica dimensiones y simplifica símbolos iguales.

        Parámetros:
            other: Unidad multiplicadora.

        Retorno:
            Unidad producto simplificada.

        Ejemplo:
            ``Unit.base("MB/s") * Unit.base("s")`` produce ``MB``.
        """
        return Unit(self.dimensions + other.dimensions)

    def __str__(self) -> str:
        """Devuelve la forma legible de la unidad.

        Retorno:
            Símbolo simplificado con numerador y denominador.

        Ejemplo:
            ``str(Unit.base("MB/s") * Unit.base("s"))`` devuelve ``"MB"``.
        """
        if self.dimensions == (("MB", 1),):
            return "MB"
        if self.dimensions == (("W", 1), ("s", 1)):
            return "J"
        if self.dimensions == (("peticiones", 1),):
            return "peticiones"
        numerator = [self._format_factor(symbol, power) for symbol, power in self.dimensions if power > 0]
        denominator = [self._format_factor(symbol, -power) for symbol, power in self.dimensions if power < 0]
        top = "·".join(numerator) or "1"
        return f"{top}/{'·'.join(denominator)}" if denominator else top

    @staticmethod
    def _format_factor(symbol: str, power: int) -> str:
        """Formatea una unidad con su exponente.

        Parámetros:
            symbol: Símbolo de unidad.
            power: Exponente positivo.

        Retorno:
            Símbolo simple o elevado.

        Ejemplo:
            ``Unit._format_factor("s", 2)`` devuelve ``"s^2"``.
        """
        return symbol if power == 1 else f"{symbol}^{power}"


@dataclass(frozen=True)
class UnitExample:
    """Contexto dimensional inmutable para una tasa acumulada.

    Ejemplo:
        ``UnitExample("Procesador", "P(t)", watt, second, joule)``.
    """

    context: str
    rate_label: str
    rate_unit: Unit
    variable_unit: Unit
    accumulated_unit: Unit
