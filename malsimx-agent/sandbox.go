package main

import (
	"fmt"
	"math/rand"
	"os"
	"path/filepath"
)

var SandboxDir string

func SetupSandbox() error {
	cwd, err := os.Getwd()
	if err != nil {
		return err
	}
	SandboxDir = filepath.Join(cwd, "sandbox")

	// Clean existing
	os.RemoveAll(SandboxDir)

	// Create fresh
	err = os.MkdirAll(SandboxDir, 0755)
	if err != nil {
		return err
	}
	fmt.Printf("[*] Sandbox initialized at: %s\n", SandboxDir)
	return nil
}

func GenerateDummyFiles(count int) {
	fmt.Printf("[*] Generating %d dummy files in sandbox...\n", count)
	extensions := []string{".txt", ".log", ".csv", ".dat"}

	// Create some nested dirs
	dirs := []string{SandboxDir}
	for i := 0; i < 3; i++ {
		nested := filepath.Join(SandboxDir, randString(8))
		os.Mkdir(nested, 0755)
		dirs = append(dirs, nested)
	}

	for i := 0; i < count; i++ {
		dir := dirs[rand.Intn(len(dirs))]
		ext := extensions[rand.Intn(len(extensions))]
		filename := fmt.Sprintf("dummy_%s%s", randString(6), ext)
		path := filepath.Join(dir, filename)

		size := rand.Intn(50*1024) + 1 // 1b to 50kb
		data := make([]byte, size)
		rand.Read(data)

		os.WriteFile(path, data, 0644)
	}
	fmt.Printf("[*] Successfully created %d dummy files.\n", count)
}

func randString(n int) string {
	var letters = []rune("abcdefghijklmnopqrstuvwxyz0123456789")
	b := make([]rune, n)
	for i := range b {
		b[i] = letters[rand.Intn(len(letters))]
	}
	return string(b)
}
