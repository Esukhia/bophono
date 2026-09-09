"""
BDRC lenient phonetic notation, ported from
lucene-bo PhoneticSystemStandardTibetan.

Tournadre MST phonology with:
- no tone (+/- stripped)
- no aspiration (h removed)
- no initial nasalization (~)
- no contour tone (~)
- no ས/ད stop (')
- no vowel length (:)
- ä folded to e
- sh written S
"""
from .sdtrie import Trie

ONSETS = [
    ('ཀ', 'k+', True),
    ('ཀྱ', 'ky+', True),
    ('ཀྲ', 'tr+', True),
    ('ཀླ', 'l+', True),
    ('དཀ', 'k+', True),
    ('དཀྱ', 'ky+', True),
    ('དཀྲ', 'tr+', True),
    ('བཀ', 'k+', True),
    ('བཀྱ', 'ky+', True),
    ('བཀྲ', 'tr+', True),
    ('བཀླ', 'l+', True),
    ('རྐ', 'k+', True),
    ('རྐྱ', 'ky+', True),
    ('ལྐ', 'k+', True),
    ('སྐ', 'k+', True),
    ('སྐྱ', 'ky+', True),
    ('སྐྲ', 'tr+', True),
    ('བརྐ', 'k+', True),
    ('བརྐྱ', 'ky+', True),
    ('བསྐ', 'k+', True),
    ('བསྐྱ', 'ky+', True),
    ('བསྐྲ', 'tr+', True),
    ('ཁ', 'kh+', True),
    ('ཁྱ', 'khy+', True),
    ('ཁྲ', 'thr+', True),
    ('མཁ', '~kh+', True),
    ('མཁྱ', '~khy+', True),
    ('མཁྲ', '~thr+', True),
    ('འཁ', '~kh+', True),
    ('འཁྱ', '~khy+', True),
    ('འཁྲ', '~thr+', True),
    ('ག', 'kh-', True),
    ('གྱ', 'khy-', True),
    ('གྲ', 'thr-', True),
    ('གླ', 'l+', True),
    ('དག', 'k-', False),
    ('དགྱ', 'ky-', True),
    ('དགྲ', 'tr-', True),
    ('བག', 'k-', False),
    ('བགྱ', 'ky-', True),
    ('བགྲ', 'tr-', True),
    ('མག', '~k-', False),
    ('མགྱ', '~ky-', True),
    ('མགྲ', '~tr-', True),
    ('འག', '~k-', False),
    ('འགྱ', '~ky-', True),
    ('འགྲ', '~tr-', True),
    ('རྒ', 'k-', True),
    ('རྒྱ', 'ky-', True),
    ('ལྒ', 'k-', True),
    ('སྒ', 'k-', True),
    ('སྒྱ', 'ky-', True),
    ('སྒྲ', 'tr-', True),
    ('བརྒ', 'k-', True),
    ('བརྒྱ', 'ky-', True),
    ('བསྒ', 'k-', True),
    ('བསྒྱ', 'ky-', True),
    ('བསྒྲ', 'tr-', True),
    ('ང', 'ng-', True),
    ('དང', 'ng+', False),
    ('མང', '~ng+', False),
    ('རྔ', 'ng+', True),
    ('ལྔ', 'ng+', True),
    ('སྔ', 'ng+', True),
    ('བརྔ', 'ng+', True),
    ('བསྔ', 'ng+', True),
    ('ཅ', 'c+', True),
    ('གཅ', 'c+', True),
    ('བཅ', 'c+', True),
    ('ལྕ', 'c+', True),
    ('ཆ', 'ch+', True),
    ('མཆ', '~ch+', True),
    ('འཆ', '~ch+', True),
    ('ཇ', 'ch-', True),
    ('མཇ', '~c-', True),
    ('འཇ', '~c-', True),
    ('རྗ', 'c-', True),
    ('ལྗ', '~c-', True),
    ('བརྗ', 'c-', True),
    ('ཉ', 'ny-', True),
    ('གཉ', 'ny+', True),
    ('མཉ', '~ny+', True),
    ('རྙ', 'ny+', True),
    ('སྙ', 'ny+', True),
    ('བརྙ', 'ny+', True),
    ('བསྙ', 'ny+', True),
    ('ཏ', 't+', True),
    ('གཏ', 't+', True),
    ('བཏ', 't+', True),
    ('རྟ', 't+', True),
    ('ལྟ', '~t+', True),
    ('སྟ', 't+', True),
    ('བརྟ', 't+', True),
    ('བལྟ', 't+', True),
    ('བསྟ', 't+', True),
    ('ཐ', 'th+', True),
    ('མཐ', '~th+', True),
    ('འཐ', '~th+', True),
    ('ད', 'th-', True),
    ('དྲ', 'thr-', True),
    ('གད', 't-', False),
    ('བད', 't-', False),
    ('མད', '~t-', False),
    ('འད', '~t-', False),
    ('འདྲ', '~tr-', True),
    ('རྡ', 't-', True),
    ('ལྡ', '~t-', True),
    ('སྡ', 't-', True),
    ('བརྡ', 't-', True),
    ('བལྡ', 't-', True),
    ('བསྡ', 't-', True),
    ('ན', 'n-', True),
    ('གན', 'n+', False),
    ('མན', '~n+', False),
    ('རྣ', 'n+', True),
    ('སྣ', 'n+', True),
    ('བརྣ', 'n+', True),
    ('བསྣ', 'n+', True),
    ('པ', 'p+', True),
    ('པྱ', 'c+', True),
    ('པྲ', 'tr+', True),
    ('དཔ', 'p+', True),
    ('དཔྱ', 'c+', True),
    ('དཔྲ', 'tr+', True),
    ('ལྤ', 'p+', True),
    ('སྤ', 'p+', True),
    ('སྤྱ', 'c+', True),
    ('སྤྲ', 'tr+', True),
    ('ཕ', 'ph+', True),
    ('ཕྱ', 'ch+', True),
    ('ཕྲ', 'thr+', True),
    ('འཕ', '~ph+', True),
    ('འཕྱ', '~ch+', True),
    ('འཕྲ', '~thr+', True),
    ('བ', 'ph-', True),
    ('བྱ', 'ch-', True),
    ('བྲ', 'thr-', True),
    ('བླ', 'l+', True),
    ('དབ', '+', False),
    ('དབྱ', 'y+', True),
    ('དབྲ', 'r+', True),
    ('འབ', '~p-', False),
    ('འབྱ', '~c-', True),
    ('འབྲ', '~tr-', True),
    ('རྦ', 'p-', True),
    ('ལྦ', 'p-', True),
    ('སྦ', 'p-', True),
    ('སྦྱ', 'c-', True),
    ('སྦྲ', 'tr-', True),
    ('མ', 'm-', True),
    ('མྱ', 'ny-', True),
    ('དམ', 'm+', False),
    ('དམྱ', 'ny+', True),
    ('རྨ', 'm+', True),
    ('རྨྱ', 'ny+', True),
    ('སྨ', 'm+', True),
    ('སྨྱ', 'ny+', True),
    ('ཙ', 'ts+', True),
    ('གཙ', 'ts+', True),
    ('བཙ', 'ts+', True),
    ('རྩ', 'ts+', True),
    ('སྩ', 'ts+', True),
    ('བརྩ', 'ts+', True),
    ('བསྩ', 'ts+', True),
    ('ཚ', 'tsh+', True),
    ('མཚ', '~tsh+', True),
    ('འཚ', '~tsh+', True),
    ('ཛ', 'tsh-', True),
    ('མཛ', '~ts-', True),
    ('འཛ', '~ts-', True),
    ('རྫ', 'ts-', True),
    ('བརྫ', 'ts-', True),
    ('ཝ', 'w-', True),
    ('ཞ', 'S-', True),
    ('གཞ', 'S-', True),
    ('བཞ', 'S-', True),
    ('ཟ', 's-', True),
    ('ཟླ', '~t-', True),
    ('གཟ', 's-', True),
    ('བཟ', 's-', True),
    ('བཟླ', 't-', True),
    ('འ', '-', True),
    ('ཡ', 'y-', True),
    ('གཡ', 'y+', True),
    ('ར', 'r-', True),
    ('རླ', 'l+', True),
    ('བརླ', 'l+', True),
    ('ལ', 'l-', True),
    ('ཤ', 'S+', True),
    ('གཤ', 'S+', True),
    ('བཤ', 'S+', True),
    ('ས', 's+', True),
    ('སྲ', 's+', True),
    ('སླ', 'l+', True),
    ('གས', 's+', False),
    ('བས', 's+', False),
    ('བསྲ', 's+', True),
    ('བསླ', 'l+', True),
    ('ཧ', 'h+', True),
    ('ཧྲ', 'rh+', True),
    ('ལྷ', 'lh+', True),
    ('ཨ', '+', True),
    ('བགླ', 'l+', True),
    ('མྲ', 'm+', True),
    ('སྨྲ', 'm+', True),
    ('ཏྲ', 'tr+', True),
    ('བརྟ', 't+', True),
    ('ཐྲ', 'thr+', True),
    ('སྣྲ', 'n+', True),
    ('ཀྭ', 'k+', True),
    ('བཀྭ', 'k+', True),
    ('ཁྭ', 'kh+', True),
    ('གྭ', 'kh-', True),
    ('གྲྭ', 'thr-', True),
    ('བཅྭ', 'c+', True),
    ('ཉྭ', 'ny-', True),
    ('ཏྭ', 't+', True),
    ('ཐྭ', 'th+', True),
    ('དྭ', 'th-', True),
    ('དྲྭ', 'thr-', True),
    ('ཕྱྭ', 'ch+', True),
    ('མྭ', 'm-', True),
    ('ཙྭ', 'ts+', True),
    ('རྩྭ', 'ts+', True),
    ('ཚྭ', 'tsh+', True),
    ('ཛྭ', 'tsh-', True),
    ('ཞྭ', 'S-', True),
    ('ཟྭ', 's-', True),
    ('རྭ', 'r-', True),
    ('ལྭ', 'l-', True),
    ('ལྷྭ', 'lh+', True),
    ('ཤྭ', 'S+', True),
    ('སྟྭ', 't+', True),
    ('སྭ', 's+', True),
    ('བསྭ', 's+', True),
    ('ཧྭ', 'h+', True),
]

