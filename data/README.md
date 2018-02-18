## Data format

The files in this directory contain the data manipulated by the code. Here are some of the conventions:

- when the first column in `roots.csv` ends with `*` (eg: `དག*`) this means that the trie must not match if the syllable contains only the given string (eg: `དག` should be decomposed in `ད`+`ག`, not `དག`+`nothing`)
- when the non-first column in `roots.csv` starts with `~` (eg: `འཕ,~ph+`) this means that `~` should be added only when the syllable is not the first one
- when the first column in `exceptions.csv` starts with `2:` (eg: `2:བ/Ca,w-`), this means that the trie should match only if it is not the first syllable
- when the first column in `exceptions.csv` ends with `/Cx` where `x` is `a`, `i`, `u`, `e`, `o` (eg: `+བ/Ca,w-`), this means that the trie should also match all the affixed particles corresponding to the syllable, appending the phonetics given in `ends.csv` for the affixed (eg: `བའི` should be `w-` combined with the phonetics of `འི` in `ends.csv` 
- when the non-first column in `ends.csv` has a `/`, the first part must be used when the syllable is not final and the second when the syllable is final
- when the non-first column in `roots.csv` has a `/`, the first part must be used when the syllable is initial and the second when not
