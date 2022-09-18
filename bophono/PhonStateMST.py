class PhonStateMST:
    # This file is handling the second column of the csv files. It is based on 
    # the Manual of Standard Tibetan by Nicolas Tournadre.
    #
    # Differences with Tournadre's book (all are not destructive)
    #
    # TODO: option to voice low tone at the beginning of words
    # softaspirationchar
    # beta at the beginning of syllables
    #
    ## In phonologic representation (not IPA):
    # - tone indication: using k+a instead of kā, k-a instead of ka̱
    # - using | as syllable splitter
    # - use ~ to indicate nasalizer (ɴ in NT, p. 397)
    # - use ~ to indicate contour tone after suffix combinations ངས and མས, instead of ' (see p. 57)
    # - use k instead of ' for the sake of simplicity
    # - only use ' to indicate a possible stop after suffixes ས and ད
    # - use g as a very exceptional suffix to indicate that the IPA should be g̊, not k
    # - use j instead of : for འི affix
    # - indicate l in the phonology so that it can be reconstructed
    #
    ## In IPA (most can be configured through options)
    # - using [ɲ] instead of [ny]
    # - using [kʰ] instead of [kh]
    # - indicate syllable breaks with [.]
    # - use tone markers \u02CA and \u02CB
    # - use nasalization marker \u0303 on nasal vowels
    # - use 'ːɪ̯' instead of 'ː' for affix འི
    # - use 'a.ɪ' instead of 'ɛːɪ' (same for other vowels) for affix འི in monosyllabic contexts
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
        self.hightonechar = options['hightonechar'] if 'hightonechar' in options else '˥' # \u0301 for phonological tones
        self.lowtonechar = options['lowtonechar'] if 'lowtonechar' in options else '˩˨'# \u0300 for phonological tones
        self.highfallingtonechar = options['highfallingtonechar'] if 'highfallingtonechar' in options else '˥˨'
        self.lowrisingfallingtonechar = options['lowrisingfallingtonechar'] if 'lowrisingfallingtonechar' in options else '˩˧˨'
        self.nasalchar = options['nasalchar'] if 'nasalchar' in options else '\u0303'
        self.syllablesepchar = options['syllablesepchar'] if 'syllablesepchar' in options else '.'
        # fully voice beginning of low tone words
        self.voicebowlowtone = options['voicebowlowtone'] if 'voicebowlowtone' in options else True
        # put a w before low tone words starting with a round vowel
        self.wbeforeround = options['wbeforeround'] if 'wbeforeround' in options else True
        self.eatR = options['eatR'] if 'eatR' in options else False
        self.eatL = options['eatL'] if 'eatL' in options else False
        self.eatP = options['eatP'] if 'eatP' in options else True
        # this is rather complex: basically 
        self.gsuffixstrategy = options['gsuffixstrategy'] if 'gsuffixstrategy' in options else "simple"
        self.gsuffixchar = options['gsuffixchar'] if 'gsuffixchar' in options else "simple"
        self.aiAffixchar = options['aiAffixchar'] if 'aiAffixchar' in options else 'ːɪ̯'
        self.aiAffixmonochar = options['aiAffixmonochar'] if 'aiAffixmonochar' in options else self.syllablesepchar+'ɪ'
        # does the འི affix in monosyllabic words change the vowel sound (a -> ä) or not (defaults to not)
        self.aiAffixmonomodif = options['aiAffixmonomodif'] if 'aiAffixmonomodif' in options else False
        # rules the way stops after suffixes ས and ད are handled, can be "eos" (end of sentence), "eow" (end of word)
        # anything else will not print any stop
        self.stopSDMode = 'stopSDMode' in options and options['stopSDMode'] or "eos"
        # use k̚ instead of ʔ
        self.useUnreleasedStops = options['useUnreleasedStops'] if 'useUnreleasedStops' in options else True
        # weak aspiration character
        self.weakAspirationChar = options['weakAspirationChar'] if 'weakAspirationChar' in options else 'ʰ'
        self.aspirateLowTones = options['aspirateLowTones'] if 'aspirateLowTones' in options else False
        # gemminates strategy: "no" => don't do anything, "len" => lengthen preceding vowel, "lentone" => lengthen + tone change
        self.aspirateMapping = {
            # nac = non-aspirated equivalent consonnant, na=non-aspirated IPA, a = aspirated IPA
            'kh' : {'a': 'kʰ', 'na': 'k', 'nac': 'k'}, #p. 435
            'khy' : {'a': 'cʰ', 'na': 'c', 'nac': 'ky'}, #p. 436
            'thr' : {'a': 'ʈʰ', 'na': 'ʈ', 'nac': 'tr'}, #p. 436
            'th' : {'a': 'tʰ', 'na': 't', 'nac': 't'}, #p. 437
            'ph' : {'a': 'pʰ', 'na': 'p', 'nac': 'p'}, #p. 439
            'rh' : {'a': 'ʂ', 'na': 'r', 'nac': 'r'}, #p. 440
            'lh' : {'a': 'l̥ʰ', 'na': 'l̥', 'nac': 'l'}, #p. 441
            'tsh' : {'nac': 'ts'}, #p. 439
            'ch' : {'nac': 'c'} #p. 439
            }
        self.aspirateMapping['ch']['a'] = self.getComplex('c', False, True)
        self.aspirateMapping['ch']['na'] = self.getComplex('c')
        self.aspirateMapping['tsh']['a'] = self.getComplex('ts', False, True)
        self.aspirateMapping['tsh']['na'] = self.getComplex('ts')
  
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

    def getComplex(self, base, voiceless=False, aspirated=False):
        """ base = c, j, ts or dz, , voiceless and aspirated should be obvious  """
        res = ''
        voicelessBelow = True
        if base == 'c':
            res = 'tɕ'
        elif base == 'j':
            res = 'dʑ'
        elif base == 'ts':
            res = 'ts'
        else:
            res = 'dz'
        if voiceless:
            res += voicelessBelow and '\u0325' or '\u030A'
        if aspirated:
            res += 'ʰ'
        return res

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
        'g': 'g̊' # only in exceptions, see comment at the top of the file
    }

    simplifyVowMapping = {
        'ä': 'a',
        'ö': 'o',
        'ü': 'u'
    }

    def getNextRootCommonPattern(self, position, tone, lastcondition, phon1, phon2, phon3):
        """ this corresponds to the most common pattern for roots: phon1 at the beginning
            of high-toned words, phon2 at the beginning of low-tones words, phon1 after
            some consonnants (if lastcondition is met), and phon3 otherwise"""
        if position == 1:
            return tone == '+' and phon1 or (self.voicebowlowtone and phon2 or phon3)
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
            elif self.tone == '-':
                if not self.aspirateLowTones:
                    return self.aspirateMapping[nrc]['na']
                else:
                    res = self.aspirateMapping[nrc]['a']
                    if self.weakAspirationChar != 'ʰ':
                        res = res.replace('ʰ', self.weakAspirationChar)
                    return res
            else:
                return self.aspirateMapping[nrc]['a']
        if nrc in PhonStateMST.simpleRootMapping:
            return PhonStateMST.simpleRootMapping[nrc]
        if nrc == '':
            return ''
        if nrc == 'k':
            lastcond = (self.final == 'p')
            return self.getNextRootCommonPattern(self.position, self.tone, lastcond, 'k', 'g', 'g̊')
        if nrc == 'ky':
            lastcond = (self.final == 'p')
            return self.getNextRootCommonPattern(self.position, self.tone, lastcond, 'c', 'ɟ', 'ɟ̊')
        if nrc == 'tr':
            lastcond = (self.final == 'p' or self.final == 'k')
            return self.getNextRootCommonPattern(self.position, self.tone, lastcond, 'ʈ', 'ɖ', 'ɖ̥')
        if nrc == 't':
            lastcond = (self.final == 'p' or self.final == 'k')
            return self.getNextRootCommonPattern(self.position, self.tone, lastcond, 't', 'd', 'd̥')
        if nrc == 'p':
            lastcond = (self.final == 'k')
            return self.getNextRootCommonPattern(self.position, self.tone, lastcond, 'p', 'b', 'b̥')
        if nrc == 'c':
            lastcond = (self.final == 'p' or self.final == 'k')
            opt1 = self.getComplex('c')
            opt2 = self.getComplex('j')
            opt3 = self.getComplex('j', True)
            return self.getNextRootCommonPattern(self.position, self.tone, lastcond, opt1, opt2, opt3)
        if nrc == 'ts':
            opt1 = self.getComplex('ts')
            opt2 = self.getComplex('dz')
            opt3 = self.getComplex('dz', True)
            lastcond = (self.final == 'p' or self.final == 'k')
            return self.getNextRootCommonPattern(self.position, self.tone, lastcond, opt1, opt2, opt3)
        print("unknown root consonant: "+nrc)
        return nrc

    def doCombineCurEnd(self, endofword, nrc='', nextvowel=''): # nrc = next root consonant
        """ combined the self.end into the self.phon """
        if not self.end:
            return
        slashi = self.end.find('/')
        if slashi != -1:
            self.end = self.end[:slashi]
        modulated = False
        if self.end.endswith('~'):
            modulated = True
            self.end = self.end[:-1]
        self.final = PhonStateMST.getFinal(self.end)
        # nasal prefix (not in NT) TODO: use white list instead
        if nrc.startswith('~'):
            nrc = nrc[1:]
            # TODO: maybe output several possibilities?
        ## vowels:
        # འི affix:
        aiAffix = False
        if self.end.endswith('j'):
            aiAffix = True
            self.end = self.end[:-1]
        self.vowel = self.end[:1]
        if self.position == 1 and endofword and aiAffix:
            if not self.aiAffixmonomodif and self.vowel in PhonStateMST.simplifyVowMapping:
                self.vowel = PhonStateMST.simplifyVowMapping[self.vowel]
        vowelPhon = ''
        nasalPhon = ''
        tonePhon = ''
        postVowelPhon = ''
        # geminates
        geminates = False
        unaspired_nrc = nrc
        if nrc in self.aspirateMapping:
            unaspired_nrc = self.aspirateMapping[nrc]['nac']
        if unaspired_nrc == self.final and self.final != '':
            geminates = True # p. 37
            postVowelPhon = 'ː'
        # main vowel code 
        if self.vowel in PhonStateMST.simpleVowMapping:
            vowelPhon = PhonStateMST.simpleVowMapping[self.vowel]
        elif self.vowel == 'a':
            # here we consider that a geminate is an open syllable
            if self.position == 1 and (geminates or self.final != 'p'):
                vowelPhon = 'a'
            else:
                vowelPhon = 'ə'
        elif self.vowel == 'e':
            # case is unclear for geminates
            if self.final != '' and self.final != 'ng':
                vowelPhon = 'ɛ'
            else:
                vowelPhon = 'e'
        elif self.vowel == 'o':
            # case is unclear for geminates
            if self.final != '' and self.final != 'ng':
                vowelPhon = 'ɔ'
            else:
                vowelPhon = 'o'
        else:
            print("unknown vowel: "+self.vowel)
        # add w at beginning of low tone words:
        if self.position == 1 and self.tone == '-' and self.vowel in ['ö', 'o', 'u'] and self.phon == '' and self.wbeforeround:
            self.phon += 'w'
        if self.position == 1:
            # by default we keep the tones flat (this is actually a bit unclear in the MST)
            tonePhon = self.tone == '+' and self.hightonechar or self.lowtonechar
            # MST, p. 36: some tones are modulated
            if (not geminates and self.final in ['p', 'k', "'"]) or modulated:
                tonePhon = self.tone == '+' and self.highfallingtonechar or self.lowrisingfallingtonechar
        if aiAffix:
            if self.position == 1 and endofword:
                postVowelPhon = self.aiAffixmonochar
            else:
                postVowelPhon = self.aiAffixchar
        ## Suffix
        finalPhon = ''
        if self.final == 'ng':
            nasalPhon = self.nasalchar
        if geminates:
            pass
        elif self.final in PhonStateMST.simpleFinalMapping:
            finalPhon = PhonStateMST.simpleFinalMapping[self.final]
        elif self.final == 'k':
            if not endofword: # p. 433
                if unaspired_nrc in ['p', 't', 'tr', 'ts', 'c', 's']:
                    finalPhon = 'k'
                elif self.vowel in ['i', 'e'] and unaspired_nrc in ['l', 'sh']:
                    finalPhon = 'k'
                elif unaspired_nrc in ['r']:
                    finalPhon = 'g̊'
                elif self.vowel not in ['e', 'i'] and unaspired_nrc in ['l', 'sh', 'm', 'ny', 'n', 'ng']:
                    finalPhon = 'ɣ'
                elif unaspired_nrc in ['k', 'ky', 'w', 'y']:
                    finalPhon = ''
                elif self.vowel in ['e', 'i'] and unaspired_nrc in ['m', 'ny', 'n', 'ng']:
                    finalPhon = 'ŋ'
                else:
                    print("unhandled case, this shouldn't happen, nrc: "+nrc+", vowel: "+self.vowel)
            else:
                finalPhon = self.useUnreleasedStops and 'ʔk̚' or 'ʔ'
        elif self.final == 'p':
            if not endofword:
                if unaspired_nrc in ['p', 't', 'tr', 'ts', 'c', 's', 'sh']:
                    finalPhon = 'p'
                else:
                    # uncommon in words but can appear in pronouncation, especially before gnyis
                    finalPhon = 'p'
            else:
                finalPhon = self.eatP and (self.useUnreleasedStops and 'ʔp̚' or 'ʔ') or 'p' # TODO: check
        elif self.final == 'n': # p. 442
            if not endofword:
                if unaspired_nrc in ['t', 'tr']:
                    finalPhon = 'n'
                elif unaspired_nrc == 'p':
                    finalPhon = 'm'
                elif unaspired_nrc == 'k':
                    finalPhon = 'ŋ'
                elif unaspired_nrc == 'ky':
                    finalPhon = 'ɲ'
                else:
                    # this case is a bit unclear in the MST
                    finalPhon = 'n'
            else:
                finalPhon = self.useUnreleasedStops and 'n̚' or ''
                nasalPhon += self.nasalchar
        elif self.final == 'r':
            finalPhon = self.eatR and 'ː' or 'r'
        elif self.final == 'l':
            finalPhon = self.eatL and 'ː' or 'l'
        elif self.final == '':
            finalPhon = ''
        elif self.final == "'":
            if endofword:
                if (self.stopSDMode == "eos" and self.endOfSentence) or self.stopSDMode == "eow":
                    finalPhon = 'ʔ'
        else:
            print("unrecognized final: "+self.final)
        self.phon += vowelPhon+nasalPhon+tonePhon+postVowelPhon
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
        if self.position == 0:
            self.tone = nextroot[-1]
        nextrootconsonant = nextroot[:-1]
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
    s = PhonStateMST()
    s.combineWith("k+", "ak")
    s.finish()
    print(s.phon)
