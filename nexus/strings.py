from getpass import getuser
import os
from os.path import *

# Environment
username = os.environ.get('SUDO_USER', os.environ.get('USERNAME'))
if username == None:
  username = getuser()

# Paths
home_dir = expanduser(f'~{username}')
nexus_dir = home_dir+'/.nexus'
dockerfiles_dir = nexus_dir+'/dockerfiles'
buildfiles_dir = nexus_dir+'/data'
image_cache_dir = nexus_dir+'/imagecache'

# Messages
program_usage_msg = \
"""Usage: nexus [command]
- nexus init
    Initializes the directories required to use nexus (~/.nexus/*)
- nexus enter [image]
    Enters an image defined in ~/.nexus/dockerfiles/
- nexus rebuild [image]
    Forces a rebuild of an image
    Use `--no-cache` to not use cache when building
- nexus clean [mode]
    Modes:
      cache - cleans nexus image cache
      env   - cleans nexus docker environment
      all   - cleans both the image cache and docker environment"""