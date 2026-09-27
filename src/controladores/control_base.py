from pathlib import Path
from typing import Optional


from src.utilidades.logger import registrar_actividad


class ControlBase:
    """
    Clase base para todos los controladores del sistema.

    Centraliza el registro de auditoría mediante el módulo
    src.utilidades.logger.
    """

    def __init__(
        self,
        ruta_log: str = "logs/LOG_CARDIO.txt",
    ) -> None:
        """
        Inicializa el controlador base.

        ruta_log se conserva por compatibilidad con los
        controladores actuales, pero la escritura real se
        realiza mediante registrar_actividad().
        """
        self.ruta_log = Path(ruta_log)

    def _registrar_log(
        self,
        usuario: Optional[str],
        accion: str,
        detalle: Optional[str] = None,
    ) -> None:
        """
        Registra una sola actividad de auditoría.

        No escribe directamente en el archivo para evitar
        duplicados. El módulo logger es el único encargado
        de guardar la línea en LOG_CARDIO.txt.
        """
        usuario_str = (
            "SISTEMA"
            if usuario is None
            else str(usuario)
        )

        detalle_str = (
            ""
            if detalle is None
            else str(detalle)
        )

        try:
            registrar_actividad(
                usuario_str,
                accion,
                detalle_str,
            )

        except Exception as error:
            import logging

            logging.getLogger(__name__).warning(
                (
                    "No se pudo registrar la auditoría: "
                    f"{error}"
                )
            )

    def _registrar_auditoria(
        self,
        usuario: Optional[str],
        accion: str,
        detalle: Optional[str] = None,
    ) -> None:
        """
        Alias compatible de _registrar_log.
        """
        self._registrar_log(
            usuario,
            accion,
            detalle,
        )