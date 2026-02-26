package main

import (
	"archive/zip"
	"io"
	"os"
	"path/filepath"
	"strings"
	"time"
)

func SimulateExfiltration() {
	Info("[Red] Starting exfiltration simulation...")

	zipPath := filepath.Join(SandboxDir, "exfil_data.zip")
	zipFile, err := os.Create(zipPath)
	if err != nil {
		Info("[Red Error] Failed to create exfil archive: %v", err)
		return
	}
	defer zipFile.Close()

	archive := zip.NewWriter(zipFile)
	defer archive.Close()

	fileCount := 0

	err = filepath.Walk(SandboxDir, func(path string, info os.FileInfo, err error) error {
		if err != nil || info.IsDir() {
			return nil
		}

		// Don't zip the zip itself or locked files
		if path == zipPath || strings.HasSuffix(path, ".locked") {
			return nil
		}

		// Open target file
		f1, err := os.Open(path)
		if err != nil {
			return nil
		}
		defer f1.Close()

		// Add to zip
		w1, err := archive.Create(filepath.Base(path))
		if err != nil {
			return nil
		}

		if _, err := io.Copy(w1, f1); err != nil {
			return nil
		}
		fileCount++
		return nil
	})

	if err != nil {
		Info("[Red Error] Error walking sandbox for exfil: %v", err)
		return
	}

	Info("[Red] Zipped %d files into staging archive.", fileCount)
	Info("[Red] Simulating secure channel upload to C2... (3 seconds)")
	time.Sleep(3 * time.Second)

	// Cleanup
	os.Remove(zipPath)
	Info("[Red] Exfiltration sequence complete. Staging archive destroyed.")
}
