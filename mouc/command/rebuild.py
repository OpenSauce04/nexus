import hashlib
import os
from os.path import join as join_path
from subprocess import run

from command.clean import cmd_clean
from command.init import cmd_init
from strings import *
from utils import *

def cmd_rebuild(image):
  dockerfile_path = join_path(dockerfiles_dir, image)
  with open(dockerfile_path, 'rb', buffering=0) as f:
    dockerfile_hash = hashlib.file_digest(f, 'md5').hexdigest()
  image_cache_path = join_path(image_cache_dir, dockerfile_hash)

  cmd_init()
  os.makedirs(join_path(buildfiles_dir, image), exist_ok=True)

  start_mouc_env()

  run(['docker', 'exec', 'mouc-env', 'sh', '-c',
      f'docker build -t mouc-managed -f /var/host/{dockerfile_path} /var/host/{buildfiles_dir}/{image} && docker save -o /var/host/{image_cache_path} mouc-managed'])