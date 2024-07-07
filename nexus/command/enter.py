import hashlib
from os.path import join as join_path
from subprocess import run

from command.rebuild import cmd_rebuild
from strings import *
from utils import *

def cmd_enter(image):
  dockerfile_path = join_path(dockerfiles_dir, image)
  with open(dockerfile_path, 'rb', buffering=0) as f:
    dockerfile_hash = hashlib.file_digest(f, 'md5').hexdigest()
  image_cache_path = join_path(image_cache_dir, dockerfile_hash)

  if not isfile(image_cache_path):
    cmd_rebuild(image, '')

  qrun(['docker', 'exec', 'nexus-env', 'sh', '-c',
        f'docker load -i /var/host/{image_cache_path}'])
  run(['docker', 'exec', '-it', 'nexus-env', 'sh', '-c',
        (
          'docker run --rm -it '
          '--privileged '
          '--device /dev/dri '
          '--env=DISPLAY '
          '--net=host '
          f'--volume /var/host/{home_dir}:/var/host/{home_dir} '
          f'--workdir "/var/host/{os.getcwd()}" '
          'nexus-managed /bin/sh'
        )
      ])