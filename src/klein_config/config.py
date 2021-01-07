# -*- coding: utf-8 -*-
"""
Environment aware config module to auto detect and manage both injected and Environment variable config
"""
import os
import argparse
import pathlib
import json
import yaml
from pyhocon import ConfigFactory, ConfigTree
from pyhocon.exceptions import ConfigMissingException


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="consumer specific configuration file (YAML)")
    parser.add_argument("--common", help="common configuration (YAML)")
    args, _ = parser.parse_known_args()
    return args


def get_config(initial=None):
    args = parse_args()
    conf = EnvironmentAwareConfig(filepath=args.common, initial=initial)
    return EnvironmentAwareConfig(filepath=args.config, initial=conf)


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

    def get(self, key, default=None):
        env_key = EnvironmentAwareConfig._env_key(key, self.prefix)
        if env_key in os.environ:
            return os.getenv(env_key)
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
        except ConfigMissingException:
            raise KeyError(item)

    def has(self, key):
        try:
            self.get(key)
            return True
        except ConfigMissingException:
            return False
