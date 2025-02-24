package main

import (
	"fmt"
	"os"
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
		createEnvCommand :=
			"docker run -dt " + commonDockerFlags + " --volume " + homeDir + ":/var/host/" + homeDir + " " +
				"--name nexus-env docker:dind"
		shellRun(createEnvCommand)
		fmt.Println("done")
	}
}

func rebuildDockerfile(dockerfile string) {
	fmt.Println("Building dockerfile '" + dockerfile + "'...")
	// Create build files dir if it doesn't exist
	os.Mkdir(buildfilesDir + "/" + dockerfile, 0755)
	
	// TODO: Handle error
	dockerfileContent, _ := os.ReadFile(dockerfilesDir + "/" + dockerfile)
	dockerfileHash := stringToMD5(string(dockerfileContent))

	// TODO: Implement --no-cache option
	extraparams := ""
	rebuildCommand :=
		"docker exec nexus-env sh -c 'docker build " + extraparams + " -t nexus-managed -f /var/host/" + dockerfilesDir + "/" + dockerfile + " " +
			"/var/host/" + buildfilesDir + "/" + dockerfile + " && docker save -o /var/host/" + imagecacheDir + "/" + dockerfileHash + " " +
			"nexus-managed'"
	result := shellRunInteractive(rebuildCommand)
	
	// If something went wrong, abort the program
	if result != nil {
		os.Exit(1)
	}
}

func enterDockerfile(dockerfile string) {
	// First, make sure that the Nexus environment is actually running
	startEnvironment()

	// TODO: Handle error
	dockerfileContent, _ := os.ReadFile(dockerfilesDir + "/" + dockerfile)
	dockerfileHash := stringToMD5(string(dockerfileContent))

	// If there is no image cache for the given Dockerfile, build it
	if !fileExists(imagecacheDir + "/" + dockerfileHash) {
		rebuildDockerfile(dockerfile)
	}

	shellRun("docker exec nexus-env sh -c 'docker load -i /var/host/" + imagecacheDir + "/" + dockerfileHash + "'")

	pwd, _ := os.Getwd()
	enterEnvironmentCommand :=
		"docker exec -it nexus-env sh -c 'docker run --rm -it " + commonDockerFlags + " " +
			"--volume /var/host/" + homeDir + ":/var/host/" + homeDir + " " +
			"--workdir \"/var/host/" + pwd + "\" nexus-managed /bin/sh'"
	shellRunInteractive(enterEnvironmentCommand)
}
