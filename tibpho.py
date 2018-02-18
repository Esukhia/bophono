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

ignored_chars = {'\u0FAD': True, '\u0F35': True, '\u0F37': True}

def is_tib_letter(c):
    """is a tibetan letter"""
    return c >= '\u0F40' and c <= '\u0FBC'

def get_next_letter_index(tibstr, current, eindex):
    """finds first letter index in tibstr after current index"""
    for i in range(current, eindex):
        letter = tibstr[i]
        if is_tib_letter(letter) and letter not in ignored_chars:
            return i
    return -1

def combine(previous, rootinfo, endinfo):
    if previous:
        return previous['phon']+rootinfo['d']+endinfo['d']
    return rootinfo['d']+endinfo['d']

def get_next_phon(tibstr, bindex, previous, eindex=-1, schema=0):
    global roots, ends, ignored_chars
    if eindex == -1:
        eindex = len(tibstr)
    rootinfo = roots.get_longest_match_with_data(tibstr, bindex, eindex, ignored_chars)
    if not rootinfo:
        return None
    endinfo = ends.get_longest_match_with_data(tibstr, rootinfo['i'], eindex, ignored_chars)
    if not endinfo:
        return None
    if endinfo['i'] < eindex and is_tib_letter(tibstr[endinfo['i']]) and (tibstr[endinfo['i']] not in ignored_chars):
        return None
    newres = combine(previous, rootinfo, endinfo)
    assert(endinfo['i']>bindex)
    return {'phon': newres, 'i': endinfo['i']}

def get_phonetics(tibstr, schema=0):
    i = 0
    res = None
    tibstrlen = len(tibstr)
    while i < tibstrlen and i >= 0: # > 0 covers the case where next_letter_index returns -1
        nextres = get_next_phon(tibstr, i, res)
        if not nextres:
            return res
        res = nextres
        i = get_next_letter_index(tibstr, nextres['i'], tibstrlen)
    return res

if __name__ == '__main__':
    """ Example use """
    print(get_phonetics('ཀྱང'))
    print(get_phonetics('བག'))
    print(get_phonetics('བག'))
    print(get_phonetics('བགའ'))
    print(get_phonetics('ཀ'))
    print(get_phonetics('ཀ\u0FAD་ཁ'))
    print(get_phonetics('རྒྱལ་རྩེ'))
    