CODAS = [
    ('', 'a'),
    ('འ', 'a:'),
    ('ག', 'ak'),
    ('གས', 'ak'),
    ('ང', 'ang'),
    ('ངས', 'ang~'),
    ('ད', "ä'"),
    ('ན', 'än'),
    ('བ', 'ap'),
    ('བས', 'ap'),
    ('མ', 'am'),
    ('མས', 'am~'),
    ('ལ', 'äl'),
    ('འི', 'ä'),
    ('འིའོ', 'aio'),
    ('འོ', 'ao'),
    ('འང', 'aang'),
    ('འམ', 'aam'),
    ('ར', 'ar'),
    ('ས', "ä'"),
    ('ི', 'i'),
    ('ིག', 'ik'),
    ('ིགས', 'ik'),
    ('ིང', 'ing'),
    ('ིངས', 'ing~'),
    ('ིད', "i'"),
    ('ིན', 'in'),
    ('ིབ', 'ip'),
    ('ིབས', 'ip'),
    ('ིམ', 'im'),
    ('ིམས', 'im~'),
    ('ིལ', 'il'),
    ('ིའི', 'i:'),
    ('ིའིའོ', 'i:o'),
    ('ིའོ', 'io'),
    ('ིའང', 'iang'),
    ('ིའམ', 'iam'),
    ('ིར', 'ir'),
    ('ིས', "i'"),
    ('ུ', 'u'),
    ('ུག', 'uk'),
    ('ུགས', 'uk'),
    ('ུང', 'ung'),
    ('ུངས', 'ung~'),
    ('ུད', "ü'"),
    ('ུན', 'ün'),
    ('ུབ', 'up'),
    ('ུབས', 'up'),
    ('ུམ', 'um'),
    ('ུམས', 'um~'),
    ('ུལ', 'ül'),
    ('ུའི', 'ü'),
    ('ུའིའོ', 'uio'),
    ('ུའོ', 'uo'),
    ('ུའང', 'uang'),
    ('ུའམ', 'uam'),
    ('ུར', 'ur'),
    ('ུས', "ü'"),
    ('ེ', 'e'),
    ('ེག', 'ek'),
    ('ེགས', 'ek'),
    ('ེང', 'eng'),
    ('ེངས', 'eng~'),
    ('ེད', "e'"),
    ('ེན', 'en'),
    ('ེབ', 'ep'),
    ('ེབས', 'ep'),
    ('ེམ', 'em'),
    ('ེམས', 'em~'),
    ('ེལ', 'el'),
    ('ེའི', 'e'),
    ('ེའིའོ', 'eio'),
    ('ེའོ', 'eo'),
    ('ེའང', 'eang'),
    ('ེའམ', 'eam'),
    ('ེར', 'er'),
    ('ེས', "e'"),
    ('ོ', 'o'),
    ('ོག', 'ok'),
    ('ོགས', 'ok'),
    ('ོང', 'ong'),
    ('ོངས', 'ong~'),
    ('ོད', "ö'"),
    ('ོན', 'ön'),
    ('ོབ', 'op'),
    ('ོབས', 'op'),
    ('ོམ', 'om'),
    ('ོམས', 'om~'),
    ('ོལ', 'öl'),
    ('ོའི', 'ö'),
    ('ོའིའོ', 'oio'),
    ('ོའོ', 'oo'),
    ('ོའང', 'oang'),
    ('ོའམ', 'oam'),
    ('ོར', 'or'),
    ('ོས', "ö'"),
    ('འུ', 'au'),
    ('འུའི', 'au'),
    ('འུའིའོ', 'auio'),
    ('འུའོ', 'auo'),
    ('འུའང', 'auang'),
    ('འུའམ', 'auam'),
    ('འུར', 'aur'),
    ('འུས', "aü'"),
    ('ིའུ', 'iu'),
    ('ིའུའི', 'iu'),
    ('ིའུའིའོ', 'iuio'),
    ('ིའུའོ', 'iuo'),
    ('ིའུའང', 'iuang'),
    ('ིའུའམ', 'iuam'),
    ('ིའུར', 'iur'),
    ('ིའུས', "iü'"),
    ('ུའུ', 'u'),
    ('ུའུའི', 'ui'),
    ('ུའུའིའོ', 'uio'),
    ('ུའུའོ', 'uo'),
    ('ུའུའང', 'uang'),
    ('ུའུའམ', 'uam'),
    ('ུའུར', 'uur'),
    ('ུའུས', "uü'"),
    ('ེའུ', 'eu'),
    ('ེའུའི', 'eui'),
    ('ེའུའིའོ', 'euio'),
    ('ེའུའོ', 'euo'),
    ('ེའུའང', 'euang'),
    ('ེའུའམ', 'euam'),
    ('ེའུར', 'eur'),
    ('ེའུས', "eü'"),
    ('ོའུ', 'ou'),
    ('ོའུའི', 'oui'),
    ('ོའུའིའོ', 'ouio'),
    ('ོའུའོ', 'ouo'),
    ('ོའུའང', 'ouang'),
    ('ོའུའམ', 'ouam'),
    ('ོའུར', 'our'),
    ('ོའུས', "oü'"),
]

