import bophono
import sys

options = {
  'aspirateLowTones': True
}
filename = 'tests/nt.txt'
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
        phon = bophono.get_phonetics(line, options = options)
        print(line + " -> " + phon)

#Chinese transcription
sentence = "བཀྲ་ཤིས་"
api = bophono.unicodetoapi.get_phonetics(sentence)
zh = bophono.apitochinese.api2chinese(api)
print("\n" + sentence + " -> " + api + \
      " -> " + zh["zhuyin"] + " -> " + zh["chinese_trad"])
