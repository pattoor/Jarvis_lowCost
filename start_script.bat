@echo off
chcp 65001 >nul
color 0B
echo.
echo ===============================================
echo        INICIANDO JARVIS VOICE ASSISTANT
echo ===============================================
echo.

:: Verificar si el entorno virtual existe
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Entorno virtual no encontrado.
    echo Ejecuta setup.bat primero para instalar todo.
    pause
    exit /b 1
)

:: Activar entorno virtual
echo [OK] Activando entorno virtual...
call venv\Scripts\activate.bat

:: Verificar modelo Vosk
if not exist "vosk-model-small-es-0.42" (
    echo [ERROR] Modelo Vosk no encontrado.
    echo Ejecuta setup.bat para descargarlo.
    pause
    exit /b 1
)

:: Verificar que Ollama este corriendo
echo [OK] Verificando Ollama...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo [ADVERTENCIA] Ollama no disponible. Iniciando sin IA...
    echo El asistente funcionara con comandos basicos solamente.
    timeout /t 3 /nobreak >nul
)

echo [OK] Iniciando Jarvis...
echo.
echo ===============================================
echo   Di "JARVIS" seguido de tu comando
echo   Ejemplo: "Jarvis, que hora es"
echo ===============================================
echo.

:: Ejecutar el asistente
python asist_Voz_v2.py

echo.
echo Jarvis desconectado. Presiona cualquier tecla para salir.
pause >nul