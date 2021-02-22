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