SKT = {
    'ཀ': 'g',
    'ཁ': 'g',
    'ག': 'g',
    'ང': 'N',
    'ཅ': 'c',
    'ཆ': 'c',
    'ཇ': 'c',
    'ཉ': 'Y',
    'ཐ': 'd',
    'ཏ': 'd',
    'ད': 'd',
    'ན': 'n',
    'པ': 'b',
    'ཕ': 'b',
    'བ': 'b',
    'མ': 'm',
    'ཙ': 'c',
    'ཚ': 'c',
    'ཛ': 'c',
    'ཝ': 'b',
    'ཞ': 'S',
    'ཟ': 's',
    'འ': '',
    'ཡ': 'y',
    'ར': 'r',
    'ལ': 'l',
    'ཤ': 'S',
    'ཥ': 'S',
    'ས': 's',
    'ཧ': '',
    'ཨ': '',
    'ཪ': 'r',
    'ཱ': '',
    'ི': 'i',
    'ུ': 'u',
    'ེ': 'e',
    'ཻ': 'e',
    'ོ': 'o',
    'ཽ': 'o',
    'ཾ': 'n',
    'ཿ': '',
    'ྀ': 'i',
    'ྂ': 'n',
    'ྃ': 'n',
    '྄': '',
    'ྐ': 'g',
    'ྑ': 'g',
    'ྒ': 'g',
    'ྔ': 'N',
    'ྕ': 'c',
    'ྖ': 'c',
    'ྗ': 'c',
    'ྙ': 'Y',
    'ྟ': 'd',
    'ྠ': 'd',
    'ྡ': 'd',
    'ྣ': 'n',
    'ྤ': 'b',
    'ྥ': 'b',
    'ྦ': 'b',
    'ྨ': 'm',
    'ྩ': 'c',
    'ྪ': 'c',
    'ྫ': 'c',
    'ྭ': '',
    'ྮ': 'S',
    'ྯ': 's',
    'ྰ': '',
    'ྱ': 'y',
    'ྲ': 'r',
    'ླ': 'l',
    'ྴ': 'S',
    'ྵ': 'S',
    'ྶ': 's',
    'ྷ': '',
    'ྸ': '',
    'ྺ': 'b',
    'ྻ': 'y',
    'ྼ': 'r',
}


