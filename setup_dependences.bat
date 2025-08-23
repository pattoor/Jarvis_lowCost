@echo off
chcp 65001 >nul
color 0A
echo.
echo ===============================================
echo    JARVIS VOICE ASSISTANT - INSTALACION
echo ===============================================
echo.

:: Verificar si Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado. Instala Python desde https://python.org
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

:: Crear entorno virtual
echo [PASO 1/6] Creando entorno virtual...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] No se pudo crear el entorno virtual
    pause
    exit /b 1
)

:: Activar entorno virtual
echo [PASO 2/6] Activando entorno virtual...
call venv\Scripts\activate.bat

:: Instalar dependencias Python
echo [PASO 3/6] Instalando dependencias Python...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Fallo instalando dependencias Python
    pause
    exit /b 1
)

:: Descargar modelo Vosk
echo [PASO 4/6] Descargando modelo Vosk (40MB)...
if not exist "vosk-model-small-es-0.42" (
    echo Descargando modelo de reconocimiento de voz...
    powershell -Command "Invoke-WebRequest -Uri 'https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip' -OutFile 'vosk-model.zip'"
    if errorlevel 1 (
        echo [ERROR] No se pudo descargar el modelo Vosk
        pause
        exit /b 1
    )
    
    echo Extrayendo modelo...
    powershell -Command "Expand-Archive -Path 'vosk-model.zip' -DestinationPath '.'"
    del vosk-model.zip
    echo [OK] Modelo Vosk instalado
) else (
    echo [OK] Modelo Vosk ya existe
)

:: Descargar e instalar Ollama
echo [PASO 5/6] Descargando e instalando Ollama...
if not exist "%USERPROFILE%\AppData\Local\Programs\Ollama\ollama.exe" (
    echo Descargando Ollama...
    powershell -Command "Invoke-WebRequest -Uri 'https://ollama.com/download/windows' -OutFile 'ollama-installer.exe'"
    
    echo Instalando Ollama...
    ollama-installer.exe /S
    timeout /t 10 /nobreak >nul
    del ollama-installer.exe
    
    echo Esperando a que Ollama se inicie...
    timeout /t 5 /nobreak >nul
) else (
    echo [OK] Ollama ya instalado
)

:: Descargar modelo de IA
echo [PASO 6/6] Descargando modelo de IA Llama 3.2...
echo Esto puede tomar varios minutos...
ollama pull llama3.2:1b
if errorlevel 1 (
    echo [ADVERTENCIA] No se pudo descargar el modelo de IA
    echo El asistente funcionara sin capacidades de IA avanzada
)

echo.
echo ===============================================
echo           INSTALACION COMPLETADA
echo ===============================================
echo.
echo Para usar el asistente:
echo 1. Ejecuta: start_jarvis.bat
echo 2. O manualmente: venv\Scripts\activate ^&^& python asist_Voz_v2.py
echo.
echo Requisitos del sistema:
echo - Microfono funcionando
echo - Parlantes/audifonos
echo - Conexion a internet (solo para instalacion)
echo.
pause