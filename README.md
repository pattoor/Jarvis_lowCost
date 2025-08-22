# 🎤 Asistente de Voz Inteligente

Un asistente de voz personal desarrollado en Python que funciona completamente offline con capacidades de procesamiento de lenguaje natural usando Ollama.

## 📝 Descripción

Este asistente de voz está diseñado para ejecutar comandos del sistema, responder preguntas y realizar búsquedas web mediante comandos de voz en español. Utiliza reconocimiento de voz para capturar comandos y síntesis de voz para responder al usuario, creando una experiencia de interacción natural y fluida.

## ⚡ Funcionalidades Principales

### 🔊 Comandos de Voz Disponibles
- **Información del sistema**: Consultar CPU, memoria y uso de disco
- **Fecha y hora**: Obtener fecha y hora actual
- **Aplicaciones**: Abrir navegador, calculadora, bloc de notas, explorador de archivos
- **Búsquedas**: Buscar en Google y YouTube
- **Control del asistente**: Activar/pausar/apagar con comandos de voz
- **Preguntas generales**: Respuestas usando IA local (Ollama)

### 🎯 Comandos Específicos
```
"recursos" o "sistema" - Muestra estado del CPU, memoria y disco
"hora" - Informa la hora actual
"fecha" - Informa la fecha actual
"abrir navegador" - Abre Chrome/navegador por defecto
"calculadora" - Abre la calculadora del sistema
"bloc de notas" - Abre Notepad
"explorador" - Abre el explorador de archivos
"buscar [término]" - Busca en Google
"buscar en youtube [término]" - Busca en YouTube
"dormir" - Pone el asistente en modo espera
"apagar asistente" - Cierra la aplicación
```

## 🛠️ Características Técnicas

### ✨ Características Funcionales
- **Activación por palabra clave**: Responde solo cuando escucha "asistente"
- **Procesamiento offline**: Funciona sin conexión a internet (excepto búsquedas web)
- **Monitoreo de recursos**: Supervisa el sistema en segundo plano
- **Feedback auditivo**: Pitidos de confirmación y respuestas por voz
- **Logging completo**: Registra todas las actividades en `assistant.log`
- **Interpretación inteligente**: Entiende comandos en lenguaje natural
- **Fallback seguro**: Sistema de respaldo si falla la IA

### 🔧 Tecnologías Utilizadas

#### **Speech Recognition (`speech_recognition`)**
- **Propósito**: Convierte audio del micrófono en texto
- **Uso**: Captura comandos de voz del usuario usando Google Speech API

#### **pyttsx3**
- **Propósito**: Síntesis de voz (texto a voz)
- **Uso**: Convierte respuestas del asistente en audio para comunicación oral
- **Ventaja**: Funciona completamente offline

#### **Ollama + Llama 3.2**
- **Propósito**: Procesamiento de lenguaje natural local
- **Uso**: Interpreta comandos naturales y responde preguntas generales
- **Modelo**: `llama3.2:1b` (modelo ligero para respuestas rápidas)

#### **Threading**
- **Propósito**: Ejecución en paralelo
- **Uso**: Monitoreo de recursos del sistema en segundo plano sin bloquear la interfaz

#### **psutil**
- **Propósito**: Monitoreo de recursos del sistema
- **Uso**: Obtiene información de CPU, memoria y disco en tiempo real

#### **subprocess**
- **Propósito**: Ejecución de comandos del sistema
- **Uso**: Abre aplicaciones del sistema (calculadora, notepad, explorer)

