import hashlib
import os
from os.path import *
from subprocess import run

from utils import *

def cmd_enter(image):
  username = os.environ.get('SUDO_USER', os.environ.get('USERNAME'))
  homedir = expanduser(f'~{username}')
  image_hash = hashlib.md5(image.encode()).hexdigest()
  image_path = f'{homedir}/.mouc/dockerfiles/{image}'
  image_cache_path = f'{homedir}/.mouc/imagecache/{image_hash}'

  qrun(['docker', 'rmi', '-f', 'mouc-managed'], True)

  if not isfile(image_cache_path):
    qrun(['docker', 'build', '-t', 'mouc-managed', '-f', image_path, '.'])
    qrun(['docker', 'save', '-o', image_cache_path, 'mouc-managed'])
    qrun(['docker', 'rmi', '-f', 'mouc-managed'])

  qrun(['docker', 'load', '-q', '-i', image_cache_path])
  run([
    'docker', 'run', '-it',
      '--volume', f'{homedir}:/var/host/{homedir}',
      '--workdir', f'/var/host/{os.getcwd()}',
      'mouc-managed'
    ])
  qrun(['docker', 'rmi', '-f', 'mouc-managed'])