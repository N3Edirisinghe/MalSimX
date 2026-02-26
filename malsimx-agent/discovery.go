package main

import (
	"net"
	"os"
	"os/user"
	"time"
)

func SimulateDiscovery() {
	Info("[Red] Starting discovery & situational awareness playbook...")

	time.Sleep(1 * time.Second)
	
	usr, err := user.Current()
	if err == nil {
		Info("[Red Recon] Current User: %s (UID: %s)", usr.Username, usr.Uid)
	}

	time.Sleep(1 * time.Second)

	hostname, _ := os.Hostname()
	Info("[Red Recon] Hostname: %s", hostname)

	time.Sleep(1 * time.Second)

	interfaces, err := net.Interfaces()
	if err == nil {
		for _, i := range interfaces {
			addrs, err := i.Addrs()
			if err != nil {
				continue
			}
			for _, addr := range addrs {
				var ip net.IP
				switch v := addr.(type) {
				case *net.IPNet:
					ip = v.IP
				case *net.IPAddr:
					ip = v.IP
				}
				if ip == nil || ip.IsLoopback() {
					continue
				}
				ip = ip.To4()
				if ip == nil {
					continue // not an ipv4 address
				}
				Info("[Red Recon] Interface: %s -> IP: %s", i.Name, ip.String())
			}
		}
	}

	Info("[Red] Discovery playbook complete.")
}
