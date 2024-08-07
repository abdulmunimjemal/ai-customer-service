from llama_index.core import ( 
                              VectorStoreIndex, 
                              SimpleDirectoryReader, 
                              StorageContext, 
                              load_index_from_storage, 
                              Settings,
                              PromptTemplate)
from llama_index.llms.together import TogetherLLM
from llama_index.embeddings.together import TogetherEmbedding
from dotenv import load_dotenv
import os
from utils import create_path

# Load environment variables
load_dotenv()

# Constants
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
EMBEDDING_MODEL = "togethercomputer/m2-bert-80M-8k-retrieval"
LLM_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"
PERSIST_DIR = "./storage"

llm = TogetherLLM(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        api_key=TOGETHER_API_KEY
    )
embed_model = TogetherEmbedding(
        model_name=EMBEDDING_MODEL,
        api_key=TOGETHER_API_KEY
    )

Settings.llm = llm
Settings.embed_model = embed_model

template = (
"We have provided context information below. \n"
"---------------------\n"
"{context_str}"
"\n---------------------\n"
"Do not give me an answer if it is not mentioned in the context as a fact. \n"
"Given this information, please provide me with an answer to the following:\n{query_str}\n")

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


def chatbot(rag: RAGManager):
    query_engine = rag.get_query_engine()
    while True:
        query = input("Enter your query: ")
        if query == "exit":
            break
        response = query_engine.query(query)
        print(response)


# Usage example
if __name__ == "__main__":
    index_manager = RAGManager()

    # # Add data
    input_files = ['data/data.txt']
    index_manager.add_data(input_files=input_files)
    chatbot(index_manager)
    
    input("Press to Update Data")
    # Update data
    index_manager.update_data(input_files=input_files)
    chatbot(index_manager)
     
    input("Press to Delete Data")
        # Delete data
    index_manager.delete_data(input_files=input_files)
    chatbot(index_manager)
