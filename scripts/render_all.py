"""Renderiza escenas del video en el orden narrativo del guion.

Ejemplo:
    ``python scripts/render_all.py --scene Scene2ConstantRate --quality l``
    renderiza una escena en calidad baja.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from group14_manim.application.validate_results import require_valid_results
from group14_manim.config.problem import EXPECTED_RESULTS, PROBLEM

SCENES = (
    ("group14_manim/presentation/scenes/scene_1_hook.py", "Scene1Hook"),
    ("group14_manim/presentation/scenes/scene_2_constant_rate.py", "Scene2ConstantRate"),
    ("group14_manim/presentation/scenes/scene_3_variable_rate.py", "Scene3VariableRate"),
    ("group14_manim/presentation/scenes/scene_4_small_contribution.py", "Scene4SmallContribution"),
    ("group14_manim/presentation/scenes/scene_5_riemann_to_integral.py", "Scene5RiemannToIntegral"),
    ("group14_manim/presentation/scenes/scene_6_exact_integral.py", "Scene6ExactIntegral"),
    ("group14_manim/presentation/scenes/scene_7_units.py", "Scene7Units"),
    ("group14_manim/presentation/scenes/scene_8_sign_and_closing.py", "Scene8SignAndClosing"),
    ("group14_manim/presentation/scenes/scene_9_credits.py", "Scene9Credits"),
)
SCENE_NAMES = tuple(scene_name for _, scene_name in SCENES)


def render_all(quality: str, scene_name: str | None = None, preview: bool = False) -> None:
    """Ejecuta Manim para todas las escenas o una escena seleccionada.

    Parámetros:
        quality: Calidad Manim ``l`` (baja) o ``h`` (alta).
        scene_name: Nombre de una escena; ``None`` renderiza todas en orden.
        preview: Abre el video al terminar cada escena seleccionada.

    Retorno:
        Ninguno; lanza ``CalledProcessError`` si falla un render.

    Ejemplo:
        ``render_all("l", "Scene2ConstantRate")`` renderiza una escena de ensayo.
    """
    environment = os.environ.copy()
    miktex_bin = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64"
    if miktex_bin.is_dir():
        environment["PATH"] = f"{miktex_bin}{os.pathsep}{environment.get('PATH', '')}"
    missing_executables = [
        executable
        for executable in ("latex", "dvisvgm")
        if shutil.which(executable, path=environment.get("PATH")) is None
    ]
    if missing_executables:
        missing = ", ".join(missing_executables)
        raise RuntimeError(
            f"No se encontraron {missing}. Instala MiKTeX y verifica que "
            "latex y dvisvgm estén disponibles en PATH."
        )

    scenes = SCENES if scene_name is None else tuple(
        scene for scene in SCENES if scene[1] == scene_name
    )
    for scene_file, current_scene_name in scenes:
        command = [
            sys.executable,
            "-m",
            "manim",
            f"-{'p' if preview else ''}q{quality}",
            str(ROOT / scene_file),
            current_scene_name,
        ]
        subprocess.run(command, cwd=ROOT, env=environment, check=True)


def main() -> None:
    """Procesa la opción de calidad y renderiza todas las escenas.

    Retorno:
        Ninguno; termina con error si Manim no puede crear algún video.

    Ejemplo:
        ``python scripts/render_all.py --quality h`` selecciona alta calidad.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--quality",
        choices=("l", "h"),
        default="l",
        help="Calidad Manim: l para ensayo; h para render final.",
    )
    parser.add_argument(
        "--scene",
        choices=SCENE_NAMES,
        help="Renderiza solo la escena indicada; por defecto renderiza las nueve.",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Abre el video al terminar; útil al renderizar una escena individual.",
    )
    arguments = parser.parse_args()
    require_valid_results(
        PROBLEM.rate,
        PROBLEM.partitions,
        PROBLEM.constant_rate_model,
        PROBLEM.negative_rate,
        PROBLEM.initial_file_size,
        EXPECTED_RESULTS,
    )
    try:
        render_all(arguments.quality, arguments.scene, arguments.preview)
    except RuntimeError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
