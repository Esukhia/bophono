import unicodedata

class PhonStateMSTPhonology:
    # Phonological transcription of the MST intermediate representation.
    # Same data as PhonStateMST, but tones are written on the vowel as in
    # Tournadre's Manual of Standard Tibetan: macron (ā) for high tone,
    # understrike (a̱) for low tone, instead of k+a / k-a.
    HIGH_TONE = '\u0304'  # combining macron
    LOW_TONE = '\u0331'   # combining macron below

    def __init__(self, options={}, pos=None, endOfSentence=False):
        self.position = 0
        self.pos = pos
        self.endOfSentence = endOfSentence
        self.end = None
        self.phon = ''
        self.options = options
        self.syllablesepchar = options['syllablesepchar'] if 'syllablesepchar' in options else '|'

    def doCombineCurEnd(self, endofword, nrc='', nextvowel=''):
        # Syllables are combined immediately in combineWith; kept for
        # UnicodeToApi's unknownSyllableMarker path.
        return

    def _tone_char(self, tone):
        if tone == '+':
            return PhonStateMSTPhonology.HIGH_TONE
        if tone == '-':
            return PhonStateMSTPhonology.LOW_TONE
        return ''

    def _add_syllable(self, root, end):
        if root.startswith('~'):
            # nasalizer is not marked in the phonological output
            root = root[1:]
        tone = ''
        if root.endswith('+') or root.endswith('-'):
            tone = self._tone_char(root[-1])
            root = root[:-1]
        if end:
            # contour tone (ངས / མས) and da drag are not marked
            end = end.replace('~', '')
            # འ suffix is stored as a: internally; Tournadre has no length mark
            if end == 'a:':
                end = 'a'
            # འི affix is stored as j internally; Tournadre writes :
            elif end.endswith('j'):
                end = end[:-1] + ':'
        if self.phon:
            self.phon += self.syllablesepchar
        if not end:
            self.phon += root
            return
        vowel = end[0]
        rest = end[1:]
        self.phon += root + vowel + tone + rest

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
        slashi = nextend.find('/')
        if slashi != -1:
            nextend = nextend[:slashi]
        if nextend.find('|') != -1:
            ends = nextend.split('|')
            self.combineWith(nextroot, ends[0])
            for endsyl in ends[1:]:
                # subsequent parts are empty-root syllables whose first
                # character is the tone marker (e.g. a|-o)
                self.combineWith(endsyl[:1], endsyl[1:])
            return
        self.position += 1
        self.end = nextend
        self._add_syllable(nextroot, nextend)

    def finish(self):
        self.phon = unicodedata.normalize('NFC', self.phon)
