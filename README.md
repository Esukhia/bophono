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

- ཀཿ་ཐོག
- study behavior for ambiguous syllables

## License

The Python code is Copyright (C) 2018 Elie Roux, provided under [MIT License](LICENSE).
