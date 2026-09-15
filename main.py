"""
   JARVIS — main loop.
   Flow: listen -> think (brain) -> act (system control / coding buddy) -> speak
   Press ESC at any time while JARVIS is talking to interrupt it.
   """

import threading
import keyboard
from modules import listener, speaker, brain, system_control

LANGUAGES = {
    "english": "en-IN",
    "hindi": "hi-IN",
    "odia": "or-IN",
   }

def speak_with_interrupt(text, language):
    speech_thread = threading.Thread(target=speaker.say, args=(text, language))
    speech_thread.start()

    while speech_thread.is_alive():
        if keyboard.is_pressed("esc"):
            speaker.stop_speaking()
            print("JARVIS: Okay, stopped.")
            break

    speech_thread.join()

def main():
    current_language = "en-IN"
    print("(Press ESC anytime to interrupt JARVIS while it's talking)")
    speak_with_interrupt("Yes boss, what can I do for you today?", current_language)

    while True:
        command = listener.listen(current_language)
        if not command:
            continue

        lower = command.strip().lower()

        if lower in ("exit", "quit", "stop"):
            speak_with_interrupt("Shutting down.", current_language)
            break

        switched = False
        for lang_name, lang_code in LANGUAGES.items():
            if f"switch to {lang_name}" in lower:
                current_language = lang_code
                speak_with_interrupt(f"Switched to {lang_name}.", current_language)
                switched = True
                break
        if switched:
            continue

        response = brain.think(command)
        speak_with_interrupt(response, current_language)

if __name__ == "__main__":
    main()