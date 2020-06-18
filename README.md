# Klein Config

Module to provide config management

## Usage

```
from klein_config import config

config.get("my.config.setting", "default value")
```

## Structure

Internally the config object uses the ConfigTree structure that is part of pyhocon. This can be traversed easily with the get method using dot notation as outlined above.

## Argparse

The module it looks for arguments passed to the script via the command line as soon as it is imported

```
parser = argparse.ArgumentParser()
parser.add_argument("--config", help="consumer specific configuration file")
parser.add_argument("--common", help="common configuration")
args, unknown = parser.parse_known_args()
```

## Order precidence

The configs are applied to the config object as follows: 

1st: Common config as identified via argument `--common`
2nd: Config that is injected via the Class constructor
3rd: Config that is identified via the argument `--config`

Configs will override any previous values as they are applied

## Environment Aware

The module is "Environment Aware" this means that it will test for envrionments variables first. If a valid variable exists then this will be used regardless of any config that may have been supplied

This only takes place when using the `get` method using a  dot notated path. The path is transformed by converting the string to uppercase and replacing all dots with underscores.

```
my.config.setting => MY_CONFIG_SETTING
```

## Changelog

### 2.0.0

* implements ability to load JSON and HOCON config structures
* moves argparsing into EnvironmentAwareConfig Object
* converts internal nested dicts into ConfigTree structures
* reduces exposed API of for the EnvironmentAwareConfig


## Development


Utilises python 3.7

### Ubuntu

```
sudo apt install python3.7
```

## Virtualenv

```
virtualenv -p python3.7 venv
source venv/bin/activate
echo -e "[global]\nindex = https://nexus.mdcatapult.io/repository/pypi-all/pypi\nindex-url = https://nexus.mdcatapult.io/repository/pypi-all/simple" > venv/pip.conf
pip install -r requirements.txt
```

### Testing
```bash
python -m pytest
```
For test coverage you can run:
```bash
python -m pytest --cov-report term --cov src/ tests/
```