# La integral más allá del área

Proyecto Manim del Grupo 14 para explicar qué representa una integral cuando la
función describe una tasa y no una altura geométrica. El ejemplo guía es la
descarga de un archivo: `r(t) = 2 + 0.5t MB/s` durante diez segundos. Cada aporte
`r(t_i*) Δt` se mide en MB; la suma de Riemann converge a la cantidad total.
La interpretación se obtiene de las magnitudes y sus unidades.

La matemática del dominio usa `Fraction` para que integrales, sumas, aportes y
validaciones sean exactos. Las escenas consultan los casos de uso: se encargan
de dibujar y animar, no de calcular resultados.

## Estructura del proyecto

```text
group14_manim/
├── domain/                            # Modelos matemáticos y unidades; sin Manim ni I/O
│   ├── rate_function.py               # Tasas afines e intervalos inmutables
│   ├── riemann.py                     # Sumas izquierda, derecha y punto medio
│   ├── integral.py                   # Antiderivada e integral exacta
│   └── units.py                       # Producto y simplificación dimensional
├── application/                       # Casos de uso que orquestan domain
│   ├── compute_riemann_table.py       # Tabla para n=5, 10 y 100
│   ├── compute_sample_contribution.py # Aporte local r(t*) Δt
│   ├── compute_constant_rate_change.py # Ejemplo de tasa constante
│   ├── compute_exact_integral.py      # Pasos de la integral exacta
│   ├── compute_net_change.py          # Cambio neto y estado final
│   ├── compute_download_summary.py    # Recibido, avance y restante
│   ├── compute_unit_examples.py       # Ejemplos dimensionales
│   ├── compute_rate_plot.py           # Adaptador de datos para curvas
│   └── validate_results.py            # Control exacto de cálculos y lógica
├── presentation/
│   ├── theme.py                       # Colores y tamaños visuales
│   ├── components/chart.py            # Ejes, curvas y formato dimensional
│   └── scenes/                        # Nueve escenas independientes
├── config/problem.py                  # Datos matemáticos y créditos editables
└── tests/                             # Pruebas pytest del dominio y aplicación
scripts/render_all.py                  # Renderiza las nueve escenas en orden
requirements.txt                       # Versiones comprobadas de Manim y pytest
VALIDACION.md                          # Cálculos exactos y revisión lógica
Readme.md                              # Esta guía
FUNCIONAMIENTO_APLICACION.txt          # Explicación del flujo y las capas
COMANDOS_ANIMACIONES.txt               # Comandos individuales para las nueve escenas
test preliminares/
├── Legacy manim seba/                 # Escenas exploratorias del prototipo
├── Logica/                            # Modelo y prueba manual anteriores
├── media/                             # Renders y cachés históricos de ensayo
└── README.txt                         # Inventario de material archivado
```

Las pruebas vigentes se mantienen en `group14_manim/tests/`. Los prototipos
anteriores y los renders generados durante los ensayos se conservaron dentro de
`test preliminares/`; no son dependencias de la aplicación nueva. El entorno
virtual `.venv/` se mantiene en la raíz para poder ejecutar el proyecto.

## Requisitos e instalación

- Windows 10/11 (los comandos de abajo están escritos para PowerShell).
- Python 3.12.
- MiKTeX con `latex` y `dvisvgm` para renderizar los textos matemáticos.

