import pytest
import tempfile
import shutil
import os
from src.utils.directory_tracker import DirectoryTracker  # Ensure this import matches your actual module name

@pytest.fixture
def test_dir():
    # Create a temporary directory
    dir = tempfile.mkdtemp()
    yield dir
    # Remove the temporary directory after the test
    shutil.rmtree(dir)

@pytest.fixture
def tracker(test_dir):
    return DirectoryTracker(test_dir)

def _create_file(file_path, content=""):
    """Helper function to create a file with the given content."""
    with open(file_path, 'w') as f:
        f.write(content)

def test_no_changes(tracker):
    # Initially, there should be no changes
    changes = tracker.check_changes()
    assert not changes['added']
    assert not changes['deleted']
    assert not changes['updated']

def test_file_added(tracker, test_dir):
    # Add a new file
    file_path = os.path.join(test_dir, 'file1.txt')
    _create_file(file_path, "Hello World")
    changes = tracker.check_changes()
    assert file_path in changes['added']
    assert not changes['deleted']
    assert not changes['updated']

def test_file_deleted(tracker, test_dir):
    # Add and then delete a file
    file_path = os.path.join(test_dir, 'file2.txt')
    _create_file(file_path, "Hello World")
    tracker.check_changes()  # Reset the state after adding the file
    os.remove(file_path)
    changes = tracker.check_changes()
    assert file_path in changes['deleted']
    assert not changes['added']
    assert not changes['updated']

def test_file_updated(tracker, test_dir):
    # Add and then update a file
    file_path = os.path.join(test_dir, 'file3.txt')
    _create_file(file_path, "Hello World")
    tracker.check_changes()  # Reset the state after adding the file
    _create_file(file_path, "Updated content")
    changes = tracker.check_changes()
    assert file_path in changes['updated']
    assert not changes['added']
    assert not changes['deleted']

def test_multiple_changes(tracker, test_dir):
    # Add multiple files and perform various changes
    file_path1 = os.path.join(test_dir, 'file4.txt')
    file_path2 = os.path.join(test_dir, 'file5.txt')
    file_path3 = os.path.join(test_dir, 'file6.txt')

    _create_file(file_path1, "Content1")
    _create_file(file_path2, "Content2")
    tracker.check_changes()  # Reset the state after adding the files

    _create_file(file_path3, "Content3")  # Add file3
    _create_file(file_path1, "Updated Content1")  # Update file1
    os.remove(file_path2)  # Delete file2

    changes = tracker.check_changes()
    assert file_path3 in changes['added']
    assert file_path1 in changes['updated']
    assert file_path2 in changes['deleted']