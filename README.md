# Klein Config

Module to provide config management

## Usage

```python
from klein_config import get_config

# Can be overriden with env variable MY_CONFIG_SETTING
config = get_config({"my": {"config": {"setting": "initialised value"}})

# Access via `get` accessor with no backup (raises ConfigMissingException if not found).
value = config.get("my.config.setting")

# Access via `get` accessor method with a backup.
backup_value = config.get("not.a.setting", "backup value")

# Access via `dict` (raises KeyError if not found).
same_value = config["my.config.setting"]

# Sub-configs are created if the value is another `dict`.
intermediate_config = config["my.config"]
same_value_again = intermediate_config["setting"]
```

### Structure
Internally the config object uses the ConfigTree structure that is part of pyhocon. This can be traversed easily with the get method using dot notation as outlined above.

### Config Initialisation
The `get_config` function looks for :
- argument `--common` or environmental variable `KLEIN_COMMON` to specify the common file; and
- argument `--config` or environmental variable `KLEIN_CONFIG` for the config file. 

However, passing both the environmental variables and the arguments for either config or common is NOT accepted as it is ambiguous what is expected.

You can also pass a `dict` into `get_config` function.

### Order precedence
The configs are applied to the config object as follows: 

1st: Common config as identified via argument `--common` or environmental variable `KLEIN_COMMON`
2nd: Config that is injected via the Class constructor
3rd: Config that is identified via the argument `--config` or environmental variable `KLEIN_CONFIG`

Configs will override any previous values as they are applied

### Environment Aware
The module is "Environment Aware" this means that it will test for envrionments variables first. If a valid variable exists then this will be used regardless of any config that may have been supplied.

The path is transformed by converting the string to uppercase and replacing all dots with underscores.

```
my.config.setting => MY_CONFIG_SETTING
```

Sub-config items are still overriden by the same environment variables as in the root config.

## Development
This project uses [pipenv](https://github.com/pypa/pipenv). To install it, run `pip install pipenv`.

### Development
```
pipenv install --dev
```

### Testing
```bash
pipenv run python -m pytest
```
For test coverage you can run:
```bash
pipenv shell
pipenv run python -m pytest --cov-report term --cov src/ tests/
```

### License
This project is licensed under the terms of the Apache 2 license, which can be found in the repository as `LICENSE.txt`
