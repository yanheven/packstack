# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013, Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
import shutil
import tempfile
from unittest import TestCase

from test_base import PackstackTestCaseMixin
from packstack.installer.engine_validators import *


class ValidatorsTestCase(PackstackTestCaseMixin, TestCase):
    def setUp(self):
        # Creating a temp directory that can be used by tests
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        # remove the temp directory
        shutil.rmtree(self.tempdir)

    def test_validate_integer(self):
        validate_integer('1')
        self.assertRaises(ParamValidationError, validate_integer, 'test')

    def test_validate_regexp(self):
        validate_regexp('Test_123', options=['\w'])
        self.assertRaises(ParamValidationError, validate_regexp,
                          '!#$%', options=['\w'])

    def test_validate_port(self):
        validate_port('666')
        self.assertRaises(ParamValidationError, validate_port, 'test')
        self.assertRaises(ParamValidationError, validate_port, '-3')

    def test_validate_not_empty(self):
        validate_not_empty('test')
        validate_not_empty(False)
        self.assertRaises(ParamValidationError, validate_not_empty, '')
        self.assertRaises(ParamValidationError, validate_not_empty, [])
        self.assertRaises(ParamValidationError, validate_not_empty, {})

    def test_validate_options(self):
        validate_options('a', options=['a', 'b'])
        validate_options('b', options=['a', 'b'])
        self.assertRaises(ParamValidationError, validate_options,
                          'c', options=['a', 'b'])

    def test_validate_ip(self):
        validate_ip('127.0.0.1')
        validate_ip('::1')
        self.assertRaises(ParamValidationError, validate_ip, 'test')

    def test_validate_file(self):
        fname = os.path.join(self.tempdir, '.test_validate_file')
        bad_name = os.path.join(self.tempdir, '.me_no_exists')
        with open(fname, 'w') as f:
            f.write('test')
        validate_file(fname)
        self.assertRaises(ParamValidationError, validate_file, bad_name)

    def test_validate_ping(self):
        # ping to broadcast fails
        self.assertRaises(ParamValidationError, validate_ping, '192.168.122.0')

    def test_validate_ssh(self):
        # ssh to broadcast fails
        self.assertRaises(ParamValidationError, validate_ssh, '192.168.122.0')
