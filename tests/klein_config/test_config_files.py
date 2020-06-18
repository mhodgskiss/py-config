import mock
import argparse

yamlString = """
key: value
level1:
  level2:
    key: value
"""

jsonString = """
{
    "key":"value",
    "level1": {
        "level2": {
            "key": "value"
        }
    }
}
"""

hoconString = '''
{
    key = value
    level1 {
        level2 = {
            key: ${key}
        }
    }
    altkey = substituted ${key}
}
'''


class TestConfigWithFiles():

    @mock.patch('argparse.ArgumentParser.parse_known_args',
                return_value=(argparse.Namespace(config="dummy.yml", common=None), argparse.Namespace()))
    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data=yamlString)
    def test_with_yaml_file(self, mock_open, mock_args):
        from src.klein_config.config import EnvironmentAwareConfig
        config = EnvironmentAwareConfig()
        mock_open.assert_called_with('dummy.yml', 'r')
        assert config.get("key") == "value"
        assert config.get("level1.level2.key") == "value"

    @mock.patch('argparse.ArgumentParser.parse_known_args',
                return_value=(argparse.Namespace(config="dummy.json", common=None), argparse.Namespace()))
    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data=jsonString)
    def test_with_json_file(self, mock_open, mock_args):
        from src.klein_config.config import EnvironmentAwareConfig
        config = EnvironmentAwareConfig()
        mock_open.assert_called_with('dummy.json', 'r')
        assert config.get("key") == "value"
        assert config.get("level1.level2.key") == "value"

    @mock.patch('argparse.ArgumentParser.parse_known_args',
                return_value=(argparse.Namespace(config="dummy.conf", common=None), argparse.Namespace()))
    @mock.patch('codecs.open', new_callable=mock.mock_open, read_data=hoconString)
    def test_with_hocon_file(self, mock_open, mock_args):
        from src.klein_config.config import EnvironmentAwareConfig
        config = EnvironmentAwareConfig()
        mock_open.assert_called_with('dummy.conf', 'r', encoding="utf-8")
        assert config.get("key") == "value"
        assert config.get("altkey") == "substituted value"
        assert config.get("level1.level2.key") == "value"

    @mock.patch('argparse.ArgumentParser.parse_known_args',
                return_value=(argparse.Namespace(config="dummy.conf", common="dummy2.conf"), argparse.Namespace()))
    @mock.patch('codecs.open', new_callable=mock.mock_open, read_data=hoconString)
    def test_with_hocon_files_config_and_common(self, mock_open, mock_args):
        from src.klein_config.config import EnvironmentAwareConfig
        config = EnvironmentAwareConfig()
        mock_open.assert_any_call('dummy2.conf', 'r', encoding="utf-8")
        mock_open.assert_any_call('dummy.conf', 'r', encoding="utf-8")
        assert config.get("key") == "value"
        assert config.get("altkey") == "substituted value"
        assert config.get("level1.level2.key") == "value"
