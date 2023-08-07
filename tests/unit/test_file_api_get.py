"""Unit Test the get_file function of the FileApi class"""
import os
import unittest
from services.file_api import FileApi
from tests.test_utils import pub_dir, PUBLIC_DIR


class TestGetFile(unittest.TestCase):
    """Test the get_file function"""

    def setUp(self):
        """Setup the test file"""
        self.file_api = FileApi(public_dir=PUBLIC_DIR)
        self.test_file = "test_get.txt"
        os.makedirs(PUBLIC_DIR, exist_ok=True)
        with open(pub_dir(self.test_file), "w", encoding="utf-8") as file:
            file.write("test file contents")

    def tearDown(self):
        """delete the test file after each test"""
        file = pub_dir(self.test_file)
        if os.path.exists(file):
            os.remove(file)

    def test_get_existing_file(self):
        """ensure that the function returns the contents of an existing file"""
        content = self.file_api.get_file(self.test_file)
        self.assertTrue(content == "test file contents")

    def test_get_nonexisting_file(self):
        """ensure that the function raises a FileNotFoundError for non-existing file"""
        with self.assertRaises(FileNotFoundError):
            self.file_api.get_file("nonexistent_file.txt")
