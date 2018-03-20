# Tibetan Phonetics Engine

The goal of this repository is to:
- provide an engine to interpret Tibetan in various phonetic transcription schemes
- implement the rules in [Tournadre](http://www.worldcat.org/oclc/916715611) (intro and Ann. 2) as a starting point

## Description

Ideally the engine will solely use configuration files, so that it can be phonetic scheme agnostic (no phonetics hardcoded).

The various steps (for the Tournadre scheme, which is the most complex) will be:
- Tibetan unicode -> Phonolical scheme (given in Tournadre)
- Phonological scheme -> IPA (according to Annex 2 of Tournadre)
- IPA -> phonetic scheme

We focus exclusively on litterary pronounciation, and have options for reading pronounciation or oral pronounciation. Our focus is to be able express how an umze would pronounce a traditional text.

## Installation

## Running

## TODO

- study behavior for ambiguous syllables (probably list some as exceptions)
- document kh¨antr¨as
- footnote 200 p. 441
- dbu 'khyud
- implement p. 36
- long aspirations (lhod lhod in one big aspiration)
- high tone ma when it's negation (ma mthong : "doesn't see" or "sees the mother")
- add : after consonnants (khams -> kʰâmː, kham -> kʰàm)
- test ཡར་འབྲོ/Co,y-a:m|~tr-
- test ཐིག་ལེ
- indicate ambiguity: ཤ་འབྲས = sh+am|tr-ä' or sha|tr-ä' according to pos
- option of word separation for exceptions, so that another syllable can be at position 1
- option for p. 432, note 196, aspirated consonnants on second syllables
- དགོན་པ: p. 442, note 201, do something about it? gø~ pa
- indicate weak pronounciation of n and ng?
- geminates: impact on a/schwa?

## License

The Python code is Copyright (C) 2018 Elie Roux, provided under [MIT License](LICENSE).
