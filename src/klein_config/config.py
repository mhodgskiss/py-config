# -*- coding: utf-8 -*-
'''
Environment aware config module to auto detect and manage both injected and Environment variable config
'''
import os
import argparse
import yaml
from klein_util.dict import traverse_dict

parser = argparse.ArgumentParser()
parser.add_argument("--config",help="consumer specific configuration file (YAML)")
parser.add_argument("--common", help="common configuration (YAML)")
ARGS, UNKNOWN = parser.parse_known_args()


def _env_key(key):
    return key.upper().replace(".", "_")


class EnvironmentAwareConfig(dict):

    def __init__(self, initial=None):
        def load_file(path):
            with open(path, 'r') as ymlfile:
                return yaml.load(ymlfile, Loader=yaml.FullLoader)

        self.__dict__ = dict()
        if ARGS.common:
            self.__dict__.update(load_file(ARGS.config))
        if initial:
            self.__dict__.update(initial)
        if ARGS.config:
            self.__dict__.update(load_file(ARGS.config))
        super().__init__()

    def _get_from_config(self, key):
        try:
            return traverse_dict(self.__dict__, key.split('.'))
        except LookupError:
            raise LookupError("Key '%s' does not exist in config" % (key))

    def get(self, key, default=None):
        env_key = _env_key(key)
        if env_key in os.environ:
            return os.getenv(env_key)
        try:
            return self._get_from_config(key)
        except LookupError as err:
            if default is not None:
                return default
            raise err

    def has(self, key):
        try:
            self.get(key)
            return True
        except LookupError:
            return False


config = EnvironmentAwareConfig()
