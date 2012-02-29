#!/usr/bin/env python
#
# test_dbgenerator.py
#
# Copyright Kostadin Atanasov(all rights reserved)
# author: Kostadin Atanasov
'''

'''

# Import standard test utilities.
import test_utils

# Import the module that we test.
from active_records import dbgenerator
# Import modules that module under test depend for it's functionality.
from active_records import dbadapter
from active_records import dbconfig

# Class to test creatino of table from __metalang__ variable.
class Post(dbgenerator.DbGenerator):
    __metalang__ = '''
                   @title: string not null
                   @content: text
                   '''
    pass

class BadMetaLang(dbgenerator.DbGenerator):
    pass

# String to test creation of python class and database table from string.
db_text = '''Person, name: text, age: integer'''

def do_test():
    adapter = dbadapter.DbAdapter('sqlite')
    adapter.open_database(dbconfig.DbConfig('testdb.ldb'))
    Post.database = adapter
    dbgenerator.DbGenerator.database = adapter
    generator_tester = Post()
    test_utils.ensure_equal(generator_tester.get_table_name(), 'posts')
    generator_tester.table_from_metalang()
    dbgenerator.DbGenerator.make_class(db_text)
