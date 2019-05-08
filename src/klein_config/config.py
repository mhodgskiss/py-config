# -*- coding: utf-8 -*-
'''
Environment aware config module to auto detect and manage both injected and Environment variable config
'''
import os
import argparse
import pathlib
import json
import yaml
from pyhocon import ConfigFactory, ConfigTree
from pyhocon.exceptions import ConfigMissingException

class EnvironmentAwareConfig(dict):
    '''
    Config object to allow use of both YAML and HOCON formats
    '''

    def __init__(self, initial=None):
        '''
        Initialise Config object by building config from 
        '''
        args = EnvironmentAwareConfig.parse_args()

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

            if any(self.__dict__):
                self.__dict__ = ConfigTree.merge_configs(self.__dict__, c)
            else:
                self.__dict__ = c

        self.__dict__ = dict()
        apply(args.common)
        apply(initial)
        apply(args.config)

        super().__init__()

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument("--config",help="consumer specific configuration file (YAML)")
        parser.add_argument("--common", help="common configuration (YAML)")
        args , _ = parser.parse_known_args()
        return args

    @staticmethod
    def _env_key(key):
        return key.upper().replace(".", "_")

    def get(self, key, default=None):       
        env_key = EnvironmentAwareConfig._env_key(key)
        if env_key in os.environ:
            return os.getenv(env_key)
        try:
            return self.__dict__.get(key)
        except ConfigMissingException as err:
            if default is not None:
                return default
            raise err

    def has(self, key):
        try:
            self.get(key)
            return True
        except ConfigMissingException:
            return False
            


config = EnvironmentAwareConfig()