Desde la raíz del repositorio:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
winget install --id MiKTeX.MiKTeX --exact
```

`requirements.txt` fija **Manim Community 0.22.0**, versión cuya API de
`Axes.get_riemann_rectangles` y `Axes.get_area` se usa en el proyecto, y pytest
8.4.2. La instalación se probó con Python 3.12.10 en Windows. Manim 0.22.0
acepta `input_sample_type="left"`, `"right"` y `"center"` para sus rectángulos.
En esta versión, el tamaño visual de los rectángulos se obtiene de coordenadas
`Axes.c2p`; no se usan los atributos `x_unit_size`/`y_unit_size`, que no están
disponibles en `Axes`.

Después de instalar MiKTeX, abre **MiKTeX Console** y permite la instalación
automática de paquetes faltantes (*Install missing packages on-the-fly* = Yes).
Abre una terminal nueva para actualizar el `PATH`. Si `latex` o `dvisvgm` no se
reconocen, agrega la carpeta de MiKTeX
`%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64` al `PATH`. La configuración de
VS Code y el script de render ya anteponen esa ubicación cuando está instalada.

## Pruebas

```powershell
.\.venv\Scripts\python.exe -m pytest -q group14_manim\tests
```

Las pruebas cubren sumas e integral exactas, cotas izquierda/derecha, exactitud
del punto medio para una tasa lineal, tabla de resultados, cambio neto,
contribución local, simplificación de unidades y tasa negativa. Los resultados
esperados y la revisión de lógica están registrados en [VALIDACION.md](./VALIDACION.md).

## Renderizar escenas

Ejecuta los comandos desde la raíz del repositorio. El script de render agrega
MiKTeX al `PATH` del proceso y comprueba que `latex` y `dvisvgm` estén
disponibles, evitando el error `FileNotFoundError` al crear textos matemáticos.
Usa `--quality l` para el ensayo y `--quality h` para el render final; agrega
`--preview` si quieres abrir el video al terminar. Los nuevos MP4 se generan
bajo `media/videos/`; los renders históricos están en `test preliminares/media/`.
La composición está ajustada al encuadre panorámico 16:9; el render final de
Manim en calidad alta usa la resolución estándar de 1920×1080.
El archivo [COMANDOS_ANIMACIONES.txt](./COMANDOS_ANIMACIONES.txt) contiene
comandos individuales listos para copiar y los comandos para renderizar las
nueve escenas en orden.

```powershell
.\.venv\Scripts\python.exe scripts\render_all.py --scene Scene1Hook --quality l --preview
.\.venv\Scripts\python.exe scripts\render_all.py --scene Scene2ConstantRate --quality l --preview
.\.venv\Scripts\python.exe scripts\render_all.py --scene Scene3VariableRate --quality l --preview
.\.venv\Scripts\python.exe scripts\render_all.py --scene Scene4SmallContribution --quality l --preview
.\.venv\Scripts\python.exe scripts\render_all.py --scene Scene5RiemannToIntegral --quality l --preview
.\.venv\Scripts\python.exe scripts\render_all.py --scene Scene6ExactIntegral --quality l --preview
.\.venv\Scripts\python.exe scripts\render_all.py --scene Scene7Units --quality l --preview
.\.venv\Scripts\python.exe scripts\render_all.py --scene Scene8SignAndClosing --quality l --preview
.\.venv\Scripts\python.exe scripts\render_all.py --scene Scene9Credits --quality l --preview
```

Para renderizar todo el video en orden, sin abrir nueve reproductores:

```powershell
.\.venv\Scripts\python.exe scripts\render_all.py --quality l
.\.venv\Scripts\python.exe scripts\render_all.py --quality h
```

El mismo script permite renderizar una escena individual con `--scene`. Detiene
el proceso e informa el error si falla una escena o si no encuentra LaTeX.

## Cambiar datos del problema

Edita `group14_manim/config/problem.py`; las escenas obtienen de esa
configuración la tasa, intervalo, unidades, particiones, tasa negativa, tamaño
del archivo y créditos. Por ejemplo, cambia `intercept` y `slope` de
`PROBLEM.rate` con valores `Fraction`, y actualiza el archivo `VALIDACION.md`
si cambias los valores esperados. Para cambiar el intervalo, actualiza también
los intervalos de los modelos constante y negativo. Ajusta los símbolos
dimensionales en `domain/units.py` o en la configuración si introduces nuevas
unidades.

Los nombres de integrantes y las referencias también se editan en
`PROBLEM.contributors` y `PROBLEM.references`. No es necesario modificar las
escenas para cambiar los datos del problema o los créditos.

Para una descripción detallada del flujo entre dominio, aplicación,
configuración, presentación y renderizado, consulta
`FUNCIONAMIENTO_APLICACION.txt`.

## VS Code

Abre la carpeta raíz del repositorio; `.vscode/settings.json` selecciona el
intérprete `.venv`. Para renderizar, abre `Ctrl+Shift+P` → **Tasks: Run Task** y
elige **Grupo 14: render all (low)** o **Grupo 14: render all (high)**. También
puedes usar desde la terminal los comandos individuales de arriba. No ejecutes
los archivos de escena directamente con **Run Code**: Manim debe importarlos y
renderizarlos con `python -m manim`.
