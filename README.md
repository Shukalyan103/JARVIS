# J.A.R.V.I.S. - AI Desktop Assistant

An intelligent desktop voice assistant that automates your daily routine by sequentially launching your software applications, responding to voice commands, and answering questions via Gemini AI.

## 🚀 Daily Routine Automation

Whenever you say:
> **"Start my daily routine"** (or *"Start daily routine"*, *"Start my routine"*)

JARVIS will respond via voice and automatically launch your workspace applications one by one with a smooth pause between each:

1. **Visual Studio Code** (`code` / AppData path)
2. **Google Chrome** (`chrome.exe`)
3. **Spotify** (`spotify:` / Windows App)
4. **Discord** (`discord:` / Web fallback)

---

## 🛠️ How to Run

Activate your virtual environment and start JARVIS:

```powershell
.\.venv\Scripts\Activate.ps1
python main.py
```

Or directly:

```powershell
.\.venv\Scripts\python.exe main.py
```

---

## 🎙️ Spoken Commands

| Command | Action |
| :--- | :--- |
| **"Start my daily routine"** | Launches VS Code, Chrome, Spotify, and Discord one by one |
| **"What do you see?"** / **"Look at this"** | Captures a webcam image and analyzes it using OpenRouter Vision |
| **"What's on my screen?"** / **"Read my screen"** | Captures desktop screenshot and explains it via OpenRouter Vision |
| **"What is the time?"** | Speaks the current local time |
| **"System status"** | Reports CPU and RAM usage percentage |
| **"Exit JARVIS"** / **"Shutdown"** | Gracefully disconnects and powers down JARVIS |
| *Any other question* | JARVIS consults its Gemini 2.5 Flash neural brain and answers |

---

## ⚙️ Customizing Applications & Delays

You can customize the list of apps, their order, or the delay between launches in [`config/routine_config.json`](file:///c:/Users/USD/Desktop/study/projects/JARVIS/config/routine_config.json):

```json
{
  "routine_name": "Daily Workspace Routine",
  "delay_between_apps_seconds": 3,
  "apps": [
    {
      "name": "Visual Studio Code",
      "voice_announcement": "Opening Visual Studio Code",
      "type": "executable",
      "primary_command": "code",
      "project_path": "c:\\Users\\USD\\Desktop\\study\\projects\\JARVIS",
      "fallback_paths": [
        "%LOCALAPPDATA%\\Programs\\Microsoft VS Code\\Code.exe"
      ]
    }
  ]
}
```

> **Tip:** You can specify `"project_path": "C:\\path\\to\\project"` (or `"args": ["C:\\path\\to\\project"]`) for VS Code or any other software to open directly to that folder/workspace. Relative paths like `"."` are also supported.

---

## 📂 Project Architecture

- [`main.py`](file:///c:/Users/USD/Desktop/study/projects/JARVIS/main.py): Core voice listening loop, command routing, and greeting.
- [`utils/routineManager.py`](file:///c:/Users/USD/Desktop/study/projects/JARVIS/utils/routineManager.py): Routine trigger detection, app discovery, and sequential launcher.
- [`config/routine_config.json`](file:///c:/Users/USD/Desktop/study/projects/JARVIS/config/routine_config.json): Routine application list and sequence configuration.
- [`Head/Ear.py`](file:///c:/Users/USD/Desktop/study/projects/JARVIS/Head/Ear.py): Microphone audio capture and Google Speech Recognition.
- [`Head/Eyes.py`](file:///c:/Users/USD/Desktop/study/projects/JARVIS/Head/Eyes.py): Optical webcam sensor and desktop screen capture with base64 encoding.
- [`Head/Mouth.py`](file:///c:/Users/USD/Desktop/study/projects/JARVIS/Head/Mouth.py): Text-to-Speech (Edge TTS + Pygame audio playback).
- [`model/geminiModel.py`](file:///c:/Users/USD/Desktop/study/projects/JARVIS/model/geminiModel.py): Conversational AI brain powered by Google Gemini.
- [`model/openRounterModel.py`](file:///c:/Users/USD/Desktop/study/projects/JARVIS/model/openRounterModel.py): Multimodal Vision AI powered by OpenRouter.
