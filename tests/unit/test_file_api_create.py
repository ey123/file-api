"""Unit tests for the create_file function in the FileApi class"""

import os
import unittest
from services.file_api import FileApi
from services.file_api import FileAlreadyExistsError
from tests.test_utils import pub_dir, PUBLIC_DIR


class TestCreateFile(unittest.TestCase):
    """Test the create_file function"""

    def setUp(self):
        """create a test file in the PUBLIC_DIR"""
        self.file_api = FileApi(public_dir=PUBLIC_DIR)
        self.test_file = "test_create.txt"
        self.test_file_new = "test_create_new.txt"
        os.makedirs(PUBLIC_DIR, exist_ok=True)
        with open(pub_dir(self.test_file), "w", encoding="utf-8") as file:
            file.write("test file contents")

    def tearDown(self):
        """delete the test file after each test"""
        for test_file in [self.test_file, self.test_file_new]:
            file = pub_dir(test_file)
            if os.path.exists(file):
                os.remove(file)

    def test_create_existing_file(self):
        """ensure that the function raises a FileAlreadyExistsError for an existing file"""
        with self.assertRaises(FileAlreadyExistsError):
            self.file_api.create_file(self.test_file, "test file contents")

    def test_create_new_file(self):
        """ensure that the function creates a new file"""
        self.file_api.create_file(self.test_file_new, "test file contents")
        self.assertTrue(
            os.path.exists(os.path.join(PUBLIC_DIR, self.test_file_new))
        )
        with open(pub_dir(self.test_file_new), "r", encoding="utf-8") as file:
            contents = file.read()
        self.assertEqual(contents, "test file contents")
