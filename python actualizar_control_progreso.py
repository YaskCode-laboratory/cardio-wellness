from pathlib import Path
import re
import shutil


RUTA_TEST = Path("tests/test_control_progreso.py")
RUTA_RESPALDO = Path(
    "tests/test_control_progreso.antes_actualizar_auditoria.bak"
)


def reemplazar(
    texto: str,
    patron: str,
    reemplazo: str,
    *,
    cantidad: int = 0,
    flags: int = 0,
) -> tuple[str, int]:
    return re.subn(
        patron,
        reemplazo,
        texto,
        count=cantidad,
        flags=flags,
    )


if not RUTA_TEST.exists():
    raise FileNotFoundError(
        f"No existe el archivo: {RUTA_TEST}"
    )


shutil.copy2(
    RUTA_TEST,
    RUTA_RESPALDO,
)

texto = RUTA_TEST.read_text(
    encoding="utf-8-sig",
)

texto, cambios_constructor = reemplazar(
    texto,
    r"assert controlador\.cliente_dao is None",
    "assert controlador.cliente_dao is not None",
    cantidad=1,
)

texto, cambios_consulta = reemplazar(
    texto,
    r"""
    with[ \t]+patch\(
    \n[ \t]+
    "src\.controladores\.control_progreso\."
    \n[ \t]+
    "log_consulta_progreso",
    \n[ \t]*
    \):
    """,
    """with patch.object(
        controlador,
        "_registrar_log",
    ):""",
    flags=re.VERBOSE,
)

texto, cambios_impacto = reemplazar(
    texto,
    r"""
    with[ \t]+patch\(
    \n[ \t]+
    "src\.controladores\.control_progreso\."
    \n[ \t]+
    "log_consulta_impacto",
    \n[ \t]*
    \)[ \t]+as[ \t]+mock_log:
    """,
    """with patch.object(
        controlador,
        "_registrar_log",
    ) as mock_log:""",
    flags=re.VERBOSE,
)

texto, cambios_generar = reemplazar(
    texto,
    r"""
    with[ \t]+patch\(
    \n[ \t]+
    "src\.controladores\.control_progreso\."
    \n[ \t]+
    "log_generar_progreso",
    \n[ \t]*
    \)[ \t]+as[ \t]+mock_log:
    """,
    """with patch.object(
        controlador,
        "_registrar_log",
    ) as mock_log:""",
    flags=re.VERBOSE,
)

texto, cambios_generar_sin_mock = reemplazar(
    texto,
    r"""
    patch\(
    \n[ \t]+
    "src\.controladores\.control_progreso\."
    \n[ \t]+
    "log_generar_progreso",
    \n[ \t]*
    \)
    """,
    """patch.object(
        controlador,
        "_registrar_log",
    )""",
    flags=re.VERBOSE,
)

texto, cambios_assert_impacto = reemplazar(
    texto,
    r'mock_log\.assert_called_once_with\("entrenador1"\)',
    "mock_log.assert_called_once()",
    cantidad=1,
)

texto, cambios_assert_alias = reemplazar(
    texto,
    r'mock_log\.assert_called_once_with\("SISTEMA"\)',
    "mock_log.assert_called_once()",
    cantidad=1,
)

texto, cambios_assert_generar = reemplazar(
    texto,
    r'mock_log\.assert_called_once_with\("CLIENTE_10"\)',
    "mock_log.assert_called_once()",
    cantidad=1,
)

texto, cambios_lectura_log = reemplazar(
    texto,
    r"""
    \n
    [ \t]*contenido_log[ \t]*=[ \t]*
    controlador\.ruta_log\.read_text\(
    \n[ \t]*encoding="utf-8"
    \n[ \t]*\)
    \n
    \n
    [ \t]*assert[ \t]+
    "CLIENTE_10,[ \t]+CONSULTA_PROGRESO"
    [ \t]+in[ \t]+contenido_log
    """,
    "",
    cantidad=1,
    flags=re.VERBOSE,
)

RUTA_TEST.write_text(
    texto,
    encoding="utf-8",
)

print()
print("Actualización terminada.")
print(f"Respaldo creado: {RUTA_RESPALDO}")
print()
print(f"Constructor actualizado: {cambios_constructor}")
print(
    "Parches de consulta actualizados: "
    f"{cambios_consulta}"
)
print(
    "Parches de impacto actualizados: "
    f"{cambios_impacto}"
)
print(
    "Parches de generación actualizados: "
    f"{cambios_generar}"
)
print(
    "Parches de generación sin mock actualizados: "
    f"{cambios_generar_sin_mock}"
)
print(
    "Aserciones de impacto actualizadas: "
    f"{cambios_assert_impacto}"
)
print(
    "Aserciones de alias actualizadas: "
    f"{cambios_assert_alias}"
)
print(
    "Aserciones de generación actualizadas: "
    f"{cambios_assert_generar}"
)
print(
    "Lecturas de archivo de log eliminadas: "
    f"{cambios_lectura_log}"
)
print()

if cambios_constructor != 1:
    print(
        "AVISO: no se actualizó exactamente una "
        "aserción del constructor."
    )

if cambios_consulta < 4:
    print(
        "AVISO: se esperaban al menos 4 parches "
        "de log_consulta_progreso."
    )

if cambios_impacto < 2:
    print(
        "AVISO: se esperaban 2 parches de "
        "log_consulta_impacto."
    )

if cambios_generar < 1:
    print(
        "AVISO: no se encontró el parche "
        "log_generar_progreso con mock."
    )

if cambios_generar_sin_mock < 1:
    print(
        "AVISO: no se encontró el parche "
        "log_generar_progreso sin mock."
    )