import sys
import os
import inspect
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import bophono
import csv

from test_helpers import assert_equal_phonetics

def load_wasur_cases():
    csv_file_path = os.path.join(os.path.dirname(__file__), 'wasur_cases.csv')
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        return [(row[0], row[1]) for row in reader]

wasur_cases = load_wasur_cases()



def test_cases_without_wasur():
    assert_equal_phonetics("KVP", "མངས", "ngé")
    assert_equal_phonetics("KVP", "མགས", "gé")
    assert_equal_phonetics("KVP", "དབས", "é")
    assert_equal_phonetics("KVP", "དངས", "ngé")
    assert_equal_phonetics("KVP", "དགས", "gé")
    assert_equal_phonetics("KVP", "དམས", "mé")
    assert_equal_phonetics("KVP", "བགས", "gé")
    assert_equal_phonetics("KVP", "འབས", "bé")
    assert_equal_phonetics("KVP", "འགས", "gé")
    
def test_wasur_cases_with_root_position_change():
    assert_equal_phonetics("KVP", "མྭངས", "mang")
    assert_equal_phonetics("KVP", "མྭགས", "mak")
    assert_equal_phonetics("KVP", "དྭབས", "dab")
    assert_equal_phonetics("KVP", "དྭངས", "dang")
    assert_equal_phonetics("KVP", "དྭགས", "dak")
    assert_equal_phonetics("KVP", "དྭམས", "dam")

@pytest.mark.parametrize("tibetan, expected", wasur_cases)
def test_wasur_case(tibetan, expected):
    assert_equal_phonetics("KVP", tibetan, expected)
