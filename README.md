# Tibetan Phonetics Engine

## Description

The goal of this code is to provide a library to:
- implement the conversion of a Tibetan Unicode word into IPA, according to different schemes / dialects
- implement some conversions between IPA and phonetics readable by people with various language backgrounds (Chinese, English, etc.)

The primary focus of this library is litterary pronounciation, ideally representing how an umze would pronounce a traditional text, but contributions for other uses are welcome. We also do not handle Sanskrit transliteration (this can be done through custom exceptions lists).

Note that this library integrates no segmenter and needs to be applied on each word separately. You can use it in combination with [pybo](https://github.com/Esukhia/pybo/) to get the phonetics of full sentences.

## Phonetics methods

We currently provide two phonetics schemes:

#### Manual of Standard Tibetan (by Tournadre)

#### Colloquial Amdo Tibetan (by Kuo-ming Sung and Lha Byams Rgyal)

## Outputs

Apart from raw IPA, we provide the following output possibilities:

#### Chinese phonetics

The Chinese is produced by a streamlined phonetic scheme in order to match the Mandarin phonology (vowels have been simplified and most of the Tibetan suffixes removed).

To produce the final output, we first transform the generated IPA into [Zhuyin](https://en.wikipedia.org/wiki/Bopomofo), and then the Zhuyin into Traditional Chinese characters, with a manually built correspondance list.

## Installation

```
pip install bophono
```

## API

To get the IPA for a word according to the `MST` scheme:

```python
import bophono

# see PhonStateMST.py for other options
options = {
  'aspirateLowTones': True
}

mstconverter = bophono.UnicodeToApi(schema="MST", options = options)
mstipa = mstconverter.get_api("སྐུ")
print(mstipa) # kú
```

Note that you must first segment your text in words and then convert each word.

## Changes

See [CHANGELOG.md](CHANGELOG.md).

## License

The Python code is Copyright (C) 2018-2023 Esukhia, provided under [MIT License](LICENSE). See [CONTRIBUTORS.md](CONTRIBUTORS.md) for a list of authors and contributors.
