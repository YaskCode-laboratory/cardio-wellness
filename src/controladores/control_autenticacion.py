from typing import Optional

from src.controladores.control_base import ControlBase
from src.modelos.usuario import Usuario
from src.persistencia.usuario_dao import UsuarioDAO
from src.servicios.gestor_seguridad import GestorSeguridad



class ControlAutenticacion(ControlBase):
    """
    Controlador para autenticación de usuarios.
    """

    def __init__(
        self,
        usuario_dao: Optional[UsuarioDAO] = None,
        ruta_log: str = "logs/LOG_CARDIO.txt",
    ) -> None:
        super().__init__(ruta_log=ruta_log)

        self.usuario_dao = (
            usuario_dao
            if usuario_dao is not None
            else UsuarioDAO()
        )

        self.usuario_actual: Optional[Usuario] = None

    @staticmethod
    def _normalizar_correo(
        correo_electronico: str,
    ) -> str:
        """
        Limpia y normaliza un correo.
        """
        return correo_electronico.strip().lower()

    def _validar_entradas_login(
        self,
        correo_electronico: str,
        contrasenia_plana: str,
    ) -> None:
        """
        Valida las credenciales del login.
        """
        if (
            not isinstance(correo_electronico, str)
            or not correo_electronico.strip()
        ):
            raise ValueError(
                "El correo electrónico es obligatorio."
            )

        if (
            not isinstance(contrasenia_plana, str)
            or not contrasenia_plana
        ):
            raise ValueError(
                "La contraseña no puede estar vacía."
            )

    def iniciar_sesion(
        self,
        correo_electronico: str,
        contrasenia_plana: str,
    ) -> Optional[Usuario]:
        """
        Inicia la sesión de un usuario.
        """
        self._validar_entradas_login(
            correo_electronico,
            contrasenia_plana,
        )

        correo_limpio = self._normalizar_correo(
            correo_electronico
        )

        usuario = self.usuario_dao.iniciar_sesion(
            correo_limpio,
            contrasenia_plana,
        )

        if usuario is None:
            self._registrar_log(
                correo_limpio,
                "LOGIN_FALLIDO",
                "Intento de inicio de sesión fallido",
            )

            self.usuario_actual = None
            return None

        self.usuario_actual = usuario

        correo_usuario = getattr(
            usuario,
            "correo_electronico",
            correo_limpio,
        )

        self._registrar_log(
            correo_usuario,
            "LOGIN_EXITOSO",
            "Inicio de sesión exitoso",
        )

        return usuario

    def cerrar_sesion(
        self,
        usuario: Optional[Usuario] = None,
    ) -> bool:
        """
        Cierra la sesión del usuario actual.
        """
        usuario_sesion = (
            usuario
            if usuario is not None
            else self.usuario_actual
        )

        if usuario_sesion is not None:
            correo = getattr(
                usuario_sesion,
                "correo_electronico",
                "USUARIO",
            )

            self._registrar_log(
                correo,
                "LOGOUT",
                "Sesión cerrada",
            )

        self.usuario_actual = None
        return True

    def cerrarSesion(
        self,
        usuario: Optional[Usuario] = None,
    ) -> bool:
        """
        Alias compatible en camelCase.
        """
        return self.cerrar_sesion(usuario)

    def validar_credenciales(
        self,
        correo_electronico: str,
        contrasenia_plana: str,
    ) -> Optional[Usuario]:
        """
        Valida credenciales sin cambiar la sesión actual.
        """
        if (
            not isinstance(correo_electronico, str)
            or not correo_electronico.strip()
        ):
            return None

        if (
            not isinstance(contrasenia_plana, str)
            or not contrasenia_plana
        ):
            return None

        correo_limpio = self._normalizar_correo(
            correo_electronico
        )

        return self.usuario_dao.iniciar_sesion(
            correo_limpio,
            contrasenia_plana,
        )

    def validarCredenciales(
        self,
        correo_electronico: str,
        contrasenia_plana: str,
    ) -> Optional[Usuario]:
        """
        Alias compatible en camelCase.
        """
        return self.validar_credenciales(
            correo_electronico,
            contrasenia_plana,
        )

    def obtener_usuario_actual(
        self,
    ) -> Optional[Usuario]:
        """
        Devuelve el usuario autenticado actualmente.
        """
        return self.usuario_actual

    def esta_autenticado(self) -> bool:
        """
        Indica si existe una sesión activa.
        """
        return self.usuario_actual is not None

    def restablecer_contrasenia_administrador(
        self,
        correo_electronico: str,
        nueva_contrasenia: str,
    ) -> bool:
        """
        Restablece la contraseña de una cuenta de
        administrador.

        Es una operación para la interfaz independiente
        del propietario de la aplicación.
        """
        if (
            not isinstance(
                correo_electronico,
                str,
            )
            or not correo_electronico.strip()
        ):
            raise ValueError(
                "El correo electrónico es obligatorio."
            )

        if (
            not isinstance(
                nueva_contrasenia,
                str,
            )
            or not nueva_contrasenia
        ):
            raise ValueError(
                "La nueva contraseña no puede estar vacía."
            )

        if not GestorSeguridad.validar_fortaleza_contrasena(
            nueva_contrasenia
        ):
            raise ValueError(
                (
                    "La contraseña debe tener al menos "
                    "8 caracteres, una mayúscula, un "
                    "número y un carácter especial."
                )
            )

        correo_limpio = self._normalizar_correo(
            correo_electronico
        )

        actualizado = (
            self.usuario_dao
            .restablecer_contrasenia_administrador(
                correo_limpio,
                nueva_contrasenia,
            )
        )

        if actualizado is not True:
            raise RuntimeError(
                (
                    "No se pudo confirmar el cambio de "
                    "contraseña del administrador."
                )
            )

        self._registrar_log(
            correo_limpio,
            "RESTABLECIMIENTO_CONTRASENIA_ADMIN",
            "Contraseña administrativa restablecida",
        )

        return True

    def listar_administradores(self) -> list:
        """
        Obtiene las cuentas de administrador registradas.

        Solo se utiliza desde la interfaz independiente
        del propietario de la aplicación.
        """
        return self.usuario_dao.listar_administradores()

    def registrar_administrador(
        self,
        nombre: str,
        apellido: str,
        correo_electronico: str,
        contrasenia_plana: str,
        edad: int,
    ) -> Usuario:
        """
        Registra un administrador.
        """
        if (
            not isinstance(nombre, str)
            or not nombre.strip()
        ):
            raise ValueError(
                "El nombre no puede estar vacío."
            )

        if (
            not isinstance(apellido, str)
            or not apellido.strip()
        ):
            raise ValueError(
                "El apellido no puede estar vacío."
            )

        if (
            not isinstance(correo_electronico, str)
            or not correo_electronico.strip()
        ):
            raise ValueError(
                "El correo electrónico es obligatorio."
            )

        if (
            not isinstance(contrasenia_plana, str)
            or not contrasenia_plana
        ):
            raise ValueError(
                "La contraseña no puede estar vacía."
            )

        if (
            not isinstance(edad, int)
            or isinstance(edad, bool)
            or edad <= 0
        ):
            raise ValueError(
                "La edad debe ser un entero mayor "
                "que cero."
            )

        correo_limpio = self._normalizar_correo(
            correo_electronico
        )

        contrasenia_hash = (
            GestorSeguridad.generar_hash(
                contrasenia_plana
            )
        )

        from src.modelos.administrador import Administrador

        administrador = Administrador(
            nombre=nombre.strip(),
            apellido=apellido.strip(),
            correo_electronico=correo_limpio,
            contrasenia_hash=contrasenia_hash,
            edad=edad,
        )

        usuario_guardado = self.usuario_dao.guardar(
            administrador,
            contrasenia_plana,
        )

        if usuario_guardado is not None:
            self._registrar_log(
                correo_limpio,
                "REGISTRO_ADMINISTRADOR",
                "Nuevo administrador registrado",
            )

        return usuario_guardado