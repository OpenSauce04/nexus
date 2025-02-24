package main

import (
	"fmt"
)

func startEnvironment() {
	// If Nexus environment exists but is stopped, start it
	isEnvironmentStopped := shellRun("if [[ $(docker ps -aq -f name=nexus-env -f status=exited) ]]; then exit 1; fi") != nil
	if isEnvironmentStopped {
		fmt.Print("Starting nexus environment...")
		shellRun("docker container start nexus-env")
		fmt.Println("done")
	}

	// If Nexus environment doesn't exist, create it
	doesEnvironmentExist := shellRun("docker container inspect nexus-env") == nil
	if !doesEnvironmentExist {
		fmt.Print("Creating nexus environment...")
		shellRun("docker pull docker:dind")
		// TODO: Understand/explain what all these options I added via trial-and-error actually do.
		// TODO: Do this without the unnecessary createEnvCommand variable.
		//       For some reason this can't just be thrown into shellRun().
		createEnvCommand := "docker run -dt --privileged --device=/dev/dri --device=/dev/fuse " +
			"--env=DISPLAY --net=host --volume " + homeDir + ":/var/host/" + homeDir + " " +
			"--name nexus-env docker:dind"
		shellRun(createEnvCommand)
		fmt.Println("done")
	}
}
