import pyttsx3
import re
import threading

_current_engine = None
_lock = threading.Lock()

def clean_for_speech(text: str) -> str:
    text = re.sub(r'[*#_`]', '', text)
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    return text

def say(text: str, language="en-IN"):
    global _current_engine
    print(f"Aries: {text}")
    spoken_text = clean_for_speech(text)

    engine = pyttsx3.init()
    with _lock:
        _current_engine = engine

    engine.say(spoken_text)
    engine.runAndWait()
    engine.stop()

    with _lock:
        _current_engine = None

def stop_speaking():
    with _lock:
        if _current_engine:
            _current_engine.stop()