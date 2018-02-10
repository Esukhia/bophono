import sdtrie

if __name__ == '__main__':
    """ Example use """
    trie = sdtrie.Trie()
    trie.add("test", "test_data")
    trie.add("te", "te_data")
    print(trie.get_longest_match_with_data("test"))
    print(trie.get_data("test"))
    print(trie.get_longest_match_with_data("tes"))