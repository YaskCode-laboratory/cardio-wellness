@echo off
setlocal EnableExtensions DisableDelayedExpansion

REM ============================================================================
REM CARDIO-WELLNESS - SUITE DE PRUEBAS
REM ============================================================================
REM Si se ejecuta desde una consola nueva, el bootstrap carga .env de forma
REM local, fuerza la base temporal y vuelve a iniciar este archivo.
REM ============================================================================

if not defined CARDIO_TEST_ENV_LOADED (
    python "%~dp0run_all_tests_bootstrap.py"
    exit /b %ERRORLEVEL%
)

chcp 65001 > nul 2>&1
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"

REM Ir a la raiz del proyecto sin importar el directorio de ejecucion.
pushd "%~dp0\.." > nul

if errorlevel 1 (
    echo [ERROR] No fue posible acceder a la raiz del proyecto.
    exit /b 1
)

REM ============================================================================
REM VALIDACION DEL ENTORNO
REM ============================================================================

if not defined DB_PASSWORD (
    echo [ERROR] DB_PASSWORD no esta definida en el entorno.
    echo [ERROR] Revise el archivo .env y el bootstrap.
    popd
    exit /b 1
)

if not defined DB_HOST (
    echo [ERROR] DB_HOST no esta definida.
    popd
    exit /b 1
)

if not defined DB_PORT (
    echo [ERROR] DB_PORT no esta definida.
    popd
    exit /b 1
)

if not defined DB_USER (
    echo [ERROR] DB_USER no esta definida.
    popd
    exit /b 1
)

if not defined DB_NAME (
    echo [ERROR] DB_NAME no esta definida.
    popd
    exit /b 1
)

REM Seguridad: prohibir ejecucion sobre la base principal.
if /I not "%DB_NAME%"=="cardio_wellness_prueba_limpieza" (
    echo [ERROR] La suite no puede ejecutarse contra "%DB_NAME%".
    echo [ERROR] Debe utilizar la base temporal:
    echo [ERROR] cardio_wellness_prueba_limpieza
    popd
    exit /b 1
)

echo ============================================================================
echo CARDIO-WELLNESS - SUITE DE PRUEBAS COMPLETA
echo ============================================================================
echo.
echo Fecha: %date% %time%
echo Base de pruebas: %DB_NAME%@%DB_HOST%:%DB_PORT%
echo.

REM ============================================================================
REM CONTADORES
REM ============================================================================

set /a total_tests=0
set /a tests_exitosos=0

REM ============================================================================
REM LIMPIEZA OPCIONAL DE DATOS
REM ============================================================================
REM Se mantiene desactivada salvo que RUN_CLEANUP sea exactamente 1.
REM No habilitar hasta revisar limpiar_datos_prueba.py.
REM ============================================================================

if /I "%RUN_CLEANUP%"=="1" (
    echo [PREVIO] Limpiando datos de prueba anteriores...
    echo -----------------------------------------------------------------------------
    python tests\integracion\limpiar_datos_prueba.py

    if errorlevel 1 (
        echo [ERROR] Fallo en limpieza de datos de prueba.
        popd
        exit /b 1
    ) else (
        echo [OK] Limpieza de datos de prueba completada.
    )

    echo.
) else (
    echo [PREVIO] Limpieza automatica omitida.
    echo [INFO] RUN_CLEANUP no esta definido como 1.
    echo.
)

REM ============================================================================
REM [1/8] PRUEBAS UNITARIAS E INTEGRACION
REM ============================================================================

echo [1/8] Ejecutando pruebas unitarias e integracion...
echo -----------------------------------------------------------------------------
python -X utf8 -m pytest tests\ -v --durations=10 --tb=short

if errorlevel 1 (
    echo [ERROR] Fallo en pruebas unitarias e integracion.
) else (
    echo [OK] Pruebas unitarias e integracion completadas.
    set /a tests_exitosos+=1
)

set /a total_tests+=1
echo.

REM ============================================================================
REM [2/8] COBERTURA
REM ============================================================================

echo [2/8] Generando reporte de cobertura...
echo -----------------------------------------------------------------------------
python -X utf8 -m pytest tests\ --cov=src --cov-report=html --cov-report=term-missing

if errorlevel 1 (
    echo [ERROR] Fallo en generacion de cobertura.
) else (
    echo [OK] Reporte de cobertura generado.
    set /a tests_exitosos+=1
)

set /a total_tests+=1
echo.

REM ============================================================================
REM [3/8] PRUEBAS AUTOMATIZADAS DE SEGURIDAD
REM ============================================================================

echo [3/8] Ejecutando pruebas automatizadas de seguridad...
echo -----------------------------------------------------------------------------
python -X utf8 tests\test_seguridad.py

