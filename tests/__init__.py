#!/usr/bin/env python
#
# __init__.py
#
# Copyright Kostadin Atanasov(all rights reserved)
# author: Kostadin Atanasov
'''
Initialization of metaflow test module.
'''

import sys
sys.dont_write_bytecode = True
import os

par_dir = os.path.abspath('..')
src_dir = os.path.abspath('../src')

if not src_dir in sys.path:
    sys.path.append(src_dir)

if not par_dir in sys.path:
    sys.path.append(par_dir)
