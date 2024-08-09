import os
from pathlib import Path
from fastapi import UploadFile

class FileManager:
    def __init__(self, path="./data"):
        self.data_path = Path(path)

    async def save_file(self, file: UploadFile):
        file_location = self.data_path / file.filename
        with open(file_location, "wb") as f:
            f.write(await file.read())
        return str(file_location)

    def list_files(self):
        return [f.name for f in self.data_path.iterdir() if f.is_file()]

    def delete_file(self, file_name: str):
        try:
            file_path = self.data_path / file_name
            os.remove(file_path)
            return True
        except FileNotFoundError:
            return False

    async def replace_file(self, file_name: str, file: UploadFile):
        # Replace an existing file
        file_path = self.data_path / file_name
        if not file_path.exists():
            return False
        with open(file_path, "wb") as f:
            f.write(await file.read())
        return True
