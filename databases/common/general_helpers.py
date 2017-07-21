# Helper functions 
__author__ = "Patryk Walaszkowski"
__email__ = "patryk.walaszkowski@misys.com, QAKPlusTech@misys.com"

import stat
import errno
import os
import fileinput
import sys

def CheckIsDir(directory):
  """ Function for check that directory exist or not"""
  try:
    return stat.S_ISDIR(os.stat(directory).st_mode)
  except OSError, e:
    if e.errno == errno.ENOENT:
      return False
    raise
