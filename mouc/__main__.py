#!/usr/bin/env python3

import sys
import messages
from command.enter import cmd_enter

if len(sys.argv) == 1:
  print(messages.program_usage)
  exit(0)

match sys.argv[1]:

  case 'enter':
    if len(sys.argv) == 2:
      print(messages.program_usage)
      exit(1)
    cmd_enter(sys.argv[2])

  case _:
    print(messages.program_usage)