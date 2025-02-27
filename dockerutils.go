package main

import (
	"fmt"
	"os"
	"time"
)

func waitForDinD() {
	// Wait for the Docker instance inside the Nexus environment to start
	for {
		result := shellRun("docker exec nexus-env sh -c 'docker version'")
		if result == nil {
			break
		}
		time.Sleep(time.Second / 2)
	}
}

func startEnvironment() {
	// If Nexus environment exists but is stopped, start it
	isEnvironmentStopped := shellRun("if [[ $(docker ps -aq -f name=nexus-env -f status=exited) ]]; then exit 1; fi") != nil
	if isEnvironmentStopped {
		fmt.Print("Starting nexus environment...")
		shellRun("docker container start nexus-env")
		waitForDinD()
		fmt.Println("done")
	}

	// If Nexus environment doesn't exist, create it
	doesEnvironmentExist := shellRun("docker container inspect nexus-env") == nil
	if !doesEnvironmentExist {
		fmt.Print("Creating nexus environment...")
		shellRun("docker pull docker:dind")
		// TODO: Understand/explain what all these options I added via trial-and-error actually do.
		createEnvCommand :=
			"docker run -dt " + commonDockerFlags + " --volume " + escapeString(homeDir) + ":/var/host/" + escapeString(homeDir) + " " +
				"--name nexus-env docker:dind"
		shellRun(createEnvCommand)
		waitForDinD()
		fmt.Println("done")
	}
}

func rebuildDockerfile(dockerfile string) {
	// First, make sure that the Nexus environment is actually running
	startEnvironment()

	fmt.Println("Building dockerfile '" + dockerfile + "'...")
	// Create build files dir if it doesn't exist
	os.Mkdir(buildfilesDir + "/" + dockerfile, 0755)
	
	// TODO: Handle error
	dockerfileContent, _ := os.ReadFile(dockerfilesDir + "/" + dockerfile)
	dockerfileHash := stringToMD5(string(dockerfileContent))

	extraparams := ""
	if len(os.Args) > 3 {
		// TODO: Maybe add more options here? If necessary?
		if os.Args[3] == "--no-cache" {
			extraparams = "--no-cache"
		}
	}
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
			"--volume /var/host/" + escapeString(homeDir) + ":/var/host/" + escapeString(homeDir) + " " +
			"--workdir /var/host/" + escapeString(pwd) + " nexus-managed /bin/sh'"
	shellRunInteractive(enterEnvironmentCommand)
}

func cleanNexus(option string) {
	switch option {
	case "all":
		cleanNexus("env")
		cleanNexus("cache")

	case "cache":
		fmt.Print("Cleaning image cache...")
		// TODO: Do this better
		os.RemoveAll(imagecacheDir)
		os.Mkdir(imagecacheDir, 0755)
		fmt.Println("done")

	case "env":
		fallthrough
	case "environment":
		fmt.Print("Cleaning environment...")
		shellRun("docker rm -fv nexus-env")
		fmt.Println("done")

	default:
		showHelpMessage()
	}
}
