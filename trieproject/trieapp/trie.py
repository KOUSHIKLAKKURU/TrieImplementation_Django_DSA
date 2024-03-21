from .models import Word

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.load_words_from_database()

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    def _dfs_print_words(self, node, current_word):
        if node.is_end_of_word:
            print(current_word)

        for char, child_node in node.children.items():
            self._dfs_print_words(child_node, current_word + char)

    def print_all_words(self):
        all_words = []
        self._dfs_print_words(self.root, '', all_words)
        return all_words

    def search_prefix(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        suggestions = []
        self._dfs(node, prefix, suggestions)
        return suggestions[:5]

    def _dfs(self, node, current_prefix, suggestions):
        if node.is_end_of_word:
            suggestions.append(current_prefix)

        for char, child_node in node.children.items():
            self._dfs(child_node, current_prefix + char, suggestions)

    def load_words_from_database(self):
        words = Word.objects.values_list('word_text', flat=True)
        for word in words:
            self.insert(word)
            print(word)