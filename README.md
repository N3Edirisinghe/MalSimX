# PurpleTrace Simulator

PurpleTrace Simulator is an educational Purple Team adversary emulation tool. It is designed to simulate realistic "malware-like" behaviors within a safe, isolated sandbox environment while simultaneously providing lightweight defender monitoring to detect those behaviors through filesystem telemetry and heuristics.

## Features

This project implements a duo-split architecture:
1. **Adversary (Red Team) Simulation**: Simulates malicious actions such as ransomware-like file encryption and periodic C2 (Command and Control) beaconing.
2. **Defender (Blue Team) Monitoring**: Actively watches the sandbox directory for suspicious activities, such as mass file modifications, high-entropy file writes (indicative of encryption), and ransomware-specific file extensions `.locked`.

### Key Components

- **`config.py`**: Initializes the sandbox environment, generates dummy files for testing, and enforces strict path-checking to prevent directory traversal attacks (sandbox escapes).
- **`main.py`**: The central orchestrator. It sets up the sandbox, starts a Mock C2 Server, initializes the Defender Watchdog, and launches the Adversary Simulator.
- **`adversary.py`**: Contains the `AdversarySimulator` logic. This script locates dummy files, applies a simple XOR cipher to simulate encryption, appends a `.locked` extension, and periodically reaches out to the Mock C2 Server.
- **`defender.py`**: Implements the `DefenderMonitor` using the `watchdog` library. It calculates file entropy on modification, alerts on mass file changes, detects `.locked` file creations, and logs all events to a JSON Lines (`.jsonl`) file in the `logs/` directory.

## Prerequisite

Ensure you have Python 3.8+ installed. The required dependencies are listed in `requirements.txt`.

Install the dependencies using `pip`:

```bash
pip install -r requirements.txt
```

## How to Run

1. Open a terminal or command prompt.
2. Navigate to the root folder of the project.
3. Run the main orchestrator script:

```bash
python main.py
```

### What happens when you run it?

1. The script will initialize a fresh `sandbox/` directory and populate it with randomly generated dummy files.
2. A Mock C2 Server will start in the background on `http://127.0.0.1:8080`.
3. The Defender Monitor will begin watching the `sandbox/` directory.
4. After a 5-second delay, the Adversary Simulator will begin its routine:
   - Encrypting files in the sandbox.
   - Sending HTTP GET beacons to the C2 Server.
5. The Defender Monitor will output color-coded alerts to the console and write structured logs to `logs/events.jsonl`.
6. To gracefully stop the simulation, press `Ctrl+C`.

## Logs and Telemetry

All filesystem events and alerts are written to `logs/events.jsonl` in a structured JSON format. This log can be consumed by external SIEMs or log aggregators for further analysis.

## Safety and Disclaimer

**This tool is for educational and testing purposes only.**
All "malicious" actions are strictly confined to the dynamically generated `sandbox/` directory. The program includes built-in safeguards to prevent operations outside of this directory. Do not modify the safety checks unless you fully understand the implications.

