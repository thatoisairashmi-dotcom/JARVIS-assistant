"""
   Decides what to do with a command:
   - if it's a system command (open app, etc) -> system_control
   - if it's a coding question -> coding_buddy
   - otherwise -> ask Gemini (with memory of the conversation)
   """

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from modules import system_control, coding_buddy

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

chat = client.chats.create(
    model="gemini-3.6-flash",
    config=types.GenerateContentConfig(
        http_options=types.HttpOptions(timeout=10000),
        system_instruction=(
            "You are JARVIS, a voice assistant. Keep answers short and "
            "conversational, like you're speaking out loud — 2-3 sentences "
            "max unless the user clearly asks for detail. Never use markdown "
            "formatting like asterisks, hashtags, or bullet points. Never "
            "include links, since they can't be spoken."
           )
       )
   )

def think(command: str) -> str:
    lower = command.strip().lower()

    if lower.startswith("open "):
        app_name = lower.replace("open ", "").strip()
        return system_control.open_app(app_name)

    if "code" in lower or "error" in lower or "bug" in lower:
        return coding_buddy.help_with(command)

    try:
       response = chat.send_message(command)
       return response.text
    except Exception as e:
       error_text = str(e)
       print(f"ERROR DETAILS: {error_text}")

       if "RESOURCE_EXHAUSTED" in error_text or "429" in error_text:
           return "I've hit my daily limit of questions for today, sir. Please try again tomorrow, or ask me to open apps in the meantime."

       return "Sorry, I couldn't reach my brain right now."
    except Exception as e:
        print(f"ERROR DETAILS: {e}")
        return "Sorry, I couldn't reach my brain right now."