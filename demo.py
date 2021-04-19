import bophono
import sys

options = {
  'aspirateLowTones': True,
  'prefixStrategy': 'always',
  'aiAffixchar': 'ː',
  'hightonechar':'',
  'lowtonechar':'',

}
filename = 'tests/demo.txt'
converter = bophono.UnicodeToApi(schema="MST", options = options) # try with CAT for Amdokä
if (len(sys.argv) > 1):
    filename = sys.argv[1]
with open(filename, 'r', encoding="utf8") as f:
    for line in f:
        line = line[:-1]
        if line == '':
            continue
        if line.startswith('#'):
            print(line[1:])
            continue
        words = line.split()
        res = ""
        for word in words:
            res += converter.get_api(word)+'  '
        print(res)

#Chinese transcription
sentence = "བཀྲ་ཤིས་"
api = converter.get_api(sentence)
zh = bophono.apitochinese.api2chinese(api)
print("\n" + sentence + " -> " + api + \
      " -> " + zh["zhuyin"] + " -> " + zh["chinese_trad"])
