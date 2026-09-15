# JARVIS — Personal PC Voice Assistant

A voice-controlled assistant that can open apps, answer questions, control the PC, and act as a coding buddy.

## Status
🚧 In development — final year project

## Features (planned)
- [ ] Voice input (speech-to-text)
- [ ] Voice output (text-to-speech)
- [ ] LLM-powered brain (answers questions, chats)
- [ ] System control (open apps, click, type)
- [ ] Coding buddy mode (explains errors, answers dev questions)

## Project structure
```
jarvis-assistant/
├── main.py              # entry point — the main loop
├── modules/
│   ├── listener.py       # speech-to-text (mic -> text)
│   ├── speaker.py         # text-to-speech (text -> voice)
│   ├── brain.py           # sends text to LLM, gets response
│   ├── system_control.py  # opens apps, controls PC
│   └── coding_buddy.py     # dev-focused prompt mode
├── requirements.txt
└── README.md
```

## Setup
```bash
pip install -r requirements.txt
python main.py
```
