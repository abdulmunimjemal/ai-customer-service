import unittest
import tempfile
import shutil
import os
from utils import DirectoryTracker  # Ensure this import matches your actual module name

class TestDirectoryTracker(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.tracker = DirectoryTracker(self.test_dir)

    def tearDown(self):
        # Remove the temporary directory after the test
        shutil.rmtree(self.test_dir)

    def _create_file(self, file_path, content=""):
        """Helper function to create a file with the given content."""
        with open(file_path, 'w') as f:
            f.write(content)

    def test_no_changes(self):
        # Initially, there should be no changes
        changes = self.tracker.check_changes()
        self.assertFalse(changes['added'])
        self.assertFalse(changes['deleted'])
        self.assertFalse(changes['updated'])

    def test_file_added(self):
        # Add a new file
        file_path = os.path.join(self.test_dir, 'file1.txt')
        self._create_file(file_path, "Hello World")
        changes = self.tracker.check_changes()
        self.assertIn(file_path, changes['added'])
        self.assertFalse(changes['deleted'])
        self.assertFalse(changes['updated'])

    def test_file_deleted(self):
        # Add and then delete a file
        file_path = os.path.join(self.test_dir, 'file2.txt')
        self._create_file(file_path, "Hello World")
        self.tracker.check_changes()  # Reset the state after adding the file
        os.remove(file_path)
        changes = self.tracker.check_changes()
        self.assertIn(file_path, changes['deleted'])
        self.assertFalse(changes['added'])
        self.assertFalse(changes['updated'])

    def test_file_updated(self):
        # Add and then update a file
        file_path = os.path.join(self.test_dir, 'file3.txt')
        self._create_file(file_path, "Hello World")
        self.tracker.check_changes()  # Reset the state after adding the file
        self._create_file(file_path, "Updated content")
        changes = self.tracker.check_changes()
        self.assertIn(file_path, changes['updated'])
        self.assertFalse(changes['added'])
        self.assertFalse(changes['deleted'])

    def test_multiple_changes(self):
        # Add multiple files and perform various changes
        file_path1 = os.path.join(self.test_dir, 'file4.txt')
        file_path2 = os.path.join(self.test_dir, 'file5.txt')
        file_path3 = os.path.join(self.test_dir, 'file6.txt')

        self._create_file(file_path1, "Content1")
        self._create_file(file_path2, "Content2")
        self.tracker.check_changes()  # Reset the state after adding the files

        self._create_file(file_path3, "Content3")  # Add file3
        self._create_file(file_path1, "Updated Content1")  # Update file1
        os.remove(file_path2)  # Delete file2

        changes = self.tracker.check_changes()
        self.assertIn(file_path3, changes['added'])
        self.assertIn(file_path1, changes['updated'])
        self.assertIn(file_path2, changes['deleted'])

if __name__ == '__main__':
    unittest.main()