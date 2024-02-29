import hashlib
from os.path import join as join_path
from subprocess import run
from time import sleep

from command.init import cmd_init
from strings import *
from utils import *

def cmd_enter(image):
  dockerfile_path = join_path(dockerfiles_dir, image)
  with open(dockerfile_path, 'rb', buffering=0) as f:
    dockerfile_hash = hashlib.file_digest(f, 'md5').hexdigest()
  image_cache_path = join_path(image_cache_dir, dockerfile_hash)

  cmd_init()
  os.makedirs(join_path(buildfiles_dir, image), exist_ok=True)

  qrun(['su', username, '-c', 'xhost local:root'])
  qrun(['docker', 'pull', 'docker'])

  # If DinD container doesn't already exist, start it and wait for Docker to init
  try:
    run(['sh', '-c', 'docker container inspect mouc-env > /dev/null 2>&1'], check=True)
  except:
    qrun(['docker', 'run', '--rm', '-dt',
          '--privileged',
          '--device', '/dev/dri',
          '--env=DISPLAY',
          '--net=host',
          '--volume', f'{home_dir}:/var/host/{home_dir}',
          '--name', 'mouc-env',
          'docker'], silent_error=True)
    sleep(2)

  if not isfile(image_cache_path):
    run(['docker', 'exec', 'mouc-env', 'sh', '-c',
          f'docker build -t mouc-managed -f /var/host/{dockerfile_path} /var/host/{buildfiles_dir}/{image} && docker save -o /var/host/{image_cache_path} mouc-managed'])

  qrun(['docker', 'exec', 'mouc-env', 'sh', '-c',
        f'docker load -i /var/host/{image_cache_path}'])
  run(['docker', 'exec', '-it', 'mouc-env', 'sh', '-c',
        (
          'docker run --rm -it '
          '--device /dev/dri '
          '--env=DISPLAY '
          '--net=host '
          f'--volume /var/host/{home_dir}:/var/host/{home_dir} '
          f'--workdir /var/host/{os.getcwd()} '
          'mouc-managed /bin/sh'
        )
      ])