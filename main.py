import time
import threading
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from watchdog.observers import Observer

from config import setup_sandbox, generate_dummy_files, SANDBOX_DIR
from adversary import AdversarySimulator
from defender import DefenderMonitor

class MockC2Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress default HTTP server logging
        pass
        
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/api/v1/heartbeat':
            print(f"[C2 SERVER] Beacon received!")
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {"status": "ok", "received": time.time()}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run_c2_server(server_instance: HTTPServer, stop_event: threading.Event):
    while not stop_event.is_set():
        server_instance.handle_request()

def main():
    print("Setting up sandbox...")
    setup_sandbox()
    generate_dummy_files(num_files=20, max_depth=3, max_size_kb=50)
    
    stop_event = threading.Event()
    
    # 1. Start Mock C2 Server
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, MockC2Handler)
    httpd.timeout = 1.0 # Allow loop to check stop_event
    c2_thread = threading.Thread(target=run_c2_server, args=(httpd, stop_event), daemon=True)
    c2_thread.start()
    print("Mock C2 server started on http://127.0.0.1:8080")
    
    # 2. Start Defender Watchdog
    defender = DefenderMonitor(SANDBOX_DIR)
    observer = Observer()
    observer.schedule(defender, str(SANDBOX_DIR), recursive=True)
    observer.start()
    print("DefenderMonitor started.")
    
    # 3. Wait and Start Adversary
    print("Waiting 5 seconds before starting adversary simulation...")
    try:
        for _ in range(5):
            time.sleep(1)
            if stop_event.is_set():
                break
    except KeyboardInterrupt:
        pass
        
    if not stop_event.is_set():
        adversary = AdversarySimulator(c2_host="127.0.0.1", c2_port=8080)
        
        # Start the simulation threads
        # Adversary threads expect the stop_event
        adversary.start(stop_event)
        
    print("Running... Press Ctrl+C to stop.")
    
    try:
        while not stop_event.is_set():
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nCtrl+C received. Shutting down...")
    finally:
        stop_event.set()
        observer.stop()
        observer.join()
        if 'adversary' in locals():
            adversary.join()
        c2_thread.join(timeout=2.0)
        print("Shutdown complete.")

if __name__ == "__main__":
    main()
