#!/usr/bin/env python3
"""
Unittests for utils module.

This module contains unit tests for the functions in utils.py:
- access_nested_map
- get_json
- memoize decorator

It uses parameterized tests and mocking where needed.
"""

import unittest
from typing import Any, Mapping, Tuple
from parameterized import parameterized
from unittest.mock import patch, Mock, PropertyMock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    Test case for utils.access_nested_map function.

    Tests that the function returns expected values for valid paths,
    and raises KeyError for invalid paths.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Mapping, path: Tuple[str, ...], expected: Any) -> None:
        """
        Test access_nested_map returns expected result.

        Args:
            nested_map (Mapping): The nested map to access.
            path (Tuple[str, ...]): The path of keys to access.
            expected (Any): The expected return value.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map: Mapping, path: Tuple[str, ...]) -> None:
        """
        Test access_nested_map raises KeyError for invalid path.

        Args:
            nested_map (Mapping): The nested map to access.
            path (Tuple[str, ...]): The invalid path of keys.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), repr(path[-1]))


class TestGetJson(unittest.TestCase):
    """
    Test case for utils.get_json function.

    Uses patching to mock requests.get to avoid real HTTP calls.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url: str, test_payload: dict, mock_get: Mock) -> None:
        """
        Test get_json returns expected payload and calls requests.get correctly.

        Args:
            test_url (str): URL to pass to get_json.
            test_payload (dict): Expected payload to be returned.
            mock_get (Mock): Mocked requests.get object.
        """
        mock_get.return_value = Mock(json=Mock(return_value=test_payload))
        self.assertEqual(get_json(test_url), test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """
    Test case for utils.memoize decorator.

    Tests that a decorated method is only called once and cached afterwards.
    """

    def test_memoize(self) -> None:
        """
        Test memoize caches the result of the decorated method.

        Defines a TestClass with a memoized property.
        """
        class TestClass:
            def a_method(self) -> int:
                """Return a fixed integer."""
                return 42

            @memoize
            def a_property(self) -> int:
                """Return value from a_method, memoized."""
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()
            self.assertEqual(obj.a_property, 42)
            self.assertEqual(obj.a_property, 42)
            mock_method.assert_called_once()
