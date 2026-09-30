"""
   ARIES — main loop.
   Flow: listen -> think (brain) -> act (system control / coding buddy) -> speak
   Press ESC at any time while JARVIS is talking to interrupt it.
   """
import re
import threading
import msvcrt
from modules import listener, speaker, brain, system_control, coding_buddy

LANGUAGES = {
    "english": "en-IN",
    "hindi": "hi-IN",
    "odia": "or-IN",
   }

def speak_with_interrupt(text, language, silent=False):
    if silent:
        print(f"ARIES(silent): {text}")
        system_control.type_text(text)
        return

    speech_thread = threading.Thread(target=speaker.say, args=(text, language))
    speech_thread.start()

    while speech_thread.is_alive():
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'\x1b':  # Esc key
                speaker.stop_speaking()
                print("ARIES: Okay, stopped.")
                break

    speech_thread.join()

def main():
    current_language = "en-IN"
    silent_mode = [False] #using a list so we can change it from inside functions easily
    awaiting_fix_permission = [False]
    print("(Press ESC anytime to interrupt JARVIS while it's talking)")
    speak_with_interrupt("Yes boss, what can I do for you today?", current_language, silent_mode[0])

    while True:
        command = listener.listen(current_language)
        if not command:
            continue


        lower = command.strip().lower()

        if re.search(r'\bwork in silent\b', lower):
          silent_mode[0] = True
          speak_with_interrupt("Switching to silent mode.", current_language, silent_mode[0])
          continue

        if re.search(r'\bcome back\b', lower):
          silent_mode[0] = False
          speak_with_interrupt("I'm back to talking normally.", current_language)
          continue
        if awaiting_fix_permission[0]:
          if re.search(r'\byes\b', lower):
           result = coding_buddy.apply_pending_fix()
           speak_with_interrupt(result, current_language, silent_mode[0])
          else:
           speak_with_interrupt("Okay, I'll leave it as is.", current_language, silent_mode[0])
          awaiting_fix_permission[0] = False
          continue

        if re.search(r'\bcheck (my|the) code\b', lower):
          result = coding_buddy.check_code()
          speak_with_interrupt(result, current_language, silent_mode[0])
          if "Permission to correct it" in result:
           awaiting_fix_permission[0] = True
          continue    

        if re.search(r'\b(exit|quit)\b', lower):
          speak_with_interrupt("Shutting down.", current_language, silent_mode[0])
          break

        if re.search(r'\b(standby|stand by)\b', lower):
          speak_with_interrupt("Going on standby. Say wake up or resume when you need me.", current_language, silent_mode[0])
          while True:
            standby_command = listener.listen(current_language)
            standby_lower = standby_command.strip().lower()
            if re.search(r'\b(wake up|resume)\b', standby_lower):
              speak_with_interrupt("I'm back, boss.", current_language, silent_mode[0])
              break
          continue

        switched = False
        for lang_name, lang_code in LANGUAGES.items():
          if f"switch to {lang_name}" in lower:
                current_language = lang_code
                speak_with_interrupt(f"Switched to {lang_name}.", current_language, silent_mode[0])
                switched = True
                break
        if switched:
          continue

        response = brain.think(command)
        speak_with_interrupt(response, current_language, silent_mode[0])

if __name__ == "__main__":
    main()