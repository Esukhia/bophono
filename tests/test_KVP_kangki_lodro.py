from test_helpers import assert_equal_phonetics

def test_kangki_lodro_one_by_one():
    tibetan = """
        གང་ གི་ བློ་ གྲོས་ སྒྲིབ་ གཉིས་ སྤྲིན་ བྲལ་ ཉི་ ལྟར་ རྣམ་ དག་ རབ་ གསལ་ བས།།
        ཇི་ སྙེད་ དོན་ ཀུན་ ཇི་ བཞིན་ གཟིགས་ ཕྱིར་ ཉིད་ ཀྱི་ ཐུགས་ ཀར་ གླེགས་ བམ་ འཛིན།།
        གང་ དག་ སྲིད་ པའི་ བཙོན་ རར་ མ་ རིག་ མུན་ འཐུམས་ སྡུག་ བསྔལ་ གྱིས་ གཟིར་ བའི།།
        འགྲོ་ ཚོགས་ ཀུན་ ལ་ བུ་ གཅིག་ ལྟར་ བརྩེ་ ཡན་ ལག་ དྲུག་ བཅུའི་ དབྱངས་ ལྡན་ གསུང༌།།
        འབྲུག་ ལྟར་ ཆེར་ སྒྲོགས་ ཉོན་ མོངས་ གཉིད་ སློང་ ལས་ ཀྱི་ ལྕགས་ སྒྲོག་ འགྲོལ་ མཛད་ ཅིང༌།།
        མ་ རིག་ མུན་ སེལ་ སྡུག་ བསྔལ་ མྱུ་ གུ་ ཇི་ སྙེད་ གཅོད་ མཛད་ རལ་ གྲི་ བསྣམས།།
        གདོད་ ནས་ དག་ ཅིང་ ས་ བཅུའི་ མཐར་ སོན་ ཡོན་ ཏན་ ལུས་ རྫོགས་ རྒྱལ་ སྲས་ ཐུ་ བོའི་ སྐུ།།
        བཅུ་ ཕྲག་ བཅུ་ དང་ བཅུ་ གཉིས་ རྒྱན་ སྤྲས་ བདག་ བློའི་ མུན་ སེལ་ འཇམ་ པའི་ དབྱངས་ ལ་ རབ་ ཏུ་ འདུད།། 
    """
    expected = """
        gang gi lo drö drib nyi trin dral nyi tar nam dak rab sal bé
        ji nyé dön kün ji zhin zik chir nyi kyi tuk kar lek bam dzin
        gang dak si pé tsön rar ma rik mün tum duk ngal gyi zir bé
        dro tsok kün la bu chik tar tsé yen lak druk chü yang den sung
        druk tar cher drok nyön mong nyi long lé kyi chak drok dröl dzé ching
        ma rik mün sel duk ngal nyu gu ji nyé chöd dzé ral dri nam
        dö né dak ching sa chü tar sön yön ten lü dzok gyal sé tu bö ku
        chu trak chu dang chu nyi gyen tré dak lö mün sel jam pé yang la rab tu dü
    """
    assert_equal_phonetics("KVP", tibetan, expected)

