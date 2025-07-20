from mem0 import MemoryClient

client = MemoryClient(api_key="**")

def add_memory(messages: list, user_id: str):
    result = client.add(messages, user_id=user_id)
    return result

def get_all_memories(user_id: str):
    return client.get_all(user_id=user_id)   




client = MemoryClient(api_key="m0-qIt4PHW0xVqOx6Q9BmFAQ9w7yAbvUShnAHKslExi")