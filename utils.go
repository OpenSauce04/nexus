package main

import (
    "crypto/md5"
    "encoding/hex"
    "os"
    "os/exec"
    "strings"
)

func shellRun(cmdString string) error {
    cmd := exec.Command("/bin/bash", "-s")
    cmd.Stdin = strings.NewReader(string(cmdString))
    return cmd.Run()
}

func shellRunInteractive(cmdString string) error {
    cmd := exec.Command("/bin/bash", "-c", cmdString)
    cmd.Stdin = os.Stdin
    cmd.Stdout = os.Stdout
    cmd.Stderr = os.Stderr
    return cmd.Run()
}

func stringToMD5(str string) string {
    hash := md5.Sum([]byte(str))
    return hex.EncodeToString(hash[:])
}

func fileExists(path string) bool {
    _, err := os.Stat(path)
    return err == nil
}

func escapeString(str string) string {
    escapedStr := str
    escapedStr = strings.ReplaceAll(escapedStr, "\"", "\\\"")
    escapedStr = strings.ReplaceAll(escapedStr, "'", "'\"'\"'")
    escapedStr = strings.ReplaceAll(escapedStr, "`", "\\`")
    escapedStr = "\"" + escapedStr + "\""
    return escapedStr
}

func initDirs() {
    // TODO: Handle errors
    os.Mkdir(homeDir, 0755)
    os.Mkdir(configDir, 0755)
    os.Mkdir(dockerfilesDir, 0755)
    os.Mkdir(buildfilesDir, 0755)
    os.Mkdir(cacheDir, 0755)
    os.Mkdir(imagecacheDir, 0755)
}
