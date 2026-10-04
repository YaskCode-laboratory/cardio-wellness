import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / ".env"
BATCH_FILE = ROOT / "tests" / "run_all_tests.bat"
TEST_DATABASE = "cardio_wellness_prueba_limpieza"


def cargar_env(path: Path) -> dict[str, str]:
    valores: dict[str, str] = {}

    for linea in path.read_text(encoding="utf-8-sig").splitlines():
        linea = linea.strip()

        if not linea or linea.startswith("#") or "=" not in linea:
            continue

        clave, valor = linea.split("=", 1)
        clave = clave.strip()
        valor = valor.strip()

        if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in {"'", '"'}:
            valor = valor[1:-1]

        valores[clave] = valor

    return valores


def obtener_ruta_venv(root: Path) -> Path | None:
    candidatos = [
        root / ".venv" / "Scripts",
        root / ".venv" / "bin",
    ]

    for candidato in candidatos:
        if candidato.exists():
            return candidato

    return None


def main() -> int:
    if not ENV_FILE.exists():
        print(f"[ERROR] No se encontro el archivo: {ENV_FILE}")
        return 1

    if not BATCH_FILE.exists():
        print(f"[ERROR] No se encontro el archivo: {BATCH_FILE}")
        return 1

    entorno = os.environ.copy()
    entorno.update(cargar_env(ENV_FILE))

    entorno["DB_NAME"] = TEST_DATABASE
    entorno["CARDIO_TEST_ENV_LOADED"] = "1"
    entorno["PYTHONUTF8"] = "1"
    entorno["PYTHONIOENCODING"] = "utf-8"

    requeridas = ["DB_HOST", "DB_PORT", "DB_USER", "DB_PASSWORD"]

    faltantes = [
        variable
        for variable in requeridas
        if not entorno.get(variable)
    ]

    if faltantes:
        print(
            "[ERROR] Faltan variables requeridas en .env: "
            + ", ".join(faltantes)
        )
        return 1

    ruta_venv = obtener_ruta_venv(ROOT)

    if ruta_venv:
        entorno["PATH"] = str(ruta_venv) + os.pathsep + entorno.get("PATH", "")

    print("===========================================================================")
    print("CARDIO-WELLNESS - INICIADOR DE SUITE")
    print("===========================================================================")
    print(f"Base de pruebas forzada: {entorno['DB_NAME']}")
    print(f"Host PostgreSQL: {entorno['DB_HOST']}:{entorno['DB_PORT']}")
    print("DB_PASSWORD cargada desde .env: SI")
    print("===========================================================================")
    print()

    proceso = subprocess.run(
        ["cmd.exe", "/c", str(BATCH_FILE)],
        cwd=ROOT,
        env=entorno,
    )

    return proceso.returncode


if __name__ == "__main__":
    raise SystemExit(main())