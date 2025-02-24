package main

import (
	"os"
)

const helpMessage =
`Usage: nexus [command] [params]
- nexus start
    Starts the nexus docker environment, or creates it if it doesn't exist
- nexus enter [dockerfile]
    Builds and/or enters the Dockerfile located at ~/.config/nexus/dockerfiles/<dockerfile>
`
const commonDockerFlags = "--privileged --device=/dev/dri --device=/dev/fuse --env=DISPLAY --net=host"

var homeDir, configDir, dockerfilesDir, buildfilesDir, cacheDir, imagecacheDir string

func initStrings() {
	homeDir, _ = os.UserHomeDir()
	configDir = homeDir + "/.config/nexus"
	dockerfilesDir = configDir + "/dockerfiles"
	buildfilesDir = configDir + "/buildfiles"
	cacheDir = homeDir + "/.cache/nexus"
	imagecacheDir = cacheDir + "/imagecache"
}
