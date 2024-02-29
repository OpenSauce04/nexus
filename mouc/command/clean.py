from glob import glob
import os
from os.path import join as join_path

from strings import *
from utils import *

def cmd_clean(mode):
  match mode:
    case 'cache':
      files = glob(join_path(image_cache_dir, '*'))
      for f in files:
        os.remove(f)

    case 'docker':
      qrun(['docker', 'kill', 'mouc-env'], silent_error=True)

    case 'all':
      cmd_clean('cache')
      cmd_clean('docker')