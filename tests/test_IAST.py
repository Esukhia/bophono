from test_helpers import assert_equal_phonetics


def test_iast_basic():
    assert_equal_phonetics("IAST", "ཀརྨ", "karma")
    assert_equal_phonetics("IAST", "པདྨ", "padma")
    assert_equal_phonetics("IAST", "ཨཱ", "ā")
    assert_equal_phonetics("IAST", "མ\u0f77ཏ", "mṝta")
    assert_equal_phonetics("IAST", "མ\u0fb2\u0f71\u0f80ཏ", "mṝta")
    assert_equal_phonetics("IAST", "ག\u0f71\u0f74", "gū")
    assert_equal_phonetics("IAST", "ག\u0f74\u0f71", "gū")
    assert_equal_phonetics("IAST", "ག\u0f84མ", "gma")
    assert_equal_phonetics("IAST", "བྷིཀྵཱུ", "bhikṣū")
    assert_equal_phonetics("IAST", "ཎཱཾ", "ṇāṃ")
    assert_equal_phonetics("IAST", "དུརྦྲྀཏྟཾ", "durbṛttaṃ")


def test_iast_phrase():
    assert_equal_phonetics(
        "IAST",
        "།ཀརྨྨོ་པ་དེ་ཤཾ་བྷིཀྵཱུ་ཎཱཾ་སརྦྦ་ཛྙཿཀརྟྟ་མུ་ཏྱ་ཏཿ།",
        "|karmmo pa de śaṃ bhikṣū ṇāṃ sarbba jñaḥkartta mu tya taḥ|",
    )
