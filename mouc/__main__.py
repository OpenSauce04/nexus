import sys

from command.clean import cmd_clean
from command.enter import cmd_enter
from command.init import cmd_init
from command.rebuild import cmd_rebuild
from strings import *
from utils import *

if len(sys.argv) == 1:
  print(program_usage_msg)
  exit(0)

match sys.argv[1]:

  case 'clean':
    if len(sys.argv) == 2:
      print(program_usage_msg)
      exit(1)
    cmd_clean(sys.argv[2])

  case 'enter':
    start_mouc_env()
    if len(sys.argv) == 2:
      print(program_usage_msg)
      exit(1)
    cmd_enter(sys.argv[2])

  case 'rebuild':
    start_mouc_env()
    if len(sys.argv) == 2:
      print(program_usage_msg)
      exit(1)
    if len(sys.argv) >= 4:
      option = sys.argv[3]
    else:
      option = ''
    cmd_rebuild(sys.argv[2], option)

  case 'init':
    cmd_init()

  case _:
    print(program_usage_msg)