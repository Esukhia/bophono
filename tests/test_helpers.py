import inspect
import bophono

def assert_equal_phonetics(schema, tibetan, expected):
    assert phonetics_for(schema, inspect.cleandoc(tibetan)) == inspect.cleandoc(expected)

def phonetics_for(schema, text):
    lines = text.split("\n")
    result = ""
    for l in lines:
        words = l.split()
        for word in words:
            result += f'{bophono.UnicodeToApi(schema=schema, options={}).get_api(word)} '
        result = result.strip() + "\n"
    return result.strip()