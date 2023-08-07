""" Unit tests for the update_file function in the FileApi class """
import os
import unittest
from services.file_api import FileApi
from tests.test_utils import pub_dir, PUBLIC_DIR


class TestUpdateFile(unittest.TestCase):
    """Test the update_file function"""

    def setUp(self):
        """create a test file in the PUBLIC_DIR"""
        self.file_api = FileApi(public_dir=PUBLIC_DIR)
        self.test_file = "test_update.txt"
        os.makedirs(PUBLIC_DIR, exist_ok=True)
        with open(pub_dir(self.test_file), "w", encoding="utf-8") as file:
            file.write("test file contents")

    def tearDown(self):
        """delete the test file after each test"""
        file = pub_dir(self.test_file)
        if os.path.exists(file):
            os.remove(file)

    def test_update_existing_file(self):
        """ensure that the function updates an existing file"""
        self.file_api.update_file(self.test_file, "test file contents updated")
        with open(
            os.path.join(PUBLIC_DIR, self.test_file), "r", encoding="utf-8"
        ) as file:
            contents = file.read()
        self.assertEqual(contents, "test file contents updated")

    def test_update_nonexistent_file(self):
        """ensure that the function raises a FileNotFoundError for a nonexistent file"""
        with self.assertRaises(FileNotFoundError):
            self.file_api.update_file(
                "nonexistent_file.txt", "test file contents updated"
            )
