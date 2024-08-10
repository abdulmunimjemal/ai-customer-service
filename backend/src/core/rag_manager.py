from llama_index.core import ( 
                              VectorStoreIndex, 
                              SimpleDirectoryReader, 
                              StorageContext, 
                              load_index_from_storage, 
                              Settings,
                              PromptTemplate)
from llama_index.llms.together import TogetherLLM
from llama_index.embeddings.together import TogetherEmbedding
from src.utils.config import settings
import os

# Constants

TOGETHER_API_KEY = settings.TOGETHER_API_KEY
EMBEDDING_MODEL = settings.EMBED_MODEL
LLM_RETRIEVAL_MODEL = settings.LLM_RETRIEVAL_MODEL
LLM_CHAT_MODEL = settings.LLM_CHAT_MODEL
PERSIST_DIR = settings.PERSISTANCE_DIR

llm = TogetherLLM(
        model=LLM_CHAT_MODEL,
        api_key=TOGETHER_API_KEY
    )
embed_model = TogetherEmbedding(
        model_name=EMBEDDING_MODEL,
        api_key=TOGETHER_API_KEY
    )

Settings.llm = llm
Settings.embed_model = embed_model

template = (
        "You are a polite, knowledgeable, and helpful Customer Support Bot.\n"
        "Your role is to assist users with accurate and concise information.\n"
        "\n"
        "Context Information:\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "\n"
        "Instructions:\n"
        "1. Only provide answers that are explicitly mentioned in the context as facts.\n"
        "2. If the answer to the user's question is not directly available in the context, inform them that the information is not available.\n"
        "3. If the user requires additional assistance, provide them with the email address support@abdulmunim.me for further help.\n"
        "4. Handle ambiguous or unclear queries by asking the user for clarification before attempting to answer.\n"
        "5. If the context contains contradictory information, prioritize the most recent and relevant data.\n"
        "6. Be aware of edge cases such as:\n"
        "   - Repeated questions: Acknowledge and rephrase the previous response.\n"
        "   - Out-of-scope questions: Politely inform the user and redirect them to appropriate channels if available.\n"
        "   - Multi-part questions: Answer each part separately and ensure clarity.\n"
        "\n"
        "Based on the provided context, please answer the following question:\n"
        "{query_str}\n"
    )

QA_PROMPT_TEMPLATE = PromptTemplate(template)

class RAGManager:
    def __init__(self, persist_dir: str = PERSIST_DIR):
        self.persist_dir = persist_dir
        self.index = self.get_index(self.persist_dir)
        self.query_engine = None

    def get_index(self, persist_dir: str) -> VectorStoreIndex:
        if os.path.exists(persist_dir):
            storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
            storage_context.index_store.index_structs()
            return load_index_from_storage(storage_context=storage_context)
        else:
            storage_context = StorageContext.from_defaults()
            return VectorStoreIndex([], storage_context=storage_context)

    def add_data(self, input_files: list):
        documents = SimpleDirectoryReader(input_files=input_files, filename_as_id=True).load_data()
        print(f"Adding {len(documents)} documents to the index.")
        for doc in documents:
            self.index.insert(doc)
        self.index.storage_context.persist(self.persist_dir)

    def update_data(self, input_files: list):
        documents = SimpleDirectoryReader(input_files=input_files, filename_as_id=True).load_data()
        for doc in documents:
            self.index.update_ref_doc(doc, update_kwargs={"delete_kwargs": {"delete_from_docstore": True}})
        self.index.storage_context.persist(self.persist_dir)

    def delete_data(self, input_files: list):
        documents = SimpleDirectoryReader(input_files=input_files, filename_as_id=True).load_data()
        for doc in documents:
            self.index.delete_ref_doc(doc.get_doc_id(), delete_kwargs={"delete_from_docstore": True})
        self.index.storage_context.persist(self.persist_dir)
    
    def get_query_engine(self):
        self.query_engine = self.index.as_query_engine(text_qa_template=QA_PROMPT_TEMPLATE)
        return self.query_engine


# Usage
if __name__ == "__main__":
    def chatbot(rag: RAGManager):
        query_engine = rag.get_query_engine()
        while True:
            query = input("Enter your query: ")
            if query == "exit":
                break
            response = query_engine.query(query)
            print(response)

    index_manager = RAGManager()
    chatbot(index_manager)
    
    # # # Add data
    # input_files = ['data/data.txt']
    # index_manager.add_data(input_files=input_files)
    # chatbot(index_manager)
    
    # input("Press to Update Data")
    # # Update data
    # index_manager.update_data(input_files=input_files)
    # chatbot(index_manager)
     
    # input("Press to Delete Data")
    #     # Delete data
    # index_manager.delete_data(input_files=input_files)
    # chatbot(index_manager)
