#!/usr/bin/env python
#
# metalang.py
#
# Copyright Kostadin Atanasov(all rights reserved)
# author: Kostadin Atanasov

# This program is released under terms of GPLv2. See LICENSE or visit:
# http://www.gnu.org/licenses/gpl.html


'''

'''

from active_records.activerecord_utils import ActiveRecordError

class MetaLang(type):
    @classmethod
    def parse_metalang(cls, lang):
        if not lang:
            err = 'Missing __metalang__ propertie for parsing'
            raise MetaLangError(err)
        line_list = lang.split('\n')
        result = dict()
        for i in xrange(len(line_list)):
            line = line_list[i].strip()
            if line.startswith('@'):
                line = line[1:].split(':')
                if len(line) != 2:
                    err = 'Malformed metalang at line number {0} '
                    err = err.format(i)
                    err += 'line is:\n{0}'.format(line_list[i].strip())
                    raise MetaLangError(err)
                result[line[0].strip()] = line[1].strip()
        return result

    @classmethod
    def parse_metastring(cls, text):
        if not text: raise MetaLangError('Missing text for parsing.')
        var_list = text.split(',')
        result = dict()
        result['table'] = var_list[0]
        for var_def in var_list[1:]:
            var = var_def.split(':')
            result[var[0].strip()] = var[1].strip()
        return result

class MetaLangError(ActiveRecordError):
    def __init__(self, msg, errno=-1):
        self.msg = msg
        self.errno = errno

    def __str__(self):
        return self.msg
