# VAPA - ASISTENTE DE VOZ LOCAL
### librerias usadas

speech_recognition - Para capturar y convertir voz a texto
pyttsx3 - Para texto a voz (funciona offline)
pyaudio - Para acceso al micrófono
threading - Para ejecutar en segundo plano
psutil - Para monitorear recursos del sistema
datetime - Para comandos de fecha/hora
subprocess - Para ejecutar comandos del sistema
os - Para operaciones del sistema de archivos

### FUNCIONAMIENTO

Palabra clave: "asistente" (puedes cambiarla en línea 202)
Modo de espera: Escucha constantemente la palabra clave
Modo activo: Después de decir "asistente", escucha tu comando
Ejecución: Procesa el comando y vuelve a modo de espera

### Comandos disponibles:

📊 "recursos/sistema" - Muestra CPU, memoria y disco
⏰ "hora" - Dice la hora actual
📅 "fecha" - Dice la fecha actual
🌐 "abrir navegador" - Abre Chrome/navegador por defecto
📝 "bloc de notas" - Abre Notepad
🔢 "calculadora" - Abre calculadora
📁 "explorador/archivos" - Abre explorador de archivos
🔍 "buscar [término]" - Busca en Google
😴 "dormir" - Pone en modo de espera
🔴 "apagar asistente" - Cierra el programa

### Caracteristicas Tecnicas

✅ Ejecuta en segundo plano
✅ Monitoreo de recursos cada 30 segundos
✅ Logging completo (archivo assistant.log)
✅ Manejo de errores robusto
✅ Multithreading para no bloquear
✅ Escalable - fácil agregar nuevos comandos
✅ Offline TTS con pyttsx3

----------------------------------------------------
## Instalación:
1. Clonar repo: `git clone tu-repo`
2. Crear entorno virtual: `python -m venv env`
3. Activar: `env\Scripts\activate`
4. Instalar deps: `pip install -r requirements.txt`
5. **Instalar Ollama:** https://ollama.com/
6. **Descargar modelo:** `ollama pull llama3.2:1b`
7. Ejecutar: `python asist_Voz.py`