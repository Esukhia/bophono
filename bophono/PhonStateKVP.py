from .PhonStateMST import PhonStateMST

class PhonStateKVP:
    def __init__(self, options={}, pos=None, endOfSentence=False):
        self.position = 0
        self.pos = pos
        self.endOfSentence = endOfSentence
        self.vowel = None
        self.final = None
        self.end = None
        self.tone = None
        self.phon = ''
        self.options = options
        self.aspirateMapping = {
            # nac = non-aspirated equivalent consonnant, na=non-aspirated IPA, a = aspirated IPA
            'kh' : {'a': 'kh', 'na': 'k', 'nac': 'k'}, #p. 435
            'khy' : {'a': 'khy', 'na': 'ky', 'nac': 'ky'}, #p. 436
            'thr' : {'a': 'tr', 'na': 'tr', 'nac': 'tr'}, #p. 436
            'th' : {'a': 'th', 'na': 't', 'nac': 't'}, #p. 437
            'ph' : {'a': 'ph', 'na': 'p', 'nac': 'p'}, #p. 439
            'rh' : {'a': 'hr', 'na': 'r', 'nac': 'r'}, #p. 440
            'lh' : {'a': 'lh', 'na': 'l', 'nac': 'l'}, #p. 441
            'tsh' : {'nac': 'ts'}, #p. 439
            'ch' : {'nac': 'c', 'a': 'c', 'nac': 'c'} #p. 439
            }


    simpleRootMapping = {
        'sh': 'sh',
        's': 's',
        'r': 'r',
        'l': 'l',
        'g': 'g',
        'd': 'd',
        'h': 'h',
        'm': 'm',
        'n': 'n',
        'ny': 'ny',
        'ng': 'ng',
        'w': 'w',
        'y': 'y'
    }

    simpleVowMapping = {
        'ä': 'e',
        'ö': 'ö',
        'u': 'u',
        'ü': 'ü',
        'i': 'i' 
    }

    simpleFinalMapping = {
        ':': 'ː',
        'm': 'm',
        'ng': 'ng',
        'g': 'g'
    }

    simplifyVowMapping = {
        'ä': 'a',
        'ö': 'o',
        'ü': 'u'
    }

    def getComplex(self, base, voiceless=False, aspirated=False):
        """ base = c, j, ts or dz, , voiceless and aspirated should be obvious  """
        res = ''
        voicelessBelow = True
        if base == 'c':
            res = 'ch'
        elif base == 'j':
            res = 'j'
        elif base == 'ts':
            res = 'ts'
        else:
            res = 'dz'
        # shouldn't be there?
        if aspirated:
            res += 'h'
        return res

    def getNextRootCommonPattern(position, tone, lastcondition, phon1, phon2, phon3):
        """ this corresponds to the most common pattern for roots: phon1 at the beginning
            of high-toned words, phon2 at the beginning of low-tones words, phon1 after
            some consonnants (if lastcondition is met), and phon3 otherwise"""
        if position == 1:
            return tone == '+' and phon1 or phon2
        return lastcondition and phon1 or phon3

    def getNextRootPhon(self, nrc): # nrc: nextrootconsonant
        # self.tone is the first tone (can be associated with current syllable)
        # self.position is the position of the syllable we're adding
        # self.final is the previous final consonnant (if any)
        if nrc.startswith('~'):
            # TODO: Do some magic here?
            nrc = nrc[1:]
        # handle aspirates, option to use them on non-first syllables
        if nrc in self.aspirateMapping:
            if self.position != 1:
                nrc = self.aspirateMapping[nrc]['nac']
            elif self.tone == '-' and not self.aspirateLowTones:
                return self.aspirateMapping[nrc]['na']
            else:
                return self.aspirateMapping[nrc]['a']
        # suffix ga is "k" except in the middle of words
        # "kn" should be separated with a space: "k n"
        # suffix ba is always b (encoded in ends.csv)
        # e at the end of a word always becomes é 
        # Exceptions: if a + i, u + i, or o + i are used as two syllables in the context of a metric system in a verse, they become a’i, u’i, or o’i
        # be’u -> "bé u""   ;   mchi’o -> "chi o"
        # dbu becomes u, dbus becomes ü
        # dba becomes wa
        # optional, from Rigpa: kun dga' -> kun-ga
        # nng or ngg -> ng
        # weak syllables: nominalizers + med, bral, bya, mi, ldan, can. "Prefix" weak syllable: rnam. Verbalizers: byed, mdzad
        if nrc in PhonStateKVP.simpleRootMapping:
            return PhonStateKVP.simpleRootMapping[nrc]
        return nrc

    def doCombineCurEnd(self, endofword, nrc='', nextvowel=''): # nrc = next root consonant
        """ combined the self.end into the self.phon """
        if not self.end:
            return
        slashi = self.end.find('/')
        if slashi != -1:
            self.end = self.end[:slashi]
        self.phon += self.end


    def combineWithException(self, exception):
        syllables = exception.split('|')
        for syl in syllables:
            indexplusminus = syl.find('+')
            if indexplusminus == -1:
                indexplusminus = syl.find('-')
            if indexplusminus == -1:
                print("invalid exception syllable: "+syl)
                continue
            self.combineWith(syl[:indexplusminus+1], syl[indexplusminus+1:])

    def combineWith(self, nextroot, nextend):
        nextrootconsonant = nextroot
        nextvowel = ''
        self.doCombineCurEnd(False, nextrootconsonant, nextvowel)
        self.position += 1
        nextrootphon = self.getNextRootPhon(nextrootconsonant)
        self.phon += nextrootphon
        # decompose multi-syllable ends:
        if nextend.find('|') != -1:
            ends = nextend.split('|')
            self.end = ends[0]
            for endsyl in ends[1:]:
                # we suppose that roots are always null
                self.combineWith(endsyl[:1], endsyl[1:])
        else:
            self.end = nextend
    
    def finish(self):
        self.doCombineCurEnd(True)

if __name__ == '__main__':
    """ Example use """
    s = PhonStateKVP()
    s.combineWith("k+", "ak")
    s.finish()
    print(s.phon)
