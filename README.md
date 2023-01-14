# Tibetan Phonetics Engine

## Description

Takes in a token in bodyig, and returns phonetics.

## Phonetics methods

Phonetics conversion is based on the Khyentse Vision Project definition.

## Installation

```
pip install git+https://github.com/Esukhia/bophono
```

## Using the API

```python

import bophono
bophono.get_phonetics('སེམས་')

```

There is also a way to add options to the phonetizer:

```python
import bophono
bophono.get_phonetics('སེམས་', options={'aspirateLowTones': False})
```

**NOTE:** that you must first tokenize input string.

## Changes

See [CHANGELOG.md](CHANGELOG.md).

## License

The Python code is Copyright (C) 2023 Esukhia, provided under [MIT License](LICENSE). See [CONTRIBUTORS.md](CONTRIBUTORS.md) for a list of authors and contributors.
