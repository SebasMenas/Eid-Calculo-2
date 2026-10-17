# Validación matemática previa a las animaciones

Todos los resultados se calcularon con `fractions.Fraction`; no se encontró una discrepancia con los valores suministrados, por lo que no fue necesario corregir el guion.

| Caso | Valor esperado | Valor calculado | Acción tomada |
|---|---:|---:|---|
| Integral exacta de `2 + t/2` entre 0 y 10 | 45 MB | 45 MB | Sin corrección |
| Suma izquierda, n=5, Δt=2 | 40 MB | 40 MB | Sin corrección |
| Suma derecha, n=5, Δt=2 | 50 MB | 50 MB | Sin corrección |
| Punto medio, n=5, Δt=2 | 45 MB | 45 MB | Sin corrección |
| Suma izquierda, n=10, Δt=1 | 42.5 MB | 42.5 MB | Sin corrección |
| Suma derecha, n=10, Δt=1 | 47.5 MB | 47.5 MB | Sin corrección |
| Punto medio, n=10, Δt=1 | 45 MB | 45 MB | Sin corrección |
| Suma izquierda, n=100, Δt=0.1 | 44.75 MB | 44.75 MB | Sin corrección |
| Suma derecha, n=100, Δt=0.1 | 45.25 MB | 45.25 MB | Sin corrección |
| Punto medio, n=100, Δt=0.1 | 45 MB | 45 MB | Sin corrección |
| Tasa constante, 4 MB/s durante 10 s | 40 MB | 40 MB | Sin corrección |
| Tasa negativa, `-(2 + t/2)` entre 0 y 10 | -45 MB | -45 MB | Sin corrección |
| Archivo de 100 MB: cantidad recibida | 45 MB | 45 MB | Sin corrección |
| Archivo de 100 MB: cantidad restante | 55 MB | 55 MB | Sin corrección |
| Potencia por tiempo | W·s = J | W·s = J | Álgebra de unidades verificada |
| Peticiones por segundo por tiempo | peticiones/s·s = peticiones | peticiones/s·s = peticiones | Álgebra de unidades verificada |

## Comprobaciones de lógica

- La tasa `r(t)=2+t/2` es creciente en el intervalo: la suma izquierda queda por debajo de la integral y la suma derecha por encima.
- El punto medio resulta exacto para esta función lineal en particiones uniformes.
- El signo negativo representa cambio neto negativo; no se toma el valor absoluto en la integral.
- Las unidades se simplifican multiplicando la unidad de la tasa por la unidad de tiempo.
- Estas propiedades se verifican también mediante pruebas automatizadas en `group14_manim/tests`.
