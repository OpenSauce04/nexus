import sys

from command.clean import cmd_clean
from command.enter import cmd_enter
from command.init import cmd_init
from command.rebuild import cmd_rebuild
import strings

if len(sys.argv) == 1:
  print(strings.program_usage)
  exit(0)

match sys.argv[1]:

  case 'clean':
    if len(sys.argv) == 2:
      print(strings.program_usage)
      exit(1)
    cmd_clean(sys.argv[2])

  case 'enter':
    if len(sys.argv) == 2:
      print(strings.program_usage)
      exit(1)
    cmd_enter(sys.argv[2])

  case 'rebuild':
    if len(sys.argv) == 2:
      print(strings.program_usage)
      exit(1)
    cmd_rebuild(sys.argv[2])

  case 'init':
    cmd_init()

  case _:
    print(strings.program_usage)