@echo off
REM ────────────────────────────────────────────────────────────────
REM Genera documentacion HTML del proyecto usando pdoc
REM Asegúrate de tener pdoc instalado: pip install pdoc
REM ────────────────────────────────────────────────────────────────

SETLOCAL
SET PYTHONPATH=.

echo Generando documentación con pdoc...
pdoc -o docs controladores modelos utilidades vistas

IF %ERRORLEVEL% NEQ 0 (
    echo Hubo un error al generar la documentación.
    pause
    EXIT /B 1
)

echo Documentación generada correctamente en la carpeta "docs".
start docs\index.html
ENDLOCAL
