import os
import sys
import time
import subprocess
import tkinter as tk
import pyautogui
import psutil
from Voice_CLI_Virtual_Assistant import config

def read_clipboard() -> str:
    """Read and return text from the system clipboard."""
    try:
        root = tk.Tk()
        root.withdraw()
        text = root.clipboard_get()
        root.destroy()
        return text
    except Exception as e:
        # Fallback using pyperclip if available
        try:
            import pyperclip
            return pyperclip.paste()
        except ImportError:
            pass
        return f"Error reading clipboard or clipboard is empty: {e}"

def capture_screenshot(save_dir: str = config.DEFAULT_SCREENSHOT_DIR) -> str:
    """Capture a timestamped desktop screenshot."""
    try:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(save_dir, filename)
        
        # Take the screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        return f"Screenshot saved successfully at: {filepath}"
    except Exception as e:
        return f"Failed to capture screenshot: {e}"

def get_battery_status() -> str:
    """Retrieve live battery telemetry monitoring details."""
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            return "No battery detected (running on AC power)."
            
        percent = battery.percent
        power_plugged = battery.power_plugged
        secsleft = battery.secsleft
        
        status = "Charging" if power_plugged else "Discharging"
        plugged_str = "plugged in" if power_plugged else "unplugged"
        
        time_left_str = ""
        if not power_plugged:
            if secsleft == psutil.POWER_TIME_UNLIMITED:
                time_left_str = " (Power unlimited)"
            elif secsleft == psutil.POWER_TIME_UNKNOWN:
                time_left_str = " (Time remaining unknown)"
            else:
                hours = secsleft // 3600
                minutes = (secsleft % 3600) // 60
                time_left_str = f" ({hours}h {minutes}m remaining)"
                
        return f"Battery is at {percent}%, status: {status} ({plugged_str}){time_left_str}."
    except Exception as e:
        return f"Failed to retrieve battery status: {e}"

def play_media_file(file_path: str) -> str:
    """Trigger media file execution using OS default player or subprocess."""
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"
    
    try:
        if sys.platform.startswith('win'):
            os.startfile(file_path)
        elif sys.platform.startswith('darwin'):
            subprocess.Popen(['open', file_path])
        else:
            subprocess.Popen(['xdg-open', file_path])
        return f"Triggered media file execution for: {os.path.basename(file_path)}"
    except Exception as e:
        return f"Failed to play media file: {e}"

def system_power_command(action: str, dry_run: bool = False) -> str:
    """Execute administrative power commands (Logout, Restart, Shutdown)."""
    action = action.lower()
    
    # Define OS commands
    if sys.platform.startswith('win'):
        commands = {
            'shutdown': 'shutdown /s /t 1',
            'restart': 'shutdown /r /t 1',
            'logout': 'shutdown /l'
        }
    else:
        commands = {
            'shutdown': 'sudo shutdown -h now',
            'restart': 'sudo shutdown -r now',
            'logout': 'pkill -KILL -u $USER'
        }
        
    if action not in commands:
        return f"Unknown power action: {action}"
        
    cmd = commands[action]
    
    if dry_run:
        return f"[Dry Run] Would execute power command: {cmd}"
        
    try:
        # Warning: executing this will immediately shutdown/restart/logout
        subprocess.Popen(cmd, shell=True)
        return f"Executing {action} command..."
    except Exception as e:
        return f"Failed to execute {action} command: {e}"
