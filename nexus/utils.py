import subprocess
from subprocess import run
from time import sleep

from strings import *

def qrun(args, silent_error = False):
  _stderr = None
  if silent_error:
    _stderr = subprocess.DEVNULL

  subprocess.run(args, stdout = subprocess.DEVNULL, stderr = _stderr)

def start_nexus_env():
  # If xhost is not configured correctly, fix it
  try:
    run(['xhost |', 'grep', 'LOCAL:'], check=True)
  except:
    qrun(['xhost', 'local:root'])

  # If container is stopped, start it
  try:
    run(['bash', '-c', 'if [[ $(docker ps -aq -f name=nexus-env -f status=exited) ]]; then exit 1; fi'], check=True)
  except:
    qrun(['docker', 'container', 'start', 'nexus-env'])
    sleep(0.2)

  # If DinD container doesn't already exist, start it and wait for Docker to init
  try:
    run(['sh', '-c', 'docker container inspect nexus-env > /dev/null 2>&1'], check=True)
  except:
    # Pull DinD image from Docker Hub
    qrun(['docker', 'pull', 'docker'])
    # Start DinD container named 'nexus-env'
    qrun(['docker', 'run', '-dt',
          '--privileged',
          '--device', '/dev/dri',
          '--env=DISPLAY',
          '--net=host',
          '--volume', f'{home_dir}:/var/host/{home_dir}',
          '--name', 'nexus-env',
          'docker'])
    sleep(5)