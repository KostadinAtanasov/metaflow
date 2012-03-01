#!/usr/bin/env python
#
# runtest.py
#
# Copyright Kostadin Atanasov(all rights reserved)
# author: Kostadin Atanasov

# This program is released under terms of GPLv2. See LICENSE or visit:
# http://www.gnu.org/licenses/gpl.html

'''
Run specific test which name is supplied as command line argument, or if test
name is not supplied run all test in test directory and it's subdirectories.
'''

import __init__
import sys
import os
from test_utils import TestError
from active_records import activerecord_utils
from test_list import all_tests

tests_executed = []
ignore_list = ['__init__.py', '__init__.pyc', 'runtest.py', 'test_utils.py']

def run_test(module_name):
    try:
        do_log('stdout', 70*'=')
        do_log('stdout', 'Running module "{0}"...'.format(module_name))
        test = __import__(module_name)
        test.do_test()
        do_log('stdout', 'Tests from "{0}" succeeded.'.format(module_name))
    except TestError as err:
        do_log('stderr', str(err))
    except ImportError as err:
        msg = 'No test "{0}" found.'.format(module_name)
        msg += '\npython error: ' + str(err) + '\n'
        do_log('stderr', msg)
    except activerecord_utils.ActiveRecordError as err:
        do_log('stderr', str(err))
    except Exception as err:
        msg = '\npython error: ' + str(err) + '\n'
        do_log('stderr', msg)
    do_log('stdout', 70*'=' + '\n' + 70*'*')

def run_test_in_dir(dir_name):
    try:
        walker = os.walk(dir_name)
        for d,sdl,fl in walker:
            for f in fl:
                if not f.endswith('.py') or f in tests_executed: continue
                if f in ignore_list: continue
                if f in tests_executed: continue
                if os.path.basename(d) != '.':
                    if not os.path.normpath(d) in sys.path:
                        sys.path.append(os.path.normpath(d))
                module_name = f[:f.find('.py')]
                run_test(module_name)
                tests_executed.append(f)
    except Exception as err:
        msg = '\npython error: ' + str(err) + '\n'
        do_log('stderr', msg)

def run_all_tests():
    cur_path = os.path.dirname(os.path.join(os.getcwd(), __file__))
    for i in xrange(len(all_tests)):
        test_dir = os.path.join(cur_path, all_tests[i][1])
        if not test_dir in sys.path:
            sys.path.append(test_dir)
        run_test(all_tests[i][0])

def do_log(out, msg):
    print(msg)

def main(argv):
    if not argv:
        run_all_tests()
    for module_name in argv:
        run_test(module_name)

if __name__ == '__main__':
    main(sys.argv[1:])
