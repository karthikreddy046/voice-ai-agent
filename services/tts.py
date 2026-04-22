import pyttsx3
import threading

lock = threading.Lock()

def speak(text):
    try:
        with lock:
            engine = pyttsx3.init()   # re-init every time (important)
            engine.setProperty('rate', 165)

            voices = engine.getProperty('voices')
            if voices:
                engine.setProperty('voice', voices[0].id)

            print("[TTS] speaking:", text)

            engine.say(text)
            engine.runAndWait()

            engine.stop()

    except Exception as e:
        print("TTS error:", e)