import sys
import csv
import os
from .sdtrie import *
from .PhonStateMST import *

def _get_trie_path(name):
    return os.path.join(os.path.split(__file__)[0], 'data', name)

roots = get_trie_from_file(_get_trie_path("roots.csv"))
ends = get_trie_from_file(_get_trie_path("ends.csv"), "ends")
exceptions = get_trie_from_file(_get_trie_path("exceptions.csv"), "exceptions", ends)

ignored_chars = {'\u0FAD': True, '\u0F35': True, '\u0F37': True}

def _is_tib_letter(c):
    """is a tibetan letter"""
    return c >= '\u0F40' and c <= '\u0FBC' and c != '\u0F7F'

def _get_next_letter_index(tibstr, current, eindex):
    """finds first letter index in tibstr after current index"""
    for i in range(current, eindex):
        letter = tibstr[i]
        if _is_tib_letter(letter) and letter not in ignored_chars:
            return i
    return -1

def _get_next_non_letter_index(tibstr, current, eindex):
    """finds first letter index in tibstr after current index"""
    for i in range(current, eindex):
        letter = tibstr[i]
        if not _is_tib_letter(letter):
            return i
    return -1

# def _combine(previous, rootinfo, endinfo=None):
#     rootinfod = rootinfo['d']
#     previousendinfod = previous and previous['endinfod'] or None
#     curphon = previous and previous['phon'] or ''
#     res = previous and previous['phon']+rootinfo['d'] or rootinfo['d']
#     return endinfo and res+endinfo['d'] or res

def _combine_next_syll_phon(tibstr, bindex, state, eindex):
    # here we consider that we deal with a syllable starting at bindex, ending at eindex
    global roots, ends, exceptions, ignored_chars
    rootinfo = roots.get_longest_match_with_data(tibstr, bindex, eindex, ignored_chars)
    if not rootinfo:
        return -1
    endinfo = ends.get_longest_match_with_data(tibstr, rootinfo['i'], eindex, ignored_chars)
    if not endinfo:
        return -1
    if endinfo['i'] < eindex and _is_tib_letter(tibstr[endinfo['i']]) and (tibstr[endinfo['i']] not in ignored_chars):
        return -1
    state.combineWith(rootinfo['d'], endinfo['d'])
    assert(endinfo['i']>bindex)
    return endinfo['i']

def get_phonetics(tibstr, bindex=0, eindex=-1, pos=None, endOfSentence=False, schema=0, options={}):
    if eindex == -1:
        eindex = len(tibstr)
    i = _get_next_letter_index(tibstr, bindex, eindex)
    if (i==-1):
        return ''
    state = PhonStateMST(options, pos, endOfSentence)
    while i < eindex and i >= 0: # > 0 covers the case where next_letter_index returns -1
        exceptioninfo = exceptions.get_longest_match_with_data(tibstr, i, eindex, ignored_chars)
        if (exceptioninfo and (state.position > 0 or not exceptioninfo['d'].startswith('2:'))) and (
                exceptioninfo['i'] >= eindex or not _is_tib_letter(tibstr[exceptioninfo['i']])):
            # if it starts with '2:' and we're in the first syllable, we ignore it:
            if exceptioninfo['d'].startswith('2:'):
                exceptioninfo['d'] = exceptioninfo['d'][2:]
            state.combineWithException(exceptioninfo['d'])
            nextidx = _get_next_letter_index(tibstr, exceptioninfo['i']+1, eindex)
            if nextidx == -1:
                nextidx = eindex
            assert(i < nextidx)
            i = nextidx
            continue
        # we combine syllable per syllable, first we search the end of next syllable:
        lastidx = _get_next_non_letter_index(tibstr, i, eindex)
        #print("found syllable '"+tibstr[i:lastidx]+"'")
        if lastidx == -1:
            lastidx = eindex
        matchlastidx = _combine_next_syll_phon(tibstr, i, state, lastidx)
        if matchlastidx == -1:
            print("couldn't understand syllable "+tibstr[i:lastidx])
            break
        if matchlastidx < lastidx:
            print("couldn't understand last "+str(lastidx-matchlastidx)+" characters of syllable "+tibstr[i:lastidx])
        i = _get_next_letter_index(tibstr, matchlastidx, eindex)
    state.finish()
    return state.phon
