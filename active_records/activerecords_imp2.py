#!/usr/bin/env python
#
# activerecords_imp2.py
#
# Copyright Kostadin Atanasov(all rights reserved).
# author: Kostadin Atanasov.

# This program is released under terms of GPLv2. See LICENSE or visit:
# http://www.gnu.org/licenses/gpl.html

'''
Actual implementation of ActiveRecord class for python 2.x.
'''

from metaflow.meta import metainfo
from metaflow.active_records.activerecord_utils import ActiveRecordError

def initialize_builder(validator, bases):
    def initialize(obj, **key_values):
        for base in bases:
            base.__init__(obj)
        for k,v in key_values.items():
            if not k in validator:
                msg = 'Unsupported keyword argument in object initialization.'
                raise ActiveRecordError(msg, ActiveRecordError.unsupported_keyword)
            setattr(obj, k, v)
    return initialize

class PropertieGenerator(type):
    def __new__(cls, name, bases, d):
        if name != 'ActiveRecord':
            table = metainfo.MetaInfo.tablename_from_text(name)
            if not ActiveRecord.database.table_exist(table):
                msg = 'No table {0} found in database: '.format(table)
                msg += '{0}.'.format(ActiveRecord.database)
                raise ActiveRecordError(msg, ActiveRecordError.table_not_found)
            columns = ActiveRecord.database.get_columns_names(table)
            # TODO: according to bases of the class add property to every
            # instance of it to be able to represent object hierarchy in the
            # database.
            if not '__init__' in d:
                d['__init__'] = initialize_builder(columns, bases)
            # List representing classes that own the current class.
            if 'owned_by' in d:
                print("owned_by -> " + str(d['owned_by']))
            # List representing classes which are own by the current class.
            if 'own_one' in d:
                print("own_one -> " + str(d['own_one']))
            # List representing classes which are own by the current class as
            # many instances.
            if 'own_many' in d:
                print("own_many -> " + str(d['own_many']))
        return type.__new__(cls, name, bases, d)

    @classmethod
    def class_columns_names(cls, base):
        columns = None
        if base.__name__ != 'ActiveRecord':
            table = metainfo.MetaInfo.tablename_from_text(base.__name__)
            if not ActiveRecord.database.table_exist(table):
                msg = 'No table {0} found in database: '.format(table)
                msg += '{0}.'.format(ActiveRecord.database)
                raise ActiveRecordError(msg, ActiveRecordError.table_not_found)
            columns = ActiveRecord.database.get_columns_names(table)
        return columns

class ActiveRecord(metainfo.MetaInfo):
    database = None # Instance of DbAdapter class.
    __metaclass__ = PropertieGenerator
    # List representing required fields in the current class.
    ensure_presence_of = []

    def __init__(self):
        if not ActiveRecord.database:
            msg = 'ActiveRecord can not be used when database is not set!'
            raise ActiveRecordError(msg, ActiveRecordError.database_not_set)
        self.pending = []
        metainfo.MetaInfo.__init__(self)

    def save(self):
        if hasattr(self, 'id'):
            if self.find(id=self.id):
                return self.update(id=self.id)
        return self.insert()

    def insert(self):
        self.do_ensures()
        table = self.get_table_name()
        if not ActiveRecord.database.table_exist(table):
            msg = '{0} table not found in database.'.format(table)
            msg += "Perhaps you didn't update it after last change?"
            raise ActiveRecordError(msg, ActiveRecordError.table_not_found)
        to_insert = self.make_row_dict(table)
        return self.database.insert_in_table(table, to_insert)

    def update(self, **conditions):
        self.do_ensures()
        table = self.get_table_name()
        if not ActiveRecord.database.table_exist(table):
            msg = '{0} table not found in database.'.format(table)
            msg += "Perhaps you didn't update it after last change?"
            raise ActiveRecordError(msg, ActiveRecordError.table_not_found)
        to_update = self.make_row_dict(table)
        self.quote_strings(table, conditions)
        return self.database.update_table(table, to_update, conditions)

    def make_row_dict(self, table):
        columns = self.database.get_columns(table)
        row_dict = {}
        for k,v in columns.items():
            if v == 'string' or v == 'text':
                value = self.database.escape_string(str(getattr(self, k)))
                row_dict[k] = "'" + value + "'"
            else:
                row_dict[k] = str(getattr(self, k))
        return row_dict

    def quote_strings(self, table, query):
        columns = self.database.get_columns(table)
        for k,v in columns.items():
            if k in query:
                if v == 'string' or v == 'text':
                    query[k] = "'" + query[k] + "'"

    @classmethod
    def get_table_name(cls):
        cls_name = cls.class_name_to_lower()
        if cls_name.endswith('s'): return cls_name+'es'
        else: return cls_name+'s'

    # Database helper functions.
    @classmethod
    def find_all(cls, **conditions):
        table = cls.get_table_name()
        attributes = [k for k in cls.database.get_columns(table)]
        db_result = cls.database.get_rows(table, conditions)
        result = []
        for el in db_result:
            obj = cls()
            for i in xrange(len(attributes)):
                setattr(obj, attributes[i], el[i])
            result.append(obj)
        return result

    @classmethod
    def find(cls, **key_values):
        table = cls.get_table_name()
        columns = cls.database.get_columns(table)
        if not key_values:
            db_result = cls.database.get_row(table)
        else:
            cls.validate_query_conditions(key_values, columns)
            query = {}
            for k,v in key_values.items():
                query[k] = str(v)
                if columns[k] == 'string' or columns[k] == 'text':
                        query[k] = "'" + query[k] + "'"
            db_result = cls.database.get_row(table, query)
        if not db_result:
            return None
        index = 0
        obj = cls()
        for k in columns:
            setattr(obj, k, db_result[index])
            index += 1
        return obj

    @classmethod
    def remove_all(cls, **key_values):
        if not key_values:
            cls.database.remove_all(cls.get_table_name())
        else:
            table = cls.get_table_name()
            columns = cls.database.get_columns(table)
            cls.validate_query_conditions(key_values, columns)
            for k in key_values:
                if columns[k] == 'string' or columns[k] == 'text':
                    key_values[k] = "'" + key_values[k] + "'"
            cls.database.remove(table, key_values)

    @classmethod
    def remove(cls, **key_values):
        if not key_values:
            msg = 'Conditions are required for remove operation!'
            raise ActiveRecordError(msg, ActiveRecordError.missing_required_field)
        table = cls.get_table_name()
        columns = cls.database.get_columns(table)
        cls.validate_query_conditions(key_values, columns)
        for k in key_values:
            if columns[k] == 'string' or columns[k] == 'text':
                key_values[k] = "'" + key_values[k] + "'"
        cls.database.remove(table, key_values)

    @classmethod
    def validate_query_conditions(cls, conditions, columns):
        for k in conditions:
            if not k in columns:
                    msg = "'{0}' condition not applicable for {1} class!"
                    msg = msg.format(k, cls.class_name_to_lower().capitalize())
                    raise ActiveRecordError(msg, ActiveRecordError.conditions_not_applicable)

    def do_ensures(self):
        for field in self.ensure_presence_of:
            if not getattr(self, field, None):
                msg = '{0} is required field!'.format(field)
                raise ActiveRecordError(msg, ActiveRecordError.missing_required_field)
