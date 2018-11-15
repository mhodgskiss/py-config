# -*- coding: utf-8 -*-
'''
Environment aware config module to auto detect and manage both injected and Environment variable config
'''
import os
import argparse
import yaml

parser = argparse.ArgumentParser()
parser.add_argument(
    "--config",
    help="consumer specific configuration file (YAML)")
parser.add_argument("--common", help="common configuration (YAML)")
args, unknown = parser.parse_known_args()

def _env_key(key):
    return key.upper().replace(".", "_")

def traverse(data, parts, path):
    remaining = len(parts)
    subkey = parts.pop(0)
    if subkey not in data:
        raise LookupError("Key '%s' does not exist in config" % (path))
    return traverse(
        data[subkey], parts, path) if remaining > 1 else data[subkey]


class EnvironmentAwareConfig(dict):

    def __init__(self, initial=None):
        def load_file(path):
            with open(path, 'r') as ymlfile:
                return yaml.load(ymlfile)

        self.__dict__ = dict()
        if args.common:
            self.__dict__.update(load_file(args.config))
        if initial:
            self.__dict__.update(initial)
        if args.config:
            self.__dict__.update(load_file(args.config))
        super().__init__()

    def _get_from_config(self, key):
        return traverse(self.__dict__, key.split('.'), key)        


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
        env_key = _env_key(key)
        if env_key in os.environ:
            return True
        try :
            traverse(self.__dict__, key.split('.'), key)
            return True
        except LookupError:
            return False
        
config = EnvironmentAwareConfig()
