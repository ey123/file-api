""" Unit tests for the list_dir function in the FileApi class """
import os
import unittest
import shutil

from services.file_api import FileApi
from tests.test_utils import pub_dir, PUBLIC_DIR


class TestListDir(unittest.TestCase):
    """Test the list_dir function"""

    def setUp(self):
        """create a test file in the PUBLIC_DIR"""
        self.file_api = FileApi(public_dir=PUBLIC_DIR)
        self.test_dir = "test_dir"
        # create a subdirectory
        os.makedirs(pub_dir(self.test_dir, "subdir"), exist_ok=True)
        os.makedirs(pub_dir(self.test_dir), exist_ok=True)
        subdir_path = pub_dir(self.test_dir, "subdir", "subdir_test_file.txt")
        with open(subdir_path, "w", encoding="utf-8") as file:
            file.write("test subdir file contents")
        for i in range(2):
            file_path = pub_dir(self.test_dir, f"test_file{i}.txt")
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(f"test file contents {i}")

    def tearDown(self):
        """delete the test dir after each test"""
        shutil.rmtree(pub_dir(self.test_dir))

    def test_list_dir_existing_folder(self):
        """ensure that the function lists the dir"""
        dir_content = self.file_api.list_dir(self.test_dir)
        result = [
            ("subdir", "d"),
            ("test_file0.txt", "f"),
            ("test_file1.txt", "f"),
        ]
        # iterate over the result and check that each file is in the dir_content with it's type
        for file in result:
            # find the file in the dir_content array
            file_name = file[0]
            file_type = file[1]
            file_found = False
            for dir_file in dir_content:
                if (
                    dir_file["name"] == file_name
                    and dir_file["type"] == file_type
                ):
                    file_found = True
                    break
            self.assertTrue(
                file_found, f"file {file_name} not found in dir_content"
            )
            len_mismatch_error_msg = "result does not match dir_content"
            self.assertEqual(
                len(result), len(dir_content), len_mismatch_error_msg
            )

    def test_list_dir_exsiting_file_file(self):
        """ensure that the function raises a NotADirectoryError for an existing file"""
        with self.assertRaises(NotADirectoryError):
            self.file_api.list_dir("test_dir/test_file1.txt")

    def test_update_nonexistent_file(self):
        """ensure that the function raises a FileNotFoundError for a nonexistent file"""
        with self.assertRaises(FileNotFoundError):
            self.file_api.list_dir("nonexistent_file.txt")
