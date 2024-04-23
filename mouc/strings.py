from getpass import getuser
import os
from os.path import *

# Environment
username = os.environ.get('SUDO_USER', os.environ.get('USERNAME'))
if username == None:
  username = getuser()

# Paths
home_dir = expanduser(f'~{username}')
mouc_dir = home_dir+'/.mouc'
dockerfiles_dir = mouc_dir+'/dockerfiles'
buildfiles_dir = mouc_dir+'/data'
image_cache_dir = mouc_dir+'/imagecache'

# Messages
program_usage_msg = \
"""Usage: mouc [command]
- mouc init
    Initializes the directories required to use mouc (~/.mouc/*)
- mouc enter [image]
    Enters an image defined in ~/.mouc/dockerfiles/
- mouc rebuild [image]
    Forces a rebuild of an image
- mouc clean [mode]
    Modes:
      cache
      env"""