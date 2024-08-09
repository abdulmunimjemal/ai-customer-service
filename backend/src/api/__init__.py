from fastapi import APIRouter, Request
from src.core.rag_manager import RAGManager

router = APIRouter()

# Initialize RAGManager for chat purposes
rag_manager = RAGManager()

@router.post("/")
async def chat(request: Request):
    data = await request.json()
    query = data.get("query")

    if not query:
        return {"error": "Query is required."}

    # Process the query using RAGManager
    response = rag_manager.answer_query(query)

    return {"response": response}
