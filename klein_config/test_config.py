from test.support import EnvironmentVarGuard
import pytest
from .config import EnvironmentAwareConfig

env = EnvironmentVarGuard()
env.set('ENV_KEY', 'env_value')
initial_config = dict()
initial_config["key"] = "value"
initial_config["level1"] = dict()
initial_config["level1"]["level2"] = dict()
initial_config["level1"]["level2"]["key"] = "value"
config = EnvironmentAwareConfig(initial_config)


def test_for_valid_environment_key_with_dot_notation():
    assert config.get("env.key") == "env_value"


def test_for_invalid_key():
    with pytest.raises(LookupError, message="Expecting LookupError"):
        config.get("bad.key")


def test_for_valid_nested_config_level():
    assert config.get("level1.level2.key") == "value"
