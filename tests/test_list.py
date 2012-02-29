#!/usr/bin/env python
#
# test_list.py
#
# Copyright Kostadin Atanasov(all rights reserved)
# author: Kostadin Atanasov
'''
Contain list of all test that should be run.
'''

# List of all tests that will be run. The format is:
# every element is tuple with first element test module
# name, and second it's directory. Tests are run according
# to their index in this list.
all_tests = [
                ('test_metainfo', 'test_meta'),
                ('test_dbgenerator', 'test_active_records'),
                ('test_activerecords', 'test_active_records'),
            ]
