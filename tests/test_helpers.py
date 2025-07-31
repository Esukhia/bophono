import inspect
import bophono as bophono

def assert_equal_phonetics(schema, tibetan, expected):
    clean_tibetan = inspect.cleandoc(tibetan)
    clean_expected = inspect.cleandoc(expected)
    phonetics = phonetics_for(schema, clean_tibetan)
    assert phonetics == clean_expected, f"Tibetan: {clean_tibetan} | Expected: {clean_expected} | Got: {phonetics}"

def phonetics_for(schema, text):
    lines = text.split("\n")
    result = ""
    for l in lines:
        words = l.split()
        for word in words:
            result += f'{bophono.UnicodeToApi(schema=schema, options={}).get_api(word)} '
        result = result.strip() + "\n"
    return result.strip()