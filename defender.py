import math
import json
import time
from collections import deque
from pathlib import Path
from typing import Optional, Dict, Any

from watchdog.events import FileSystemEventHandler
from colorama import init, Fore, Style

from config import LOG_DIR, is_safe_path

init(autoreset=True)

def calculate_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    entropy = 0.0
    for x in range(256):
        p_x = float(data.count(x)) / len(data)
        if p_x > 0:
            entropy += - p_x * math.log2(p_x)
    return entropy

class DefenderMonitor(FileSystemEventHandler):
    def __init__(self, sandbox_dir: Path):
        self.sandbox_dir = sandbox_dir
        self.log_file = LOG_DIR / "events.jsonl"
        self.event_window = deque()
        self.window_duration = 10.0
        self.mass_mod_threshold = 20

    def log_event(self, event_type: str, path: str = "", entropy: Optional[float] = None, details: Optional[Dict[str, Any]] = None):
        event = {
            "timestamp_utc": time.time(),
            "event_type": event_type,
            "path": str(path),
            "entropy": entropy,
            "details": details or {}
        }
        try:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(event) + "\n")
        except Exception:
            pass

    def check_mass_modification(self):
        current_time = time.time()
        # Remove old events
        while self.event_window and current_time - self.event_window[0] > self.window_duration:
            self.event_window.popleft()
            
        if len(self.event_window) > self.mass_mod_threshold:
            print(f"{Fore.YELLOW}[YELLOW ALERT] Mass Modification Detected: {len(self.event_window)} events in {self.window_duration}s{Style.RESET_ALL}")
            self.log_event("MASS_MODIFICATION_ALERT", details={"count": len(self.event_window)})
            self.event_window.clear()

    def process_event(self, event_path: str, action_type: str):
        if not is_safe_path(event_path):
            print(f"{Fore.RED}[WARNING] Sandbox escape attempt ignored: {event_path}{Style.RESET_ALL}")
            self.log_event("SANDBOX_ESCAPE_ATTEMPT", path=event_path)
            return

        self.event_window.append(time.time())
        self.check_mass_modification()

        if event_path.endswith(".locked") and action_type == "created":
            print(f"{Fore.RED}[RED ALERT] Ransomware Activity Detected! Created: {event_path}{Style.RESET_ALL}")
            self.log_event("RANSOMWARE_ALERT", path=event_path)
            return

        if action_type in ("created", "modified") and Path(event_path).is_file():
            try:
                # Calculate entropy
                with open(event_path, "rb") as f:
                    data = f.read(256 * 1024) # Cap read to 256KB
                ent = calculate_entropy(data)
                
                if ent > 7.5:
                    print(f"{Fore.RED}[RED ALERT] High Entropy ({ent:.2f}) Detected: {event_path}{Style.RESET_ALL}")
                    self.log_event("HIGH_ENTROPY_ALERT", path=event_path, entropy=ent)
                else:
                    print(f"{Fore.GREEN}[INFO] File {action_type}: {event_path} (Entropy: {ent:.2f}){Style.RESET_ALL}")
                    self.log_event(f"FILE_{action_type.upper()}", path=event_path, entropy=ent)
            except Exception:
                pass
        else:
            print(f"{Fore.GREEN}[INFO] File {action_type}: {event_path}{Style.RESET_ALL}")
            self.log_event(f"FILE_{action_type.upper()}", path=event_path)

    def on_created(self, event):
        if not event.is_directory:
            self.process_event(event.src_path, "created")

    def on_modified(self, event):
        if not event.is_directory:
            self.process_event(event.src_path, "modified")

    def on_deleted(self, event):
        if not event.is_directory:
            self.process_event(event.src_path, "deleted")

    def on_moved(self, event):
        if not event.is_directory:
            self.process_event(event.dest_path, "renamed")
