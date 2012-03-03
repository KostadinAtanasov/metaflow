#!/usr/bin/env python
#
# test_activerecords.py
#
# Copyright Kostadin Atanasov(all rights reserved)
# author: Kostadin Atanasov

# This program is released under terms of GPLv2. See LICENSE or visit:
# http://www.gnu.org/licenses/gpl.html

'''
This test should be run after successful run of the test for DbGenerator
so we can be sure that there's tables 'posts', and 'persons' in the
testdb.ldb. Furthermore from the required test we also know that in the
table 'persons' there is row with values for 'name', and 'age' - Kosta,
and 30 respectively.
'''

# Import standard test utilities.
import test_utils

# Import the module that we test.
import metaflow.active_records.activerecords as activerecords

# Import modules that module under test depend for it's functionality.
from metaflow.active_records import dbadapter
from metaflow.active_records import dbconfig
# Import the error modules.
from metaflow.active_records.activerecord_utils import ActiveRecordError

# Import module generated from DbGenerator.
adapter = dbadapter.DbAdapter('sqlite')
adapter.open_database(dbconfig.DbConfig('testdb.ldb'))
activerecords.ActiveRecord.database = adapter
from person import Person

# Class to test setting properties based on table in database
# by simply inheriting from ActiveRecord.
class Post(activerecords.ActiveRecord):
    # Do not allow posts without title nor without content.
    ensure_presence_of = ['title', 'content']
    # Set that every post is own by person.
    owned_by = ['Person']

post_title = 'dbgenarator metalang parsing and activerecords extrackting'
post_content = '''  This post is part of table in database which is generated
with the help of metaflow framework, more precisely metaflow active_records
part, and to be absolutly precise - in python we'll say:
metaflow.active_records.dbgenerator.DbGenerator is the class which parse
Post class __metalang__, and create table for it in the database.
  The post is extracted from the database also with the help of metaflow, and
again going more precise - this post is represented in our program with class
which inherit from metaflow.active_records.activerecords.ActiveRecord, which
is different from the Post class used to generate the table in the database.
'''

def do_test():
    do_Person_tests()
    do_Post_tests()

def do_Person_tests():
    print('Listing all persons:')
    print(70*'-')
    for person in Person.find_all():
        print(person.name, person.age)
        print(70*'-')
    if Person.find(name='Kosta'):
        Person.remove_all(name='Kosta')
    Kosta = Person(name='Kosta', age=30)
    if not Kosta.save():
        raise test_utils.TestError('Unable to save ActiveRecord')
    del Kosta
    all_persons = Person.find_all()
    test_utils.ensure_boolean_validity(all_persons)
    for person in all_persons:
        if person.name == 'Kosta':
            Kosta = person
            break
    test_utils.ensure_equal(Kosta.age, 30)
    Kosta = Person.find(name='Kosta')
    test_utils.ensure_boolean_validity(Kosta)
    test_utils.ensure_equal(Kosta.age, 30)
    del Kosta
    Kosta = Person.find(age=30)
    test_utils.ensure_equal(Kosta.name, 'Kosta')
    Person.remove(name='Kosta', age=30)
    Vanq = Person.find(name='Vanq')
    if Vanq:
        Vanq.age += 1
        if Vanq.age == 30:
            Vanq.age += 1
        Vanq.update(name='Vanq')
    else:
        Vanq = Person(name='Vanq', age=1)
        Vanq.save()

def do_Post_tests():
    if Post.find(title='test_activerecords'):
        Post.remove(title='test_activerecords')
    post = Post()
    try:
        # This save should fail because we ensuring that posts
        # can not be saved when they have not 'title' nor 'content'.
        # And we miss both required fields.
        post.save()
        raise test_utils.TestError('Saved without required field!')
    except ActiveRecordError as err:
        if err.errno != ActiveRecordError.missing_required_field:
            raise
    post.title = 'test_activerecords'
    try:
        # This save should fail just like the previous one.
        # We miss 'content' field this time.
        post.save()
        raise test_utils.TestError('Saved without required field!')
    except ActiveRecordError as err:
        if err.errno != ActiveRecordError.missing_required_field:
            raise
    print('ensure_presence_of working properly.')
    post.content = 'test_activerecords content :-)'
    post.save()
    del post
    if not Post.find(title=post_title):
        post = Post()
        post.title = post_title
        post.content = post_content
        post.save()
        del post
    print('Listing all posts:\n' + 70*'-')
    for post in Post.find_all():
        print('Post with title: {0}'.format(post.title))
        print(70*'-')
        print(post.content)
        print(70*'-')
        if post.title != post_title:
                Post.remove(title=post.title)
    test_utils.ensure_boolean_validity(Post.find_all())
