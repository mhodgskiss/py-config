# copyright 2022 Medicines Discovery Catapult
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-

import os
import mock
from src.klein_config.config import EnvironmentAwareConfig

config = EnvironmentAwareConfig()


@mock.patch.dict(os.environ, {'TEST_STRING': 'hello'})
def test_overridden_string_is_string():
    assert config.get("test.string") == "hello"


@mock.patch.dict(os.environ, {'TEST_INT': '10'})
def test_overridden_int_is_int():
    assert config.get("test.int") == 10


@mock.patch.dict(os.environ, {'TEST_FLOAT': '10.232'})
def test_overridden_float_is_float():
    assert config.get("test.float") == 10.232


@mock.patch.dict(os.environ, {'TEST_BOOL': 'true'})
def test_overridden_bool_is_bool_1():
    assert config.get("test.bool") is True


@mock.patch.dict(os.environ, {'TEST_BOOL': 'yes'})
def test_overridden_bool_is_bool_2():
    assert config.get("test.bool") is True


@mock.patch.dict(os.environ, {'TEST_BOOL': 'y'})
def test_overridden_bool_is_bool_3():
    assert config.get("test.bool") is True


@mock.patch.dict(os.environ, {'TEST_BOOL': 'false'})
def test_overridden_bool_is_bool_4():
    assert config.get("test.bool") is False


@mock.patch.dict(os.environ, {'TEST_BOOL': 'no'})
def test_overridden_bool_is_bool_5():
    assert config.get("test.bool") is False


@mock.patch.dict(os.environ, {'TEST_BOOL': 'n'})
def test_overridden_bool_is_bool_6():
    assert config.get("test.bool") is False


@mock.patch.dict(os.environ, {'TEST_BOOL': 'TRUE'})
def test_overridden_bool_is_bool_1():
    assert config.get("test.bool") is True


@mock.patch.dict(os.environ, {'TEST_BOOL': 'FALSE'})
def test_overridden_bool_is_bool_1():
    assert config.get("test.bool") is False


@mock.patch.dict(os.environ, {'TEST_BOOL': 'tre'})
def test_incorrectly_spelled_overridden_bool_is_string():
    assert config.get("test.bool") == 'tre'
