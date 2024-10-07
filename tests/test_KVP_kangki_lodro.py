import sys
import os
import inspect

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import bophono
import csv

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
        gang gi lo trö drib nyi trin dral nyi tar nam dak rab sal we
        ji nye dön kun ji zhin zik chir nyi kyi tuk kar lek bam dzin
        gang dak si pe tsön rar ma rik mun tum duk ngal gyi zir we
        dro tsok kun la bu chik tar tse yen lak druk chu yang den sung
        druk tar cher drok nyön mong nyi long le kyi chak drok dröl dze ching
        ma rik mun sel duk ngal nyu gu ji nye chöd dze ral tri nam
        dö ne dak ching sa chu tar sön yön ten lu dzok gyal se tu wö ku
        chu trak chu dang chu nyi gyen tre dak lö mun sel jam pe yang la rab tu du
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
        gangi lodrö dribnyi trindral nyitar namdak rabsalwe
        jinye dönkun jizhin zigchir nyikyi tugkar legbamzin
        gangdak sipe tsönrar marik muntum dugngal gyizirwe
        drotsok kunla buchik tartse yenlak drugchu yangdensung
        drugtar cherdrok nyönmong nyilong lekyi chagdrok drölzeching
        marik munsel dugngal nyugu jinye chödze raldrinam
        döne dagching sachu tarsön yönten luzok gyalse tuwöku
        chutrak chudang chugnyi gyentre daglö munsel jampe yangla rabtudu
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
        gangi lodrö dribnyi trindral nyi tar namdak rabsalwe
        jinye dön kun jizhin zik chir nyikyi tugkar legbam dzin
        gangdak sipe tsönrarmarik mun tum dugngal gyi zirwe
        dro tsok kun la bu chik tar tse yenlak druk chu yangden sung
        druk tar cher drok nyönmong nyi long lekyi chagdrok dröl dze ching
        marik munsel dugngal nyugu jinye chöd dze raldri nam
        dö ne dak ching sachu tar sön yönten luzok gyalse tuwö ku
        chutrak chu dang chugnyi gyen tre dak lö munsel jampe yang la rabtu du
    """
    assert_equal_phonetics("KVP", tibetan, expected)
