# -*- coding: utf-8 -*-
import subprocess
import webbrowser
import psutil
from datetime import datetime

class CommandHandler:
    def __init__(self, logger, speak_function):
        self.logger = logger
        self.speak_and_show = speak_function
        
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
        """Interpreta comando natural con Ollama"""
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
            return self.interpret_basic(text)
    
    def interpret_basic(self, text):
        """Interpretación básica sin IA"""
        command = text.lower()
        #agregar comandos
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
        interpreted = self.interpret_with_ollama(command_text)
        
        try:
            # Pregunta general con IA
            if interpreted.startswith('pregunta:'):
                return self.handle_question(interpreted)
            
            # Búsquedas
            elif interpreted.startswith('buscar_youtube:'):
                return self.search_youtube(interpreted)
            elif interpreted.startswith('buscar_google:'):
                return self.search_google(interpreted)
            
            # Comandos del sistema
            command = interpreted.lower()
            
            if "recursos" in command or "sistema" in command:
                return self.get_resources()
            elif "hora" in command or "tiempo" in command:
                return self.get_time()
            elif "fecha" in command:
                return self.get_date()
            elif command == "abrir_navegador" or "navegador" in command:
                return self.open_browser()
            elif command == "bloc_notas" or "notas" in command:
                return self.open_notepad()
            elif command == "calculadora" or "calculadora" in command:
                return self.open_calculator()
            elif command == "explorador" or "archivos" in command:
                return self.open_explorer()
            elif "buscar" in command:
                return self.search_fallback(command)
            elif command == "dormir" or "dormir" in command:
                return self.sleep_mode()
            elif command == "apagar" or "apagar" in command:
                return self.shutdown()
            else:
                return self.unknown_command(command)
                
        except Exception as e:
            error_msg = f"Error ejecutando comando: {str(e)}"
            self.logger.error(error_msg)
            self.speak_and_show("Hubo un error ejecutando el comando")
            return f"Error: {error_msg}"

    # =============== COMANDOS INDIVIDUALES ===============
    
    def handle_question(self, interpreted):
        """Maneja preguntas generales con IA"""
        question = interpreted.replace('pregunta:', '').strip()
        try:
            import ollama
            response = ollama.chat(
                model='llama3.2:1b',
                messages=[{'role': 'user', 'content': f'Responde brevemente en español: {question}'}]
            )
            answer = response['message']['content'].strip()
            self.speak_and_show(answer)
            return f"Pregunta respondida: {answer}"
        except:
            response = "No puedo responder esa pregunta en este momento"
            self.speak_and_show(response)
            return response

    def search_youtube(self, interpreted):
        """Buscar en YouTube"""
        search_term = interpreted.replace('buscar_youtube:', '').strip()
        if search_term:
            webbrowser.open(f'https://www.youtube.com/results?search_query={search_term.replace(" ", "+")}')
            response = f"Buscando {search_term} en YouTube"
            self.speak_and_show(response)
            return f"Búsqueda en YouTube: {search_term}"
        return "No especificaste qué buscar en YouTube"

    def search_google(self, interpreted):
        """Buscar en Google"""
        search_term = interpreted.replace('buscar_google:', '').strip()
        if search_term:
            webbrowser.open(f'https://www.google.com/search?q={search_term.replace(" ", "+")}')
            response = f"Buscando {search_term} en Google"
            self.speak_and_show(response)
            return f"Búsqueda en Google: {search_term}"
        return "No especificaste qué buscar en Google"

    def get_resources(self):
        """Información del sistema"""
        info = self.get_system_info()
        response = f"Tu sistema está funcionando con CPU al {info['cpu']}, memoria al {info['memoria']}, y disco al {info['disco']}"
        self.speak_and_show(response)
        return "Información del sistema comunicada"

    def get_time(self):
        """Hora actual"""
        now = datetime.now()
        time_str = now.strftime("%H:%M")
        response = f"Son las {time_str}"
        self.speak_and_show(response)
        return f"Hora actual comunicada: {time_str}"

    def get_date(self):
        """Fecha actual"""
        now = datetime.now()
        date_str = now.strftime("%d de %B de %Y")
        response = f"Hoy es {date_str}"
        self.speak_and_show(response)
        return f"Fecha actual comunicada: {date_str}"

    def open_browser(self):
        """Abrir navegador"""
        webbrowser.open('https://www.google.com')
        response = "He abierto el navegador para ti"
        self.speak_and_show(response)
        return "Navegador abierto y confirmado"

    def open_notepad(self):
        """Abrir bloc de notas"""
        subprocess.Popen(['notepad.exe'])
        response = "He abierto el bloc de notas"
        self.speak_and_show(response)
        return "Bloc de notas abierto y confirmado"

    def open_calculator(self):
        """Abrir calculadora"""
        subprocess.Popen(['calc.exe'])
        response = "He abierto la calculadora para ti"
        self.speak_and_show(response)
        return "Calculadora abierta y confirmada"

    def open_explorer(self):
        """Abrir explorador de archivos"""
        subprocess.Popen(['explorer.exe'])
        response = "He abierto el explorador de archivos"
        self.speak_and_show(response)
        return "Explorador abierto y confirmado"

    def search_fallback(self, command):
        """Búsqueda genérica (fallback)"""
        search_term = command.replace("buscar", "").strip()
        if search_term:
            webbrowser.open(f'https://www.google.com/search?q={search_term}')
            response = f"Buscando {search_term}"
            self.speak_and_show(response)
            return f"Búsqueda realizada: {search_term}"
        else:
            response = "¿Qué quieres buscar?"
            self.speak_and_show(response)
            return "Esperando término de búsqueda"

    def sleep_mode(self):
        """Modo de espera"""
        response = "Entrando en modo de espera. Di mi palabra clave para activarme"
        self.speak_and_show(response)
        return "sleep"  # Señal especial para el main

    def shutdown(self):
        """Apagar asistente"""
        response = "Apagando asistente. ¡Hasta luego!"
        self.speak_and_show(response)
        return "shutdown"  # Señal especial para el main

    def unknown_command(self, command):
        """Comando no reconocido"""
        response = "No entendí ese comando. Prueba con recursos, hora, fecha, abrir navegador, calculadora o buscar algo"
        self.speak_and_show(response)
        return f"Comando no reconocido: {command}"