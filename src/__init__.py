import sys
import os
my_dir = os.path.abspath(os.path.dirname(__file__))
if not my_dir in sys.path:
    sys.path.append(my_dir)
