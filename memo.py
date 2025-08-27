from mem0 import MemoryClient
import os

from dotenv import load_dotenv
load_dotenv()

client = MemoryClient(api_key= os.getenv("MEM0_API_KEY"))

def add_memory(messages: list, user_id: str):
    result = client.add(messages, user_id=user_id)
    return result

def get_all_memories(user_id: str):
    return client.get_all(user_id=user_id)   
