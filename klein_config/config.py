# -*- coding: utf-8 -*-
import configparser
import os.path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--config", help="consumer specific configuration file")
parser.add_argument("--common", help="common configuration")
args, unknown = parser.parse_known_args()

config = configparser.ConfigParser()
config.read(args.config)

if args.common:
    common = configparser.ConfigParser()
    common.read(args.common)
    common.update(config)
    config = common




