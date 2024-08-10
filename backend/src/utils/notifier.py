import time
import threading
from src.core.rag_manager import RAGManager
from src.utils.directory_tracker import DirectoryTracker

class Notifier:
    def __init__(self, directory_path, rag_manager: RAGManager, check_interval=5):
        self.directory_path = directory_path
        self.check_interval = check_interval
        self.tracker = DirectoryTracker(directory_path, rag_manager)
        self.rag_manager = rag_manager
        self.running = False

    def start(self):
        self.running = True
        print(f"Starting directory watcher for: {self.directory_path}")
        while self.running:
            changes = self.tracker.check_changes()
            if changes['added']:
                print(f"Added files detected: {changes['added']}")
                self.rag_manager.add_data(changes['added'])
            if changes['updated']:
                print(f"Updated files detected: {changes['updated']}")
                self.rag_manager.update_data(changes['updated'])
            if changes['deleted']:
                print(f"Deleted files detected: {changes['deleted']}")
                self.rag_manager.delete_data(changes['deleted'])
            time.sleep(self.check_interval)

    def stop(self):
        self.running = False
        print(f"Stopping directory watcher for: {self.directory_path}")

    def run_in_thread(self):
        self.thread = threading.Thread(target=self.start)
        self.thread.start()

    def join(self):
        self.thread.join()
