from glob import glob
import os
from os.path import join as join_path

from strings import *
from utils import *

def cmd_clean():
  files = glob(join_path(image_cache_dir, '*'))
  qrun(['docker', 'kill', 'mouc-env'], silent_error=True)
  for f in files:
    os.remove(f)