package main

import (
	"fmt"
	"time"
)

func main() {
	c2Url := "http://localhost:3000/api/beacon"
	status := "active"

	fmt.Println("[Red] MalSimX Go Agent Starting...")

	err := SetupSandbox()
	if err != nil {
		fmt.Printf("[!] Failed to setup sandbox: %v\n", err)
		return
	}

	GenerateDummyFiles(20)
	fmt.Println("[Red] Sandbox ready.")

	for {
		fmt.Printf("[Red] Beaconing %s...\n", c2Url)
		
		_, err := SendBeacon(c2Url, status)
		if err != nil {
			fmt.Printf("[Red Error] C2 Beacon failed: %v\n", err)
		} else {
			fmt.Println("[Red] C2 Beacon successful: HTTP 200")
			
			// Always simulate ransomware on successful check-in for MVP
			SimulateRansomware()
		}

		time.Sleep(5 * time.Second)
	}
}
