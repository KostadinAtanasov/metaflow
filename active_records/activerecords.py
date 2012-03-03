#!/usr/bin/env python
#
# activerecords.py
#
# Copyright Kostadin Atanasov(all rights reserved).
# author: Kostadin Atanasov.

# This program is released under terms of GPLv2. See LICENSE or visit:
# http://www.gnu.org/licenses/gpl.html

'''
Base class for all classes which want active record pattern.
'''

import sys
if sys.version_info >= (3,):
    from metaflow.active_records.activerecords_imp3 import ActiveRecord as ActiveRecord
else:
    from metaflow.active_records.activerecords_imp2 import ActiveRecord as ActiveRecord
