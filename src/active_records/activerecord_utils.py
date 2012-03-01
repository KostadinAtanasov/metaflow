#!/usr/bin/env python
#
# activerecord_utils.py
#
# Copyright Kostadin Atanasov(all rights reserved)
# author: Kostadin Atanasov

# This program is released under terms of GPLv2. See LICENSE or visit:
# http://www.gnu.org/licenses/gpl.html

'''

'''

class ActiveRecordError(Exception):
    def __init__(self, msg, errno=-1):
        self.msg = msg
        self.errno = errno

    def __str__(self):
        return self.msg

    # Error numbers.
    database_not_set          = 0
    table_not_found           = 1
    unsupported_keyword       = 2
    conditions_required       = 3
    conditions_not_applicable = 4
    missing_required_field    = 5
