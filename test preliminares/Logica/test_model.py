from model import (
    suma_izq,
    suma_der,
    suma_medio,
    integral_exacta
)

n = 5

for duracion in [2, 5, 10, 20]:
    print(f"\nDuración: {duracion} segundos")
    print(f"Izquierda: {suma_izq(n, duracion):.2f} MB")
    print(f"Derecha:   {suma_der(n, duracion):.2f} MB")
    print(f"Punto medio: {suma_medio(n, duracion):.2f} MB")
    print(f"Integral:  {integral_exacta(duracion):.2f} MB")
