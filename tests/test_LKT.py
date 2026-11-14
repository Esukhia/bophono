import pytest

from bophono import UnicodeToApi


@pytest.mark.parametrize(('source', 'expected'), [
    ('བོད', 'bö'),
    ('རྡོ་རྗེ', 'dorje'),
    ('བཛྲ་སཏྭ', 'vajra sattva'),
    ('སརྦ', 'sarva'),
    ('ཨོཾ་ཨཱཿཧཱུྃ', 'om ah hum'),
    ('ཧཱུྂ', 'hum'),
    ('རཀྟའི', 'rakte'),
    ('ཙཀ', 'cak'),
    ('རཀ', 'rak'),
    ('ཅིཏ་ཏའི', 'citte'),
    ('རྒྱས་འདེབས', 'gyendeb'),
    ('ཀྵ', 'ksa'),
])
def test_lkt_corpus_readings(source, expected):
    assert UnicodeToApi(schema='LKT').get_api(source) == expected


def test_lkt_respects_offsets_and_unknown_marker():
    lkt = UnicodeToApi(schema='LKT', options={'unknownSyllableMarker': True})
    assert lkt.get_api('xབཛྲx', bindex=1, eindex=4) == 'vajra'
    assert lkt.get_api('བཛྲ་ྀཨཚ་སརྦ') == 'vajra (?)  sarva'
    assert UnicodeToApi(schema='LKT').get_api('བཛྲ་ྀཨཚ་སརྦ') == 'vajra'
    assert '(?)' in UnicodeToApi(schema='KVP', options={'unknownSyllableMarker': True}).get_api('ཧཱུྃ')
    assert UnicodeToApi(schema='IAST').get_api('ཧཱུཾ') == 'hūṃ'
