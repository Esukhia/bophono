import sdtrie
import csv

def get_trie_from_file(filename, type="roots"):
    trie = sdtrie.Trie()
    with open(filename, newline='') as csvfile:
        freader = csv.reader(csvfile)
        for row in freader:
            if row[0][-1:] == '*':
                trie.add(row[0][0:-1], row[1], False)
            else:
                trie.add(row[0], row[1])
    return trie

roots = get_trie_from_file("data/roots.csv")
ends = get_trie_from_file("data/ends.csv")

def get_phonetics(str, schema=0):
    global roots, ends
    rootinfo = roots.get_longest_match_with_data(str)
    if not rootinfo:
        return None
    enddata = ends.get_data(str[rootinfo['i']:])
    if not enddata:
        return None
    return rootinfo['d']+enddata

if __name__ == '__main__':
    """ Example use """
    print(get_phonetics('ཀྱང'))
    print(get_phonetics('བག'))
    print(get_phonetics('བག'))
    print(get_phonetics('བགའ'))
    print(get_phonetics('ཀ'))
