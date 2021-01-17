from unittest import TestCase
from redscope.project.helpers import format_model_name


class TestFormatModelName(TestCase):

    def setUp(self) -> None:
        self.test_values = {
            'users': 'User',
            'MONSTERS': 'Monster',
            'TAbLesss':  'Table'
        }

    def test_format_model_name(self) -> None:
        for test_val, expected in self.test_values.items():
            self.assertEqual(format_model_name(test_val), expected)

    def test_raises_attribute_error(self) -> None:
        self.assertRaises(AttributeError, format_model_name, 123)
