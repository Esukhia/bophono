import re

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
        self.accentuateWL = options['accentuateWL'] if 'accentuateWL' in options else ["rime", "de", "ame", "chone", "dune", "dome", "tone", "chime", "done", "mine", "lame", "pale", "mare"]
        self.accentuateall = options['accentuateWL'] if 'accentuateWL' in options else True

    def doCombineCurEnd(self, endofword, nrc='', nextvowel=''): # nrc = next root consonant
        """ combined the self.end into the self.phon """
        if not self.end:
            return
        # ' from ends.csv should be replaced with a space
        self.end = self.end.replace("'", ' ')
        # suffix ga is "k" except in the middle of words
        if self.end.endswith("k") and not endofword:
            self.end = self.end[:-1]+"g"
        if self.end.endswith("ng") and nrc.startswith("g"):
            self.end = self.end[:-1]
        if self.end.endswith("ng") and nrc.startswith("ng"):
            self.end = self.end[:-2]
        if self.end.endswith("g") and nrc.startswith("g"):
            self.end = self.end[:-1]+"k"
        if self.end.endswith("n") and nrc.startswith("n"):
            self.end = self.end[:-1]
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
        if nextrootconsonant == "-":
            self.phon += ""
        elif nextrootconsonant.startswith("dz") and self.position > 1:
            self.phon += "z"
        elif nextrootconsonant.startswith("tdr"):
            # Here the KVP rules have the rather puzzling convention to have different rules
            # for syllables that have the exact same phonology in Tibetan. It has:
            # བྲ -> always dra
            # དྲ -> dra in second position, tra in first position
            # which doesn't make sense as Tibetans make no difference between བྲ and དྲ.
            # We thus have to artificially differentiate them at the phonological level recorded in roots.csv
            # By having "tdra" for དྲ.
            if self.position == 1:
                self.phon += "tr"
            else:
                self.phon += "dr"
        else:
            self.phon += nextrootconsonant
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
