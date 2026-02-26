package main

import (
	"time"
)

func main() {
	c2Url := "http://localhost:3000/api/beacon"
	logUrl := "http://localhost:3000/api/logs"
	status := "active"

	// Start asynchronous log flushing to the C2
	go FlushLogs(logUrl)

	Info("[Red] MalSimX Go Agent Starting...")

	err := SetupSandbox()
	if err != nil {
		Info("[!] Failed to setup sandbox: %v", err)
		return
	}

	GenerateDummyFiles(20)
	Info("[Red] Sandbox ready.")

	for {
		Info("[Red] Beaconing %s...", c2Url)
		
		resp, err := SendBeacon(c2Url, status)
		if err != nil {
			Info("[Red Error] C2 Beacon failed: %v", err)
		} else {
			if resp.Command != "" && resp.Command != "sleep" {
				Info("[Red] C2 command received: %s", resp.Command)
				
				switch resp.Command {
				case "ransomware":
					SimulateRansomware()
				case "exfiltration":
					SimulateExfiltration()
				case "discovery":
					SimulateDiscovery()
				default:
					Info("[Red] Unknown command from C2: %s", resp.Command)
				}
			}
		}

		time.Sleep(5 * time.Second)
	}
}
