
"""
Read output of ms_print and repeat only lines with snapshot data.

"""

import re
import sys

for l in sys.stdin.readlines():
    if re.match(r'\s+\d+\s+\d+,', l):
        print l.strip()

