import tkinter as tk
import speech_recognition as sr
import threading

# Variable de control para detener la grabación
grabando = False

# Función para grabar y transcribir el audio
def grabar_y_transcribir():
    global grabando
    grabando = True
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        status_label.config(text="Ajustando el ruido ambiente... Por favor espera unos segundos.")
        root.update()
        recognizer.adjust_for_ambient_noise(source)  # Ajustar el ruido ambiente
        status_label.config(text="Escuchando... No se está reconociendo ningún ruido.")
        root.update()

        try:
            while grabando:  # Mantener escuchando hasta que se detenga la grabación
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)  # Limitar duración de la grabación

                if grabando:
                    try:
                        # Intentamos reconocer si se dijo algo
                        texto = recognizer.recognize_google(audio, language="es-ES")
                        transcripcion_text.delete(1.0, tk.END)  # Limpiar la caja de texto
                        transcripcion_text.insert(tk.END, texto)  # Mostrar la transcripción
                        status_label.config(text="Reconociendo ruido...")  # Si se reconoce habla o ruido
                        root.update()
                    except sr.UnknownValueError:
                        # Si no se entendió nada
                        status_label.config(text="No se está reconociendo ningún ruido.")
                        root.update()
                    except sr.RequestError:
                        status_label.config(text="Error en la conexión al servicio de reconocimiento de voz.")
                        root.update()

        except Exception as e:
            status_label.config(text=f"Error: {str(e)}")
            root.update()
        finally:
            grabando = False
            status_label.config(text="No se está reconociendo ningún ruido.")
            root.update()

# Función para detener la grabación
def detener_grabacion():
    global grabando
    grabando = False
    status_label.config(text="Grabación detenida.")
    root.update()

# Crear la ventana principal
root = tk.Tk()
root.title("Grabador y Transcriptor de Audio")

# Establecer tamaño de la ventana
root.geometry("500x400")

# Etiqueta de estado
status_label = tk.Label(root, text="No se está reconociendo ningún ruido.", font=("Arial", 12), pady=20)
status_label.pack()

# Botón para grabar audio
record_button = tk.Button(root, text="Grabar Audio", font=("Arial", 14), command=lambda: threading.Thread(target=grabar_y_transcribir).start())
record_button.pack(pady=10)

# Botón para detener la grabación
stop_button = tk.Button(root, text="Detener Grabación", font=("Arial", 14), command=detener_grabacion)
stop_button.pack(pady=10)

# Cuadro de texto para mostrar la transcripción
transcripcion_text = tk.Text(root, height=10, width=50, font=("Arial", 12))
transcripcion_text.pack(pady=10)

# Iniciar la interfaz gráfica
root.mainloop()
