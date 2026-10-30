# Real-Time Voice Assistant

A desktop-based personal voice assistant for Bangla and English. It listens to speech, responds through text-to-speech, remembers user information, can search the web, and can open a few approved desktop apps.

This project is built in Python and uses:
- Speech recognition for microphone input
- OpenAI Responses API for AI conversation
- Edge TTS for voice output
- DuckDuckGo search for web queries
- SQLite for local memory and conversation history
- Tkinter desktop overlay UI

## Project overview

The assistant is centered around `assistant.py`, which initializes the app and routes user requests. It supports a lightweight command layer for local actions before forwarding general conversation to the AI model.

Key capabilities:
- Voice input using the microphone
- Bilingual responses in Bangla and English
- Web search with summarized results
- Local app launching for approved desktop programs
- Saved memories and recent conversation context
- Floating desktop avatar/assistant window
- Photo capture utility for the default camera

## Repository structure

```text
.
├── assistant.py              # Main app entry point and command router
├── AiUse.py                 # OpenAI integration and system prompt
├── meamory_storage.py       # SQLite memory and conversation storage
├── desktopMate.py           # Tkinter desktop assistant UI and voice loop
├── text_to_voice.py         # Microphone input and speech synthesis
├── autowork.py              # Camera capture script
├── bondhu_memory.db         # SQLite database for memories/history
├── chatbot.png              # Desktop assistant image asset
├── photo.jpg                # Generated snapshot from camera
├── requirements.txt         # Python dependencies
├── .env                     # Local environment variables (not committed in some setups)
├── .gitignore               # Standard Git ignore rules
└── .venv-py313              # Local virtual environment folder
```

## Features

### 1. Bilingual voice assistant
The assistant listens for spoken input and tries recognition in both Bangla and English:
- `bn-BD`
- `en-US`

This is handled in `text_to_voice.py` using `SpeechRecognition`.

### 2. AI-powered conversation
The `AiUse.py` module loads the OpenAI API key from `.env` and sends chat history plus saved memories to the OpenAI Responses API. The assistant replies in the user’s language unless another language is requested.

### 3. Local command handling
`assistant.py` intercepts commands such as:
- “remember that ...”
- “what do you remember?”
- “search for ...”
- “open notepad”
- “open calculator”
- “open paint”
- “search google for ...”
- exit phrases like “stop assistant”

These shortcuts are processed locally before the AI is asked for a general reply.

### 4. Web search with summarized results
The app uses `duckduckgo_search` via `ddgs` to fetch web results. Search results are formatted and then passed to the AI model for summarization.

### 5. Memory and chat history
The project stores:
- remembered facts in `memories`
- recent conversations in `conversations`

These are stored in SQLite database file `bondhu_memory.db` through `meamory_storage.py`.

### 6. Desktop assistant UI
`desktopMate.py` creates a transparent floating desktop widget using Tkinter. It can:
- show assistant status text
- move around the screen
- pause/resume listening
- exit the app

### 7. Voice output
The app generates speech using Microsoft Edge TTS. If the input contains Bengali, it selects a Bengali neural voice. Otherwise, it uses an English neural voice and plays the generated MP3 through pygame.

### 8. Camera utility
`autowork.py` opens the default camera, captures one frame, and saves it as `photo.jpg` in the project directory.

## Technology stack

- Python 3.10+
- OpenAI Python SDK
- SpeechRecognition
- pygame
- edge-tts
- ddgs
- sqlite3
- tkinter
- OpenCV (`cv2` for camera capture)

## Requirements

Install project dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with your OpenAI credentials:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

Optional:
- `OPENAI_MODEL` defaults to `gpt-6-luna` in `AiUse.py`, but you should set a valid model name for your account.

## How to run

From the project root:

```bash
python assistant.py
```

This starts the voice assistant loop and desktop mate UI.

## Example usage

Examples of voice commands the assistant supports:

- “Hello”
- “Search for Python tutorials”
- “Open notepad”
- “Remember that my name is Rahim”
- “What do you remember?”
- “Search Google for weather in Dhaka”
- “Stop assistant”

The assistant responds in the language used by the user.

## Notes

- The app uses online services for speech recognition and TTS, so internet access is required.
- The project is designed for a desktop environment, especially Windows, because it opens Windows apps like `notepad.exe`, `calc.exe`, `mspaint.exe`, and `explorer.exe`.
- The voice assistant is intended for personal use and does not perform arbitrary shell commands.
- AI replies may reflect web search results and database memory, but local safety checks are limited to approved app opening and command routing.

## License

This project does not currently include a license file. If you plan to share or distribute it publicly, add an appropriate open-source license before doing so.

## Important implementation note

A few files contain small naming or runtime quirks:
- `meamory_storage.py` uses the spelling `meamory` instead of `memory`
- `AiUse.py` sets a default model value `gpt-6-luna`, which may not match the actual OpenAI model available in your account
- `text_to_voice.py` calls Google speech recognition online and may fail if your network is unavailable or the service rejects the request

These are practical project details rather than architectural blockers.

## Suggested next improvements

- Add a proper README badge and screenshots
- Add Windows/macOS/Linux compatibility checks
- Improve command parsing and intent detection
- Add user settings for assistant name, voice, language, and app list
- Add a clean uninstall/setup script
- Add automated tests for command routing and memory logic
