class PhonStateNT:
    def __init__(self, options={}):
        self.position = 0
        self.rootconsonant = None
        self.vowel = None
        self.final = None
        self.end = None
        self.tone = None
        self.phon = ''
        self.options = options
  
    def getFinal(endstr):
        """ returns the final consonant or '' """
        if not endstr:
            return ''
        simplesuffixes = "mpn'krl"
        lastchar = endstr[-1]
        if lastchar == 'g':
            return 'ng'
        elif lastchar in simplesuffixes:
            return lastchar
        return ''

    simpleRootMapping = {
        'kh': 'kʰ', #p. 435
        'khy': 'cʰ', #p. 436
        'thr': 'ʈʰ', #p. 436
        'th': 'tʰ', #p. 437
        'ph': 'pʰ', #p. 438
        'ch': 'tɕʰ', #p. 439
        'sh': 'ɕ', #p. 440
        'rh': 'ʂ', #p. 440
        's': 's', #p. 440
        'l': 'l', #p. 441
        'lh': 'l̥ʰ', #p. 441
        'h': 'h', #p. 441
        'm': 'm', #p. 441
        'n': 'n', #p. 442
        'ny': 'ɲ', #p. 442
        'ng': 'ŋ', #p. 442
        'w': 'w', #p. 443
        'y': 'j' #p. 443
    }

    simpleVowMapping = {
        'ä': 'ɛ', #p. 443
        'ö': 'ø', #p. 444
        'u': 'u', #p. 444
        'ü': 'y', #p. 444
        'i': 'i' #p. 444
    }

    simpleFinalMapping = {
        "'": 'ʔ', #p. 435
        ":": 'ː', #p. 435
        'm': 'm', #p. 444
        'ng': 'ŋ' #p. 442
    }

    def getNextRootCommonPattern(position, tone, lastcondition, phon1, phon2, phon3):
        """ this corresponds to the most common pattern for roots: phon1 at the beginning
            of high-toned words, phon2 at the beginning of low-tones words, phon1 after
            some consonnants (if lastcondition is met), and phon3 otherwise"""
        if position == 1:
            return tone == '+' and phon1 or phon2
        return lastcondition and phon1 or phon3

    def getNextRootPhon(nrc, tone, pos, lastfinal): # nrc: nextrootconsonant
        if nrc.startswith('~'):
            # TODO: Do some magic here?
            nrc = nrc[1:]
        if nrc in PhonStateNT.simpleRootMapping:
            return PhonStateNT.simpleRootMapping[nrc]
        if nrc == '':
            return ''
        if nrc == 'k':
            lastcond = (lastfinal == 'p')
            return PhonStateNT.getNextRootCommonPattern(pos, tone, lastcond, 'k', 'g', 'g̥')
        if nrc == 'ky':
            lastcond = (lastfinal == 'p')
            return PhonStateNT.getNextRootCommonPattern(pos, tone, lastcond, 'c', 'ɟ', 'ɟ̥')
        if nrc == 'tr':
            lastcond = (lastfinal == 'p' or lastfinal == 'k')
            return PhonStateNT.getNextRootCommonPattern(pos, tone, lastcond, 'ʈ', 'ɖ', 'ɖ̥')
        if nrc == 't':
            lastcond = (lastfinal == 'p' or lastfinal == 'k')
            return PhonStateNT.getNextRootCommonPattern(pos, tone, lastcond, 't', 'd', 'd̥')
        if nrc == 'p':
            lastcond = (lastfinal == 'k')
            return PhonStateNT.getNextRootCommonPattern(pos, tone, lastcond, 'p', 'b', 'b̥')
        if nrc == 'c':
            lastcond = (lastfinal == 'p' or lastfinal == 'k')
            return PhonStateNT.getNextRootCommonPattern(pos, tone, lastcond, 'tɕ', 'dʑ', 'ɖ̥ʑ')
        if nrc == 'ts':
            lastcond = (lastfinal == 'p' or lastfinal == 'k')
            return PhonStateNT.getNextRootCommonPattern(pos, tone, lastcond, 'ts', 'dz', 'dz̥')
        print("unknown root consonant: "+nrc)
        return nrc

    def doCombineCurEnd(self, endofword, nrc='', nextvowel=''): # nrc = next root consonant
        """ combined the self.end into the self.phon """
        if not self.end:
            return
        slashi = self.end.find('/')
        if slashi != -1:
            self.end = self.end[:slashi]
        self.vowel = self.end[:1]
        # do something about final ~ ?
        if self.end.endswith('~'):
            self.end = self.end[:-1]
        self.final = PhonStateNT.getFinal(self.end)
        ## vowels:
        vowelPhon = ''
        if self.vowel in PhonStateNT.simpleVowMapping:
            vowelPhon = PhonStateNT.simpleVowMapping[self.vowel]
        elif self.vowel == 'a':
            if self.position == 1 and self.final != 'p':
                vowelPhon = 'a'
            else:
                vowelPhon = 'ə'
        elif self.vowel == 'e':
            if self.final != '':
                vowelPhon = 'ɛ'
            else:
                vowelPhon = 'e'
        elif self.vowel == 'o':
            if self.final != '':
                vowelPhon = 'ɔ'
            else:
                vowelPhon = 'o'
        else:
            print("unknown vowel: "+self.vowel)
        # add w at beginning of low tone words:
        if self.position == 1 and self.vowel in "öou" and self.phon == '':
            self.phon += 'w'
        self.phon += vowelPhon
        if self.position == 1:
            self.phon += self.tone == '+' and '\u02CA' or '\u02CB'
        # TODO: option for r and l, replace : with ː
        finalPhon = ''
        if self.final in PhonStateNT.simpleFinalMapping:
            vowelPhon = PhonStateNT.simpleFinalMapping[self.final]
        elif self.final == 'k':
            if not endofword: # p. 433
                if nrc in ['p', 't', 'tr', 'ts', 'c', 's']:
                    finalPhon = 'k'
                elif self.vowel in ['i', 'e'] and nrc in ['l', 'sh']:
                    finalPhon = 'k'
                elif nrc in ['r', 'l']:
                    finalPhon = 'g̥'
                elif self.vowel in ['o', 'u', 'a'] and nrc in ['l', 'sh', 'm', 'ny', 'n', 'ng']:
                    finalPhon = 'ɣ'
                elif nrc in ['k', 'ky', 'w', 'y']:
                    finalPhon = ''
                elif self.vowel in ['e', 'i'] and nrc in ['m', 'ny', 'n', 'ng']:
                    finalPhon = 'ŋ'
                else:
                    print("unhandled case, this shouldn't happen")
            else:
                finalPhon = 'ʔ'
        elif self.final == 'p':
            if not endofword:
                if nrc in ['p', 't', 'tr', 'ts', 'c', 's', 'sh']:
                    finalPhon = 'p'
                else:
                    finalPhon = '' # TODO: or 'b̥'?
            else:
                finalPhon = 'ʔ' # TODO: option
        elif self.final == 'n':
            if not endofword:
                if nrc in ['t', 'tr']:
                    finalPhon = 'n'
                elif nrc == 'p':
                    finalPhon = 'm'
                elif nrc == 'k':
                    finalPhon = 'ŋ'
                elif nrc == 'ky':
                    finalPhon = 'ɲ'
                else:
                    finalPhon = 'n' # TODO: or ''?
            else:
                finalPhon = '' # TODO: or '~'?
        else:
            print("unrecognized final: "+self.final)
        self.phon += finalPhon


    def combineWith(self, nextroot, nextend):
        self.position += 1
        slashi = nextroot.find('/')
        if slashi != -1:
            if position > 1:
                nextroot = nextroot[slashi+1:]
            else:
                nextroot = nextroot[:slashi]
        if self.position == 1:
            self.tone = nextroot[-1]
        nextrootconsonant = nextroot[:-1]
        nextvowel = ''
        self.doCombineCurEnd(False, nextrootconsonant, nextvowel)
        nextrootphon = PhonStateNT.getNextRootPhon(nextrootconsonant, self.tone, self.position, self.final)
        self.phon += nextrootphon
        self.end = nextend
    
    def finish(self):
        self.doCombineCurEnd(True)

if __name__ == '__main__':
    """ Example use """
    s = PhonStateNT()
    s.combineWith("k+", "ak")
    s.finish()
    print(s.phon)
