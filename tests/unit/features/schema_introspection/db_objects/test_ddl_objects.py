from unittest import TestCase
from redscope.features.schema_introspection.db_objects import Table, Group, UserGroup, \
    User, View, Constraint, Schema

expected_properties = ['file_name', 'create', 'create_if_not_exist', 'drop', 'drop_if_exist']
ddl_objects = [Table, Group, UserGroup, User, View, Constraint, Schema]


class TestGroup(TestCase):
    expected_create = "CREATE GROUP spam;"
    expected_drop = "DROP GROUP spam;"

    def setUp(self) -> None:
        self.group = Group('spam')

    def test_properties(self):
        for prop in expected_properties:
            p = getattr(self.group, prop, None)
            self.assertIsNotNone(p)

    def test_create(self):
        self.assertEqual(self.expected_create, self.group.create)
        self.assertEqual(self.expected_create, self.group.create_if_not_exist)

    def test_drop(self):
        self.assertEqual(self.expected_drop, self.group.drop)
        self.assertEqual(self.expected_drop, self.group.drop_if_exist)


class TestUser(TestCase):
    expected_create = "CREATE USER brian WITH PASSWORD xxxxxxxxxx;"
    expected_drop = "DROP USER brian;"

    def setUp(self) -> None:
        self.user = User('brian')

    def test_properties(self):
        for prop in expected_properties:
            p = getattr(self.user, prop, None)
            self.assertIsNotNone(p)

    def test_create(self):
        self.assertEqual(self.expected_create, self.user.create)
        self.assertEqual(self.expected_create, self.user.create_if_not_exist)