def test_kangki_lodro_two_by_two():
    tibetan = """
        གང་གི་ བློ་གྲོས་ སྒྲིབ་གཉིས་ སྤྲིན་བྲལ་ ཉི་ལྟར་ རྣམ་དག་ རབ་གསལ་བས།།
        ཇི་སྙེད་ དོན་ཀུན་ ཇི་བཞིན་ གཟིགས་ཕྱིར་ ཉིད་ཀྱི་ ཐུགས་ཀར་ གླེགས་བམ་འཛིན།།
        གང་དག་ སྲིད་པའི་ བཙོན་རར་ མ་རིག་ མུན་འཐུམས་ སྡུག་བསྔལ་ གྱིས་གཟིར་བའི།།
        འགྲོ་ཚོགས་ ཀུན་ལ་ བུ་གཅིག་ ལྟར་བརྩེ་ ཡན་ལག་ དྲུག་བཅུའི་ དབྱངས་ལྡན་གསུང༌།།
        འབྲུག་ལྟར་ ཆེར་སྒྲོགས་ ཉོན་མོངས་ གཉིད་སློང་ ལས་ཀྱི་ ལྕགས་སྒྲོག་ འགྲོལ་མཛད་ཅིང༌།།
        མ་རིག་ མུན་སེལ་ སྡུག་བསྔལ་ མྱུ་གུ་ ཇི་སྙེད་ གཅོད་མཛད་ རལ་གྲི་བསྣམས།།
        གདོད་ནས་ དག་ཅིང་ ས་བཅུའི་ མཐར་སོན་ ཡོན་ཏན་ ལུས་རྫོགས་ རྒྱལ་སྲས་ ཐུ་བོའི་སྐུ།།
        བཅུ་ཕྲག་ བཅུ་དང་ བཅུ་གཉིས་ རྒྱན་སྤྲས་ བདག་བློའི་ མུན་སེལ་ འཇམ་པའི་ དབྱངས་ལ་ རབ་ཏུ་འདུད།།
    """
    expected = """
        gangi lodrö dribnyi trindral nyitar namdak rabsalwé
        jinyé dönkün jizhin zigchir nyikyi tugkar legbamdzin
        gangdak sipé tsönrar marik müntum dugngal gyizirwé
        drotsok künla buchik tartsé yenlak drugchü yangdensung
        drugtar cherdrok nyönmong nyilong lekyi chagdrok dröldzeching
        marik münsel dugngal nyugu jinyé chödzé raldrinam
        döné dagching sachü tarsön yönten lüdzok gyalsé tuwöku
        chutrak chudang chunyi gyentré daglö münsel jampé yangla rabtudü
    """
    assert_equal_phonetics("KVP", tibetan, expected)

def test_kangki_lodro_word_by_word():
    tibetan = """
        གང་གི་ བློ་གྲོས་ སྒྲིབ་གཉིས་ སྤྲིན་བྲལ་ ཉི་ ལྟར་ རྣམ་དག་ རབ་གསལ་བས །། 
        ཇི་སྙེད་ དོན་ ཀུན་ ཇི་བཞིན་ གཟིགས་ ཕྱིར་ ཉིད་ཀྱི་ ཐུགས་ཀར་ གླེགས་བམ་ འཛིན །། 
        གང་དག་ སྲིད་པའི་ བཙོན་རར་མ་རིག་ མུན་ འཐུམས་ སྡུག་བསྔལ་ གྱིས་ གཟིར་བའི །། 
        འགྲོ་ ཚོགས་ ཀུན་ ལ་ བུ་ གཅིག་ ལྟར་ བརྩེ་ ཡན་ལག་ དྲུག་ བཅུའི་ དབྱངས་ལྡན་ གསུང༌ །། 
        འབྲུག་ ལྟར་ ཆེར་ སྒྲོགས་ ཉོན་མོངས་ གཉིད་ སློང་ ལས་ཀྱི་ ལྕགས་སྒྲོག་ འགྲོལ་ མཛད་ ཅིང༌ །། 
        མ་རིག་ མུན་སེལ་ སྡུག་བསྔལ་ མྱུ་གུ་ ཇི་སྙེད་ གཅོད་ མཛད་ རལ་གྲི་ བསྣམས །། 
        གདོད་ ནས་ དག་ ཅིང་ ས་བཅུའི་ མཐར་ སོན་ ཡོན་ཏན་ ལུས་རྫོགས་ རྒྱལ་སྲས་ ཐུ་བོའི་ སྐུ །། 
        བཅུ་ཕྲག་ བཅུ་ དང་ བཅུ་གཉིས་ རྒྱན་ སྤྲས་ བདག་ བློའི་ མུན་སེལ་ འཇམ་པའི་ དབྱངས་ ལ་ རབ་ཏུ་ འདུད །།
    """
    expected = """
        gangi lodrö dribnyi trindral nyi tar namdak rabsalwé
        jinyé dön kün jizhin zik chir nyikyi tugkar legbam dzin
        gangdak sipé tsönrarmarik mün tum dugngal gyi zirwé
        dro tsok kün la bu chik tar tsé yenlak druk chü yangden sung
        druk tar cher drok nyönmong nyi long lekyi chagdrok dröl dzé ching
        marik münsel dugngal nyugu jinyé chöd dzé raldri nam
        dö né dak ching sachü tar sön yönten lüdzok gyalsé tuwö ku
        chutrak chu dang chunyi gyen tré dak lö münsel jampé yang la rabtu dü
    """
    assert_equal_phonetics("KVP", tibetan, expected)
