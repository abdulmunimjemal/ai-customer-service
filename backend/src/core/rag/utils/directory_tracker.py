import hashlib
import os

class DirectoryTracker:
    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.file_hashes = self._calculate_directory_hashes()

    def _calculate_file_hash(self, file_path):
        """Calculate the hash of a single file."""
        hasher = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                buf = f.read()
                hasher.update(buf)
        except FileNotFoundError:
            return ''
        return hasher.hexdigest()

    def _calculate_directory_hashes(self):
        """Calculate the hash of all files in the directory."""
        file_hashes = {}
        for root, _, files in os.walk(self.directory_path):
            for file in sorted(files):  # Sort files to ensure consistent order
                file_path = os.path.join(root, file)
                file_hashes[file_path] = self._calculate_file_hash(file_path)
        return file_hashes

    def check_changes(self):
        """Check if any file in the directory has been added, updated, or deleted."""
        current_hashes = self._calculate_directory_hashes()
        changes = {
            'added': [],
            'deleted': [],
            'updated': []
        }

        # Check for added and updated files
        for file_path, current_hash in current_hashes.items():
            if file_path not in self.file_hashes:
                changes['added'].append(file_path)
            elif current_hash != self.file_hashes[file_path]:
                changes['updated'].append(file_path)

        # Check for deleted files
        for file_path in self.file_hashes:
            if file_path not in current_hashes:
                changes['deleted'].append(file_path)

        # Update the stored hashes to the new ones
        self.file_hashes = current_hashes
        return changes



# Example usage
directory_path = './data'
tracker = DirectoryTracker(directory_path)

changes = tracker.check_changes()
if changes['added'] or changes['deleted'] or changes['updated']:
    print("Changes detected:")
    if changes['added']:
        print(f"Added files: {changes['added']}")
    if changes['deleted']:
        print(f"Deleted files: {changes['deleted']}")
    if changes['updated']:
        print(f"Updated files: {changes['updated']}")
else:
    print(f"No changes detected in {directory_path}.")