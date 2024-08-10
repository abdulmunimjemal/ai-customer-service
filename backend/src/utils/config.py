import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY") # get this from https://www.together.ai/
    EMBED_MODEL = os.getenv("EMBED_MODEL", "togethercomputer/m2-bert-80M-8k-retrieval") # "togethercomputer/m2-bert-80M-8k-retrieval"
    LLM_RETRIEVAL_MODEL = os.getenv("LLM_MODEL", "mistralai/Mixtral-8x7B-Instruct-v0.1") # "mistralai/Mixtral-8x7B-Instruct-v0.1"
    LLM_CHAT_MODEL = os.getenv("LLM_CHAT_MODEL", "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo") # "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", 512)) # max tokens 
    PERSISTANCE_DIR = os.getenv("PERSISTANCE_DIR", "./storage") # directory to store the index
    CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 5)) # check interval for the directory watcher

settings = Settings()