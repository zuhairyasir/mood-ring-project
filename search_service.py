class TrieNode:
    def __init__(self):
        self.children = {}
        self.chat_ids = set()

class Trie:
    def __init__(self):
        self.root = TrieNode()  

    def insert(self, word, chat_id):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.chat_ids.add(chat_id)

    def search_prefix(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return set() 
            node = node.children[char]
        return node.chat_ids


class SearchService:
    def build_and_search(self, chats, query):
        trie = Trie()
        for chat_id, chat_data in chats.items():
            for message in chat_data.messages:
                for word in message.text.lower().split():
                    trie.insert(word, chat_id)

        matching_ids = trie.search_prefix(query.lower())
        return list(matching_ids)