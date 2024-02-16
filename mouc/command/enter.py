import hashlib
from os.path import join as join_path
from subprocess import run

from strings import *
from utils import *

def cmd_enter(image):
  dockerfile_path = join_path(dockerfiles_dir, image)
  with open(dockerfile_path, 'rb', buffering=0) as f:
    dockerfile_hash = hashlib.file_digest(f, 'md5').hexdigest()
  image_cache_path = join_path(image_cache_dir, dockerfile_hash)

  qrun(['docker', 'rmi', '-f', 'mouc-managed'], True)

  if not isfile(image_cache_path):
    qrun(['docker', 'build', '-t', 'mouc-managed', '-f', dockerfile_path, home_dir])
    qrun(['docker', 'save', '-o', image_cache_path, 'mouc-managed'])
    qrun(['docker', 'rmi', '-f', 'mouc-managed'])

  qrun(['docker', 'load', '-q', '-i', image_cache_path])
  run([
    'docker', 'run', '-it',
      '--volume', f'{home_dir}:/var/host/{home_dir}',
      '--workdir', f'/var/host/{os.getcwd()}',
      'mouc-managed', '/bin/bash'
    ])
  qrun(['docker', 'rmi', '-f', 'mouc-managed'])