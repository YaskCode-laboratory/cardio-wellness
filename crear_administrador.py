import tkinter as tk

from src.controladores.control_autenticacion import (
    ControlAutenticacion,
)
from src.interfaz.ventana_registro_administrador import (
    VentanaRegistroAdministrador,
)


def main() -> None:
    """
    Abre la ventana independiente para que el propietario
    cree una cuenta de administrador.
    """
    root = tk.Tk()

    control_autenticacion = ControlAutenticacion()

    VentanaRegistroAdministrador(
        root=root,
        control_autenticacion=control_autenticacion,
    )

    root.mainloop()


if __name__ == "__main__":
    main()