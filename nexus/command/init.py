import os

from strings import *

def cmd_init():
  os.makedirs(nexus_dir, exist_ok=True)
  os.makedirs(dockerfiles_dir, exist_ok=True)
  os.makedirs(buildfiles_dir, exist_ok=True)
  os.makedirs(image_cache_dir, exist_ok=True)
