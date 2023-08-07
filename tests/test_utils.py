"""Test utilities for the file_api testing"""
import os

PUBLIC_DIR = "tmp"


def pub_dir(*args):
    """return the path to a file in the PUBLIC_DIR"""
    return os.path.join(PUBLIC_DIR, *args)
