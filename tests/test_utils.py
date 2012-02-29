#!/usr/bin/env python
#
# test_utils.py
#
# Copyright Kostadin Atanasov(all rights reserved)
# author: Kostadin Atanasov
'''

'''

import traceback

def ensure_equal(val1, val2):
    if val1 != val2:
        err_msg = '{0} == {1} test faild!'.format(val1, val2)
        err_msg += traceback.format_stack()[::-1][1].strip()
        raise TestError(err_msg)

def ensure_boolean_validity(value):
    if not value:
        err_msg = 'Ensure boolean validity failed!\n'
        err_msg += traceback.format_stack()[::-1][1].strip()
        raise TestError(err_msg)

class TestError(Exception):
    def __init__(self, msg, errno=0):
        self.msg = msg
        self.errno = errno

    def __str__(self):
        return self.msg
