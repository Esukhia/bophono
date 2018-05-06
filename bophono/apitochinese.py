import os
from .sdtrie import *

api4chinese_table = {
    "equivalence":("k̊", "g̊", "d͡z̥", "ɖ͡ʐ̊", "t̥", "d̥", "ɖ̥", "b̥", "p̥", "ɟ̊"),
    "clean":("ː", "̚", "̯", "g̊", "k", "p", "r", "l", "ɣ", "ɪ", "ˊ", "ˋ"),
}

def _get_trie_path(name):
    return os.path.join(os.path.split(__file__)[0], 'data', 'chinese', name)

zhuyin_csv = get_trie_from_file(_get_trie_path("zhuyin.csv"), "zhuyin_csv")
chinese_trad_csv = get_trie_from_file(_get_trie_path("chinese_trad.csv"), "chinese_trad_csv")
equivalence_csv = get_trie_from_file(_get_trie_path("equivalence.csv"), "equivalence_csv")
exception_csv = get_trie_from_file(_get_trie_path("exception.csv"), "exception_csv")

space = " "*2

def api2chinese(api, phon={"zhuyin":[], "chinese_trad":[]}) :
    ws = [api.split(".")]
    for index, w in enumerate(ws) :
        #Exception
        wj = ".".join(w)
        if exception_csv.get_data(wj) :
            r = exception_csv.get_data(wj).split("|")
            phon["zhuyin"].append(r[0] + space)
            if len(w) > 1 or len(r) > 1  :
                phon["chinese_trad"].append(r[1] + space)
            else :
                phon["chinese_trad"].append(chinese_trad_csv.get_data(r[0]) + space)
            continue

        for i, s in enumerate(w) :
            if not s or s[-1:] == "ɪ" :
                continue
            #Tone
            s += "+" if not i and "ˊ" in s else "-"

            so = s  #Keep the original one

            # radicale
            for a in api4chinese_table["equivalence"] :
                if a in s and s.index(a) == 0 :
                    s = s.replace(a, equivalence_csv.get_data(a))
            # cleaning
            for x in api4chinese_table["clean"] :
                if x in s[1:] :
                    s = s.replace(x, "")
            # m
            if "m" in s[1:] :
                s = s.replace("m", "̃ŋ")
                if "ø" in s :
                    s = s.replace("ø", "o")
            # ~
            elif "n" in s[1:] and not "̃" in s :
                s = s.replace("n", "̃n")
            elif "ŋ" in s[1:] and not "̃" in s :
                s = s.replace("ŋ", "̃ŋ")
            # voyelle
            if "ə" in s :
                s = s.replace("ə", "a")
            elif "ɛ" in s :
                s = s.replace("ɛ", "e")
            elif "ỹŋ" in s :
                s = s.replace("y", "i")

            #Exception for simplified transcription
            if exception_csv.get_data("@"+s) :
                r = exception_csv.get_data("@"+s).split("|")
                phon["zhuyin"].append(r[0] + space)
                if len(r) > 1:
                    phon["chinese_trad"].append(r[1] + space)
                else:
                    phon["chinese_trad"].append(chinese_trad_csv.get_data(r[0]) + space)
                continue
            elif zhuyin_csv.get_data(s) :
                zhuyin = zhuyin_csv.get_data(s)
                chinese_trad = chinese_trad_csv.get_data(zhuyin)
            else :
                print("Can't find the syllable: " + so)
                zhuyin = chinese_trad = "?"

            phon["zhuyin"].append(zhuyin + space)
            phon["chinese_trad"].append(chinese_trad + space)

    zhuyin = "".join(phon["zhuyin"]).strip(' ')
    chinese_trad = "".join(phon["chinese_trad"]).strip(' ')

    phon["zhuyin"].clear()
    phon["chinese_trad"].clear()

    return {"zhuyin":zhuyin, "chinese_trad":chinese_trad}
