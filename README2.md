# Cardio Wellness

## Activar el entorno virtual

Desde la raíz del proyecto, ejecuta:

```powershell
.\.venv\Scripts\Activate.ps1
```

Cuando se active correctamente, PowerShell mostrará:

```text
(.venv)
```

---

## Ejecutar la aplicación principal

```powershell
python main.py
```

Si el archivo principal está dentro de `src`, ejecuta:

```powershell
python .\src\main.py
```

---

## Crear una cuenta de administrador

Ejecuta el archivo de creación de administrador:

```powershell
python .\src\crear_administrador.py
```

> Si tu archivo tiene otro nombre, reemplaza `crear_administrador.py` por el nombre real del archivo encargado de registrar administradores.

---

## Ejecutar todas las pruebas

Desde la raíz del proyecto:

```powershell
.\tests\run_all_tests.bat
```

Si PowerShell no permite ejecutar el archivo directamente:

```powershell
cmd /c .\tests\run_all_tests.bat
```