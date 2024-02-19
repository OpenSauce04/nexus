from os.path import join as join_path
from subprocess import run

from command.init import cmd_init
from strings import *
from utils import *

def cmd_enter(image):
  dockerfile_path = join_path(dockerfiles_dir, image)
  cmd_init()
  os.makedirs(join_path(buildfiles_dir, image), exist_ok=True)

  qrun(['docker', 'rmi', '-f', 'mouc-managed'], True)
  qrun(['docker', 'build', '-t', 'mouc-managed', '-f', dockerfile_path, join_path(buildfiles_dir, image)])

  qrun(['su', username, '-c', 'xhost local:root'])
  run([
    'docker', 'run', '-it',
      '--volume', f'{home_dir}:/var/host/{home_dir}',
      '--device', '/dev/dri',
      '--env=DISPLAY',
      '--net=host',
      '--workdir', f'/var/host/{os.getcwd()}',
      'mouc-managed', '/bin/bash'
    ])

  qrun(['docker', 'rmi', '-f', 'mouc-managed'])