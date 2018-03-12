class PhonStateNT:
    # Differences with Tournadre's book
    #
    ## In intermediate representation (not IPA):
    # - using k+a instead of kā, k-a instead of ka̱
    # - using | as syllable splitter
    # - use ~ to indicate nasalizer (small capital N in NT, p. 397)
    # - use ~ to indicate contour tone after suffix combinations ངས and མས, instead of ' (see p. 57)
    # - use k instead of ' for the sake of simplicity
    # - only use ' to indicate a possible stop after suffixes ས and ད
    # - use g as a very exceptional suffix to indicate that the IPA should be g̥, not k
    #
    ## In IPA (most can be configured through options)
    # - using [ɲ] instead of [ny]
    # - using [kʰ] instead of [kh]
    # - indicate syllable breaks with [.]
    # - use tone markers \u02CA and \u02CB
    # - use nasalization marker \u0303 on nasal vowels
    # - use unreleased stops [p̚], [n̚], [k̚] instead of glottal stop [ʔ]
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
        self.hightonechar = 'hightonechar' in options and options['hightonechar'] or '\u02CA'
        self.lowtonechar = 'lowtonechar' in options and options['lowtonechar'] or '\u02CB'
        self.nasalchar = 'nasalchar' in options and options['nasalchar'] or '\u0303'
        self.syllablesepchar = 'syllablesepchar' in options and options['syllablesepchar'] or '.'
        self.syllablesepchar = 'syllablesepchar' in options and options['syllablesepchar'] or '.'
        self.eatR = 'eatR' in options and options['eatR'] or False
        self.eatL = 'eatL' in options and options['eatL'] or False
        self.eatP = 'eatP' in options and options['eatP'] or True
        self.eatK = 'eatK' in options and options['eatK'] or True
        # rules the way stops after suffixes ས and ད are handled, can be "eos" (end of sentence), "eow" (end of word)
        # anything else will not print any stop
        self.stopSDMode = 'stopSDMode' in options and options['stopSDMode'] or "eos"
        self.useUnreleasedStops = 'useUnreleasedStops' in options and options['useUnreleasedStops'] or True
        self.aspirateLowTones = 'aspirateLowTones' in options and options['aspirateLowTones'] or False
  
    def getFinal(endstr):
        """ returns the final consonant or empty string """
        if not endstr:
            return ''
        simplesuffixes = ['m', 'p', 'n', "'", 'k', 'r', 'l', 'g']
        lastchar = endstr[-1]
        if endstr.endswith('ng'):
            return 'ng'
        elif lastchar in simplesuffixes:
            return lastchar
        return ''

    #TODO: remove aspiration on low tones
    simpleRootMapping = {
        'sh': 'ɕ', #p. 440
        's': 's', #p. 440
        'r': 'r', #p. 441
        'l': 'l', #p. 441
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
        ':': 'ː', #p. 435
        'm': 'm', #p. 444
        'ng': 'ŋ', #p. 442
        'g': 'g̥' # only in exceptions, see comment at the top of the file
    }

    aspirateMapping = {
        # nac = non-aspirated equivalent consonnant, na=non-aspirated IPA, a = aspirated IPA
        'kh' : {'a': 'kʰ', 'na': 'k', 'nac': 'k'}, #p. 435
        'khy' : {'a': 'cʰ', 'na': 'c', 'nac': 'ky'}, #p. 436
        'thr' : {'a': 'ʈʰ', 'na': 'ʈ', 'nac': 'tr'}, #p. 436
        'th' : {'a': 'tʰ', 'na': 't', 'nac': 't'}, #p. 437
        'ph' : {'a': 'pʰ', 'na': 'p', 'nac': 'p'}, #p. 439
        'ch' : {'a': 'tɕʰ', 'na': 'tɕ', 'nac': 'c'}, #p. 439
        'tsh' : {'a': 'tsʰ', 'na': 'ts', 'nac': 'ts'}, #p. 439
        'rh' : {'a': 'ʂ', 'na': 'r', 'nac': 'r'}, #p. 440
        'lh' : {'a': 'l̥ʰ', 'na': 'l̥', 'nac': 'l'} #p. 441
    }

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
        if nrc in PhonStateNT.aspirateMapping:
            if self.position != 1:
                nrc = PhonStateNT.aspirateMapping[nrc]['nac']
            elif self.tone == '-' and not self.aspirateLowTones:
                return PhonStateNT.aspirateMapping[nrc]['na']
            else:
                return PhonStateNT.aspirateMapping[nrc]['a']
        if nrc in PhonStateNT.simpleRootMapping:
            return PhonStateNT.simpleRootMapping[nrc]
        if nrc == '':
            return ''
        if nrc == 'k':
            lastcond = (self.final == 'p')
            return PhonStateNT.getNextRootCommonPattern(self.position, self.tone, lastcond, 'k', 'g', 'g̥')
        if nrc == 'ky':
            lastcond = (self.final == 'p')
            return PhonStateNT.getNextRootCommonPattern(self.position, self.tone, lastcond, 'c', 'ɟ', 'ɟ̥')
        if nrc == 'tr':
            lastcond = (self.final == 'p' or self.final == 'k')
            return PhonStateNT.getNextRootCommonPattern(self.position, self.tone, lastcond, 'ʈ', 'ɖ', 'ɖ̥')
        if nrc == 't':
            lastcond = (self.final == 'p' or self.final == 'k')
            return PhonStateNT.getNextRootCommonPattern(self.position, self.tone, lastcond, 't', 'd', 'd̥')
        if nrc == 'p':
            lastcond = (self.final == 'k')
            return PhonStateNT.getNextRootCommonPattern(self.position, self.tone, lastcond, 'p', 'b', 'b̥')
        if nrc == 'c':
            lastcond = (self.final == 'p' or self.final == 'k')
            return PhonStateNT.getNextRootCommonPattern(self.position, self.tone, lastcond, 'tɕ', 'dʑ', 'ɖ̥ʑ')
        if nrc == 'ts':
            lastcond = (self.final == 'p' or self.final == 'k')
            return PhonStateNT.getNextRootCommonPattern(self.position, self.tone, lastcond, 'ts', 'dz', 'dz̥')
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
        modulated = False
        if self.end.endswith('~'):
            modulated = True
            self.end = self.end[:-1]
        self.final = PhonStateNT.getFinal(self.end)
        # p. 36, we use the following notation:
        # '+_' flat high tone
        # '+\' for falling high tone
        # '-_' for low tone flat, slightly rising
        # '-^' for low tone rising followed by short fall
        tonecountour = self.tone
        if self.final in ['', 'n', 'm', 'ng']:
            tonecountour = self.tone == '+' and '+_' or '-_'
        elif self.final in ['p', 'k'] or (modulated and self.final in ['m', 'n', 'ng']):
            tonecountour = self.tone == '+' and '+\\' or '-^'
        # nasal prefix (not in NT) TODO: use white list instead
        if nrc.startswith('~'):
            nrc = nrc[1:]
            # TODO: maybe output several possibilities?
        ## vowels:
        vowelPhon = ''
        if self.vowel in PhonStateNT.simpleVowMapping:
            vowelPhon = PhonStateNT.simpleVowMapping[self.vowel]
        elif self.vowel == 'a':
            if (self.position == 1 and self.final != 'p') or self.final == 'ng':
                vowelPhon = 'a'
            else:
                vowelPhon = 'ə'
        elif self.vowel == 'e':
            if self.final != '' and self.final != 'ng':
                vowelPhon = 'ɛ'
            else:
                vowelPhon = 'e'
        elif self.vowel == 'o':
            if self.final != '' and self.final != 'ng':
                vowelPhon = 'ɔ'
            else:
                vowelPhon = 'o'
        else:
            print("unknown vowel: "+self.vowel)
        if self.final == 'ng':
            vowelPhon += self.nasalchar
        # add w at beginning of low tone words:
        if self.position == 1 and self.tone == '-' and self.vowel in ['ö', 'o', 'u'] and self.phon == '':
            self.phon += 'w'
        self.phon += vowelPhon
        if self.position == 1:
            self.phon += self.tone == '+' and self.hightonechar or self.lowtonechar
        finalPhon = ''
        if self.final in PhonStateNT.simpleFinalMapping:
            finalPhon = PhonStateNT.simpleFinalMapping[self.final]
        elif self.final == 'k':
            if not endofword: # p. 433
                if nrc in ['p', 't', 'tr', 'ts', 'c', 's']:
                    finalPhon = self.eatK and (self.useUnreleasedStops and 'k̚' or 'ʔ') or 'k'
                elif self.vowel in ['i', 'e'] and nrc in ['l', 'sh']:
                    finalPhon = 'k'
                elif nrc in ['r']:
                    finalPhon = 'g̥'
                elif self.vowel not in ['e', 'i'] and nrc in ['l', 'sh', 'm', 'ny', 'n', 'ng']:
                    finalPhon = 'ɣ'
                elif nrc in ['k', 'ky', 'w', 'y']:
                    finalPhon = ''
                elif self.vowel in ['e', 'i'] and nrc in ['m', 'ny', 'n', 'ng']:
                    finalPhon = 'ŋ'
                else:
                    print("unhandled case, this shouldn't happen, nrc: "+nrc+", vowel: "+self.vowel)
            else:
                finalPhon = self.useUnreleasedStops and 'k̚' or 'ʔ'
        elif self.final == 'p':
            if not endofword:
                if nrc in ['p', 't', 'tr', 'ts', 'c', 's', 'sh']:
                    finalPhon = 'p'
                else:
                    finalPhon = self.eatP and (self.useUnreleasedStops and 'p̚' or 'ʔ') or 'b̥'
            else:
                finalPhon = self.eatP and (self.useUnreleasedStops and 'p̚' or 'ʔ') or 'b̥' # TODO: check
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
                    finalPhon = self.useUnreleasedStops and 'n̚' or ''
            else:
                finalPhon = self.useUnreleasedStops and 'n̚' or '' # TODO: or '~'?
        elif self.final == 'r':
            finalPhon = self.eatR and 'ː' or 'r'
        elif self.final == 'l':
            finalPhon = self.eatL and 'ː' or 'l'
        elif self.final == '':
            finalPhon = ''
        elif self.final == "'":
            if endofword:
                if (self.stopSDMode == "eos" and self.endOfSentence) or self.stopSDMode == "eow":
                    finalPhon = self.useUnreleasedStops and 'k̚' or 'ʔ'
        else:
            print("unrecognized final: "+self.final)
        self.phon += finalPhon
        if not endofword:
            self.phon += self.syllablesepchar

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
        slashi = nextroot.find('/')
        if slashi != -1:
            if self.position > 0:
                nextroot = nextroot[slashi+1:]
            else:
                nextroot = nextroot[:slashi]
        if self.position == 0:
            self.tone = nextroot[-1]
        nextrootconsonant = nextroot[:-1]
        nextvowel = ''
        self.doCombineCurEnd(False, nextrootconsonant, nextvowel)
        self.position += 1
        nextrootphon = self.getNextRootPhon(nextrootconsonant)
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
