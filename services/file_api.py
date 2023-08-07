"""File API module"""
import os
import pathlib
from os.path import isfile, join

# import locking from threading
from threading import Lock


class FileAlreadyExistsError(Exception):
    """Exception when file already exists"""


class FileBusy(Exception):
    """Exception when file is busy"""


class InvalidTypeError(Exception):
    """Exception when invalid type is used"""


def find_file(exception_on="missing"):
    """Decorator that finds a file in the PUBLIC_DIR
    If the file is not found and exception_on is missing, raise a FileNotFoundError
    If the file is found and exception_on is found, raise a FileAlreadyExistsError
    """

    def inner_find_file(func):
        def wrapper(self, *args, **kwargs):
            file = os.path.join(self.public_dir, args[0])
            found = os.path.exists(file)
            if exception_on == "missing" and not found:
                raise FileNotFoundError
            if exception_on == "found" and found:
                raise FileAlreadyExistsError
            return func(self, file, *args[1:], **kwargs)

        return wrapper

    return inner_find_file


class FileApi:
    """File API class"""

    def __init__(self, public_dir="public"):
        """Initialize the FileApi class"""
        self.public_dir = public_dir
        self.file_locks = {}

    def get_or_create_lock(self, file):
        """get or create a lock for a file"""
        lock = self.file_locks.get(file)
        if not lock:
            lock = Lock()
            self.file_locks[file] = lock
        if lock.locked():
            raise FileBusy
        return lock

    @find_file()
    def get_file(self, file):
        """returns the content of the file in the PUBLIC_DIR"""
        with open(file, "r", encoding="utf-8") as f:
            return f.read()

    @find_file()
    def update_file(self, file, content):
        """updates file in the PUBLIC_DIR
        If the file is not found, raise a FileNotFoundError
        If the file is found, overwrite it with the new content
        Do not allow concurrent access to the same file
        """
        lock = self.get_or_create_lock(file)
        with lock:
            with open(file, "w", encoding="utf-8") as f:
                f.write(content)

    @find_file("found")
    def create_file(self, file, content):
        """creates file in the PUBLIC_DIR
        if the file is found, raise a FileAlreadyExistsError
        Do not allow concurrent access to the same file
        """
        lock = self.get_or_create_lock(file)
        with lock:
            os.makedirs(pathlib.Path(file).parent.resolve(), exist_ok=True)
            with open(file, "w", encoding="utf-8") as f:
                f.write(content)

    @find_file()
    def delete_file(self, file):
        """deletes file in the PUBLIC_DIR
        If the file is not found, raise a FileNotFoundError
        If the file is found, delete it
        """
        os.remove(file)

    @find_file()
    def list_dir(self, folder):
        """lists the contents of a directory in the PUBLIC_DIR
        If the directory is not found, raise a FileNotFoundError
        If dir is not a directory, raise a NotADirectoryError
        If the directory is found, list its contents
        """
        if not os.path.isdir(folder):
            raise InvalidTypeError
        return [
            {
                "name": f,
                "type": "file" if isfile(join(folder, f)) else "directory",
            }
            for f in os.listdir(folder)
        ]