_HIGH_VOWELS = set("ieouM")
_VOWEL_LETTERS = set("aieou")
_DBA_VOWELS = set("\u0f72\u0f74\u0f7a\u0f7c")


def _is_tib_letter_or_digit(c):
    return ("\u0F40" <= c <= "\u0FBC") or ("\u0F20" <= c <= "\u0F33") or c == "\u0F00"


class PhoneticSystemBDRCLenient:
    def __init__(self, options=None):
        options = options or {}
        self.ignoreInitialNasalization = options.get("ignoreInitialNasalization", True)
        self.ignoreTone = options.get("ignoreTone", True)
        self.ignoreAspiration = options.get("ignoreAspiration", True)
        self.ignoreContourTone = options.get("ignoreContourTone", True)
        self.ignoreSDSuffix = options.get("ignoreSDSuffix", True)
        self.ignoreLengthener = options.get("ignoreLengthener", True)
        self.foldAE = options.get("foldAE", True)
        self.syllablesepchar = options.get("syllablesepchar", "")
        self.implicitA = options.get("implicitA", "")
        self.onsetTrie = Trie()
        self.vowelCoda = {}
        for onset, phonetic, canbefinal in ONSETS:
            self._add_onset(onset, phonetic, canbefinal)
        for coda, phonetic in CODAS:
            self._add_vowel_coda(coda, phonetic)
        self.sktPhonetic = dict(SKT)

    def _add_onset(self, onset, phonetic, canbefinal=True):
        if self.ignoreInitialNasalization and phonetic.startswith("~"):
            phonetic = phonetic[1:]
        if self.ignoreTone and phonetic:
            phonetic = phonetic[:-1]
        if self.ignoreAspiration and "h" in phonetic:
            phonetic = phonetic.replace("h", "")
        self.onsetTrie.add(onset, phonetic, canbefinal)

    def _add_vowel_coda(self, vowelCoda, phonetic):
        if self.ignoreContourTone and phonetic.endswith("~"):
            phonetic = phonetic[:-1]
        if self.ignoreSDSuffix and phonetic.endswith("'"):
            phonetic = phonetic[:-1]
        if self.ignoreLengthener and ":" in phonetic:
            phonetic = phonetic.replace(":", "")
        if self.foldAE and "ä" in phonetic:
            phonetic = phonetic.replace("ä", "e")
        self.vowelCoda[vowelCoda] = phonetic

    def get_phonetics(self, s):
        if not s:
            return None
        onset = self._find_onset(s)
        if not onset:
            return None
        nbchar, phonetic = onset
        second = s[nbchar:]
        vowel_coda = self.vowelCoda.get(second)
        if vowel_coda is None:
            return None
        if (nbchar == 2 and s[0] == "ད" and s[1] == "བ" and len(s) > 2
                and s[2] not in _DBA_VOWELS):
            phonetic = "w"
        if len(phonetic) == 1 and vowel_coda and vowel_coda[0] == "i":
            if phonetic[0] == "G":
                phonetic = "g"
            elif phonetic[0] == "Y":
                phonetic = "n"
        return phonetic + vowel_coda

    def _find_onset(self, s):
        # data may be "" (དབ / ཨ / འ after tone stripping); do not treat that as missing
        node = self.onsetTrie.head
        best = None
        for i, ch in enumerate(s):
            if ch not in node.children:
                break
            node = node.children[ch]
            if node.data is not None and (node.canbefinal or i < len(s) - 1):
                best = (i + 1, node.data)
        return best

    def get_skt_phonetics(self, s):
        if not s:
            return None
        phonetic = []
        for c in s:
            if c in self.sktPhonetic:
                phonetic.append(self.sktPhonetic[c])
            else:
                phonetic.append(c)
        res = "".join(phonetic)
        if not res or res[-1] not in _HIGH_VOWELS:
            res += self.implicitA
        elif len(res) > 1 and res[-1] == "M" and res[-2] not in _VOWEL_LETTERS:
            res = res[:-1] + "am"
        elif res[-1] == "M":
            res = res[:-1] + "m"
        return res

    def convert_syllable(self, s):
        phon = self.get_phonetics(s)
        if phon is not None:
            return phon
        return self.get_skt_phonetics(s)

    def convert(self, tibstr, bindex=0, eindex=-1):
        if eindex == -1:
            eindex = len(tibstr)
        i = self._next_letter(tibstr, bindex, eindex)
        parts = []
        while 0 <= i < eindex:
            last = self._next_non_letter(tibstr, i, eindex)
            if last == -1:
                last = eindex
            phon = self.convert_syllable(tibstr[i:last])
            if phon:
                parts.append(phon)
            i = self._next_letter(tibstr, last, eindex)
        return self.syllablesepchar.join(parts)

    def _next_letter(self, tibstr, current, eindex):
        for i in range(current, eindex):
            if _is_tib_letter_or_digit(tibstr[i]):
                return i
        return -1

    def _next_non_letter(self, tibstr, current, eindex):
        for i in range(current, eindex):
            if not _is_tib_letter_or_digit(tibstr[i]):
                return i
        return -1


