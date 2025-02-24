package main

import (
	"os"
)

var homeDir string

func initStrings() {
	homeDir, _ = os.UserHomeDir()
}
