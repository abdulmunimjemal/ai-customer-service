from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from src.core.file_manager import FileManager
from src.utils.notifier import Notifier

router = APIRouter()
file_manager = FileManager()

# Ensure the Notifier and RAGManager instances are passed in from the main application
def get_notifier():
    from src.main import get_notifier
    notifier = get_notifier()
    return notifier

def get_rag_manager():
    from src.main import get_rag_manager
    rag_manager = get_rag_manager()
    return rag_manager

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...), notifier: Notifier = Depends(get_notifier)):
    file_path = await file_manager.save_file(file)
    notifier.tracker.check_changes()  # Manually trigger check to update RAGManager
    return {"file_path": file_path}

@router.get("/")
async def list_files(notifier: Notifier = Depends(get_notifier)):
    files = file_manager.list_files()
    return {"files": files}

@router.delete("/{file_name}")
async def delete_file(file_name: str, notifier: Notifier = Depends(get_notifier)):
    success = file_manager.delete_file(file_name)
    notifier.tracker.check_changes()  # Manually trigger check to update RAGManager
    if not success:
        raise HTTPException(status_code=404, detail="File not found")
    return {"message": "File deleted"}

@router.put("/replace/{file_name}")
async def replace_file(file_name: str, file: UploadFile = File(...), notifier: Notifier = Depends(get_notifier)):
    success = file_manager.replace_file(file_name, file)
    notifier.tracker.check_changes()  # Manually trigger check to update RAGManager
    if not success:
        raise HTTPException(status_code=404, detail="File not found or unable to replace")
    return {"message": "File replaced"}
