from backends.memory.chroma_memory import (

    save_memory,

    search_memory,

    update_user_profile,

    get_user_profile
)

class MemoryAgent:

    def store_memory(self, text):
        save_memory(text)
        update_user_profile(text)

    def retrieve_memory(self, query):
        return search_memory(query)

    def get_profile(self):
        return get_user_profile()