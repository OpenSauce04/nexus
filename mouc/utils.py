import subprocess
from subprocess import run
from time import sleep

from strings import *

def qrun(args, silent_error = False):
  _stderr = None
  if silent_error:
    _stderr = subprocess.DEVNULL

  subprocess.run(args, stdout = subprocess.DEVNULL, stderr = _stderr)

def start_mouc_env():
  qrun(['su', username, '-c', 'xhost local:root'])
  qrun(['docker', 'pull', 'docker'])

  # If container is stopped, start it
  try:
    run(['sh', '-c', 'if [[ $(docker ps -aq -f name=mouc-env -f status=exited) ]]; then exit 1; fi'], check=True)
  except:
    qrun(['docker', 'container', 'start', 'mouc-env'])
    sleep(0.2)

  # If DinD container doesn't already exist, start it and wait for Docker to init
  try:
    run(['sh', '-c', 'docker container inspect mouc-env > /dev/null 2>&1'], check=True)
  except:
    qrun(['docker', 'run', '-dt',
          '--privileged',
          '--device', '/dev/dri',
          '--env=DISPLAY',
          '--net=host',
          '--volume', f'{home_dir}:/var/host/{home_dir}',
          '--name', 'mouc-env',
          'docker'])
    sleep(2)