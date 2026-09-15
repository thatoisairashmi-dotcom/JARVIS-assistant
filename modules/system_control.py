import subprocess
import webbrowser

   # map spoken app names -> actual Windows commands
APP_MAP = {
    "notepad": "notepad",
    "calculator": "calc",
    "chrome": "chrome",
    "paint": "mspaint",
    "explorer": "explorer",
    "file explorer": "explorer",
    "cmd": "cmd",
    "command prompt": "cmd",
   }

   # map spoken website names -> actual URLs
WEBSITE_MAP = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://www.github.com",
    "gmail": "https://mail.google.com",
    "chatgpt": "https://chat.openai.com",
    "whatsapp": "https://web.whatsapp.com",
   }

def open_app(app_name: str) -> str:
    app_name = app_name.strip().lower()

    if app_name in APP_MAP:
        try:
            subprocess.Popen(f"start {APP_MAP[app_name]}", shell=True)
            return f"Opening {app_name}."
        except Exception:
            return f"Something went wrong opening {app_name}."

    if app_name in WEBSITE_MAP:
        webbrowser.open(WEBSITE_MAP[app_name])
        return f"Opening {app_name}."

    return f"I don't know how to open {app_name} yet."