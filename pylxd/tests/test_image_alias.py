# Copyright (c) 2015 Canonical Ltd
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from ddt import data
from ddt import ddt
import mock
import unittest

from pylxd import api
from pylxd import connection

from pylxd.tests import annotated_data
from pylxd.tests import fake_api


@ddt
class LXDUnitTestAlias(unittest.TestCase):

    def setUp(self):
        super(LXDUnitTestAlias, self).setUp()
        self.lxd = api.API()

    def test_alias_list(self):
        with mock.patch.object(connection.LXDConnection, 'get_object') as ms:
            ms.return_value = ('200', fake_api.fake_alias_list())
            self.assertEqual(['ubuntu'], self.lxd.alias_list())
            ms.assert_called_once_with('GET', '/1.0/images/aliases')

    @data(True, False)
    def test_alias_defined(self, expected):
        with mock.patch.object(connection.LXDConnection, 'get_status') as ms:
            ms.return_value = expected
            self.assertEqual(expected, self.lxd.alias_defined('fake'))
            ms.assert_called_once_with('GET', '/1.0/images/aliases/fake')

    def test_alias_show(self):
        with mock.patch.object(connection.LXDConnection, 'get_object') as ms:
            ms.return_value = ('200', fake_api.fake_alias())
            self.assertEqual(
                fake_api.fake_alias(), self.lxd.alias_show('fake')[1])
            ms.assert_called_once_with('GET', '/1.0/images/aliases/fake')

    @annotated_data(
        ('create', 'POST', '', ('fake',), ('"fake"',)),
        ('update', 'PUT', '/test-alias',
         ('test-alias', 'fake',), ('"fake"',)),
        ('rename', 'POST', '/test-alias',
         ('test-alias', 'fake',), ('"fake"',)),
        ('delete', 'DELETE', '/test-alias', ('test-alias',)),
    )
    def test_alias_operations(self, method, http, path, args, call_args=()):
        with mock.patch.object(connection.LXDConnection, 'get_status') as ms:
            ms.return_value = True
            self.assertTrue(getattr(self.lxd, 'alias_' + method)(*args))
            ms.assert_called_once_with(
                http,
                '/1.0/images/aliases' + path,
                *call_args
            )
