"""
Coding buddy: reads code visible on screen, asks the AI to check it,
and offers to fix a single line with permission.
"""

import os
from dotenv import load_dotenv
from google import genai
from modules import system_control

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# remembers the last suggested fix so we can apply it if the user says "yes"
_pending_fix = {"line": None, "fix": None}

def check_code() -> str:
    screen_text = system_control.read_screen_text()

    prompt = (
        "The following text was captured from a screenshot of a code editor. "
        "It may include extra UI text mixed in with the code - ignore that. "
        "Find ONE clear bug or mistake in the actual code, if any. "
        "If you find one, reply in EXACTLY this format:\n"
        "LINE: <the exact broken line of code>\n"
        "FIX: <the corrected line of code>\n"
        "EXPLANATION: <one short sentence>\n"
        "If there is no clear bug, just reply: NO ISSUES FOUND\n\n"
        f"Screen text:\n{screen_text}"
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )
        result = response.text.strip()
    except Exception as e:
        return f"I couldn't check the code right now: {e}"

    if "NO ISSUES FOUND" in result:
        return "I don't see any obvious issues, boss."

    # try to parse the LINE/FIX/EXPLANATION format
    lines = result.split("\n")
    broken_line, fixed_line, explanation = None, None, ""
    for line in lines:
        if line.startswith("LINE:"):
            broken_line = line.replace("LINE:", "").strip()
        elif line.startswith("FIX:"):
            fixed_line = line.replace("FIX:", "").strip()
        elif line.startswith("EXPLANATION:"):
            explanation = line.replace("EXPLANATION:", "").strip()

    if broken_line and fixed_line:
        _pending_fix["line"] = broken_line
        _pending_fix["fix"] = fixed_line
        return f"Boss, that line looks wrong. {explanation} Permission to correct it?"

    return "I noticed something might be off, but couldn't pin down an exact fix."

def apply_pending_fix() -> str:
    if not _pending_fix["fix"]:
        return "There's no pending fix to apply, boss."

    # type the corrected line as a new line (safe: doesn't touch the rest of the file)
    system_control.type_text(f"\n# JARVIS fix: {_pending_fix['fix']}")

    fix_applied = _pending_fix["fix"]
    _pending_fix["line"] = None
    _pending_fix["fix"] = None
    return f"Done, boss. I've added the corrected line: {fix_applied}"

def help_with(question: str) -> str:
    # kept for general coding questions that aren't "check my code"
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=f"You are a helpful coding assistant. Answer briefly: {question}"
        )
        return response.text
    except Exception as e:
        return f"Sorry, I couldn't reach my brain right now."