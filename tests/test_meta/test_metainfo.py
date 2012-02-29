#!/usr/bin/env python
#
# test_metainfo.py
#
# Copyright Kostadin Atanasov(all rights reserved)
# author: Kostadin Atanasov
'''

'''

from meta import metainfo
import test_utils

class TestMetaInfo(metainfo.MetaInfo):
    pass

def do_test():
    test_utils.ensure_equal(TestMetaInfo.class_name_to_lower(), 'testmetainfo')
