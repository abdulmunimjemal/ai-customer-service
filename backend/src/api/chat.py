from fastapi import APIRouter, Request, Depends
from src.core.rag_manager import RAGManager

router = APIRouter()

# Dependency function to retrieve the RAGManager instance
def get_rag_manager(rag_manager: RAGManager):
    return rag_manager

@router.post("/")
async def chat(request: Request, rag_manager: RAGManager = Depends(get_rag_manager)):
    data = await request.json()
    query = data.get("query")
    query_engine = rag_manager.get_query_engine()

    if not query:
        return {"error": "Query is required."}

    # Process the queryr
    response = query_engine.query(query)

    return {"response": response}
