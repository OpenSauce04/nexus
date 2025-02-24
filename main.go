package main

import (
	"fmt"
	"os"
)

func main() {
	// Set values for global strings used throughout the program
	initStrings()

	// Process args and run appropriate subroutine
	if len(os.Args) == 1 {
		fmt.Println(helpMessage)
	} else {
		switch os.Args[1] {
		case "start":
			startEnvironment()
		default:
			fmt.Println(helpMessage)
		}
	}
}
