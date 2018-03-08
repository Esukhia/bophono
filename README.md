# Tibetan Phonetics Engine

The goal of this repository is to:
- provide an engine to interpret Tibetan in various phonetic transcription schemes
- implement the rules in [Tournadre](http://www.worldcat.org/oclc/916715611) (intro and Ann. 2) as a starting point

## Description

Ideally the engine will solely use configuration files, so that it can be phonetic scheme agnostic (no phonetics hardcoded).

The various steps (for the Tournadre scheme, which is the most complex) will be:
- Tibetan unicode -> Tournadre basic scheme (introduction)
- Tournadre basis scheme -> IPA (Annex 2)
- IPA -> phonetic scheme

## Installation

## Running

## TODO

- study behavior for ambiguous syllables (probably list some as exceptions)
- document annotations
- da/sa glottal stop only at end of sentence
- p. 443: closed syllable = when final has sound (including glottal stop)
- document kh¨antr¨as
- khon pa as gompa
- footnote 200 p. 441
- dmag mi p. 65 noted with '
- dbu 'khyud
- document non-nasalized words
- implement p. 36

## License

The Python code is Copyright (C) 2018 Elie Roux, provided under [MIT License](LICENSE).
