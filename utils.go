package main

import (
	"os/exec"
	"strings"
)

func shellRun(cmd_string string) error {
	cmd := exec.Command("/bin/bash", "-s")
	cmd.Stdin = strings.NewReader(string(cmd_string))
	return cmd.Run()
}
