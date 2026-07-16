# Voice & CLI-Driven System Virtual Assistant

A multi-modal Python-based Virtual Assistant designed to perform automated system operations, fetch live web scraped intelligence, and process inputs via both Voice Commands (Speech Recognition) and a CLI interface.

## Features

### 🎙️ Speech & NLP Layer
*   **Dynamic Greeting:** Custom time-of-day greeting (Good morning/afternoon/evening) upon startup.
*   **Offline TTS:** Synthesizes voice output using `pyttsx3`.
*   **STT processing:** Speech recognition decoding utilizing standard microphones through `SpeechRecognition`.

### 🌐 Web & Knowledge Integrations
*   **Wikipedia Summarization:** Extract short summaries of any searched topics directly.
*   **Google Querying:** Direct browser-based execution of standard queries.
*   **YouTube Streaming:** Query and play video results inside default browser windows.
*   **Live Weather Indexing:** Fetches real-time localized weather updates for **Jamshedpur** (via `wttr.in`).
*   **Live Top News Headlines:** Parses Google News RSS feeds to fetch the latest top headlines.

### ⚙️ System Automation Engine
*   **Clipboard Reader:** Retrieves and reads text currently in the system clipboard.
*   **Screen Capturing:** Desktop screenshot capability, saving timestamped files in user picture directory.
*   **Battery Telemetry:** Live battery status, percentage, charging states, and estimated time remaining.

### 🛠️ OS-Level Hooks
*   **Media Playback:** Launches media files utilizing OS-default associated player applications.
*   **Administrative Power Hooks:** Secure Logout, Restart, and Shutdown protocols with built-in user confirmation safety checks.

## Setup & Installation

Install dependencies:
```bash
pip install -r requirements.txt
```

> **Note:** Speech recognition requires PyAudio. If you don't have PyAudio installed or have microphone issues, the assistant will gracefully fall back to text-only CLI mode.

## Usage

Start the assistant:
```bash
python -m Voice_CLI_Virtual_Assistant.assistant
```
You will be prompted to choose either **CLI mode (1)** or **Voice mode (2)**.
