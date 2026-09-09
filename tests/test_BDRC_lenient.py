from test_helpers import assert_equal_phonetics, phonetics_for


def test_bdrc_lenient_java_examples():
    # lucene-bo PhoneticsFilterTest.testStandardTibetanSimple
    assert_equal_phonetics("BDRC_lenient", "གཤན", "Sen")
    assert_equal_phonetics("BDRC_lenient", "བཤན", "Sen")
    assert_equal_phonetics("BDRC_lenient", "རྟེན", "ten")
    assert_equal_phonetics("BDRC_lenient", "བསྟན", "ten")
    assert_equal_phonetics("BDRC_lenient", "ཐེན", "ten")


def test_bdrc_lenient_nasalization_ignored():
    assert phonetics_for("BDRC_lenient", "འཕྲིན་ལས") == phonetics_for("BDRC_lenient", "ཕྲིན་ལས")
    assert_equal_phonetics("BDRC_lenient", "འཕྲིན་ལས", "trinle")


def test_bdrc_lenient_basic():
    assert_equal_phonetics("BDRC_lenient", "སྐུ", "ku")
    assert_equal_phonetics("BDRC_lenient", "བཀྲ་ཤིས", "traSi")
    assert_equal_phonetics("BDRC_lenient", "དབའ", "wa")
    assert_equal_phonetics("BDRC_lenient", "དབུ", "u")
    assert_equal_phonetics("BDRC_lenient", "སྒམ་པོ་པ", "kampopa")
