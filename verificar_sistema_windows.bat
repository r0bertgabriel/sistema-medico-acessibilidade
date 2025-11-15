@echo off
REM ============================================================================
REM Script de Verificación del Sistema
REM Verifica todas las dependencias antes de la instalación
REM Incluye verificación de FFmpeg (opcional)
REM ============================================================================

title Verificacion de Sistema

echo.
echo ============================================================================
echo   VERIFICACION DE DEPENDENCIAS DEL SISTEMA MEDICO
echo ============================================================================
echo.

REM ======================================
REM Verificar Python
REM ======================================
echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] FALLO: Python no encontrado
    echo     Descargue Python desde: https://python.org/downloads
    echo     Asegurese de marcar "Add Python to PATH" durante la instalacion
    set PYTHON_OK=0
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo [✓] OK: Python %PYTHON_VERSION% encontrado
    set PYTHON_OK=1
)
echo.

REM ======================================
REM Verificar pip
REM ======================================
echo [2/5] Verificando pip (gestor de paquetes)...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [X] FALLO: pip no encontrado
    echo     Reinstale Python con pip incluido
    set PIP_OK=0
) else (
    for /f "tokens=2" %%i in ('python -m pip --version 2^>^&1') do set PIP_VERSION=%%i
    echo [✓] OK: pip %PIP_VERSION% encontrado
    set PIP_OK=1
)
echo.

REM ======================================
REM Verificar requirements.txt
REM ======================================
echo [3/5] Verificando archivo de requisitos...
if not exist requirements.txt (
    echo [X] FALLO: requirements.txt no encontrado
    echo     Asegurese de estar en el directorio correcto del proyecto
    set REQ_OK=0
) else (
    echo [✓] OK: requirements.txt encontrado
    set REQ_OK=1
)
echo.

REM ======================================
REM Verificar dependencias Python
REM ======================================
echo [4/5] Verificando dependencias instaladas...

set DEPS_OK=1

echo Verificando Flask...
python -c "import flask; print(flask.__version__)" >nul 2>&1
if errorlevel 1 (
    echo [X] Flask no instalado
    set DEPS_OK=0
) else (
    for /f %%i in ('python -c "import flask; print(flask.__version__)"') do echo [✓] Flask %%i
)

echo Verificando gTTS...
python -c "import gtts" >nul 2>&1
if errorlevel 1 (
    echo [X] gTTS no instalado
    set DEPS_OK=0
) else (
    echo [✓] gTTS instalado
)

echo Verificando pygame...
python -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo [X] pygame no instalado
    set DEPS_OK=0
) else (
    echo [✓] pygame instalado
)

echo Verificando OpenAI...
python -c "import openai" >nul 2>&1
if errorlevel 1 (
    echo [X] OpenAI no instalado
    set DEPS_OK=0
) else (
    echo [✓] OpenAI instalado
)

echo Verificando Pillow...
python -c "import PIL" >nul 2>&1
if errorlevel 1 (
    echo [X] Pillow no instalado
    set DEPS_OK=0
) else (
    echo [✓] Pillow instalado
)

echo Verificando matplotlib...
python -c "import matplotlib" >nul 2>&1
if errorlevel 1 (
    echo [X] matplotlib no instalado
    set DEPS_OK=0
) else (
    echo [✓] matplotlib instalado
)

echo.

REM ======================================
REM Verificar FFmpeg (opcional)
REM ======================================
echo [5/6] Verificando FFmpeg (OPCIONAL - para aceleracion de audio)...

ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo [!] FFmpeg no encontrado
    echo     Sistema funcionara sin aceleracion de audio
    echo.
    echo     Para instalar FFmpeg:
    echo     1. Via Chocolatey: choco install ffmpeg
    echo     2. Manual: Ver INSTALACAO_FFMPEG_WINDOWS.md
    echo     3. Download: https://www.gyan.dev/ffmpeg/builds/
    set FFMPEG_OK=0
) else (
    for /f "tokens=3" %%i in ('ffmpeg -version 2^>^&1 ^| findstr /C:"ffmpeg version"') do set FFMPEG_VERSION=%%i
    echo [✓] FFmpeg %FFMPEG_VERSION% encontrado
    set FFMPEG_OK=1
)

echo.

REM ======================================
REM Verificar estructura del proyecto
REM ======================================
echo [6/6] Verificando estructura del proyecto...

set STRUCT_OK=1

if not exist app.py (
    echo [X] app.py no encontrado
    set STRUCT_OK=0
) else (
    echo [✓] app.py encontrado
)

if not exist config.py (
    echo [X] config.py no encontrado
    set STRUCT_OK=0
) else (
    echo [✓] config.py encontrado
)

if not exist templates\ (
    echo [X] Directorio templates/ no encontrado
    set STRUCT_OK=0
) else (
    echo [✓] Directorio templates/ encontrado
)

if not exist static\ (
    echo [X] Directorio static/ no encontrado
    set STRUCT_OK=0
) else (
    echo [✓] Directorio static/ encontrado
)

echo.
echo ============================================================================
echo   RESUMEN DE VERIFICACION
echo ============================================================================
echo.

set ALL_OK=1

if %PYTHON_OK%==0 (
    echo [X] Python: FALTA
    set ALL_OK=0
) else (
    echo [✓] Python: OK
)

if %PIP_OK%==0 (
    echo [X] pip: FALTA
    set ALL_OK=0
) else (
    echo [✓] pip: OK
)

if %REQ_OK%==0 (
    echo [X] requirements.txt: FALTA
    set ALL_OK=0
) else (
    echo [✓] requirements.txt: OK
)

if %DEPS_OK%==0 (
    echo [!] Dependencias: FALTAN ALGUNAS
    set ALL_OK=0
) else (
    echo [✓] Dependencias: OK
)

if %STRUCT_OK%==0 (
    echo [X] Estructura del proyecto: INCOMPLETA
    set ALL_OK=0
) else (
    echo [✓] Estructura del proyecto: OK
)

if %FFMPEG_OK%==0 (
    echo [!] FFmpeg: NO INSTALADO (OPCIONAL)
    echo     Audio sin aceleracion
) else (
    echo [✓] FFmpeg: OK (audio acelerado)
)

echo.
echo ============================================================================

if %ALL_OK%==0 (
    echo.
    echo   RESULTADO: SISTEMA NO ESTA LISTO
    echo.
    if %DEPS_OK%==0 (
        echo   ACCION REQUERIDA: Instale las dependencias faltantes
        echo.
        echo   Ejecute: pip install -r requirements.txt
        echo.
    )
    echo ============================================================================
    pause
    exit /b 1
) else (
    echo.
    echo   RESULTADO: SISTEMA LISTO PARA USAR
    echo.
    echo   Puede ejecutar iniciar_sistema.bat para iniciar el servidor
    echo.
    echo ============================================================================
    pause
    exit /b 0
)
