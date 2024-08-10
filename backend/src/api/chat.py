from fastapi import APIRouter, Depends, Query
from src.core.rag_manager import RAGManager

router = APIRouter()

# Use the dependency injection mechanism to get the RAGManager
def get_rag_manager():
    from src.main import get_rag_manager
    return get_rag_manager()

@router.get("/")
async def chat(query: str = Query(..., description="The query for the chat"), rag_manager: RAGManager = Depends(get_rag_manager)):
    if not query:
        return {"error": "Query is required."}
    query_engine = rag_manager.get_query_engine()
    # Process the query using RAGManager
    response = query_engine.query(query).response
    return {"response": response}
