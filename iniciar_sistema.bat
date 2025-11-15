@echo off
REM ============================================================================
REM Sistema Médico de Análisis de ECG y Hemogramas
REM Launcher para Windows
REM ============================================================================

title Sistema Médico - Inicializando...

echo.
echo ============================================================================
echo   SISTEMA MEDICO DE ANALISIS - ACCESIBILIDAD
echo ============================================================================
echo.
echo Verificando dependencias...
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado en el sistema
    echo Por favor, instale Python 3.8 o superior desde https://python.org
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

REM Verificar se Flask está instalado
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Flask no encontrado. Instalando dependencias...
    echo.
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Fallo al instalar dependencias
        pause
        exit /b 1
    )
    echo.
    echo [OK] Dependencias instaladas con exito
) else (
    echo [OK] Dependencias verificadas
)

echo.
echo ============================================================================
echo   INICIANDO SERVIDOR...
echo ============================================================================
echo.
echo El sistema estara disponible en:
echo.
echo    http://localhost:5000
echo.
echo Para acceder desde otros dispositivos en la red, use:
echo    http://[IP-de-esta-computadora]:5000
echo.
echo Presione Ctrl+C para detener el servidor
echo.
echo ============================================================================
echo.

REM Definir variáveis de ambiente (opcional)
REM set OPENAI_API_KEY=tu_clave_api_aqui
REM set DEBUG=True

REM Iniciar aplicação Flask
python app.py

REM Se o servidor parar, aguardar antes de fechar
echo.
echo.
echo ============================================================================
echo   SERVIDOR DETENIDO
echo ============================================================================
pause
