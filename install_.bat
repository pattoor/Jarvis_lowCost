REM install.bat - Script de instalación para Windows
@echo off
echo ===============================================
echo    INSTALADOR ASISTENTE DE VOZ LOCAL
echo ===============================================
echo.

echo [1/6] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado. Instala Python desde python.org
    pause
    exit /b 1
)
echo ✅ Python encontrado

echo.
echo [2/6] Creando entorno virtual...
if exist env (
    echo ⚠️  El entorno virtual ya existe, usando el existente
) else (
    python -m venv env
    echo ✅ Entorno virtual creado
)

echo.
echo [3/6] Activando entorno virtual...
call env\Scripts\activate
echo ✅ Entorno virtual activado

echo.
echo [4/6] Instalando dependencias Python...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Error instalando dependencias. Verifica requirements.txt
    pause
    exit /b 1
)
echo ✅ Dependencias Python instaladas

echo.
echo [5/6] Verificando Ollama...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ⚠️  OLLAMA NO ENCONTRADO
    echo.
    echo PASOS PARA INSTALAR OLLAMA:
    echo 1. Ve a: https://ollama.com/
    echo 2. Descarga: ollama-windows-amd64.exe
    echo 3. Ejecuta el instalador
    echo 4. Reinicia esta terminal
    echo 5. Ejecuta de nuevo: install.bat
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Ollama encontrado
)

echo.
echo [6/6] Descargando modelo de IA...
ollama list | find "llama3.2:1b" >nul
if errorlevel 1 (
    echo Descargando llama3.2:1b (esto puede tomar varios minutos)...
    ollama pull llama3.2:1b
    if errorlevel 1 (
        echo ❌ Error descargando modelo
        pause
        exit /b 1
    )
    echo ✅ Modelo descargado
) else (
    echo ✅ Modelo ya existe
)

echo.
echo ===============================================
echo        ✅ INSTALACIÓN COMPLETADA
echo ===============================================
echo.
echo PARA USAR EL ASISTENTE:
echo 1. Activa el entorno: env\Scripts\activate
echo 2. Ejecuta: python asist_Voz.py
echo 3. Di "asistente" para activar
echo.
echo COMANDOS DE EJEMPLO:
echo - "recursos" / "cómo está mi PC"
echo - "abrir calculadora"
echo - "buscar gatos en YouTube"
echo - "qué es Python"
echo.
pause

REM ===================================================
REM install.sh - Script de instalación para Linux/Mac
REM ===================================================

#!/bin/bash

# Hacer ejecutable con: chmod +x install.sh

echo "==============================================="
echo "    INSTALADOR ASISTENTE DE VOZ LOCAL"
echo "==============================================="
echo

echo "[1/6] Verificando Python..."
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ Python no encontrado. Instala Python 3.8+"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi
echo "✅ Python encontrado: $PYTHON_CMD"

echo
echo "[2/6] Creando entorno virtual..."
if [ -d "env" ]; then
    echo "⚠️  El entorno virtual ya existe, usando el existente"
else
    $PYTHON_CMD -m venv env
    echo "✅ Entorno virtual creado"
fi

echo
echo "[3/6] Activando entorno virtual..."
source env/bin/activate
echo "✅ Entorno virtual activado"

echo
echo "[4/6] Instalando dependencias del sistema..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detectado: Linux"
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y portaudio19-dev python3-pyaudio
    elif command -v yum &> /dev/null; then
        sudo yum install -y portaudio-devel
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detectado: macOS"
    if command -v brew &> /dev/null; then
        brew install portaudio
    else
        echo "⚠️  Se recomienda instalar Homebrew para dependencias"
    fi
fi

echo
echo "[5/6] Instalando dependencias Python..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Error instalando dependencias. Verifica requirements.txt"
    exit 1
fi
echo "✅ Dependencias Python instaladas"

echo
echo "[6/6] Verificando Ollama..."
if ! command -v ollama &> /dev/null; then
    echo
    echo "⚠️  OLLAMA NO ENCONTRADO"
    echo
    echo "INSTALANDO OLLAMA..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -fsSL https://ollama.com/install.sh | sh
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            brew install ollama
        else
            echo "Descarga manualmente desde: https://ollama.com/"
            exit 1
        fi
    fi
    echo "✅ Ollama instalado"
else
    echo "✅ Ollama encontrado"
fi

echo
echo "[7/7] Descargando modelo de IA..."
if ollama list | grep -q "llama3.2:1b"; then
    echo "✅ Modelo ya existe"
else
    echo "Descargando llama3.2:1b (esto puede tomar varios minutos)..."
    ollama pull llama3.2:1b
    if [ $? -ne 0 ]; then
        echo "❌ Error descargando modelo"
        exit 1
    fi
    echo "✅ Modelo descargado"
fi

echo
echo "==============================================="
echo "        ✅ INSTALACIÓN COMPLETADA"
echo "==============================================="
echo
echo "PARA USAR EL ASISTENTE:"
echo "1. Activa el entorno: source env/bin/activate"
echo "2. Ejecuta: python asist_Voz.py"
echo "3. Di 'asistente' para activar"
echo
echo "COMANDOS DE EJEMPLO:"
echo "- 'recursos' / 'cómo está mi PC'"
echo "- 'abrir calculadora'"
echo "- 'buscar gatos en YouTube'"
echo "- 'qué es Python'"
echo