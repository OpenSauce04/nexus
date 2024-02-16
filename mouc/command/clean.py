from glob import glob
import os
from os.path import join as join_path

from strings import *

def cmd_clean():
  files = glob(join_path(image_cache_dir, '*'))
  for f in files:
    os.remove(f)