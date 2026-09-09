from test_helpers import assert_equal_phonetics, phonetics_for


def test_mst_phonetics_is_alias_of_mst():
    samples = ["སྐུ", "དགའ་པོ", "བཀྲ་ཤིས", "རྐང་པ", "ཨ", "འ"]
    for tibetan in samples:
        assert phonetics_for("MST", tibetan) == phonetics_for("MST_phonetics", tibetan)


def test_mst_phonology_high_and_low_tone():
    assert_equal_phonetics("MST_phonology", "སྐུ", "kū")
    assert_equal_phonetics("MST_phonology", "ཀ", "kā")
    assert_equal_phonetics("MST_phonology", "ག", "kha̱")
    assert_equal_phonetics("MST_phonology", "ཨ", "ā")
    assert_equal_phonetics("MST_phonology", "འ", "a̱")


def test_mst_phonology_syllables_and_exceptions():
    assert_equal_phonetics("MST_phonology", "བཀྲ་ཤིས", "trā|shī'")
    assert_equal_phonetics("MST_phonology", "རྐང་པ", "kāng|pā")
    assert_equal_phonetics("MST_phonology", "དགའ", "ka̱")
    assert_equal_phonetics("MST_phonology", "དགའ་པོ", "ka̱|pō")
    assert_equal_phonetics("MST_phonology", "བཀའ", "kā")
    assert_equal_phonetics("MST_phonology", "སྐུའི", "kǖ:")
    assert_equal_phonetics("MST_phonology", "བཀའི", "kǟ:")
    assert_equal_phonetics("MST_phonology", "མིའི", "mi̱:")
    assert_equal_phonetics("MST_phonology", "དཀོན་པོ", "kȫn|pō")
    assert_equal_phonetics("MST_phonology", "བཀའོ", "kā|o̱")
    assert_equal_phonetics("MST_phonology", "འཕར", "phār")
    assert_equal_phonetics("MST_phonology", "སྐུ་འཕར", "kū|phār")
    assert_equal_phonetics("MST_phonology", "དགེ་འདུན", "ke̱n|tü̱n")
    assert_equal_phonetics("MST_phonology", "བླ་བྲང", "lāp|ra̱ng")
    assert_equal_phonetics("MST_phonology", "ཁངས", "khāng")
    assert_equal_phonetics("MST_phonology", "ཀུན", "kǖn")
