from getpass import getpass

from src.persistencia.usuario_dao import UsuarioDAO
from src.servicios.gestor_seguridad import GestorSeguridad


CORREO = "pedro123@gmail.com"

dao = UsuarioDAO()

usuario = dao.buscar_por_correo(CORREO)

if usuario is None:
    print("No se encontró el usuario.")
else:
    print(f"ID: {usuario.id_usuario}")
    print(f"Correo: {usuario.correo_electronico}")
    print(
        f"Hash actual: "
        f"{usuario.contrasenia_hash[:7]}"
    )

    clave_vieja = getpass(
        "Escribe la clave VIEJA real: "
    )

    clave_nueva = getpass(
        "Escribe la clave NUEVA real: "
    )

    vieja_correcta = (
        GestorSeguridad.verificar_contrasenia(
            clave_vieja,
            usuario.contrasenia_hash,
        )
    )

    nueva_correcta = (
        GestorSeguridad.verificar_contrasenia(
            clave_nueva,
            usuario.contrasenia_hash,
        )
    )

    print()
    print(
        "Clave vieja correcta:",
        vieja_correcta,
    )
    print(
        "Clave nueva correcta:",
        nueva_correcta,
    )