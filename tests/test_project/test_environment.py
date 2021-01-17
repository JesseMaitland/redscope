import os
from unittest import TestCase
from unittest.mock import patch, Mock
from pathlib import Path
from configparser import ConfigParser

# test all functions in the environment module
from redscope.project.environment import (
    get_redshift_connection,
    get_redscope_config,
    load_redscope_env,
    init_redscope_env
)


class TestGetRedshiftConfig(TestCase):

    def setUp(self) -> None:
        self.config_path = Path(__file__).parent.parent / "fixtures" / ".redscope"
        self.dummy_config = """
        [env]
        file = my_test_file.env

        [redshift]
        connection = TEST_REDSHIFT_URL
        """

    def test_load_redscope_config(self) -> None:
        expected_config = ConfigParser()
        expected_config.read_string(self.dummy_config)

        parsed_config = get_redscope_config(self.config_path)
        self.assertEqual(expected_config, parsed_config)

    def test_returns_config_parser(self) -> None:
        self.assertIsInstance(get_redscope_config(self.config_path), ConfigParser)

    @patch('redscope.project.environment.environment.load_dotenv')
    @patch('redscope.project.environment.environment.get_redscope_config')
    def test_load_redscope_env_no_config(self, p_get_config: Mock, p_load_dotenv: Mock) -> None:
        load_redscope_env()
        p_get_config.assert_called()
        p_load_dotenv.assert_called()

    @patch('redscope.project.environment.environment.load_dotenv')
    def test_load_redscope_env_with_config(self, p_load_dotenv: Mock) -> None:
        dummy_config = ConfigParser()
        dummy_config.read_string(self.dummy_config)
        load_redscope_env(dummy_config)
        p_load_dotenv.assert_called_once_with('my_test_file.env')

    @patch('redscope.project.environment.environment.psycopg2.connect')
    def test_get_redshift_connection_with_name(self, p_connect: Mock) -> None:
        os.environ['TEST_REDSHIFT_URL'] = 'connect_foo'
        _ = get_redshift_connection('TEST_REDSHIFT_URL')
        p_connect.assert_called_once_with('connect_foo')

    @patch('redscope.project.environment.environment.get_redscope_config')
    @patch('redscope.project.environment.environment.psycopg2.connect')
    def test_get_redshift_connection_without_name(self, p_connect: Mock, p_get_config: Mock) -> None:

        # dummy environment vars and config
        os.environ['TEST_REDSHIFT_URL'] = 'connect_foo'
        dummy_config = ConfigParser()
        dummy_config.read_string(self.dummy_config)

        # when get_redshift_connection is called, it will have access to the dummy config
        # via the patched function get_redscope_config
        p_get_config.return_value = dummy_config
        _ = get_redshift_connection()
        p_connect.assert_called_once_with('connect_foo')
