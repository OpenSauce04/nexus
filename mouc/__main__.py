#!/usr/bin/env python3

import sys

from command.clean import cmd_clean
from command.enter import cmd_enter
import strings

if len(sys.argv) == 1:
  print(strings.program_usage)
  exit(0)

match sys.argv[1]:

  case 'enter':
    if len(sys.argv) == 2:
      print(strings.program_usage)
      exit(1)
    cmd_enter(sys.argv[2])

  case 'clean':
    cmd_clean()

  case _:
    print(strings.program_usage)