from unittest import TestCase
from unittest.mock import MagicMock
from pathlib import Path
from redscope.project.database.models import (
    Table, View, Function, Procedure, Column, Constraint, Schema, DDL, UserDefinedObject
)


class DummyDDL(DDL):

    def ddl(self) -> str:
        return "DUMMY DDL VALUE"


class TestDDLModel(TestCase):

    def setUp(self) -> None:
        self.dummy_ddl = DummyDDL('foo', 'bar')

    def test_ddl_properties(self) -> None:
        self.assertTrue(hasattr(DDL, 'schema'))
        self.assertTrue(hasattr(DDL, 'name'))
        self.assertTrue(hasattr(DDL, 'qualified_name'))
        self.assertTrue(hasattr(DDL, 'file_path'))
        self.assertTrue(hasattr(DDL, 'save_file'))
        self.assertTrue(hasattr(DDL, 'ddl'))

    def test_ddl_attribute(self) -> None:
        self.assertEqual(self.dummy_ddl.ddl(), 'DUMMY DDL VALUE')

    def test_save_file_path(self) -> None:
        path = Path("foo/dummyddls/foo.bar.sql")
        self.assertEqual(path, self.dummy_ddl.file_path)

    def test_save_file(self) -> None:
        mock_path = MagicMock()
        mock_local_path = MagicMock()
        mock_path.__truediv__.return_value = mock_local_path

        self.dummy_ddl.save_file(mock_path)

        # assure the correct path gets built
        mock_path.__truediv__.assert_called_once_with(self.dummy_ddl.file_path.as_posix())

        # make sure all the proper create dir / file methods are called and the ddl string gets saved.
        mock_local_path.parent.mkdir.assert_called_once()
        mock_local_path.touch.assert_called_once()
        mock_local_path.write_text.assert_called_with('DUMMY DDL VALUE')


class TestSchemaModel(TestCase):

    def setUp(self) -> None:
        self.schema = Schema(name='test_schema')

    def test_attributes(self) -> None:
        self.assertEqual(self.schema.name, 'test_schema')
        self.assertEqual(self.schema.schema, 'test_schema')

    def test_is_ddl_object(self) -> None:
        self.assertTrue(issubclass(Schema, DDL))

    def test_qualified_name(self) -> None:
        self.assertEqual(self.schema.qualified_name, 'test_schema')

    def test_ddl(self) -> None:
        self.assertEqual(self.schema.ddl(), 'CREATE SCHEMA IF NOT EXISTS test_schema;')

    def test_file_path(self):
        file_path = Path("test_schema/test_schema.sql")
        self.assertEqual(file_path, self.schema.file_path)


class TestUserDefinedObjects(TestCase):

    def test_user_defined_object(self) -> None:
        self.assertTrue(issubclass(UserDefinedObject, DDL))

    def test_view_type(self) -> None:
        self.assertTrue(issubclass(View, DDL))
        self.assertTrue(issubclass(View, UserDefinedObject))

    def test_function_type(self) -> None:
        self.assertTrue(issubclass(Function, DDL))
        self.assertTrue(issubclass(Function, UserDefinedObject))

    def test_procedure_type(self) -> None:
        self.assertTrue(issubclass(Procedure, DDL))
        self.assertTrue(issubclass(Procedure, UserDefinedObject))
