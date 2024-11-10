import sys

path = '/app'
if path not in sys.path:
    sys.path.append(path)

from bot import app as application