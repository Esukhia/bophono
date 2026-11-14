"""Corpus-backed Sanskrit readings and fallback for LKT."""
from __future__ import annotations

import re
import unicodedata
from functools import lru_cache

from .tibskritconv import CHAR_TOKENS, Cats, normalize_unicode, tibskrit_to_iast

# Restore established Sanskrit spellings for these attested Tibetan variants.
SANSKRIT_READINGS = {
    'ༀ': 'om',
    'ཨ་བྷི་ཥིཉྩ': 'abhisinca',
    'ཨཱཿ': 'ah',
    'ཨཿ': 'ah',
    'ཨཱོྃ': 'om',
    'ཨོྂ': 'om',
    'ཨོྃ': 'om',
    'ཀརྐོ་ཊ': 'karkota',
    'ཀརྐོཊ': 'karkota',
    'ཅིཏ་ཏ': 'citta',
    'ཙིཏ་ཏ': 'citta',
    'ཛཉ་ན': 'jnana',
    'ཏདྱ་ཐཱ': 'tadyatha',
    'ཏདྱཐཱ': 'tadyatha',
    'བ་ཛྲ': 'vajra',
    'བཛྲ': 'vajra',
    'བཛྲཱ': 'vajra',
    'བཛྲཱ་ཡ': 'vajraya',
    'བཛྲེ': 'vajre',
    'བིདྱ': 'vidya',
    'བིདྱཱ': 'vidya',
    'བཻ་ཌཱུ་རྱ': 'vaidurya',
    'བཻ་ཌཱུརྱ': 'vaidurya',
    'བཻ་དཱུ་རྱ': 'vaidurya',
    'བཻ་དཱུརྱ': 'vaidurya',
    'བཻ་དཱུརྱ': 'vaidurya',
    'བཻཌཱུརྱ': 'vaidurya',
    'མཎྜལ': 'mandala',
    'ཙཀ': 'cak',
    'ཛྙཱ་ན': 'jnana',
    'རཀ': 'rak',
    'རཏ་ན': 'ratna',
    'ཕཏ': 'phat',
    'ཕཊ': 'phat',
    'ཕཊ྄': 'phat',
    'ཕཊཿ': 'phat',
    'ཕཊ྄ཿ': 'phat',
    'སཏྱ': 'satya',
    'སཏྭ': 'sattva',
    'སཏྭཾ': 'sattvam',
    'སརྦ': 'sarva',
    'སརྦཱ': 'sarva',
    'སརྦྦ': 'sarva',
    'སྭཱ་ཧཱ': 'svaha',
    'སྭཱཧཱ': 'svaha',
    'ཧཱུཾ': 'hum',
    'ཧཱུྂ': 'hum',
    'ཧཱུྃ': 'hum',
}
# These spellings are already explicit in upstream LKT's exception table.
LKT_EXCEPTIONS = {
    'ཌཱཀྐི': 'daki',
    'ཎཱི': 'ni',
    'པཱུ་ཛཱ': 'puja',
}
READINGS = {**LKT_EXCEPTIONS, **SANSKRIT_READINGS}
MAX_READING_SYLLABLES = max(source.count('་') + 1 for source in READINGS)
SYLLABLE_BOUNDARY = re.compile(r'[་༌\s]+|(?<=ཿ)(?=[ཀ-ཬ])')
# Stacks and vowels that distinguish Sanskrit from ordinary Tibetan spelling.
SANSKRIT_MARKS = frozenset('ཊཋཌཎཥཱཻཽཾཿ྄ྀྂྃ྅ྙྚྛྜྞྟྠྡྣྤྥྦྨྩྪྫྭྴྵྷྺྻྼ')
SANSKRIT_STACKS = re.compile(r'ཀྐ|ངྒ|གྒ|ཉྗ|[དནརསཧ]ྱ|ཤྲ|ལླ|ཀླ|ཀྲ')
SANSKRIT_SYMBOLS = re.compile(r"[a-z]+(?:'[a-z]*)?\Z")
INVALID_SANSKRIT_MARKS = re.compile(r'[ཾཿྂྃ]{2}|(?<![རལྲླ])ྀ')
GENITIVE = {'a': 'e', 'e': 'e', 'i': 'i', 'o': 'ö', 'u': 'y'}


@lru_cache(maxsize=10000)
def sanskrit_syllable(source: str) -> str | None:
    normalized = normalize_unicode(unicodedata.normalize('NFD', source))
    if not (SANSKRIT_MARKS.intersection(normalized) or SANSKRIT_STACKS.search(normalized)):
        return None
    if not normalized or any(char not in CHAR_TOKENS for char in normalized):
        return None
    vowel_marks = normalized.replace('ཱྀ', 'ྀ')
    if CHAR_TOKENS[normalized[0]][1] != Cats.Base or INVALID_SANSKRIT_MARKS.search(vowel_marks):
        return None
    plain = ''.join(c for c in unicodedata.normalize('NFD', tibskrit_to_iast(normalized)) if not unicodedata.combining(c))
    plain = plain.replace('’', "'")
    return plain if SANSKRIT_SYMBOLS.fullmatch(plain) else None


def _sanskrit_reading(source: str) -> str | None:
    if source.endswith('འི'):
        stem = source[:-2]
        reading = SANSKRIT_READINGS.get(stem) or sanskrit_syllable(stem)
        if reading and reading[-1] in GENITIVE:
            return reading[:-1] + GENITIVE[reading[-1]]
    return sanskrit_syllable(source)


def _convert(text, render, mark_unknown):
    source = text.rstrip('་༌ ')
    explicit = READINGS.get(source)
    if explicit is not None:
        return explicit
    if source.endswith('འི') and source[:-2] in SANSKRIT_READINGS:
        reading = _sanskrit_reading(source)
        if reading is not None:
            return reading

    result = render(text, True)
    missing = not result or '(?)' in result
    parts = SYLLABLE_BOUNDARY.split(source)
    if len(parts) == 1:
        if missing:
            return _sanskrit_reading(source) or (result if mark_unknown else render(text, False))
        return result
    phonetics, tibetan = [], []
    index = 0
    while index < len(parts):
        part = parts[index]
        stop = min(len(parts), index + MAX_READING_SYLLABLES)
        for end in range(stop, index, -1):
            reading = READINGS.get('་'.join(parts[index:end]))
            if reading is not None:
                break
        else:
            end = index + 1
            if missing and '(?)' in render(part, True):
                reading = _sanskrit_reading(part)
        index = end
        if reading is None:
            tibetan.append(part)
            continue
        if tibetan:
            chunk = '་'.join(tibetan)
            converted = render(chunk, True)
            if not mark_unknown and '(?)' in converted:
                phonetics.append(render(chunk, False))
                return ' '.join(part for part in phonetics if part)
            phonetics.append(converted)
            tibetan.clear()
        phonetics.append(reading)
    if not phonetics:
        return render(text, False) if missing and not mark_unknown else result
    if tibetan:
        phonetics.append(render('་'.join(tibetan), mark_unknown))
    return ' '.join(part for part in phonetics if part)


def convert_lkt(text, render, mark_unknown=False):
    return _convert(text, render, mark_unknown).replace('é', 'e')