#### **webbrowser**
- **Propósito**: Interacción con navegadores web
- **Uso**: Abre búsquedas en Google y YouTube automáticamente

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/tuusuario/voice-assistant.git
cd voice-assistant
```

### 2. Crear entorno virtual
```bash
python -m venv venv
```

### 3. Instalar dependencias de Python
```bash
pip install -r requirements.txt
```

### 4. Configurar Ollama
1. Instalar Ollama desde: https://ollama.ai/download
2. Descargar el modelo:
```bash
ollama pull llama3.2:1b
```

### 5. Ejecutar el Asistente
```bash
python voice_assistant.py
```

## 📋 Uso

1. **Iniciar**: Ejecuta el script y el asistente entrará en modo de escucha
2. **Activar**: Di "asistente" para activar el reconocimiento de comandos
3. **Comandar**: Escucha el pitido y da tu comando
4. **Esperar**: El asistente procesará y responderá por voz

## 📊 Características Adicionales

- **Registro de actividad**: Todas las interacciones se guardan en `assistant.log`
- **Alertas de recursos**: Notifica cuando CPU o memoria superan 90%
- **Configuración de voz**: Selecciona automáticamente voces en español
- **Timeouts inteligentes**: Vuelve a modo espera si no detecta comandos

## 🔧 Personalización

- **Palabra clave**: Cambiar `wake_word="asistente"` en la línea de configuración
- **Idioma**: Modificar `language="es-ES"` para otros dialectos del español
- **Velocidad de voz**: Ajustar `rate=180` en la configuración TTS
- **Volumen**: Modificar `volume=0.8` para ajustar el volumen de respuesta

## ⚠️ Limitaciones

- Requiere micrófono funcional
- Conexión a internet necesaria para reconocimiento de voz y búsquedas web
- Optimizado para Windows (comandos de sistema específicos)
- Ollama debe estar instalado y funcionando para funcionalidades de IA

---
**Desarrollado con ❤️ para automatización personal y productividad**


<!-- # 🎤 Asistente de Voz Local con IA

Un asistente de voz completamente local que funciona offline usando Ollama para interpretación natural y respuestas inteligentes.

## ✨ Funcionalidades

### 🎯 **Activación por Voz**
- Palabra clave personalizable (por defecto: "asistente")
- Funciona en segundo plano
- Monitoreo de recursos automático

### 🤖 **IA Local con Ollama**
- Interpretación natural de comandos
- Respuestas a preguntas generales
- Completamente offline y privado
- Fallback a reglas básicas si falla la IA

### 📊 **Comandos Disponibles**

#### **Información del Sistema:**
- `"recursos"` / `"cómo está mi PC"` → Estado CPU, memoria, disco
- `"hora"` / `"qué hora es"` → Hora actual
- `"fecha"` / `"qué día es"` → Fecha actual

#### **Aplicaciones:**
- `"abrir navegador"` / `"abre internet"` → Chrome/navegador por defecto
- `"calculadora"` / `"quiero hacer cuentas"` → Calculadora de Windows
- `"bloc de notas"` / `"necesito escribir"` → Notepad
- `"explorador"` / `"ver archivos"` → Explorador de archivos

#### **Búsquedas:**
- `"buscar [término] en Google"` → Búsqueda en Google
- `"buscar [término] en YouTube"` → Búsqueda en YouTube
- `"busca información sobre Python"` → Búsqueda automática

#### **Preguntas Generales:**
- `"¿Qué es Python?"` → Respuesta de IA
- `"¿Cuál es la capital de Francia?"` → Respuesta inteligente
- `"Explícame qué es la fotosíntesis"` → Explicación detallada

#### **Control:**
- `"dormir"` / `"descansa"` → Modo de espera
- `"apagar asistente"` / `"salir"` → Cerrar programa

### 🔧 **Funciones Especiales**

#### **Monitoreo de Recursos**
- Revisa CPU, memoria y disco cada 30 segundos
- Alerta automática si los recursos superan el 90%
- Log detallado en `assistant.log`

#### **Respuestas Confirmadas**
- El asistente confirma cada acción realizada
- Feedback vocal de lo que ejecutó
- Mensajes claros en consola con emojis

#### **Manejo de Errores Robusto**
- Continúa funcionando aunque falle la IA
- Fallback a interpretación básica
- Logging completo de errores

## 📋 Dependencias

### **Librerías Python:**
```
SpeechRecognition==3.14.3  # Reconocimiento de voz
pyttsx3==2.99              # Texto a voz offline  
pyaudio==0.2.14            # Acceso al micrófono
psutil==7.0.0              # Monitoreo de recursos
ollama                     # IA local
```

### **Dependencias del Sistema:**
- **Ollama** - Runtime de IA local
- **Modelo llama3.2:1b** - Modelo de lenguaje (1GB)

## 🚀 Instalación

### **Método 1: Script Automático**

#### Windows:
```bash
# Ejecutar install.bat
install.bat
```

#### Linux/Mac:
```bash
# Ejecutar install.sh
chmod +x install.sh
./install.sh
```

### **Método 2: Instalación Manual**

#### **1. Clonar repositorio:**
```bash
git clone <tu-repositorio>
cd asistente-voz-local
```

#### **2. Crear entorno virtual:**
```bash
python -m venv env

