#!/usr/bin/env python
#
# test_metainfo.py
#
# Copyright Kostadin Atanasov(all rights reserved)
# author: Kostadin Atanasov

# This program is released under terms of GPLv2. See LICENSE or visit:
# http://www.gnu.org/licenses/gpl.html

'''

'''

from meta import metainfo
import test_utils

class TestMetaInfo(metainfo.MetaInfo):
    pass

def do_test():
    test_utils.ensure_equal(TestMetaInfo.class_name_to_lower(), 'testmetainfo')
