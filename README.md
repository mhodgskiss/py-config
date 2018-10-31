# Klein Config

Module to detect cli argument for file based configuration and generate config object

```
parser = argparse.ArgumentParser()
parser.add_argument("--config", help="consumer specific configuration file")
parser.add_argument("--common", help="common configuration")
args, unknown = parser.parse_known_args()
```