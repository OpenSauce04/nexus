package main

import (
	"os"
)

const helpMessage =
`Usage: nexus [command] [params]
- nexus start
    Starts the nexus docker environment, or creates it if it doesn't exist
`

var homeDir string

func initStrings() {
	homeDir, _ = os.UserHomeDir()
}
