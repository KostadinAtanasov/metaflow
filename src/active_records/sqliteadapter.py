#!/usr/bin/env python
#
# sqliteadapter.py
#
# Copyright Kostadin Atanasov(all rights reserved).
# author: Kostadin Atanasov.
'''
Module which adapt sqlite database for usage in activeRecords of metaflow.
'''

import sqlite3
import dbconfig

version = 0.1

class SqliteAdapter:
    def __init__(self):
        self.con = None
        self.cur = None
        self.dbname = None

    def use_database(self, db_config):
        self.con = sqlite3.connect(db_config.dbconnector)
        self.cur = self.con.cursor()
        self.dbname = db_config.dbconnector

    def execute(self, sqltext):
        self.cur.execute(sqltext)
        self.con.commit()
        return [row for row in self.cur]

    def close(self):
        if self.dbname:
            self.con.close()

    def create_table(self, name, table_columns):
        command = "create table " + name + " ("
        for k,v in table_columns.items():
            command += k + " " + v + ", "
        command = command.rstrip(", ")
        command += ")"
        return self.execute(command)

    def table_exist(self, name):
        command = "select name from sqlite_master where type='table'"
        result = self.execute(command)
        if result:
            for element in result:
                if name in element:
                    return True
        return False

    def get_table_columns(self, table):
        table_info = self.get_table_info(table)
        columns = [(column[1], column[2]) for column in table_info]
        return dict(columns)

    def get_table_info(self, table):
        return self.execute("pragma table_info('{0}')".format(table))

    def insert_in_table(self, name, table_columns):
        command = "insert into {0} (".format(name)
        values = "values ("
        for k,v in table_columns.items():
            command += k + ", "
            values += v + ", "
        command = command.rstrip(", ") + ")"
        values = values.rstrip(", ") + ")"
        command = command + " " + values
        self.execute(command)
        return True

    def get_property(self, table_name, property_name, obj_id=None):
        command = 'select {0}.{1} '.format(table_name, property_name)
        command += 'from {0}'.table_name
        if obj_id:
            command += ' where id={0}'.format(obj_id)
        return self.execute(command)

    def is_same(self, db_config):
        return self.dbname == db_config.dbconnector
