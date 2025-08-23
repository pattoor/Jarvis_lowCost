# -*- coding: utf-8 -*-
import vosk
import pyaudio
import json
import pyttsx3      # Convierte texto a voz
import threading    # Para ejecutar cosas en paralelo
import time         # Para pausas y delays
import psutil       # Para monitorear CPU/memoria
import logging
from commands import CommandHandler     # Importar los comandos

class VoskVoiceAssistant:
    def __init__(self, wake_word="jarvis", language="es"):
        self.wake_word = wake_word.lower()
        self.language = language
        self.is_listening = True
        self.is_active = False
        self.current_command = ""
        self.last_word_time = 0
        self.silence_threshold = 3.0  # 3 segundos de silencio
        
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
        
        # Configurar Vosk (reconocimiento offline)
        try:
            # Necesitas descargar: https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip
            model_path = "vosk-model-small-es-0.42"
            self.vosk_model = vosk.Model(model_path)
            self.vosk_rec = vosk.KaldiRecognizer(self.vosk_model, 16000)
            self.vosk_rec.SetWords(True)
        except Exception as e:
            self.logger.error(f"Error cargando modelo Vosk: {e}")
            self.logger.error("Descarga el modelo desde: https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip")
            raise
        
        # Configurar audio
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.sample_rate = 16000
        self.chunk_size = 1024
        
        self.audio = pyaudio.PyAudio()
        self.stream = None
        
        # Configurar texto a voz
        self.tts_engine = pyttsx3.init()
        voices = self.tts_engine.getProperty('voices')
        
        for voice in voices:
            if 'spanish' in voice.name.lower() or 'es' in voice.id.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
        
        self.tts_engine.setProperty('rate', 180)
        self.tts_engine.setProperty('volume', 0.8)
        
        # Inicializar manejador de comandos
        self.command_handler = CommandHandler(self.logger, self.speak_and_show)
        
        self.logger.info(f"Asistente Vosk inicializado. Palabra clave: '{self.wake_word}'")
        self.speak_and_show("Jarvis con Vosk activado y listo")

    def start_audio_stream(self):
        """Inicia el stream de audio"""
        self.stream = self.audio.open(
            format=self.audio_format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )

    def stop_audio_stream(self):
        """Detiene el stream de audio"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

    def play_beep(self):
        """Reproduce un pitido"""
        try:
            import winsound
            winsound.Beep(800, 200)
        except:
            print("BEEP")
    
    def speak_and_show(self, text, show_text=None):
        """Convierte texto a voz Y lo muestra en pantalla"""
        display_text = show_text if show_text else text
        print(f"Jarvis dice: {display_text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def check_for_wake_word(self, text):
        """Verifica si el texto contiene la palabra clave"""
        return self.wake_word in text.lower()

    def process_audio_chunk(self):
        """Procesa un chunk de audio y devuelve texto si lo hay"""
        try:
            audio_chunk = self.stream.read(self.chunk_size, exception_on_overflow=False)
            
            # Procesar con Vosk
            if self.vosk_rec.AcceptWaveform(audio_chunk):
                result = json.loads(self.vosk_rec.Result())
                text = result.get('text', '').strip()
                return text, True  # Texto final
            else:
                # Resultado parcial
                partial_result = json.loads(self.vosk_rec.PartialResult())
                partial_text = partial_result.get('partial', '').strip()
                return partial_text, False  # Texto parcial
                
        except Exception as e:
            self.logger.error(f"Error procesando audio: {e}")
            return "", False

    def monitor_resources(self):
        """Monitorea recursos del sistema en segundo plano"""
        while self.is_listening:
            try:
                info = self.command_handler.get_system_info()
                
                cpu_high = float(info['cpu'].replace('%', '')) > 90
                memory_high = float(info['memoria'].replace('%', '')) > 90
                
                if cpu_high or memory_high:
                    alert = f"Recursos altos - CPU: {info['cpu']}, Memoria: {info['memoria']}"
                    print(f"[ALERTA] {alert}")
                    self.logger.warning(alert)
                
                time.sleep(30)
                
            except Exception as e:
                self.logger.error(f"Error monitoreando recursos: {e}")
                time.sleep(60)

    def main_loop(self):
        """Bucle principal con detección continua"""
        print(f"Jarvis escuchando palabra clave: '{self.wake_word}'")
        print("Di 'jarvis' seguido de tu comando")
        print("El sistema escribirá en tiempo real lo que digas")
        
        # Iniciar stream de audio
        self.start_audio_stream()
        
        # Iniciar monitoreo de recursos
        resource_thread = threading.Thread(target=self.monitor_resources, daemon=True)
        resource_thread.start()
        
        try:
            while self.is_listening:
                text, is_final = self.process_audio_chunk()
                
                if text:
                    # Modo de espera - buscando palabra clave
                    if not self.is_active:
                        if self.check_for_wake_word(text):
                            print(f"\n[ACTIVADO] Palabra clave detectada: {text}")
                            self.is_active = True
                            self.current_command = ""
                            self.last_word_time = time.time()
                            self.play_beep()
                            
                            # Quitar la palabra clave del comando
                            command_start = text.lower().find(self.wake_word) + len(self.wake_word)
                            remaining_text = text[command_start:].strip()
                            if remaining_text:
                                self.current_command = remaining_text
                                print(f"Comando: {remaining_text}", end="", flush=True)
                                self.last_word_time = time.time()
                    
                    # Modo activo - capturando comando
                    else:
                        if is_final and text.strip():
                            # Texto final confirmado
                            if text not in self.current_command:
                                self.current_command += " " + text
                            print(f"\nTexto final: {text}")
                            print(f"Comando completo hasta ahora: {self.current_command.strip()}")
                            self.last_word_time = time.time()
                        elif not is_final and text.strip():
                            # Texto parcial - mostrar en tiempo real
                            print(f"\rEscuchando: {text}", end="", flush=True)
                            self.last_word_time = time.time()
                
                # Verificar timeout de silencio
                if self.is_active and (time.time() - self.last_word_time) > self.silence_threshold:
                    print(f"\n\n[EJECUTANDO] Comando después de {self.silence_threshold}s de silencio")
                    print(f"Comando final: '{self.current_command.strip()}'")
                    
                    if self.current_command.strip():
                        # Ejecutar comando
                        result = self.command_handler.execute_command(self.current_command.strip())
                        print(f"Resultado: {result}")
                        
                        # Manejar comandos especiales
                        if result == "sleep":
                            print("Entrando en modo de espera...")
                        elif result == "shutdown":
                            self.is_listening = False
                            break
                    else:
                        print("No se detectó comando válido")
                    
                    # Volver a modo de espera
                    self.is_active = False
                    self.current_command = ""
                    print(f"\n[ESPERANDO] Di '{self.wake_word}' para activar...")
                
                time.sleep(0.01)  # Pequeña pausa para no saturar CPU
                
        except KeyboardInterrupt:
            print("\nInterrumpido por usuario")
        finally:
            self.stop_audio_stream()

    def run(self):
        """Inicia el asistente"""
        try:
            self.main_loop()
        except Exception as e:
            self.logger.error(f"Error fatal: {e}")
        finally:
            self.stop_audio_stream()
            self.audio.terminate()
            print("Jarvis desconectado")

if __name__ == "__main__":
    assistant = VoskVoiceAssistant(
        wake_word="jarvis",
        language="es"
    )
    assistant.run()