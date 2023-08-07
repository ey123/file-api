"""Test the delete_file function in the FileApi class"""

import os
import unittest
from services.file_api import FileApi
from tests.test_utils import pub_dir, PUBLIC_DIR


class TestDeleteFile(unittest.TestCase):
    """Test the delete_file function"""

    def setUp(self):
        """create a test file in the PUBLIC_DIR"""
        self.file_api = FileApi(public_dir=PUBLIC_DIR)
        self.test_file = "test_delete.txt"
        os.makedirs(PUBLIC_DIR, exist_ok=True)
        with open(pub_dir(self.test_file), "w", encoding="utf-8") as file:
            file.write("test file contents")

    def tearDown(self):
        """delete the test file after each test"""
        file = pub_dir(self.test_file)
        if os.path.exists(file):
            os.remove(file)

    def test_delete_existing_file(self):
        """ensure that the function deletes an existing file"""
        self.file_api.delete_file(self.test_file)
        self.assertFalse(os.path.exists(pub_dir(self.test_file)))

    def test_delete_nonexistent_file(self):
        """ensure that the function raises a FileNotFoundError for a nonexistent file"""
        with self.assertRaises(FileNotFoundError):
            self.file_api.delete_file("nonexistent_file.txt")
