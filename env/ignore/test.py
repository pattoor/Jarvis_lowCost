import speech_recognition as sr

# Crear el reconocedor
r = sr.Recognizer()

# Usar el micrófono como fuente
with sr.Microphone() as source:
    print("Ajustando el ruido de fondo... un momento")
    r.adjust_for_ambient_noise(source)  # para mejorar precisión
    print("Estoy escuchando, habla ahora:")

    # Escuchar
    audio = r.listen(source, timeout=5)

    try:
        # Reconocer usando Google
        texto = r.recognize_google(audio, language="es-AR")
        print("Escuché: " + texto)
    except sr.UnknownValueError:
        print("No entendí lo que dijiste.")
    except sr.RequestError as e:
        print("Error con el servicio de reconocimiento; {0}".format(e))
