import os
import pytest
import csv

from test_helpers import assert_equal_phonetics

def load_csv(filename):
    csv_file_path = os.path.join(os.path.dirname(__file__), filename)
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Get the header row
        tibetan_idx = header.index("Tibetan segmented")
        kvp_idx = header.index("KVP")
        return [(row[kvp_idx], row[tibetan_idx]) for row in reader]

new_requirements_cases = load_csv('new-requirements.csv')

@pytest.mark.parametrize("expected, tibetan", new_requirements_cases)
def test_kvp_new_requirements_csv(expected, tibetan):
    assert_equal_phonetics("KVP", tibetan, expected)

def test_kvp_specifics():
    assert_equal_phonetics("KVP", "མདོ་སྔགས", "do ngak")
    assert_equal_phonetics("KVP", "ལྡེའུ་བཙན", "deutsen")
    assert_equal_phonetics("KVP", "མྱ་ངན་", "nya ngen")
    assert_equal_phonetics("KVP", "ཉི་ཟླ་", "nyi da")
    assert_equal_phonetics("KVP", "དབྱེར་མེད་པས", "yermepé")
    assert_equal_phonetics("KVP", "རྫས་", "dzé")
    assert_equal_phonetics("KVP", "ལྷ་རྫས་", "lhadzé")
    assert_equal_phonetics("KVP", "རང་གི", "rangi")
    assert_equal_phonetics("KVP", "རིག་འཛིན་", "rigdzin")
    assert_equal_phonetics("KVP", "ཡིག་དཀར་ པོ", "yigkar po")
    assert_equal_phonetics("KVP", "ཡིག་ དཀར་པོ", "yik karpo")
    assert_equal_phonetics("KVP", "གཏིབས", "tib")
    assert_equal_phonetics("KVP", "དཱི་པཾ་ཀ་ར", "dipamkara")
    assert_equal_phonetics("KVP", "དཱི་པྃ་ཀ་ར", "dipamkara")
    assert_equal_phonetics("KVP", "དཱི་པྂ་ཀ་ར", "dipamkara")
    assert_equal_phonetics("KVP", "རྒྱ་མཚོ", "gyatso")
    assert_equal_phonetics("KVP", "དབེན་ས", "ensa")
    assert_equal_phonetics("KVP", "སྐུ་གསུང་ཐུགས", "ku sung tuk")
    assert_equal_phonetics("KVP", "ཨ་བ་དྷཱུ་ཏི", "awadhuti")
    assert_equal_phonetics("KVP", "ཨ་བ་ དྷཱུ་ཏི", "awa dhuti")
    assert_equal_phonetics("KVP", "བྷནྡྷ", "bhandha")
    assert_equal_phonetics("KVP", "བྷནྡྷས", "bhandhé")
    assert_equal_phonetics("KVP", "ད་ལྟ", "da ta")
    assert_equal_phonetics("KVP", "དབུག", "uk")
    assert_equal_phonetics("KVP", "དབུགས", "uk")
    assert_equal_phonetics("KVP", "དབུགས་དབྱུང", "ugyung")
    assert_equal_phonetics("KVP", "གཟུང་འཛིན", "zungdzin")
    assert_equal_phonetics("KVP", "མཛད", "dzé")
    assert_equal_phonetics("KVP", "རླབས", "lab")   # Normal RA character
    assert_equal_phonetics("KVP", "རློབས", "lob")   # Normal RA character
    assert_equal_phonetics("KVP", "ཪླབས", "lab")  # Fixed-form RA character
    assert_equal_phonetics("KVP", "ཪློབས", "lob")  # Fixed-form RA character
    assert_equal_phonetics("KVP", "བརླངས", "lang") # Fixed-form RA character
    assert_equal_phonetics("KVP", "ཟ་འོག", "za'ok")