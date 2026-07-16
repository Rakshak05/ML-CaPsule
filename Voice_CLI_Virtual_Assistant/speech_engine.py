import sys
import speech_recognition as sr
import pyttsx3
from Voice_CLI_Virtual_Assistant import config

class SpeechEngine:
    def __init__(self):
        # Initialize pyttsx3 TTS engine
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', config.TTS_RATE)
            self.tts_engine.setProperty('volume', config.TTS_VOLUME)
            
            # Select voice
            voices = self.tts_engine.getProperty('voices')
            if voices:
                index = min(config.TTS_VOICE_INDEX, len(voices) - 1)
                self.tts_engine.setProperty('voice', voices[index].id)
            self.tts_available = True
        except Exception as e:
            print(f"[Warning] Text-to-Speech engine could not be initialized: {e}")
            print("[Warning] Falling back to text-only output.")
            self.tts_available = False

        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()

    def speak(self, text: str):
        """Synthesize text to speech (and also print it to terminal)."""
        print(f"Assistant: {text}")
        if self.tts_available:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                # If speak fails, don't crash
                pass

    def listen(self, timeout: int = 5, phrase_time_limit: int = 5) -> str:
        """Capture microphone input and decode it to text. Fallback to CLI input if microphone fails."""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
                print("\n[Listening... Speak now]")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                
            print("[Processing audio...]")
            query = self.recognizer.recognize_google(audio, language='en-in')
            print(f"User (Voice): {query}")
            return query
        except sr.WaitTimeoutError:
            print("[No speech detected within timeout limit]")
            return ""
        except sr.UnknownValueError:
            self.speak("Sorry, I could not understand what you said.")
            return ""
        except sr.RequestError as e:
            self.speak(f"Could not request speech recognition results; {e}")
            return ""
        except Exception as e:
            print(f"[Warning] Microphone or audio subsystem error: {e}")
            print("Please type your command in the CLI instead.")
            # Fall back to CLI input if voice input has system-level failure
            try:
                query = input("\nUser (CLI input fallback): ")
                return query
            except (KeyboardInterrupt, EOFError):
                return "exit"
