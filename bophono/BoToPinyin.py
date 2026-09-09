import re
from .UnicodeToApi import UnicodeToApi


_TONE_CHARS = set("˥˩˨˧")

# Vowel detection in MST IPA output
_VOWELS = set(list("aeiouy") + ['ɛ', 'ɔ', 'ø', 'ə'])


def _strip_tones(s):
    return "".join(ch for ch in s if ch not in _TONE_CHARS)


def _split_syllables(api):
    if not api:
        return []
    return api.split(".")


def _map_onset_ipa_to_zwpy(onset_ipa):
    """
    Map MST IPA onset to Tibetan pinyin per Wikipedia (approximate).
    Reference: Tibetan pinyin — Wikipedia (ZWPY)
    """
    s = onset_ipa

    # Order matters: match longer/more specific sequences first
    mapping = [
        # alveolo-palatals
        (r"^tɕʰ", "q"),
        (r"^dʑ", "q"),
        (r"^tɕ", "j"),
        (r"^ɕ", "x"),
        # retroflex series
        (r"^ʈʰ", "ch"),
        (r"^ɖ", "ch"),
        (r"^ʈ", "zh"),
        (r"^ʂ", "sh"),
        # alveolar affricates
        (r"^tsʰ", "c"),
        (r"^dz", "c"),
        (r"^ts", "z"),
        # velars
        (r"^kʰ", "k"),
        (r"^g̊", "k"),
        (r"^g", "k"),
        (r"^k", "g"),
        # dentals
        (r"^tʰ", "t"),
        (r"^d", "t"),
        (r"^t", "d"),
        # bilabials
        (r"^pʰ", "p"),
        (r"^b", "p"),
        (r"^p", "b"),
        # liquids and approximants
        (r"^l̥ʰ", "lh"),
        (r"^l̥", "lh"),
        (r"^l", "l"),
        (r"^ʐ", "r"),
        (r"^r", "r"),
        (r"^j", "y"),
        (r"^w", "w"),
        # nasals
        (r"^ɲ", "ny"),
        (r"^ŋ", "ng"),
        (r"^n", "n"),
        (r"^m", "m"),
        # sibilants and glottals
        (r"^s", "s"),
        (r"^z", "z"),
        (r"^h", "h"),
    ]

    for pat, out in mapping:
        if re.match(pat, s):
            return out
    # fallback: empty or unknown onset
    return ""


def _map_vowel_and_coda(nucleus_with_marks, coda, style="diacritic"):
    """
    Map a vowel nucleus (possibly with nasalization) and coda to Tibetan pinyin.
    style: 'diacritic' (default) uses ê, ô, ä, ö, ü; 'ascii' uses e, o, ai, oi, u
    """
    # Extract vowel base and nasalization
    nasal = "̃" in nucleus_with_marks
    # Remove length mark
    core = nucleus_with_marks.replace("ː", "")
    # Strip nasalization combining mark for base matching
    core = core.replace("̃", "")

    # Base vowel mapping
    if style == "ascii":
        base_map = {
            "i": "i",
            "e": "e",
            "ɛ": "ai",
            "a": "a",
            "u": "u",
            "o": "o",   # will handle close-mid vs open-mid roughly
            "ɔ": "o",
            "y": "u",   # no ASCII ü; approximate
            "ø": "oi",
            "ə": "a",
        }
    else:
        base_map = {
            "i": "i",
            "e": "ê",
            "ɛ": "ä",
            "a": "a",
            "u": "u",
            "o": "ô",
            "ɔ": "o",
            "y": "ü",
            "ø": "ö",
            "ə": "a",
        }

    base = base_map.get(core, core)

    # Nasalization mapping (Wikipedia shows nasal vowels written with n, not diacritics)
    if nasal:
        # Special handling for front rounded vowels and e/ɛ
        if core == "y":
            base = "ün" if style != "ascii" else "un"
        elif core == "ø":
            base = "ön" if style != "ascii" else "oin"
        elif core in ("e",):
            base = "en"
        elif core in ("ɛ",):
            base = "än" if style != "ascii" else "ain"
        elif core in ("o", "ɔ"):
            base = "on"
        elif core == "i":
            base = "in"
        elif core == "a" or core == "ə":
            base = "an"
        elif core == "u":
            base = "un"

    # Coda mapping for explicit consonants (rare when nasalization already encoded)
    # Map unreleased stops and glottal stop to b/g per Wikipedia note (approximate).
    c = coda or ""
    if "ŋ" in c:
        return base + "ng"
    if "m" in c:
        return base + "m"
    if "n" in c:
        return base + "n"
    if "l" in c:
        return base + "l"
    if "r" in c:
        return base + "r"
    if "p̚" in c or c.endswith("p"):
        return base + "b"
    if "k̚" in c or c.endswith("k"):
        return base + "g"
    if "ʔ" in c:
        return base + "g"

    return base


def _syllable_to_zwpy(ipa_syllable, style="diacritic"):
    # Remove tone marks
    s = _strip_tones(ipa_syllable)
    if not s:
        return ""

    # Find vowel start index
    vowel_idx = -1
    for i, ch in enumerate(s):
        if ch in _VOWELS:
            vowel_idx = i
            break
    if vowel_idx == -1:
        # No vowel detected; treat entire syllable as onset (edge case)
        return _map_onset_ipa_to_zwpy(s)

    onset_ipa = s[:vowel_idx]
    rest = s[vowel_idx:]

    # Nucleus: first vowel + possible combining nasal/length marks
    nucleus = rest[0]
    j = 1
    while j < len(rest) and rest[j] in ["ː", "̃", "ɪ", "̯"]:
        nucleus += rest[j]
        j += 1
    coda = rest[j:] if j < len(rest) else ""

    onset = _map_onset_ipa_to_zwpy(onset_ipa)
    rime = _map_vowel_and_coda(nucleus, coda, style=style)
    return onset + rime


def tibetan_to_pinyin(tibetan_text, schema="MST", options=None, style="diacritic"):
    """
    Convert Tibetan Unicode text into Tibetan pinyin (ZWPY) by composing Unicode->IPA (MST)
    and IPA->ZWPY mapping rules approximated from Wikipedia.

    style:
      - 'diacritic' (default): ê, ô, ä, ö, ü
      - 'ascii': e, o, ai, oi, u
    """
    if options is None:
        options = {}
    api = UnicodeToApi(schema=schema, options=options).get_api(tibetan_text)
    syllables = _split_syllables(api)
    out = []
    for idx, syl in enumerate(syllables):
        if not syl:
            continue
        out.append(_syllable_to_zwpy(syl, style=style))
    return " ".join(filter(None, out))

if __name__ == "__main__":
    pinyin = tibetan_to_pinyin("རྟོག་དཔྱོད་ཀྱིས་གོ་ཡང་མྱོང་ཐོག་ཏུ་མ་ཆགས།།")
    print(pinyin)
