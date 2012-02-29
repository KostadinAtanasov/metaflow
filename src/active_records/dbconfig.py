#!/usr/bin/env python
#
# dbconfig.py
#
# Copyright Kostadin Atanasov(all rights reserved).
# author: Kostadin Atanasov.
'''
Module to hold agregation for database configurations.
'''

class DbConfig:
    '''
    Container for varius variables needed in defferent database configurations.
    '''
    def __init__(self, dbconnector, user='', port='',
                 datadir='', log='', errlog=''):
        self.dbconnector = dbconnector
        self.user=user
        self.port = port
        self.datadir = datadir
        self.log = log
        self.errlog = errlog
