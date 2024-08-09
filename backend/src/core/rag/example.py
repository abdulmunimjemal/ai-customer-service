from src.utils.notifier import Notifier
from src.RAG import RAGManager

if __name__ == "__main__":
    directory_path = './data'
    rag_manager = RAGManager(persist_dir="./storage")
    notifier = Notifier(directory_path, rag_manager)
    notifier.run_in_thread()

    # Example of how the main application can continue running
    try:
        while True:
            print("We running this sh!")
            time.sleep(5)
    except KeyboardInterrupt:
        notifier.stop()
        notifier.join()
