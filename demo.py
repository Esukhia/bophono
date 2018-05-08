import bophono
import sys

options = {
  'aspirateLowTones': True
}
filename = 'tests/nt.txt'
converter = bophono.UnicodeToApi(schema="CAT", options = options) # try with CAT for Amdokä
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
        phon = converter.get_api(line)
        print(line + " -> " + phon)

#Chinese transcription
sentence = "བཀྲ་ཤིས་"
api = converter.get_api(sentence)
zh = bophono.apitochinese.api2chinese(api)
print("\n" + sentence + " -> " + api + \
      " -> " + zh["zhuyin"] + " -> " + zh["chinese_trad"])
