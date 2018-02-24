class PhonStateNT:
    def __init__(self):
        self.position = 0
        self.rootconsonant = None
        self.vowel = None
        self.final = None
        self.end = None
        self.tone = None
        self.phon = ''
  
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
        'n': 'n', #p. 442
        'ng': 'ŋ', #p. 442
        'w': 'w', #p. 443
        'y': 'j' #p. 443
    }

    simpleEndMapping = {
        'ä': 'ɛ', #p. 443
        'ö': 'ø', #p. 444
        'u': 'u', #p. 444
        'ü': 'y', #p. 444
        'i': 'i' #p. 444
    }

    def getNextRootPhon(self, nrc): # nrc: nextrootconsonant
        if nrc.startswith('~'):
            # TODO: Do some magic here?
            nrc = nrc[1:]
        if nrc in PhonStateNT.simpleRootMapping:
            return PhonStateNT.simpleRootMapping[nrc]
        return nrc

    def doCombineCurEnd(self, endofword, rootconsonant=''):
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
        self.phon += "v"

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
        rootconsonant = nextroot[:-1]
        self.doCombineCurEnd(False, rootconsonant)
        nextrootphon = self.getNextRootPhon(rootconsonant)
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
