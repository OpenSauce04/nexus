import subprocess

def qrun(args, silent_error = False):
  _stderr = None
  if silent_error:
    _stderr = subprocess.DEVNULL

  subprocess.run(args, stdout = subprocess.DEVNULL, stderr = _stderr)