# -*- coding: utf-8 -*-
"""
Environment aware config module to auto detect and manage both injected and Environment variable config
"""
import argparse
import json
import logging
import os
import pathlib

import yaml
from pyhocon import ConfigFactory, ConfigTree
from pyhocon.exceptions import ConfigMissingException

LOGGER = logging.getLogger(__name__)
COMMON_ENVVAR_NAME = "KLEIN_COMMON"
CONFIG_ENVVAR_NAME = "KLEIN_CONFIG"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="consumer specific configuration file (YAML)")
    parser.add_argument("--common", help="common configuration (YAML)")
    args, _ = parser.parse_known_args()
    return args


def get_config(initial=None):
    args = parse_args()

    # Handle legacy configs
    common_from_args = args.common
    config_from_args = args.config
    common_from_env = os.environ.get(COMMON_ENVVAR_NAME)
    config_from_env = os.environ.get(CONFIG_ENVVAR_NAME)
    if common_from_args or config_from_args:
        LOGGER.warning("Arguments --config and --common are deprecated. "
                       "Use environmental variables %s and %s instead", COMMON_ENVVAR_NAME, CONFIG_ENVVAR_NAME)
    if common_from_args and common_from_env:
        LOGGER.warning("Deprecated --common arg has shadowed the %s env var. Please use the latter only. ", COMMON_ENVVAR_NAME)
    if config_from_args and config_from_env:
        LOGGER.warning("Deprecated --config arg has shadowed the %s env var. Please use the latter only. ", CONFIG_ENVVAR_NAME)
    # End: Handle legacy configs

    common_file = common_from_args or common_from_env
    config_file = config_from_args or config_from_env

    conf = EnvironmentAwareConfig(filepath=common_file)
    if isinstance(initial, dict):
        ConfigTree.merge_configs(conf, ConfigTree(initial))
    return EnvironmentAwareConfig(filepath=config_file, initial=conf)


class EnvironmentAwareConfig(ConfigTree):
    """
    Config object to allow use of both YAML and HOCON formats
    """

    def __init__(self, filepath=None, initial=None, prefix=None):
        """
        Initialise Config object by building config from
        """
        self.prefix = prefix
        super().__init__()

        def load_file(path):
            if pathlib.Path(path).suffix in [".yml", ".yaml"]:
                with open(path, 'r') as f:
                    return ConfigFactory.from_dict(yaml.load(f, Loader=yaml.FullLoader))

            if pathlib.Path(path).suffix in [".json", ".js"]:
                with open(path, 'r') as f:
                    return ConfigFactory.from_dict(json.load(f))
            return ConfigFactory.parse_file(path)

        def apply(param):
            if not param:
                param = dict()

            c = ConfigFactory.from_dict(param) if (isinstance(param, dict)) else load_file(param)
            ConfigTree.merge_configs(self, c)

        apply(initial)
        apply(filepath)

    @staticmethod
    def _env_key(key, prefix=None):
        if isinstance(prefix, str):
            return ".".join([prefix, key]).upper().replace(".", "_")
        return key.upper().replace(".", "_")

    @staticmethod
    def _as_type(val: str):
        try:
            return int(val)
        except ValueError:
            pass

        try:
            return float(val)
        except ValueError:
            pass

        if val.lower() in ['true', 'yes', 'y']:
            return True

        if val.lower() in ['false', 'no', 'n']:
            return False

        return val

    def get(self, key, default=None):
        env_key = EnvironmentAwareConfig._env_key(key, self.prefix)
        if env_key in os.environ:
            return EnvironmentAwareConfig._as_type(os.getenv(env_key))
        try:
            result = super().get(key)
            if isinstance(result, dict):
                return EnvironmentAwareConfig(initial=result, prefix=key if self.prefix is None else ".".join([self.prefix, key]))
            return result
        except ConfigMissingException as err:
            if default is not None:
                return default
            raise err

    def __getitem__(self, item):
        try:
            return self.get(item)
        except ConfigMissingException as err:
            raise KeyError(item) from err

    def has(self, key):
        try:
            self.get(key)
            return True
        except ConfigMissingException:
            return False
