import bophono
import sys

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
  'syllablesepchar': '',
  'splitNG': True,
  'splitKN': True
}

filename = 'tests/demo.txt'
converter_ktt = bophono.UnicodeToApi(schema="KTT", options=options_fast)
if len(sys.argv) > 1:
    filename = sys.argv[1]
with open(filename, 'r', encoding="utf8") as f:
    for line in f:
        line = line[:-1]
        if line == '':
            continue
        if line.startswith('#'):
            print(line[1:])
            continue
        print(line)
        words = line.split()
        res = []
        for word in words:
            res.append(converter_ktt.get_api(word))
        res = ' '.join(res)
        print(res)
