class PhonStateCAT:

    def __init__(self, options={}, pos=None, endOfSentence=False):
        self.position = 0
        self.pos = pos
        self.latent = ''
        self.endOfSentence = endOfSentence
        self.vowel = ''
        self.final = None
        self.end = None
        self.tone = None
        self.phon = ''
        self.options = options
        self.syllablesepchar = 'syllablesepchar' in options and options['syllablesepchar'] or '.'
        self.nasalchar = 'nasalchar' in options and options['nasalchar'] or '\u0303'
        self.latentExpression = 'latentExpression' in options and options['latentExpression'] or 'afteropen'
        # use k̚ instead of ʔ
        self.useUnreleasedStops = 'useUnreleasedStops' in options and options['useUnreleasedStops'] or True
        # retroflex instead of alveo-palatal, ex: ʈʂ instead of tɕ
        self.useRetroflex = 'useRetroflex' in options and options['useRetroflex'] or True
        # gemminates strategy: "no" => don't do anything, "len" => lengthen preceding vowel, "lentone" => lengthen + tone change
        self.gemminatesStrategy = 'gemminatesStrategy' in options and options['gemminatesStrategy'] or 'len'
        self.simpleRootMapping = { # p. 7
            'k': 'k',
            'k+': 'kʰ',
            'g': 'g',
            'j': self.getComplex('j'),
            't': 't',
            't+': 'tʰ',
            'd': 'd',
            'p': 'p',
            'p+': 'pʰ',
            'b': 'b',
            'dz': self.getComplex('dz'),
            'zh': 'ʒ',
            'z': 'z',
            'tr': 'ʈ', # tr in the book
            'tr+': 'ʈʰ',
            'dr': 'd͡ʐ',
            'sr': 'ʂ',
            'R': 'ʁ',
            'hw': 'hw',
            'Rw': 'ʁw',
            's': 's',
            's+': 'sʰ',
            'sh': 'ɕ',
            'l+': 'ɬ',
            'l': 'l',
            'h': 'h',
            'm': 'm',
            'n': 'n',
            'ny': 'ɲ',
            'ng': 'ŋ',
            'w': 'w',
            'y': 'j',
            'x': 'x', # not sure about that
            'ts': self.getComplex('ts'),
            'ts+': self.getComplex('ts', aspirated=True),
            'c': self.getComplex('c'),
            'c+': self.getComplex('c', aspirated=True),
        }
  
    simpleLatentMapping = {
        'm': 'ŋ',
        '\'': 'ŋ',
        'b': 'b', # is f or v sometimes
        'r': 'ʁ',
        'l': 'r', # ?
        's': 'x' # ?
    }

    simpleFinalMapping = {
        ':': 'ː',
        'm': 'm',
        'ng': 'ŋ',
        'x': 'x', # ?
        'r': '',
        'l': 'l',
        'n': 'n',
        't': 'l', # p.40: could be t as an option
        'b': 'b', # p. 40: could be v as an option
    }

    def getFinal(endstr):
        """ returns the final consonant or empty string """
        if not endstr:
            return ''
        if endstr.endswith('ng'):
            return 'ng'
        lastchar = endstr[-1]
        if lastchar in ['m', 'b', 'n', "x", 'r', 'l', 't', 'x']:
            return lastchar
        return ''

    def getComplex(self, base, aspirated=False):
        """ base = c, j, ts or dz, , voiceless and aspirated should be obvious  """
        res = ''
        if base == 'c':
            res = self.useRetroflex and 'ʈ͡ʂ' or 't͡ɕ'
        elif base == 'j':
            res = self.useRetroflex and 'ɖ͡ʐ' or 'd͡ʑ'
        elif base == 'ts':
            res = 't͡s'
        else:
            res = 'd͡z'
        if aspirated:
            res += 'ʰ'
        return res

    def getNextRootPhon(self, nrc): # nrc: nextrootconsonant
        # self.tone is the first tone (can be associated with current syllable)
        # self.position is the position of the syllable we're adding
        # self.final is the previous final consonnant (if any)
        if nrc.startswith('['):
            self.latent = nrc[1]
            nrc = nrc[3:]
        else:
            self.latent = ''
        if nrc in self.simpleRootMapping:
            return self.simpleRootMapping[nrc]
        elif nrc == 'r':
            return self.position == 1 and 'ʐ' or 'ɾ'
        elif nrc == '':
            pass
        print("unknown root consonant: "+nrc)
        return nrc

    def doCombineCurEnd(self, endofword, nrc='', nextvowel=''): # nrc = next root consonant
        """ combined the self.end into the self.phon """
        if not self.end:
            return
        self.final = PhonStateCAT.getFinal(self.end)
        nasalPhon = ''
        tonePhon = ''
        postVowelPhon = ''
        # geminates
        geminates = False
        self.vowel = self.end[:1]
        vowelPhon = self.vowel
        if nrc == self.final and self.final != '':
            geminates = True
            if self.gemminatesStrategy == 'len' or self.gemminatesStrategy == 'lentone':
                postVowelPhon = 'ː'
        ## Suffix
        finalPhon = ''
        if self.final == 'ng':
            nasalPhon = self.nasalchar # ?
        if geminates:
            pass
        elif self.final in PhonStateCAT.simpleFinalMapping:
            finalPhon = PhonStateCAT.simpleFinalMapping[self.final]
        elif self.final == '':
            if self.latent != '':
                finalPhon = PhonStateCAT.simpleLatentMapping[self.latent]
            finalPhon = ''
        else:
            print("unrecognized final: "+self.final)
        self.phon += vowelPhon+nasalPhon+postVowelPhon+finalPhon
        if not endofword:
            self.phon += self.syllablesepchar

    def combineWithException(self, exception):
        syllables = exception.split('|')
        for syl in syllables:
            indexsep = syl.find('-')
            if indexsep == -1:
                print("invalid exception syllable: "+syl)
                continue
            self.combineWith(syl[:indexsep+1], syl[indexsep+1:])

    def combineWith(self, nextroot, nextend):
        nextvowel = ''
        self.doCombineCurEnd(False, nextroot, nextvowel)
        self.position += 1
        nextrootphon = self.getNextRootPhon(nextroot)
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
