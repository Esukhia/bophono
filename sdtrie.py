# Simple decorated Trie with helper functions

## inspired from https://gist.github.com/nickstanisha/733c134a0171a00f66d4

class Node:
    def __init__(self, label=None, data=None, canbefinal=True):
        self.label = label
        self.data = data
        self.canbefinal = canbefinal
        self.children = {}
    
    def addChild(self, key, data=None, canbefinal=True):
        if not isinstance(key, Node):
            self.children[key] = Node(key, data, canbefinal)
        else:
            self.children[key.label] = key
    
    def __getitem__(self, key):
        return self.children[key]

class Trie:
    def __init__(self):
        self.head = Node()
    
    def __getitem__(self, key):
        return self.head.children[key]
    
    def add(self, word, data=True, canbefinal=True):
        current_node = self.head
        for c in word:
            if c not in current_node.children:
                current_node.addChild(c)
            current_node = current_node.children[c]
        current_node.data = data
        current_node.canbefinal = canbefinal
    
    def get_longest_match_with_data(self, word, bindex=0):
        if word == '':
            return None
        current_node = self.head
        wordlen = len(word)
        latest_match_node = None
        latest_match_i = 0
        for i in range(bindex, wordlen):
            letter = word[i]
            if letter in current_node.children:
                current_node = current_node.children[letter]
                if current_node.data and (i+1 < wordlen or current_node.canbefinal):
                    latest_match_node = current_node
                    latest_match_i = i+1
            else:
                break
        if latest_match_node == None:
            return None
        return {"i": latest_match_i, "d": latest_match_node.data}

    def get_data(self, word, bindex=0):
        current_node = self.head
        for i in range(bindex, len(word)):
            letter = word[i]
            if letter in current_node.children:
                current_node = current_node.children[letter]
            else:
                return None
        return current_node.data

    def _walk_all_data_rec(self, iterator, node, word, prefix):
        """ Recursive function walking the tree """
        # If we're still in the prefix:
        if len(prefix) > 0:
            letter = prefix[0]
            if letter in node.children:
                child_node = top_node.children[letter]
                self._walk_all_data_rec(iterator, child_node, word+letter, prefix[1:])
            return
        if node.data:
            iterator(word, node.data)
        for letter, child_node in node.children.items():
            self._walk_all_data_rec(iterator, child_node, word+letter, prefix)

    def walk_all_data(self, iterator, prefix=''):
        """ Iterates over all the data of a trie """
        self._walk_all_data_rec(iterator, self.head, '', prefix)
        

if __name__ == '__main__':
    """ Example use """
    trie = Trie()
    trie.add("test", "test_data")
    trie.add("t", "t_data")
    print(trie.get_longest_match_with_data("test"))
    print(trie.get_data("test"))
    print(trie.get_longest_match_with_data("tes"))
    trie.add("te", "te_data", False)
    print(trie.get_longest_match_with_data("tes"))
    print(trie.get_longest_match_with_data("te"))
    def iteratortest(word, data):
        print("data for \""+word+"\": "+data)
    trie.walk_all_data(iteratortest)
