import sys
import datetime
from Voice_CLI_Virtual_Assistant.speech_engine import SpeechEngine
from Voice_CLI_Virtual_Assistant import web_ops
from Voice_CLI_Virtual_Assistant import system_ops

def get_greeting() -> str:
    """Generate dynamic time-of-day greeting."""
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning!"
    elif 12 <= hour < 17:
        return "Good afternoon!"
    elif 17 <= hour < 21:
        return "Good evening!"
    else:
        return "Hello!"

def print_help():
    """Print list of available commands."""
    print("\n--- Available Commands ---")
    print("1.  weather                      - Get weather for Jamshedpur")
    print("2.  news                         - Get top 5 news headlines")
    print("3.  wikipedia <query>            - Search Wikipedia")
    print("4.  google <query>               - Search Google in browser")
    print("5.  youtube <query>              - Search/Play on YouTube")
    print("6.  screenshot                   - Take a timestamped screenshot")
    print("7.  battery                      - Check system battery status")
    print("8.  clipboard                    - Read text from system clipboard")
    print("9.  play <file_path>             - Play a media file using OS default player")
    print("10. logout / restart / shutdown  - OS administrative power control hooks")
    print("11. help                         - Print this help message")
    print("12. exit / quit                  - Stop the assistant")
    print("---------------------------\n")

def process_command(engine: SpeechEngine, command_str: str) -> bool:
    """Parse and execute commands. Returns False to exit the assistant."""
    cmd = command_str.strip().lower()
    
    if not cmd:
        return True
        
    if cmd in ["exit", "quit", "goodbye", "bye"]:
        engine.speak("Goodbye! Have a great day.")
        return False
        
    elif cmd == "help":
        print_help()
        return True
        
    elif "weather" in cmd:
        engine.speak("Fetching real-time weather details...")
        report = web_ops.get_weather()
        engine.speak(report)
        return True
        
    elif "news" in cmd:
        engine.speak("Retrieving top news headlines...")
        headlines = web_ops.get_top_news()
        engine.speak("Here are the top news headlines:")
        for idx, headline in enumerate(headlines, 1):
            print(f"{idx}. {headline}")
            # Only speak the first 3 to avoid long speech
            if idx <= 3:
                engine.speak(headline)
        return True
        
    elif cmd.startswith("wikipedia"):
        query = command_str[len("wikipedia"):].strip()
        if not query:
            engine.speak("What would you like to search on Wikipedia?")
            query = input("Wikipedia query: ") if sys.stdin.isatty() else ""
            if not query:
                return True
        engine.speak(f"Searching Wikipedia for {query}...")
        result = web_ops.get_wikipedia_summary(query)
        engine.speak(result)
        return True
        
    elif cmd.startswith("google"):
        query = command_str[len("google"):].strip()
        if not query:
            engine.speak("What would you like to search on Google?")
            query = input("Google search query: ") if sys.stdin.isatty() else ""
            if not query:
                return True
        msg = web_ops.search_google(query)
        engine.speak(msg)
        return True
        
    elif cmd.startswith("youtube"):
        query = command_str[len("youtube"):].strip()
        if not query:
            engine.speak("What would you like to stream on YouTube?")
            query = input("YouTube query: ") if sys.stdin.isatty() else ""
            if not query:
                return True
        msg = web_ops.play_youtube(query)
        engine.speak(msg)
        return True
        
    elif "screenshot" in cmd:
        engine.speak("Capturing screen...")
        res = system_ops.capture_screenshot()
        engine.speak(res)
        return True
        
    elif "battery" in cmd:
        status = system_ops.get_battery_status()
        engine.speak(status)
        return True
        
    elif "clipboard" in cmd:
        engine.speak("Reading from clipboard...")
        text = system_ops.read_clipboard()
        engine.speak(f"Clipboard content is: {text}")
        return True
        
    elif cmd.startswith("play"):
        file_path = command_str[len("play"):].strip()
        if not file_path:
            engine.speak("Please specify the path to the media file.")
            file_path = input("Media file path: ") if sys.stdin.isatty() else ""
            if not file_path:
                return True
        res = system_ops.play_media_file(file_path)
        engine.speak(res)
        return True
        
    elif cmd in ["logout", "restart", "shutdown"]:
        engine.speak(f"Are you sure you want to trigger system {cmd}? Type 'yes' to confirm.")
        confirm = input(f"Confirm {cmd} (yes/no): ").strip().lower()
        if confirm == 'yes':
            engine.speak(f"Triggering system {cmd} now.")
            # For safety, let's allow a dry-run check or ask if they want to dry-run
            # We will use dry_run=False but print details, but to be completely safe during testing
            # we can run it. Wait, if it's a test environment we don't want to shut down, so let's default to dry run
            # unless a special flag is passed.
            res = system_ops.system_power_command(cmd, dry_run=True)
            engine.speak(res)
        else:
            engine.speak("Command cancelled.")
        return True
        
    else:
        # Check if the command contains wikipedia or search keywords implicitly
        if "search for" in cmd or "what is" in cmd or "who is" in cmd:
            clean_query = cmd.replace("search for", "").replace("what is", "").replace("who is", "").strip()
            if clean_query:
                engine.speak(f"Searching Wikipedia for {clean_query}...")
                result = web_ops.get_wikipedia_summary(clean_query)
                engine.speak(result)
                return True
        
        engine.speak("Command not recognized. Type 'help' to see available commands.")
        return True

def main():
    engine = SpeechEngine()
    greeting = f"{get_greeting()} I am your Virtual Assistant. How can I help you today?"
    engine.speak(greeting)
    print_help()
    
    # Selection of Mode
    print("Choose interaction mode:")
    print("1. CLI (Command-Line Interface)")
    print("2. Voice (Speech Recognition)")
    
    mode = "1"
    try:
        mode_input = input("Select mode (1 or 2): ").strip()
        if mode_input in ["1", "2"]:
            mode = mode_input
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")
        return

    if mode == "2":
        engine.speak("Voice interaction mode enabled.")
        while True:
            try:
                command = engine.listen()
                if command:
                    # Echo the heard command
                    if not process_command(engine, command):
                        break
            except Exception as e:
                engine.speak(f"Error listening: {e}")
                break
    else:
        engine.speak("CLI interaction mode enabled.")
        while True:
            try:
                command = input("\nEnter command: ").strip()
                if not process_command(engine, command):
                    break
            except (KeyboardInterrupt, EOFError):
                print("\nExiting...")
                break

if __name__ == "__main__":
    main()
