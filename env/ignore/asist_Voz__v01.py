# -*- coding: utf-8 -*-
import speech_recognition as sr     # Captura audio del micrófono
import pyttsx3      # Convierte texto a voz
import threading    # Para ejecutar cosas en paralelo
import time     # Para pausas y delays
import psutil   # Para monitorear CPU/memoria
import logging
from commands import CommandHandler  # Importar los comandos

class VoiceAssistant:
    def __init__(self, wake_word="jarvis", language="es-ES"):
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
        
        # Inicializar manejador de comandos (NUEVO)
        self.command_handler = CommandHandler(self.logger, self.speak_and_show)
            
        self.logger.info(f"Asistente inicializado. Palabra clave: '{self.wake_word}'")
        self.speak_and_show("Jarvis activado y listo")

    def play_beep(self, frequency=800, duration=200):
        """Reproduce un pitido para indicar que está escuchando"""
        try:
            import winsound
            winsound.Beep(frequency, duration)
        except:
            print("BEEP")
    
    def speak_and_show(self, text, show_text=None):
        """Convierte texto a voz Y lo muestra en pantalla"""
        display_text = show_text if show_text else text
        print(f"Jarvis dice: {display_text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen(self, timeout=1, phrase_time_limit=5):
        """Escucha audio del micrófono"""
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                
            text = self.recognizer.recognize_google(audio, language=self.language)
            return text.lower()
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            self.logger.error(f"Error en el servicio de reconocimiento: {e}")
            return None

    def monitor_resources(self):
        """Monitorea recursos del sistema en segundo plano"""
        while self.is_listening:
            try:
                info = self.command_handler.get_system_info()
                
                cpu_high = float(info['cpu'].replace('%', '')) > 90
                memory_high = float(info['memoria'].replace('%', '')) > 90
                
                if cpu_high or memory_high:
                    alert = f"Recursos altos - CPU: {info['cpu']}, Memoria: {info['memoria']}"
                    print(alert)
                    self.logger.warning(alert)
                
                time.sleep(30)
                
            except Exception as e:
                self.logger.error(f"Error monitoreando recursos: {e}")
                time.sleep(60)

    def main_loop(self):
        """Bucle principal del asistente"""
        print(f"Jarvis escuchando... Di '{self.wake_word}' para activar")
        print("Monitoreo de recursos activo")
        print("Comandos: recursos, hora, fecha, abrir navegador, calculadora, bloc de notas, explorador, buscar [término], dormir, apagar")
        
        # Iniciar monitoreo de recursos en hilo separado
        resource_thread = threading.Thread(target=self.monitor_resources, daemon=True)
        resource_thread.start()
        
        while self.is_listening:
            try:
                # Modo de espera - Solo escuchar palabra clave
                if not self.is_active:
                    audio_text = self.listen(timeout=1)
                    if audio_text and self.wake_word in audio_text:
                        print(f"Escuché: {audio_text}")
                        print(f"Palabra clave detectada: '{self.wake_word}'")
                        self.is_active = True
                        self.speak_and_show("¿En qué puedo ayudarte?")
                        continue
                
                # Modo activo - Procesar comandos
                else:
                    print("Esperando comando...")
                    self.play_beep()
                    print("BEEP - Escuchando...")
                    
                    audio_text = self.listen(timeout=5, phrase_time_limit=8)
                    
                    if audio_text:
                        print(f"Escuché: '{audio_text}'")
                        
                        # USAR EL COMMAND_HANDLER PARA EJECUTAR
                        result = self.command_handler.execute_command(audio_text)
                        print(f"Resultado: {result}") ###
                        
                        # Manejar comandos especiales
                        if result == "sleep":
                            self.is_active = False
                        elif result == "shutdown":
                            self.is_listening = False
                            break
                        else:
                            # Volver a modo de espera después de comando normal
                            if self.is_listening:
                                time.sleep(1)
                                self.is_active = False
                                print(f"Volviendo a modo de espera. Di '{self.wake_word}' para activar")
                    else:
                        # Timeout - volver a modo de espera
                        self.is_active = False
                        print(f"Timeout. Volviendo a modo de espera. Di '{self.wake_word}' para activar")
                
            except KeyboardInterrupt:
                print("\nInterrumpido por usuario")
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
            print("Jarvis desconectado")

if __name__ == "__main__":
    assistant = VoiceAssistant(
        wake_word="jarvis escuchame", #palabra clave para activar
        language="es-ES"    #idioma
    )
    assistant.run()