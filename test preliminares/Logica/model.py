
# Modelo matemático de descarga de un archivo
# Tasa: r(t) = 2 + 0.5*t MB/s

def r(t):
    """Devuelve la tasa de descarga en MB/s."""
    return 2 + 0.5 * t


def suma_izq(n, duracion):
    """Suma de Riemann por extremo izquierdo."""
    dt = duracion / n
    total = 0

    for i in range(n):
        t = i * dt
        total += r(t) * dt

    return total


def suma_der(n, duracion):
    """Suma de Riemann por extremo derecho."""
    dt = duracion / n
    total = 0

    for i in range(1, n + 1):
        t = i * dt
        total += r(t) * dt

    return total


def suma_medio(n, duracion):
    """Suma de Riemann por punto medio."""
    dt = duracion / n
    total = 0

    for i in range(n):
        t = (i + 0.5) * dt
        total += r(t) * dt

    return total


def integral_exacta(duracion):
    """Integral exacta desde t=0 hasta t=duracion."""
    return 2 * duracion + 0.25 * duracion**2