# Windows
env\Scripts\activate

# Linux/Mac  
source env/bin/activate
```

#### **3. Instalar dependencias Python:**
```bash
pip install -r requirements.txt
```

#### **4. Instalar Ollama:**

**Windows:**
1. Ve a [ollama.com](https://ollama.com/)
2. Descarga `ollama-windows-amd64.exe`
3. Ejecuta el instalador
4. Reinicia la terminal

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Mac:**
```bash
# Descargar desde https://ollama.com/
# O usando Homebrew:
brew install ollama
```

#### **5. Descargar modelo de IA:**
```bash
ollama pull llama3.2:1b
```

#### **6. Verificar instalación:**
```bash
ollama list  # Debe mostrar llama3.2:1b
```

## ⚙️ Configuración

### **Cambiar Palabra de Activación:**
En `asist_Voz.py`, línea 202:
```python
assistant = VoiceAssistant(
    wake_word="tu_palabra_aqui",  # Ej: "jarvis", "computer"
    language="es-ES"
)
```

### **Cambiar Idioma:**
```python
assistant = VoiceAssistant(
    wake_word="asistente",
    language="en-US"  # Para inglés
)
```

## 🏃‍♂️ Uso

### **1. Ejecutar:**
```bash
python asist_Voz.py
```

### **2. Activar:**
Di tu palabra clave (por defecto: "asistente")

### **3. Comandar:**
Habla normalmente:
- "¿Cómo está mi computadora?"
- "Abre la calculadora"
- "Busca gatos en YouTube"
- "¿Qué es machine learning?"

### **4. Control:**
- **Ctrl+C** para salir manualmente
- Di "apagar asistente" para salir por voz

## 📁 Estructura del Proyecto

```
asistente-voz-local/
├── asist_Voz.py          # Código principal
├── requirements.txt       # Dependencias Python
├── install.bat           # Instalador Windows
├── install.sh            # Instalador Linux/Mac
├── README.md             # Este archivo
├── .env                  # Variables de entorno (crear si es necesario)
├── .gitignore            # Archivos ignorados por Git
└── assistant.log         # Log del asistente (se crea automáticamente)
```

## 🔧 Resolución de Problemas

### **Error: "No module named 'speech_recognition'"**
- Asegúrate de que el entorno virtual esté activado
- Reinstala dependencias: `pip install -r requirements.txt`

### **Error: "Ollama not found"**
- Verifica instalación: `ollama --version`
- Reinstala Ollama desde [ollama.com](https://ollama.com/)
- Reinicia la terminal

### **Error con PyAudio en Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

### **Modelo no encontrado:**
```bash
ollama pull llama3.2:1b
ollama list  # Verificar que esté descargado
```

### **Problema de micrófono:**
- Verifica permisos de micrófono en Windows
- Prueba con diferentes dispositivos de audio

## 📊 Recursos del Sistema

### **Uso de Memoria:**
- **Programa base:** ~50-100MB
- **Modelo Ollama:** ~1-2GB RAM cuando activo
- **Total estimado:** ~2GB RAM

### **Uso de CPU:**
- **En espera:** <1% CPU
- **Procesando voz:** 5-15% CPU
- **Usando IA:** 20-60% CPU (momentáneo)

### **Almacenamiento:**
- **Código:** ~50KB
- **Dependencias:** ~200MB
- **Ollama + modelo:** ~1.5GB

## 🔒 Privacidad

- ✅ **Completamente offline** después de la instalación
- ✅ **Sin envío de datos** a servidores externos
- ✅ **Procesamiento local** de voz y IA
- ✅ **Logs solo locales** en tu máquina

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m 'Agregar nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Crea un Pull Request

## 📝 Licencia

MIT License - Ver archivo LICENSE para detalles

## 📧 Soporte

Si tienes problemas:
1. Revisa la sección de **Resolución de Problemas**
2. Verifica el archivo `assistant.log`
3. Crea un Issue en el repositorio

---

**¿Necesitas ayuda?** Abre un Issue con:
- Sistema operativo
- Versión de Python
- Mensaje de error completo
- Contenido de `assistant.log`

"""
-->
