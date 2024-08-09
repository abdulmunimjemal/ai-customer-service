from fastapi import FastAPI
from src.api import chat, files
from src.core.rag_manager import RAGManager
from src.utils.notifier import Notifier

app = FastAPI()

# Initialize RAGManager and Notifier
rag_manager = RAGManager()
notifier = Notifier(directory_path='./data', rag_manager=rag_manager)

# Run the Notifier in a background thread
notifier.run_in_thread()

@app.on_event("shutdown")
def shutdown_event():
    # Stop the notifier gracefully on shutdown
    notifier.stop()
    notifier.join()

# Pass the notifier instance to the file router
app.include_router(chat.router, prefix="/chat", default=rag_manager)
app.include_router(files.router, prefix="/files", default=notifier)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI backend!"}