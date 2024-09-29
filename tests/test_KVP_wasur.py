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
    assert_equal_phonetics("KVP", "དགས", "gé")
    assert_equal_phonetics("KVP", "དངས", "ngé")
    assert_equal_phonetics("KVP", "ཁགས", "khak")

@pytest.mark.parametrize("tibetan, expected", wasur_cases)
def test_wasur_case(tibetan, expected):
    assert_equal_phonetics("KVP", tibetan, expected)
