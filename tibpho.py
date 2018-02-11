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

config = {
    "useLitterary": True
}

def is_tib_letter(c):
    """is a tibetan letter"""
    return c >= '\u0F40' and c <= '\u0FBC'

def get_next_letter_index(tibstr, current):
    """finds first letter index in tibstr after current index"""
    for i in range(current, len(tibstr)):
        letter = tibstr[i]
        if is_tib_letter(letter):
            return i
    return -1

def combine(previous, rootinfo, endinfo):
    if previous:
        return previous['phon']+rootinfo['d']+endinfo['d']
    return rootinfo['d']+endinfo['d']

def get_next_phon(tibstr, bindex, previous, schema=0):
    global roots, ends
    rootinfo = roots.get_longest_match_with_data(tibstr, bindex)
    if not rootinfo:
        return None
    endinfo = ends.get_longest_match_with_data(tibstr, rootinfo['i'])
    if not endinfo:
        return None
    if endinfo['i'] < len(tibstr) and is_tib_letter(tibstr[endinfo['i']]):
        print(endinfo['i'])
        return None
    newres = combine(previous, rootinfo, endinfo)
    assert(endinfo['i']>bindex)
    return {'phon': newres, 'i': endinfo['i']}

def get_phonetics(tibstr, schema=0):
    i = 0
    res = None
    while i < len(tibstr) and i >= 0: # > 0 covers the case where next_letter_index returns -1
        nextres = get_next_phon(tibstr, i, res)
        if not nextres:
            return res
        res = nextres
        i = get_next_letter_index(tibstr, nextres['i'])
    return res

if __name__ == '__main__':
    """ Example use """
    print(get_phonetics('ཀྱང'))
    print(get_phonetics('བག'))
    print(get_phonetics('བག'))
    print(get_phonetics('བགའ'))
    print(get_phonetics('ཀ'))
    print(get_phonetics('ཀ་ཁ'))
