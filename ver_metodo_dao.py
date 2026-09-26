import inspect

from src.persistencia.cliente_dao import ClienteDAO


print(
    inspect.getsource(
        ClienteDAO.restablecer_contrasenia
    )
)