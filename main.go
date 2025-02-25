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
		case "clean":
			if len(os.Args) <= 2 {
				showHelpMessage()
			} else {
				cleanNexus(os.Args[2])
			}

		case "enter":
			if len(os.Args) <= 2 {
				showHelpMessage()
			} else {
				enterDockerfile(os.Args[2])
			}

		case "rebuild":
			if len(os.Args) <= 2 {
				showHelpMessage()
			} else {
				rebuildDockerfile(os.Args[2])
			}

		case "start":
			startEnvironment()

		default:
			showHelpMessage()
		}
	}
}