if errorlevel 1 (
    echo [ERROR] Fallo en pruebas automatizadas de seguridad.
) else (
    echo [OK] Pruebas automatizadas de seguridad completadas.
    set /a tests_exitosos+=1
)

set /a total_tests+=1
echo.

REM ============================================================================
REM [4/8] SIMULACION AUTOMATIZADA DE FLUJOS
REM ============================================================================

echo [4/8] Simulacion automatizada de flujos con 100 cuentas...
echo -----------------------------------------------------------------------------
python -X utf8 tests\test_usabilidad_masivo.py

if errorlevel 1 (
    echo [ERROR] Fallo en simulacion automatizada de flujos.
) else (
    echo [OK] Simulacion automatizada de flujos completada.
    set /a tests_exitosos+=1
)

set /a total_tests+=1
echo.

REM ============================================================================
REM [5/8] STRESS TEST POSTGRESQL
REM ============================================================================

echo [5/8] Stress test PostgreSQL (30 usuarios, 40 segundos, 100 clientes)...
echo -----------------------------------------------------------------------------

python -X utf8 tests\stress_test_postgresql.py ^
  --host "%DB_HOST%" ^
  --port "%DB_PORT%" ^
  --db "%DB_NAME%" ^
  --user "%DB_USER%" ^
  --usuarios 30 ^
  --duracion 40 ^
  --clientes 100

if errorlevel 1 (
    echo [ERROR] Fallo en stress test PostgreSQL.
) else (
    echo [OK] Stress test PostgreSQL completado.
    set /a tests_exitosos+=1
)

set /a total_tests+=1
echo.

REM ============================================================================
REM [6/8] PRUEBA HISTORICA SQLITE
REM ============================================================================
REM SQLite no representa la arquitectura final basada en PostgreSQL.
REM ============================================================================

echo [6/8] Prueba historica SQLite (no representa PostgreSQL)...
echo -----------------------------------------------------------------------------
python -X utf8 tests\stress_test_sqlite.py --usuarios 20 --duracion 30

if errorlevel 1 (
    echo [ERROR] Fallo en prueba historica SQLite.
) else (
    echo [OK] Prueba historica SQLite completada.
    set /a tests_exitosos+=1
)

set /a total_tests+=1
echo.

REM ============================================================================
REM [7/8] PRUEBAS DE INTEGRACION
REM ============================================================================

echo [7/8] Ejecutando pruebas de integracion completa...
echo -----------------------------------------------------------------------------
python -X utf8 tests\integracion\test_integracion_completa.py

if errorlevel 1 (
    echo [ERROR] Fallo en pruebas de integracion.
) else (
    echo [OK] Pruebas de integracion completadas.
    set /a tests_exitosos+=1
)

set /a total_tests+=1
echo.

REM ============================================================================
REM [8/8] VERIFICACION DE LOGS
REM ============================================================================

echo [8/8] Verificando existencia de logs...
echo -----------------------------------------------------------------------------

if exist "logs\LOG_CARDIO.txt" (
    echo [OK] Archivo de log encontrado: logs\LOG_CARDIO.txt
    echo.
    echo Ultimas 15 entradas del log:
    echo -----------------------------------------------------------------------------
    powershell -NoProfile -Command "Get-Content 'logs\LOG_CARDIO.txt' -Tail 15"
    echo -----------------------------------------------------------------------------
    set /a tests_exitosos+=1
) else (
    echo [ERROR] No se encontro logs\LOG_CARDIO.txt
)

set /a total_tests+=1
echo.

REM ============================================================================
REM OPTIMIZACION DE RENDIMIENTO
REM ============================================================================
REM No se ejecuta automaticamente porque puede realizar cambios persistentes
REM sobre PostgreSQL. Debe revisarse y ejecutarse por separado.
REM ============================================================================

echo [INFO] Optimizacion de rendimiento omitida de la suite automatica.
echo [INFO] Revisar tests\optimizar_rendimiento.py antes de ejecutarlo manualmente.
echo.

REM ============================================================================
REM RESUMEN
REM ============================================================================

echo ============================================================================
echo RESUMEN: %tests_exitosos%/%total_tests% pruebas completadas exitosamente
echo ============================================================================
echo.
echo Resultados y evidencia:
echo   - Cobertura HTML: htmlcov\index.html
echo   - Documentacion de pruebas: tests\RUN_TESTS.md
echo   - Logs: logs\LOG_CARDIO.txt
echo   - Stress PostgreSQL: docs\resultado_stress_postgresql_2026-10-03.txt
echo.
echo Nota:
echo   - La simulacion automatizada con 100 cuentas no sustituye una prueba
echo     de usabilidad con participantes humanos.
echo   - SQLite es una prueba historica; PostgreSQL es el motor principal.
echo.

popd
pause
exit /b 0