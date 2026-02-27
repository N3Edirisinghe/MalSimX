# MalSimX Commercial Edition

MalSimX has evolved from a local Python script into a **distributed, commercial-grade Breach and Attack Simulation (BAS) architecture**. It is designed to act as an educational Command & Control (C2) and payload testing framework.

The project is split into two distinct components:
1. **`malsimx-c2`**: A Next.js Web Dashboard acting as the C2 Server.
2. **`malsimx-agent`**: A standalone, compiled Go binary acting as the simulated malware payload.

## Architecture

* **The C2 Dashboard**: Provides a real-time, dark-mode hacker UI to track active implants. It queues commands in a local JSON database and serves a `/api/beacon` endpoint for agents to check into.
* **The Go Agent**: When executed on a target machine, it initializes a safe `sandbox/` directory filled with dummy data. It runs silently in the background, beaconing the C2 server every 5 seconds.
* **Live Telemetry**: The agent features a custom `logger`, intercepting all payload execution outputs and streaming them back to the C2 Dashboard so learners can watch exactly what the adversary is doing in real-time.

## The Playbooks (Attack Library)
From the dashboard, users can interactively deploy the following simulations:
* 📘 **Discovery (Reconnaissance)**: Gathers Current User, Hostname, and Network Interfaces.
* 💛 **Exfiltration**: Zips the dummy sandbox directory and simulates a secure data upload.
* 💀 **Ransomware**: Executes a local XOR-cipher encryption across the `sandbox/` directory, appending `.locked` to the files.

---

## 🚀 How to Run MalSimX

You will need to run the C2 Server and the Agent simultaneously in two separate terminal windows.

### 1. Start the Command & Control (C2) Server
Ensure you have Node.js and `npm` installed.

```bash
cd malsimx-c2
npm install
npm run dev
```
Once it says `Ready`, open your browser horizontally to **http://localhost:3000** to view the Command & Control dashboard.

### 2. Start the MalSimX Agent
Ensure you have Go installed (`go1.20+`). Open a **second terminal window**:

```bash
cd malsimx-agent
go build -ldflags="-w -s" -o malsimx-agent
./malsimx-agent
```

As soon as the agent spins up, it will begin beaconing. Check your web dashboard—you will see the new endpoint appear in the Grid, and you can now dispatch Playbooks and view its Live Terminal logs!

## Safety and Disclaimer

**This tool is for educational and testing purposes only.**
All "malicious" actions, such as the ransomware encryption and exfiltration archiving, are strictly confined to the dynamically generated `sandbox/` directory inside the agent folder.
