package main

import (
	"fmt"
	"os"
)

func showHelpMessage() {
	fmt.Println(helpMessage)
}

func main() {
	// Set values for global strings used throughout the program
	initStrings()
	// Create Nexus directories for configuration, cache, etc
	initDirs()

	// Process args and run appropriate subroutine
	if len(os.Args) <= 1 {
		showHelpMessage()
	} else {
		switch os.Args[1] {
		case "start":
			startEnvironment()

		case "enter":
			if len(os.Args) <= 2 {
				showHelpMessage()
			} else {
				enterDockerfile(os.Args[2])
			}

		default:
			showHelpMessage()
		}
	}
}
