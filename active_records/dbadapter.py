#!/usr/bin/env python
#
# dbadapter.py
#
# Copyright Kostadin Atanasov(all rights reserved).
# author: Kostadin Atanasov.

# This program is released under terms of GPLv2. See LICENSE or visit:
# http://www.gnu.org/licenses/gpl.html

'''
Module which adapt different databases for usage in ActiveRecords.
'''

from metaflow.active_records.activerecord_utils import ActiveRecordError

version = 0.1


class DbAdapter:
    supported_databases = ['sqlite'] # , 'mysql', 'postgre']

    def __init__(self, dbtype):
        self.set_database_type(dbtype)
        self.db = None

    def open_database(self, db_config):
        '''
        Open(make connection to database), if it does not exist
        it will be created.
        '''
        if self.db:
            if not self.db.is_same(db_config):
                self.db.close()
            self.db.use_database(db_config)
        else:
            self.db = make_adapter_impl(self.dbtype)
            self.db.use_database(db_config)

    def close(self):
        self.db.close()
        self.db = None

    def table_exist(self, name):
        return self.db.table_exist(name)

    def create_table(self, name, table_columns):
        '''
        Pass command to underlying database to create table - 'name',
        with columns hold as keys in the dictionary 'table_columns',
        the values of the later parameter are the types to be
        hold in the columns.
        '''
        return self.db.create_table(name, table_columns)

    def insert_in_table(self, name, columns):
        return self.db.insert_in_table(name, columns)

    def update_table(self, table, values, conditions):
        command = "update {0} set ".format(table)
        for k,v in values.items():
            command += str(k) + '=' + str(v) + ', '
        command = command.rstrip(', ')
        if conditions:
            if not self.get_row(table, conditions):
                msg = 'Row not found for update with given conditions {0}.'
                msg = msg.format(conditions)
                raise DbAdapterError(msg, DbAdapterError.row_not_found)
            command += ' where '
            for k,v in conditions.items():
                command += str(k) + '=' + str(v) +' and '
            command = command.rstrip(' and ')
        return self.db.execute(command)

    def get_columns_names(self, table):
        return [k for k in self.db.get_table_columns(table)]

    def get_columns(self, table):
        return self.db.get_table_columns(table)

    def get_row(self, table, conditions):
        '''
        Get single row(first returned) from table base on conditons.
        @table - name of the table from which will get.
        @conditions - dictionary with keys names for fields that are
                      used as conditions and values their values.
        @return - dictionary with keys names of the fields of desired rows
                  and values their correspondint values.
        '''
        command = "select * from {0}".format(table)
        if conditions:
            command += ' where '
            for k,v in conditions.items():
                command += str(k) + '=' + str(v) + ' and '
            command = command.rstrip(' and')
        result = self.db.execute(command)
        return result[0] if result else result

    def get_rows(self, table, conditions=None):
        '''
        Get all rows that correspond to given conditions.
        @table - name of the table from which will get.
        @conditions - dictionary with keys names for fields that are
                      used as conditions and values their values.
        @return - list of dictionary with keys names of the fields of desired
                  rows and values their correspondint values.
        '''
        if not conditions:
            command = "select * from {0}".format(table)
            return self.db.execute(command)
        msg = 'get_rows currently does not support conditions'
        raise DbAdapterError(msg, DbAdapterError.operation_not_supported)

    def get_row_values(self, table, values, conditions):
        '''
        Get all values from row that correspond to given conditions.
        @table - name of the table from which will get.
        @values - list of names for fields that we want to get.
        @conditions - dictionary with keys names for fields that are
                      used as conditions and values their values.
        @return - dictionary with keys names of the fields as in
                  values parameter and values their corresponding values.
        '''
        msg = 'get_row_values not yet implemented.'
        raise DbAdapterError(msg, DbAdapterError.operation_not_supported)

    def get_values(self, table, values, conditions):
        '''
        Get all values from all rows that correspond to given conditions.
        @table - name of the table from which will get.
        @values - list of names for fields that we want to get.
        @conditions - dictionary with keys names for fields that are
                      used as conditions and values their values.
        @return - list of dictionaries with keys names of the fields as in
                  values parameter and values their corresponding values.
        '''
        msg = 'get_values not yet implemented.'
        raise DbAdapterError(msg, DbAdapterError.operation_not_supported)

    def remove(self, table, conditions):
        '''
        Remove row(s) from the storage corresponding to given conditions.
        @table - name of table from which row(s) will be deleted.
        @conditions - dictionary with keys names for fields that are
                      used as conditions and values their values.
        '''
        command = 'delete from {0}'.format(table)
        if conditions:
            command += ' where '
            for k,v in conditions.items():
                command += str(k) + '=' + str(v) + ' and '
            command = command.rstrip(' and ')
        self.db.execute(command)
        return True

    def remove_all(self, table):
        self.db.execute('delete from {0}'.format(table))

    def execute(self, sqltext):
        '''
        Pass string to underlying database for execution, returning
        the result as python list object.
        @sqltext - sql stetement to be executed.
        @return - list representing the results of the statement.
        '''
        return self.db.execute(sqltext)

    def escape_string(self, text):
        return text.replace("'", "''")

    def set_database_type(self, dbtype):
        if dbtype not in DbAdapter.supported_databases:
            msg = 'Unsupported database type requested!'
            raise DbAdapterError(msg, DbAdapterError.operation_not_supported)
        self.dbtype = dbtype

class DbAdapterError(ActiveRecordError):
    '''
    Class for usage as exception.
    '''
    def __init__(self, msg, errno=-1):
        self.msg = msg
        self.errno = errno

    def __str__(self):
        return self.msg

    # Error codes.
    operation_not_supported       = 1
    row_not_found                 = 2
    row_not_found_with_conditions = 3
    database_not_supported        = 4

def make_adapter_impl(dbtype):
    '''
    Create and return appropriate database adaptor base on the string
    given as argument, raises exception if the given type is not supported.
    '''
    if dbtype == DbAdapter.supported_databases[0]:
        import metaflow.active_records.sqliteadapter as sqliteadapter
        return sqliteadapter.SqliteAdapter()
    else:
        raise DbAdapterError('Unsupported database type requested!')
