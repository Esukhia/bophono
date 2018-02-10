# Simple decorated Trie with helper functions

## inspired from https://gist.github.com/nickstanisha/733c134a0171a00f66d4

class Node:
    def __init__(self, label=None, data=None):
        self.label = label
        self.data = data
        self.children = dict()
    
    def addChild(self, key, data=None):
        if not isinstance(key, Node):
            self.children[key] = Node(key, data)
        else:
            self.children[key.label] = key
    
    def __getitem__(self, key):
        return self.children[key]

class Trie:
    def __init__(self):
        self.head = Node()
    
    def __getitem__(self, key):
        return self.head.children[key]
    
    def add(self, word, data):
        current_node = self.head
        word_finished = True
        
        for i in range(len(word)):
            if word[i] in current_node.children:
                current_node = current_node.children[word[i]]
            else:
                word_finished = False
                break
        
        # For ever new letter, create a new child node
        if not word_finished:
            while i < len(word):
                current_node.addChild(word[i])
                current_node = current_node.children[word[i]]
                i += 1
        current_node.data = data
    
    def get_longest_match_with_data(self, word):
        if word == '' or word == None:
            return False
        current_node = self.head
        latest_match_node = None
        latest_match_i = 0
        i = 0
        for letter in word:
            if letter in current_node.children:
                current_node = current_node.children[letter]
                i = i+1
                if current_node.data != None:
                    latest_match_node = current_node
                    latest_match_i = i
            else:
                break
        if latest_match_node == None:
            return None
        return {"i": latest_match_i, "d": latest_match_node.data}

    def get_data(self, word):
        if word == '' or word == None:
            return False
        current_node = self.head
        for letter in word:
            if letter in current_node.children:
                current_node = current_node.children[letter]
            else:
                return None
        return current_node.data

if __name__ == '__main__':
    """ Example use """
    trie = Trie()
    trie.add("test", "test_data")
    trie.add("te", "te_data")
    print(trie.get_longest_match_with_data("test"))
    print(trie.get_data("test"))
    print(trie.get_longest_match_with_data("tes"))