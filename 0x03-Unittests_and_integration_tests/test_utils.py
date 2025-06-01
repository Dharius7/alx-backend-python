#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map
import pytest

class TestMyFunction:
    @pytest.mark.parametrize(
        "input_val, expected",
        [
            (1, 2),
            (2, 3),
            (3, 4),
        ]
    )
    def test_increment(self, input_val, expected):
        assert input_val + 1 == expected

class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), repr(path[-1]))

from unittest.mock import patch, Mock
from utils import get_json

class TestGetJson(unittest.TestCase):
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        mock_get.return_value = Mock(json=Mock(return_value=test_payload))
        self.assertEqual(get_json(test_url), test_payload)
        mock_get.assert_called_once_with(test_url)

from utils import memoize

class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()
            self.assertEqual(obj.a_property, 42)
            self.assertEqual(obj.a_property, 42)
            mock_method.assert_called_once()

from client import GithubOrgClient
from unittest import TestCase
from unittest.mock import patch
from parameterized import parameterized

class TestGithubOrgClient(TestCase):
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, test_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

from unittest.mock import patch, PropertyMock

    def test_public_repos_url(self):
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/test/repos"}
            client = GithubOrgClient("test")
            self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/test/repos")


@patch("client.get_json")
def test_public_repos(self, mock_get_json):
    mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]
    with patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock) as mock_url:
        mock_url.return_value = "https://api.github.com/orgs/test/repos"
        client = GithubOrgClient("test")
        self.assertEqual(client.public_repos(), ["repo1", "repo2"])
        mock_url.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD

@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url.endswith("orgs/google"):
                return Mock(json=lambda: cls.org_payload)
            elif url.endswith("orgs/google/repos"):
                return Mock(json=lambda: cls.repos_payload)
            raise ValueError("Unexpected URL")

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
