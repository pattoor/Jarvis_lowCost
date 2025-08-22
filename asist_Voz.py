# -*- coding: utf-8 -*-
import speech_recognition as sr     #Para capturar y convertir voz a texto
import pyttsx3      #Para texto a voz (funciona offline)
import threading    #Para ejecutar en segundo plano
import time
import psutil       #Para monitorear recursos del sistema
import subprocess   #Para ejecutar comandos del sistema
import os           #Para operaciones del sistema de archivos
import webbrowser
from datetime import datetime   #Para comandos de fecha/hora
import json
import logging

class VoiceAssistant:
    def __init__(self, wake_word="asistente", language="es-ES"):
        self.wake_word = wake_word.lower()
        self.language = language
        self.is_listening = True
        self.is_active = False
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('assistant.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Inicializar reconocimiento de voz
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Configurar texto a voz
        self.tts_engine = pyttsx3.init()
        voices = self.tts_engine.getProperty('voices')
        
        # Buscar voz en español
        for voice in voices:
            if 'spanish' in voice.name.lower() or 'es' in voice.id.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
        
        self.tts_engine.setProperty('rate', 180)
        self.tts_engine.setProperty('volume', 0.8)
        
        # Ajustar micrófono
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
        self.logger.info(f"Asistente inicializado. Palabra clave: '{self.wake_word}'")
        self.speak_and_show("Asistente de voz activado y listo")

    def play_beep(self, frequency=800, duration=200):
        """Reproduce un pitido para indicar que está escuchando"""
        try:
            import winsound
            winsound.Beep(frequency, duration)
        except:
            # Si falla winsound, usar print como alternativa
            print("🔔 *BEEP*")
    
    def speak_and_show(self, text, show_text=None):
        """Convierte texto a voz Y lo muestra en pantalla"""
        display_text = show_text if show_text else text
        print(f"🔊 Asistente dice: {display_text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen(self, timeout=1, phrase_time_limit=5):
        """Escucha audio del micrófono"""
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                
            # Reconocer voz
            text = self.recognizer.recognize_google(audio, language=self.language)
            return text.lower()
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            self.logger.error(f"Error en el servicio de reconocimiento: {e}")
            return None

    def get_system_info(self):
        """Obtiene información del sistema"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        info = {
            'cpu': f"{cpu_percent}%",
            'memoria': f"{memory.percent}%",
            'disco': f"{disk.percent}%",
            'memoria_disponible': f"{memory.available / (1024**3):.1f} GB"
        }
        return info

    def interpret_with_ollama(self, text):
        """Interpreta comando natural con Ollama (local y gratis)"""
        try:
            import ollama
            
            prompt = f"""Eres un asistente que interpreta comandos de voz en español. 
            
COMANDOS DISPONIBLES:
- recursos: consultar CPU, memoria, disco
- hora: obtener hora actual  
- fecha: obtener fecha actual
- abrir_navegador: abrir Chrome/browser
- calculadora: abrir calculadora
- bloc_notas: abrir notepad
- explorador: abrir explorador de archivos
- buscar_youtube: buscar en YouTube
- buscar_google: buscar en Google
- dormir: pausar asistente
- apagar: cerrar asistente
- pregunta: responder pregunta general

INSTRUCCIONES:
1. Si es un comando de acción, devuelve SOLO el comando (ej: "recursos")
2. Si es una pregunta general, devuelve "pregunta: [respuesta breve]"
3. Si quiere buscar algo, devuelve "buscar_google: [término]" o "buscar_youtube: [término]"

Comando del usuario: "{text}"

Respuesta:"""
            
            response = ollama.chat(
                model='llama3.2:1b',
                messages=[{'role': 'user', 'content': prompt}]
            )
            return response['message']['content'].strip()
        except Exception as e:
            self.logger.error(f"Error con Ollama: {e}")
            # Fallback a interpretación básica
            return self.interpret_basic(text)
    
    def interpret_basic(self, text):
        """Interpretación básica sin IA"""
        command = text.lower()
        
        # Mapeo de frases naturales
        if any(word in command for word in ['recursos', 'sistema', 'cpu', 'memoria', 'computadora', 'pc']):
            return 'recursos'
        elif any(word in command for word in ['hora', 'tiempo']):
            return 'hora'
        elif any(word in command for word in ['fecha', 'día']):
            return 'fecha'
        elif any(word in command for word in ['navegador', 'internet', 'chrome', 'browser']):
            return 'abrir_navegador'
        elif any(word in command for word in ['calculadora', 'calcular', 'cuentas']):
            return 'calculadora'
        elif any(word in command for word in ['notas', 'escribir', 'notepad']):
            return 'bloc_notas'
        elif any(word in command for word in ['archivos', 'carpetas', 'explorador']):
            return 'explorador'
        elif 'youtube' in command:
            search_term = command.replace('youtube', '').replace('buscar', '').strip()
            return f'buscar_youtube: {search_term}'
        elif any(word in command for word in ['buscar', 'busca', 'google']):
            search_term = command.replace('buscar', '').replace('busca', '').replace('google', '').strip()
            return f'buscar_google: {search_term}'
        elif any(word in command for word in ['dormir', 'descansar', 'pausa']):
            return 'dormir'
        elif any(word in command for word in ['apagar', 'salir', 'cerrar']):
            return 'apagar'
        else:
            return f'pregunta: {command}'

    def execute_command(self, command_text):
        """Ejecuta comandos basados en el texto reconocido"""
        # Intentar interpretar con Ollama primero
        interpreted = self.interpret_with_ollama(command_text)
        
        try:
            # Si es una pregunta general
            if interpreted.startswith('pregunta:'):
                question = interpreted.replace('pregunta:', '').strip()
                try:
                    import ollama
                    response = ollama.chat(
                        model='llama3.2:1b',
                        messages=[{'role': 'user', 'content': f'Responde brevemente en español: {question}'}]
                    )
                    answer = response['message']['content'].strip()
                    self.speak_and_show(answer)
                    return f"❓ Pregunta respondida: {answer}"
                except:
                    response = "No puedo responder esa pregunta en este momento"
                    self.speak_and_show(response)
                    return f"❓ {response}"
            
            # Si es búsqueda en YouTube
            elif interpreted.startswith('buscar_youtube:'):
                search_term = interpreted.replace('buscar_youtube:', '').strip()
                if search_term:
                    webbrowser.open(f'https://www.youtube.com/results?search_query={search_term.replace(" ", "+")}')
                    response = f"Buscando {search_term} en YouTube"
                    self.speak_and_show(response)
                    return f"✅ Búsqueda en YouTube: {search_term}"
                
            # Si es búsqueda en Google  
            elif interpreted.startswith('buscar_google:'):
                search_term = interpreted.replace('buscar_google:', '').strip()
                if search_term:
                    webbrowser.open(f'https://www.google.com/search?q={search_term.replace(" ", "+")}')
                    response = f"Buscando {search_term} en Google"
                    self.speak_and_show(response)
                    return f"✅ Búsqueda en Google: {search_term}"
            
            # Comandos normales
            command = interpreted.lower()
            
            # Comandos de información del sistema
            if "recursos" in command or "sistema" in command:
                info = self.get_system_info()
                response = f"Tu sistema está funcionando con CPU al {info['cpu']}, memoria al {info['memoria']}, y disco al {info['disco']}"
                self.speak_and_show(response, f"✅ Sistema: CPU {info['cpu']}, Memoria {info['memoria']}, Disco {info['disco']}")
                return f"✅ Información del sistema comunicada"
            
            elif "hora" in command or "tiempo" in command:
                now = datetime.now()
                time_str = now.strftime("%H:%M")
                response = f"Son las {time_str}"
                self.speak_and_show(response)
                return f"✅ Hora actual comunicada: {time_str}"
            
            elif "fecha" in command:
                now = datetime.now()
                date_str = now.strftime("%d de %B de %Y")
                response = f"Hoy es {date_str}"
                self.speak_and_show(response)
                return f"✅ Fecha actual comunicada: {date_str}"
            
            # Comandos de aplicaciones
            elif "abrir navegador" in command or "abrir chrome" in command or command == "abrir_navegador":
                webbrowser.open('https://www.google.com')
                response = "He abierto el navegador para ti"
                self.speak_and_show(response)
                return "✅ Navegador abierto y confirmado"
            
            elif "bloc de notas" in command or "notepad" in command or command == "bloc_notas":
                subprocess.Popen(['notepad.exe'])
                response = "He abierto el bloc de notas"
                self.speak_and_show(response)
                return "✅ Bloc de notas abierto y confirmado"
            
            elif "calculadora" in command or command == "calculadora":
                subprocess.Popen(['calc.exe'])
                response = "He abierto la calculadora para ti"
                self.speak_and_show(response)
                return "✅ Calculadora abierta y confirmada"
            
            elif "explorador" in command or "archivos" in command or command == "explorador":
                subprocess.Popen(['explorer.exe'])
                response = "He abierto el explorador de archivos"
                self.speak_and_show(response)
                return "✅ Explorador abierto y confirmado"
            
            # Comandos de búsqueda (fallback si no se detectó antes)
            elif "buscar" in command:
                search_term = command.replace("buscar", "").strip()
                if search_term:
                    webbrowser.open(f'https://www.google.com/search?q={search_term}')
                    response = f"Buscando {search_term}"
                    self.speak_and_show(response)
                    return f"✅ Búsqueda realizada: {search_term}"
                else:
                    response = "¿Qué quieres buscar?"
                    self.speak_and_show(response)
                    return "❓ Esperando término de búsqueda"
            
            # Comando para dormir/pausar
            elif "dormir" in command or "descansar" in command or command == "dormir":
                response = "Entrando en modo de espera. Dí mi palabra clave para activarme"
                self.speak_and_show(response)
                self.is_active = False
                return "😴 Asistente en modo de espera"
            
            # Comando para apagar
            elif "apagar asistente" in command or "salir" in command or command == "apagar":
                response = "Apagando asistente. ¡Hasta luego!"
                self.speak_and_show(response)
                self.is_listening = False
                return "🔴 Asistente apagado"
            
            else:
                response = "No entendí ese comando. Prueba con recursos, hora, fecha, abrir navegador, calculadora o buscar algo"
                self.speak_and_show(response)
                return f"❓ Comando no reconocido: {command}"
                
        except Exception as e:
            error_msg = f"Error ejecutando comando: {str(e)}"
            self.logger.error(error_msg)
            self.speak_and_show("Hubo un error ejecutando el comando")
            return f"❌ {error_msg}"

    def monitor_resources(self):
        """Monitorea recursos del sistema en segundo plano"""
        while self.is_listening:
            try:
                info = self.get_system_info()
                
                # Alertar si los recursos están muy altos
                cpu_high = float(info['cpu'].replace('%', '')) > 90
                memory_high = float(info['memoria'].replace('%', '')) > 90
                
                if cpu_high or memory_high:
                    alert = f"⚠️ Recursos altos - CPU: {info['cpu']}, Memoria: {info['memoria']}"
                    print(alert)
                    self.logger.warning(alert)
                
                time.sleep(30)  # Revisar cada 30 segundos
                
            except Exception as e:
                self.logger.error(f"Error monitoreando recursos: {e}")
                time.sleep(60)

    def main_loop(self):
        """Bucle principal del asistente"""
        print(f"🎤 Asistente escuchando... Di '{self.wake_word}' para activar")
        print("📊 Monitoreo de recursos activo")
        print("🔧 Comandos disponibles: recursos, hora, fecha, abrir navegador, calculadora, bloc de notas, explorador, buscar [término], dormir, apagar asistente")
        
        # Iniciar monitoreo de recursos en hilo separado
        resource_thread = threading.Thread(target=self.monitor_resources, daemon=True)
        resource_thread.start()
        
        while self.is_listening:
            try:
                # Si no está activo, solo escuchar la palabra clave
                if not self.is_active:
                    audio_text = self.listen(timeout=1)
                    if audio_text and self.wake_word in audio_text:
                        print(f"👂 Escuché: {audio_text}")
                        print(f"🟢 Palabra clave detectada: '{self.wake_word}'")
                        self.is_active = True
                        self.speak_and_show("¿En qué puedo ayudarte?")
                        continue
                
                # Si está activo, procesar comandos
                else:
                    print("🎤 Esperando comando...")
                    self.play_beep()  # Pitido cuando empieza a escuchar
                    print("🔊 *BEEP* - Escuchando...")
                    
                    audio_text = self.listen(timeout=5, phrase_time_limit=8)
                    
                    if audio_text:
                        print(f"👂 Escuché: '{audio_text}'")
                        result = self.execute_command(audio_text)
                        print(f"📝 Resultado: {result}")
                        # Extraer y decir el mensaje limpio
                        if ": " in result:
                            message = result.split(": ", 1)[1]
                            self.speak_and_show(message)
                        
                        # Volver a modo de espera después de ejecutar comando
                        if self.is_listening:  # Solo si no se apagó
                            time.sleep(1)
                            self.is_active = False
                            print(f"😴 Volviendo a modo de espera. Di '{self.wake_word}' para activar")
                    else:
                        # Si no escucha nada por 5 segundos, volver a modo de espera
                        self.is_active = False
                        print(f"😴 Timeout. Volviendo a modo de espera. Di '{self.wake_word}' para activar")
                
            except KeyboardInterrupt:
                print("\n🛑 Interrumpido por usuario")
                self.is_listening = False
                break
            except Exception as e:
                self.logger.error(f"Error en bucle principal: {e}")
                continue

    def run(self):
        """Inicia el asistente"""
        try:
            self.main_loop()
        except Exception as e:
            self.logger.error(f"Error fatal: {e}")
        finally:
            print("👋 Asistente desconectado")

if __name__ == "__main__":
    # Configuración del asistente
    assistant = VoiceAssistant(
        wake_word="jarvis",  # Cambia por la palabra que prefieras
        language="es-ES"       # Idioma español de España
    )
    
    # Ejecutar asistente
    assistant.run()