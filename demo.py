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
  'syllablesepchar': ''
}


options_fastidious = {
  'weakAspirationChar': '3',
  'aspirateLowTones': True,
  'prefixStrategy': 'always',
  'aiAffixchar': 'ː',
  'hightonechar':'̄',
  'lowtonechar':'̱',
  'nasalchar': '',
  'stopSDMode': "eow",
  'eatP': False,
  'useUnreleasedStops': True,
  'eatK': False,
  'syllablesepchar': ''
}

def toEnglish(s, mode):
    s = s.replace("y", "ü")
    if (mode == "expert"):
        s = s.replace("ɔ", "o1")
        s = s.replace("ɣ", "g2")
        s = s.replace("̊", "1")
        s = s.replace("̥", "1")
       
    else:
        s = s.replace("ɔ", "o")
        s = s.replace("ɣ", "g")
        s = s.replace("̊", "")
        s = s.replace("̥", "")
    s = s.replace("ɖ", "ḍ")
    s = s.replace("ʈ", "ṭ")
    s = s.replace("ɲ", "ny")
    s = s.replace("ø", "ö")
    s = s.replace("ɟ", "gy")
    s = s.replace("c", "ky")
    s = s.replace("j", "y")
    s = s.replace("ɛ", "è")
    s = s.replace("e", "é")
    s = s.replace("ŋ", "ṅ")
    s = s.replace("tɕ", "ch")
    s = s.replace("ɕ", "sh")
    s = s.replace("dʑ", "j")
    s = s.replace("dz", "z")

    return s

filename = 'tests/demo.txt'
converter_fastidious = bophono.UnicodeToApi(schema="MST", options = options_fastidious)
converter_fast = bophono.UnicodeToApi(schema="MST", options = options_fast)
converter_kvp = bophono.UnicodeToApi(schema="KVP", options = options_fast)
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
        print("Unicode:      "+line)
        words = line.split()
        res_kvp = ""
        res_api = ""
        for word in words:
            res_kvp += converter_kvp.get_api(word)+'  '
            res_api += converter_fast.get_api(word)+' '
        print("MST-schema:   "+res_api)
        print("KVP-schema:   "+res_kvp)
        

#Chinese transcription
sentence = "བཀྲ་ཤིས་"
api = converter_fast.get_api(sentence)
zh = bophono.apitochinese.api2chinese(api)
print("\n" + sentence + " -> " + api + \
      " -> " + zh["zhuyin"] + " -> " + zh["chinese_trad"])
