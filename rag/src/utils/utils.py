import os

def create_path(path):
    """Create a directory path if it does not exist."""
    if not os.path.exists(path):
        os.makedirs(path)