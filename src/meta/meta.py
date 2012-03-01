#!/usr/bin/env python
#
# meta.py
#
# Copyright Kostadin Atanasov(all rights reserved).
# author: Kostadin Atanasov.

# This program is released under terms of GPLv2. See LICENSE or visit:
# http://www.gnu.org/licenses/gpl.html

# Helper dummy classes
class NewStyleClass(object):
    pass

class OldStyleClass:
    pass

new_style_class = type(NewStyleClass)
old_style_class = type(OldStyleClass)

def is_class(cls_candidate):
    cls_type = type(cls_candidate)
    if (cls_type == new_style_class) or (cls_type == old_style_class):
        return True
    else:
        return False

def base_classes_iterator(cls):
    return (base for base in cls.__bases__)

def base_classes_list(cls):
    return [base for base in cls.__bases__]
