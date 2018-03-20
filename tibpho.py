import sdtrie
import csv
import PhonStateNT
import sys

Cx_to_vow = {'a': '', 'b': '', 'c': '', 'i': 'ི', 'u': 'ུ', 'e': 'ེ', 'o': 'ོ'}
Cx_affix_list = ['', 'འི', 'འིའོ', 'འོ', 'འང', 'འམ', 'ར', 'ས']
Cx_affix_list_a = ['འ', 'འི', 'འིའོ', 'འོ', 'འང', 'འམ', 'ར', 'ས']
Cx_suffix_list = ['འ', 'འི', 'འིའོ', 'འོ', 'འང', 'འམ', 'ར', 'ས', 'ག', 'གས', 'ང', 'ངས', 'ད', 'ན', 'བ', 'བས', 'མ', 'མས', 'ལ']

def add_association_in_trie(unicodeTib, phonStr, trie, phonType, endsTrie=None):
    if len(unicodeTib) > 2 and unicodeTib[-3] == '/' and unicodeTib[-2] == 'C':
        letter = unicodeTib[-1:]
        vow = Cx_to_vow[letter]
        # convention:
        # - b is for when all suffixes are possible, including འ, but an absence of suffix is not
        # - c is for when all affixes are possible, but in the absence of affix, འ is mandatory
        suffix_list = Cx_affix_list
        if letter == 'b':
            suffix_list = Cx_suffix_list
        if letter == 'c':
            suffix_list = Cx_affix_list_a
        for affix in suffix_list:
            phonVowAffix = endsTrie.get_data(vow+affix)
            #print("add in trie: "+unicodeTib[0:-3]+affix+" -> "+phonStr+phonVowAffix)
            add_association_in_trie(unicodeTib[0:-3]+affix, phonStr+phonVowAffix, trie, phonType)
        return
    if unicodeTib.startswith('2:'):
        trie.add(unicodeTib[2:], '2:'+phonStr)
    if unicodeTib.endswith('*'):
        trie.add(unicodeTib[0:-1], phonStr, False)
    else:
        trie.add(unicodeTib, phonStr)


def get_trie_from_file(filename, phonType="roots", endsTrie=None):
    trie = sdtrie.Trie()
    with open(filename, newline='') as csvfile:
        freader = csv.reader(csvfile)
        for row in freader:
            if row[0].startswith('#'):
                continue
            add_association_in_trie(row[0], row[1], trie, phonType, endsTrie)
    return trie

roots = get_trie_from_file("data/roots.csv")
ends = get_trie_from_file("data/ends.csv", "ends")
exceptions = get_trie_from_file("data/exceptions.csv", "exceptions", ends)

config = {
    "useLitterary": True
}

ignored_chars = {'\u0FAD': True, '\u0F35': True, '\u0F37': True}

def is_tib_letter(c):
    """is a tibetan letter"""
    return c >= '\u0F40' and c <= '\u0FBC' and c != '\u0F7F'

def get_next_letter_index(tibstr, current, eindex):
    """finds first letter index in tibstr after current index"""
    for i in range(current, eindex):
        letter = tibstr[i]
        if is_tib_letter(letter) and letter not in ignored_chars:
            return i
    return -1

def get_next_non_letter_index(tibstr, current, eindex):
    """finds first letter index in tibstr after current index"""
    for i in range(current, eindex):
        letter = tibstr[i]
        if not is_tib_letter(letter):
            return i
    return -1

def combine(previous, rootinfo, endinfo=None):
    rootinfod = rootinfo['d']
    previousendinfod = previous and previous['endinfod'] or None
    curphon = previous and previous['phon'] or ''
    res = previous and previous['phon']+rootinfo['d'] or rootinfo['d']
    return endinfo and res+endinfo['d'] or res

def finishcombination(phonres):
    if not phonres:
        return None

def combine_next_syll_phon(tibstr, bindex, state, eindex=-1):
    # here we consider that we deal with a syllable starting at bindex, ending at eindex
    global roots, ends, exceptions, ignored_chars
    if eindex == -1:
        eindex = len(tibstr)
    exceptioninfo = exceptions.get_data(tibstr, bindex, eindex, ignored_chars)
    if exceptioninfo and (state.position > 0 or not exceptioninfo.startswith('2:')):
        # if it starts with '2:' and we're in the first syllable, we ignore it:
        if exceptioninfo.startswith('2:'):
            exceptioninfo = exceptioninfo[2:]
        state.combineWithException(exceptioninfo)
        return eindex
    rootinfo = roots.get_longest_match_with_data(tibstr, bindex, eindex, ignored_chars)
    if not rootinfo:
        return -1
    endinfo = ends.get_longest_match_with_data(tibstr, rootinfo['i'], eindex, ignored_chars)
    if not endinfo:
        return -1
    if endinfo['i'] < eindex and is_tib_letter(tibstr[endinfo['i']]) and (tibstr[endinfo['i']] not in ignored_chars):
        return -1
    state.combineWith(rootinfo['d'], endinfo['d'])
    assert(endinfo['i']>bindex)
    return endinfo['i']

def get_phonetics(tibstr, bindex=0, eindex=-1, pos=None, endOfSentence=False, schema=0, options={}):
    if eindex == -1:
        eindex = len(tibstr)
    i = get_next_letter_index(tibstr, bindex, eindex)
    if (i==-1):
        return ''
    state = PhonStateNT.PhonStateNT(options, pos, endOfSentence)
    while i < eindex and i >= 0: # > 0 covers the case where next_letter_index returns -1
        # we combine syllable per syllable, first we search the end of next syllable:
        lastidx = get_next_non_letter_index(tibstr, i, eindex)
        #print("found syllable '"+tibstr[i:lastidx]+"'")
        if lastidx == -1:
            lastidx = eindex
        matchlastidx = combine_next_syll_phon(tibstr, i, state, lastidx)
        if matchlastidx == -1:
            print("couldn't understand syllable "+tibstr[i:lastidx])
            break
        if matchlastidx < lastidx:
            print("couldn't understand last "+str(lastidx-matchlastidx)+" characters of syllable "+tibstr[i:lastidx])
        i = get_next_letter_index(tibstr, matchlastidx, eindex)
    state.finish()
    return state.phon

if __name__ == '__main__':
    """ Example use """
    #print(get_phonetics("བག་ལེབ"))
    filename = 'tests/nt.txt'
    if (len(sys.argv) > 1):
        filename = sys.argv[1]
    with open(filename, 'r') as f:
        for line in f:
            line = line[:-1]
            if line == '':
                continue
            if line.startswith('#'):
                print(line[1:])
                continue
            phon = get_phonetics(line)
            print(line + " -> " + phon)
