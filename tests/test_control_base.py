from unittest.mock import patch


from src.controladores.control_base import ControlBase


def test_control_base_registro_log():
    control = ControlBase()

    with patch(
        "src.controladores.control_base.registrar_actividad",
    ) as mock_registrar_actividad:
        control._registrar_log(
            "usuario_demo",
            "ACCION_PRUEBA",
        )

    mock_registrar_actividad.assert_called_once_with(
        "usuario_demo",
        "ACCION_PRUEBA",
        "",
    )


def test_control_base_registro_log_con_detalle():
    control = ControlBase()

    with patch(
        "src.controladores.control_base.registrar_actividad",
    ) as mock_registrar_actividad:
        control._registrar_log(
            "usuario_demo",
            "ACCION_PRUEBA",
            detalle="META: Bajar de peso",
        )

    mock_registrar_actividad.assert_called_once_with(
        "usuario_demo",
        "ACCION_PRUEBA",
        "META: Bajar de peso",
    )


def test_control_base_usa_sistema_si_usuario_es_none():
    control = ControlBase()

    with patch(
        "src.controladores.control_base.registrar_actividad",
    ) as mock_registrar_actividad:
        control._registrar_log(
            None,
            "ACCION_SISTEMA",
        )

    mock_registrar_actividad.assert_called_once_with(
        "SISTEMA",
        "ACCION_SISTEMA",
        "",
    )


def test_control_base_registra_actividad_externa():
    control = ControlBase()

    with patch(
        "src.controladores.control_base.registrar_actividad",
    ) as mock_registrar_actividad:
        control._registrar_log(
            "usuario_demo",
            "ACCION_PRUEBA",
            detalle="Detalle adicional",
        )

    mock_registrar_actividad.assert_called_once_with(
        "usuario_demo",
        "ACCION_PRUEBA",
        "Detalle adicional",
    )


def test_control_base_envia_detalle_vacio_a_logger():
    control = ControlBase()

    with patch(
        "src.controladores.control_base.registrar_actividad",
    ) as mock_registrar_actividad:
        control._registrar_log(
            "usuario_demo",
            "ACCION_SIN_DETALLE",
        )

    mock_registrar_actividad.assert_called_once_with(
        "usuario_demo",
        "ACCION_SIN_DETALLE",
        "",
    )


def test_control_base_alias_registrar_auditoria():
    control = ControlBase()

    with patch.object(
        control,
        "_registrar_log",
    ) as mock_registrar_log:
        control._registrar_auditoria(
            "admin",
            "ACCION_AUDITORIA",
            detalle="Prueba de alias",
        )

    mock_registrar_log.assert_called_once_with(
        "admin",
        "ACCION_AUDITORIA",
        "Prueba de alias",
    )


def test_control_base_no_interrumpe_si_falla_logger_externo():
    control = ControlBase()

    with patch(
        "src.controladores.control_base.registrar_actividad",
        side_effect=RuntimeError(
            "Error de logger externo",
        ),
    ), patch(
        "logging.Logger.warning",
    ) as mock_warning:
        control._registrar_log(
            "usuario_demo",
            "ACCION_CON_ERROR",
        )

    mock_warning.assert_called_once()

    mensaje = mock_warning.call_args.args[0]

    assert "No se pudo registrar la auditoría" in mensaje
    assert "Error de logger externo" in mensaje