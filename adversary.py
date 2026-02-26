import os
import time
import urllib.request
import urllib.error
import threading
from pathlib import Path

# Import safe utilities and constants from Dev A's config module
from config import SANDBOX_DIR, is_safe_path, safe_open, safe_unlink, safe_walk

class AdversarySimulator:
    def __init__(self, c2_host: str = "127.0.0.1", c2_port: int = 8080):
        self.c2_url = f"http://{c2_host}:{c2_port}/api/v1/heartbeat"
        self.threads = []
        
    def _xor_cipher(self, data: bytes) -> bytes:
        """Realistic XOR cipher using a 32-byte key stream to increase file entropy."""
        key = os.urandom(32)
        encrypted = bytearray(len(data))
        for i in range(len(data)):
            encrypted[i] = data[i] ^ key[i % len(key)]
        return bytes(encrypted)

    def simulate_ransomware(self, stop_event: threading.Event):
        """Simulates ransomware by finding files and XOR-ing them."""
        print("[Red] Starting ransomware simulation...")
        
        while not stop_event.is_set():
            files_to_encrypt = []
            
            # 1. Discover targets
            try:
                for root, _, files in safe_walk(SANDBOX_DIR):
                    for file in files:
                        if not file.endswith(".locked"):
                            filepath = Path(root) / file
                            files_to_encrypt.append(filepath)
            except ValueError as e:
                print(f"[Red Error] Directory traversal blocked: {e}")
                
            if not files_to_encrypt:
                # No more targets, wait a bit and check again
                print("[Red] No more files to encrypt. Ransomware simulation idle.")
                time.sleep(10)
                continue
                
            # 2. Encrypt targets
            for target in files_to_encrypt:
                if stop_event.is_set():
                    break
                    
                print(f"[Red] Encrypting: {target.name}")
                try:
                    # Read original
                    with safe_open(target, 'rb') as f:
                        plaintext = f.read()
                        
                    # Encrypt with pseudo-random stream to increase entropy
                    ciphertext = self._xor_cipher(plaintext)
                    
                    # Write .locked
                    locked_path = target.with_suffix(target.suffix + ".locked")
                    with safe_open(locked_path, 'wb') as f:
                        f.write(ciphertext)
                        
                    # Delete original
                    safe_unlink(target)
                    
                    # Simulate time taken to encrypt
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"[Red Error] Failed to encrypt {target}: {e}")

    def simulate_beacon(self, stop_event: threading.Event, interval: int = 3):
        """Simulates periodic C2 beaconing using standard urllib."""
        print("[Red] Starting C2 beacon simulation...")
        
        while not stop_event.is_set():
            try:
                print(f"[Red] Beaconing {self.c2_url}...")
                req = urllib.request.Request(self.c2_url, headers={'User-Agent': 'AdversarySimBot/1.0'})
                # We expect Dev B's server might not be running immediately, so handle errors
                with urllib.request.urlopen(req, timeout=2) as response:
                    print(f"[Red] C2 Beacon successful: HTTP {response.getcode()}")
            except urllib.error.URLError as e:
                print(f"[Red Error] C2 Beacon failed (Server down?): {e.reason}")
            except Exception as e:
                print(f"[Red Error] C2 Request failed: {e}")
                
            # Sleep in small chunks so we can respond to stop_event quickly
            for _ in range(interval * 10):
                if stop_event.is_set():
                    break
                time.sleep(0.1)

    def start(self, stop_event: threading.Event):
        """Starts the adversary simulation threads."""
        ransom_thread = threading.Thread(target=self.simulate_ransomware, args=(stop_event,), daemon=True)
        beacon_thread = threading.Thread(target=self.simulate_beacon, args=(stop_event,), daemon=True)
        
        self.threads.extend([ransom_thread, beacon_thread])
        
        for t in self.threads:
            t.start()
            
        print("[Red] Simulation started.")

    def join(self):
        """Waits for simulator threads to finish."""
        for t in self.threads:
            t.join()
        print("[Red] Simulation finished.")

# --- Standalone Testing ---
if __name__ == "__main__":
    from config import setup_sandbox, generate_dummy_files
    
    # 1. Setup Sandbox
    setup_sandbox()
    generate_dummy_files(num_files=5)
    
    # 2. Run Simulator Test
    print("\n--- Starting Standalone Test ---")
    sim = AdversarySimulator()
    main_stop_event = threading.Event()
    
    try:
        sim.start(main_stop_event)
        
        # Test will run for 10 seconds then shut down
        print("[Test] Simulator running for 10 seconds. Press Ctrl+C to abort early.")
        for i in range(10):
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n[Test] Caught Ctrl+C.")
    finally:
        print("[Test] Shutting down...")
        main_stop_event.set()
        sim.join()
        print("[Test] Complete.")
