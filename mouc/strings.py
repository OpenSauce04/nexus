import os
from os.path import *

# Environment
username = os.environ.get('SUDO_USER', os.environ.get('USERNAME'))

# Paths
home_dir = expanduser(f'~{username}')
mouc_dir = home_dir+'/.mouc'
dockerfiles_dir = mouc_dir+'/dockerfiles'

# Messages
program_usage = "Usage: enter"