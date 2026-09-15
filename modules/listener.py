import speech_recognition as sr

recognizer = sr.Recognizer()

def listen(language="en-IN") -> str:
    with sr.Microphone() as source:
        print("Adjusting for background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print(f"Listening... (language: {language})")
        audio = recognizer.listen(source, phrase_time_limit=8)

    try:
        text = recognizer.recognize_google(audio, language=language)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        print("Speech service is unavailable right now.")
        return ""