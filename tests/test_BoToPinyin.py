from bophono import tibetan_to_pinyin


def test_tibetan_to_pinyin_diacritic():
    assert tibetan_to_pinyin("སྐུ") == "gu"
    assert tibetan_to_pinyin("བཀྲ་ཤིས") == "zha xi"
    assert tibetan_to_pinyin("ལྷ་ས") == "lha sa"
    assert tibetan_to_pinyin("བོད") == "bö"
    assert tibetan_to_pinyin("དགའ་པོ") == "ka pô"


def test_tibetan_to_pinyin_ascii():
    assert tibetan_to_pinyin("བོད", style="ascii") == "boi"
    assert tibetan_to_pinyin("དགའ་པོ", style="ascii") == "ka po"
    assert tibetan_to_pinyin("བཀྲ་ཤིས", style="ascii") == "zha xi"
