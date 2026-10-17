"""Renderiza las nueve escenas en el orden narrativo del guion.

Ejemplo:
    ``python scripts/render_all.py --quality l`` renderiza en calidad baja.
"""

from __future__ import annotations

import argparse
import os
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


def render_all(quality: str) -> None:
    """Ejecuta Manim para cada escena en el orden configurado.

    Parámetros:
        quality: Calidad Manim ``l`` (baja) o ``h`` (alta).

    Retorno:
        Ninguno; lanza ``CalledProcessError`` si falla un render.

    Ejemplo:
        ``render_all("l")`` crea los videos de ensayo de todas las escenas.
    """
    environment = os.environ.copy()
    miktex_bin = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64"
    if miktex_bin.is_dir():
        environment["PATH"] = f"{miktex_bin}{os.pathsep}{environment.get('PATH', '')}"
    for scene_file, scene_name in SCENES:
        command = [
            sys.executable,
            "-m",
            "manim",
            f"-q{quality}",
            str(ROOT / scene_file),
            scene_name,
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
    arguments = parser.parse_args()
    require_valid_results(
        PROBLEM.rate,
        PROBLEM.partitions,
        PROBLEM.constant_rate_model,
        PROBLEM.negative_rate,
        PROBLEM.initial_file_size,
        EXPECTED_RESULTS,
    )
    render_all(arguments.quality)


if __name__ == "__main__":
    main()
