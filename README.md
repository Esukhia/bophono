# Tibetan Phonetics Engine

## Description

The goal of this code is to provide a library to:

- implement the conversion of a Tibetan Unicode word into IPA, according to different schemes / dialects
- implement some conversions between IPA and phonetics readable by people with various language backgrounds (Chinese, English, etc.)

The primary focus of this library is litterary pronounciation, ideally representing how an umze would pronounce a traditional text, but contributions for other uses are welcome. Sanskrit in Tibetan script can be transliterated with the `IAST` scheme; pronunciation of Sanskrit is not handled (that can still be done through custom exceptions lists).

Note that this library integrates no segmenter and needs to be applied on each word separately. You can use it in combination with [pybo](https://github.com/Esukhia/pybo/) to get the phonetics of full sentences.

## Phonetics methods

We currently provide the following phonetics schemes:

#### Manual of Standard Tibetan (by Tournadre)

- `MST` / `MST_phonetics`: IPA phonetics (`MST_phonetics` is an alias of `MST`)
- `MST_phonology`: the intermediate phonological representation, with tone marked on the vowel as in Tournadre (macron `ā` for high tone, understrike `a̱` for low tone) instead of `k+a` / `k-a`

#### Colloquial Amdo Tibetan (by Kuo-ming Sung and Lha Byams Rgyal)

#### IAST (Sanskrit in Tibetan script)

`IAST` converts Indic text written in Tibetan Unicode to [IAST](https://en.wikipedia.org/wiki/International_Alphabet_of_Sanskrit_Transliteration). This is not a pronunciation scheme: it transliterates Sanskrit (and other Indic) stacks, ignoring characters it cannot convert.

```python
import bophono
iast = bophono.UnicodeToApi(schema="IAST")
print(iast.get_api("ཀརྨ"))  # karma
print(iast.get_api("པདྨ"))  # padma
```

## Outputs

Apart from raw IPA, we provide the following output possibilities:

#### Chinese phonetics

The Chinese is produced by a streamlined phonetic scheme in order to match the Mandarin phonology (vowels have been simplified and most of the Tibetan suffixes removed).

To produce the final output, we first transform the generated IPA into [Zhuyin](https://en.wikipedia.org/wiki/Bopomofo), and then the Zhuyin into Traditional Chinese characters, with a manually built correspondance list.

#### Tibetan pinyin

`tibetan_to_pinyin()` converts Tibetan Unicode to [Tibetan pinyin](https://en.wikipedia.org/wiki/Tibetan_pinyin) (ZWPY) via the MST IPA. Use `style="diacritic"` (default: ê, ô, ä, ö, ü) or `style="ascii"`.

```python
from bophono import tibetan_to_pinyin
print(tibetan_to_pinyin("བཀྲ་ཤིས"))  # zha xi
```

## Installation

```
pip install bophono
```

## API

To get the IPA for a word according to the `MST` / `MST_phonetics` scheme:

```python
import bophono

# see PhonStateMST.py for other options
options = {
  'aspirateLowTones': True
}

mstconverter = bophono.UnicodeToApi(schema="MST_phonetics", options = options)
mstipa = mstconverter.get_api("སྐུ")
print(mstipa) # ku˥
```

`schema="MST"` remains valid and is equivalent to `MST_phonetics`.

To get the phonological transcription (`MST_phonology`):

```python
phonology = bophono.UnicodeToApi(schema="MST_phonology")
print(phonology.get_api("སྐུ"))       # kū
print(phonology.get_api("བཀྲ་ཤིས"))  # trā|shī'
```

Note that you must first segment your text in words and then convert each word.

## Options

### unknownSyllableMarker

When set to `True`, unrecognized syllables (e.g., Sanskrit) will be replaced with a `(?)` marker instead of stopping the conversion. This is useful for processing texts that contain Sanskrit mantras or other non-standard Tibetan syllables.

```python
import bophono

converter = bophono.UnicodeToApi(schema="KVP", options={'unknownSyllableMarker': True})
result = converter.get_api("ཧཱུྃ་")
print(result)  # (?)
```

By default, this option is `False` to preserve backward compatibility.

## How to cite

If you use this library in academic work, please cite:

> Elie Roux. *bophono: Tibetan Phonetics Engine*. https://github.com/Esukhia/bophono

```bibtex
@software{roux_bophono,
  author = {Roux, Elie},
  title = {bophono: Tibetan Phonetics Engine},
  url = {https://github.com/Esukhia/bophono},
  year = {2018}
}
```

## Changes

See [CHANGELOG.md](CHANGELOG.md).

## License

The Python code is Copyright (C) 2018-2023 Esukhia, provided under [MIT License](LICENSE). See [CONTRIBUTORS.md](CONTRIBUTORS.md) for a list of authors and contributors.
