import pytest


@pytest.fixture(autouse=True)
def bloquear_cuadros_dialogo(monkeypatch):
    """
    Evita que las pruebas abran cuadros de diálogo reales
    de Tkinter, ya que bloquean la ejecución automática.
    """
    monkeypatch.setattr(
        "src.interfaz.interfaz_base.messagebox.showerror",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(
        "src.interfaz.interfaz_base.messagebox.showinfo",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(
        "src.interfaz.interfaz_base.messagebox.showwarning",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(
        "src.interfaz.interfaz_base.messagebox.askyesno",
        lambda *args, **kwargs: True,
    )
    monkeypatch.setattr(
        "src.interfaz.interfaz_base.messagebox.askokcancel",
        lambda *args, **kwargs: True,
    )