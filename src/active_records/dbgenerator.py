#!/usr/bin/env python
#
# dbgenerator.py
#
# Copyright Kostadin Atanasov(all rights reserved)
# author: Kostadin Atanasov

# This program is released under terms of GPLv2. See LICENSE or visit:
# http://www.gnu.org/licenses/gpl.html

'''
Module to create database or table in existing database from provided
string(the string could be pass to function of DbGenerator derived class).
'''

from meta import metainfo
from meta import metalang
from activerecord_utils import ActiveRecordError

class DbGenerator(metainfo.MetaInfo):
    database = None # Instance of DbAdapter class.

    def __init__(self):
        if not self.database:
            msg = 'DbGenerator can not be used when database is not set!'
            raise DbGeneratorError(msg, DbGeneratorError.database_not_set)
        self.pending = []

    def set_database(self, dbconfig):
        '''
        Set database for usage(will be created if not exist).
        @dbconfig - instance of DbConfig class which describe the database.
        '''
        self.dbconfig = dbconfig
        self.database.open_database(dbconfig)

    @classmethod
    def get_table_name(cls):
        cls_name = cls.class_name_to_lower()
        if cls_name.endswith('s'): return cls_name+'es'
        else: return cls_name+'s'

    @classmethod
    def make_class(cls, text, location='./'):
        values = metalang.MetaLang.parse_metastring(text)
        name = values['table'].lower()
        table = name + 'es' if name.endswith('s') else name + 's'
        del values['table']
        if not cls.database.table_exist(table):
            cls.database.create_table(table, values)
        if not location.endswith('/'): location = location + '/'
        bases = [('ActiveRecord', 'metaflow.active_records.activerecords')]
        ClassFileBuilder.build(name.capitalize(), location, bases)

    def create_table_from_text(self, table_name, text):
        '''
        Creates table from given text. Text should be of the form:
        element_name:value, element_name:value...
        Important - the text is not validated here, all the checks,
        like ensuring no sql injection will happen, should be done
        before this function is called.
        '''
        text = text.split(',')
        table = dict()
        for element in text:
            table.__setitem__(*[el.strip() for el in element.split(':')])
        self.database.create_table(table_name, table)

    def table_from_metalang(self):
        if not self.database.table_exist(self.get_table_name()):
            table= metalang.MetaLang.parse_metalang(self.__metalang__)
            self.database.create_table(self.get_table_name(), table)

class ClassFileBuilder(object):
    indentation = '    '
    @classmethod
    def build(cls, name, location, bases=None, properties=None):
        '''
        '''
        f = open(location + name.lower() + '.py', 'w')
        imports = ''
        base_classes = ''
        if bases:
            base_classes = '('
            for base in bases:
                imports += 'from ' + base[1] +' import ' + base[0] + '\n'
                base_classes += base[0] + ', '
            base_classes = base_classes.strip(', ') + ')'
        cls_def = 'class ' + name + base_classes + ':' + '\n'
        cls_impl = ''
        if properties:
            pass
        else:
            cls_impl = 'pass'
        cls_def += cls.indentation + cls_impl
        f.write(imports + '\n' + cls_def + '\n')

class DbGeneratorError(ActiveRecordError):
    def __init__(self, msg, errno=-1):
        self.msg = msg

    def __str__(self):
        return self.msg

    # Error numbers.
    database_not_set = 0
