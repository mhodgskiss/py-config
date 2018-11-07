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
        def traverse(data, parts):
            remaining = len(parts)
            subkey = parts.pop(0)
            if subkey not in data:
                raise LookupError("Key '%s' does not exist in config" % (key))
            return traverse(
                data[subkey], parts) if remaining > 1 else data[subkey]
        return traverse(self.__dict__, key.split('.'))

    def get(self, key):
        env_key = key.upper().replace(".", "_")
        if env_key in os.environ:
            return os.getenv(env_key)
        return self._get_from_config(key)


config = EnvironmentAwareConfig()
