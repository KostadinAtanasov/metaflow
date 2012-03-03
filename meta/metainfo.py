#!/usr/bin/env python
#
# metainfo.py
#
# Copyright Kostadin Atanasov(all rights reserved)
# author: Kostadin Atanasov

# This program is released under terms of GPLv2. See LICENSE or visit:
# http://www.gnu.org/licenses/gpl.html

'''
Module to define classes for access of meta information about classes,
such as: class name.
'''

class MetaInfo(object):
    @classmethod
    def class_name_to_lower(cls):
        return cls.__name__.lower()

    @classmethod
    def tablename_from_text(cls, text):
        text = text.lower()
        return text+'es' if text.endswith('s') else text+'s'
