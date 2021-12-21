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
        self.splitNG = options['splitNG'] if 'splitNG' in options else False
        self.splitKN = options['splitKN'] if 'splitKN' in options else False
        self.accentuateWL = options['accentuateWL'] if 'accentuateWL' in options else ["dome", "tone", "chime", "done", "mine", "lame", "pale", "mare"]

    def getNextRootCommonPattern(position, tone, lastcondition, phon1, phon2, phon3):
        """ this corresponds to the most common pattern for roots: phon1 at the beginning
            of high-toned words, phon2 at the beginning of low-tones words, phon1 after
            some consonnants (if lastcondition is met), and phon3 otherwise"""
        if position == 1:
            return tone == '+' and phon1 or phon2
        return lastcondition and phon1 or phon3

    def doCombineCurEnd(self, endofword, nrc='', nextvowel=''): # nrc = next root consonant
        """ combined the self.end into the self.phon """
        if not self.end:
            return
        slashi = self.end.find('/')
        if slashi != -1:
            self.end = self.end[:slashi]
        # suffix ba is always b (encoded in ends.csv)
        # be’u -> "bé u""   ;   mchi’o -> "chi o" (encoded in ends.csv)
        # e at the end of a word becomes é when there's a risk of confusion with an existing English word
        # (dome, tone, chime, etc.)
        if self.end.endswith("e") and endofword:
            if self.phon+'e' in self.accentuateWL:
                self.end = self.end[:-1]+"é"
        # suffix ga is "k" except in the middle of words
        if self.end.endswith("k") and not endofword:
            self.end = self.end[:-1]+"g"
        # nng or ngg -> ng
        if self.end.endswith("g") and nrc.startswith("g"):
            self.end = self.end[:-1]
        if self.end.endswith("n") and nrc.startswith("n"):
            self.end = self.end[:-1]
        # I suppose? TODO: check
        if self.end.endswith("ng") and nrc.startswith("ng"):
            self.end = self.end[:-2]
        # optional, from Rigpa: kun dga' -> kun-ga
        if self.splitNG and self.end.endswith("n") and nrc.startswith("g"):
            self.end += "-"
        # optional, "kn" should be separated with a space: "k n"
        if self.splitKN and self.end.endswith("k") and nrc.startswith("n"):
            self.end += " "
        self.phon += self.end


    def combineWithException(self, exception):
        syllables = exception.split('|')
        for syl in syllables:
            indexplusminus = syl.find('-')
            if indexplusminus == -1:
                print("invalid exception syllable: "+syl)
                continue
            self.combineWith(syl[:indexplusminus], syl[indexplusminus+1:])

    def combineWith(self, nextroot, nextend):
        nextrootconsonant = nextroot
        nextvowel = ''
        self.doCombineCurEnd(False, nextrootconsonant, nextvowel)
        self.position += 1
        self.phon += "" if nextrootconsonant == "-" else nextrootconsonant
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
