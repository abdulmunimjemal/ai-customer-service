from fastapi import FastAPI, Depends
from src.api import chat, files
from src.core.rag_manager import RAGManager
from src.utils.notifier import Notifier

app = FastAPI()

# Initialize RAGManager and Notifier
rag_manager = RAGManager()
notifier = Notifier(directory_path='./data', rag_manager=rag_manager)

@app.on_event("startup")
async def startup_event():
    # Start the Notifier in the background during the startup of FastAPI
    notifier.run_in_thread()

@app.on_event("shutdown")
def shutdown_event():
    # Stop the Notifier when FastAPI shuts down
    notifier.stop()
    notifier.join()

# Dependency injection for the RAGManager and Notifier
def get_rag_manager():
    return rag_manager

def get_notifier():
    return notifier

# Pass the dependencies to the routers
app.include_router(chat.router, prefix="/chat", dependencies=[Depends(get_rag_manager)])
app.include_router(files.router, prefix="/files", dependencies=[Depends(get_notifier), Depends(get_rag_manager)])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI backend!"}