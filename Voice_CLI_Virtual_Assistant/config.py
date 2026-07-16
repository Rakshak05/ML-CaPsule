# Configuration settings for the Voice & CLI Virtual Assistant

DEFAULT_WEATHER_CITY = "Jamshedpur"

# Speech Settings
TTS_RATE = 150  # Speed of speech
TTS_VOLUME = 1.0  # Volume level (0.0 to 1.0)
TTS_VOICE_INDEX = 0  # 0 for male, 1 for female (depends on OS voices installed)

# Default save path for screenshots
import os
DEFAULT_SCREENSHOT_DIR = os.path.join(os.path.expanduser("~"), "Pictures", "AssistantScreenshots")
if not os.path.exists(DEFAULT_SCREENSHOT_DIR):
    try:
        os.makedirs(DEFAULT_SCREENSHOT_DIR)
    except Exception:
        # Fallback to current working directory if Pictures path fails
        DEFAULT_SCREENSHOT_DIR = os.getcwd()
