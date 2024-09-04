from pathlib import Path
import re

import bophono
from botok import WordTokenizer


options_fast = {
  'weakAspirationChar': '',
  'aspirateLowTones': False,
  'prefixStrategy': 'always',
  'aiAffixchar': 'ː',
  'hightonechar':'',
  'lowtonechar':'',
  'nasalchar': '',
  'stopSDMode': "eow",
  'useUnreleasedStops': False,
  'eatR': True,
  'eatL': True,
  'syllablesepchar': ''
}
converter_tmd = bophono.UnicodeToApi(schema="TMD", options = options_fast)

in_path = Path('TMD_input')
out_path = Path('TMD_output')
w = WordTokenizer()

for f in in_path.glob('*.txt'):
    out = []
    raw = f.read_text(encoding='utf-8')
    for line in raw.splitlines():
        phon = []
        tokens = w.tokenize(line, split_affixes=False)
        words = [t.text for t in tokens]
        for word in words:
            p = converter_tmd.get_api(word)
            phon.append(p)
        phon = ' '.join(phon)
        out.append(phon)
    out_file = out_path / f.name
    out_file.write_text('\n'.join(out), encoding='utf-8')
