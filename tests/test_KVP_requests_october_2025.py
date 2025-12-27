import pytest
from test_helpers import assert_equal_phonetics

concludingParticleCases = [
  [ "ཕྱག་འཚལ་ལོ", "chagtsal lo" ],
  [ "རིག་གོ", "rik go" ],
  [ "བྱེད་དོ", "jé do" ],
  [ "ཡིན་ནོ", "yin no" ],
  [ "འགྲུབ་བོ", "drub bo" ],
  [ "གསུམ་མོ", "sum mo" ],
  [ "འགྱུར་རོ", "gyur ro" ],
  [ "ལགས་སོ", "lak so" ],
  [ "མཆི་འོ", "chi'o" ],
]

@pytest.mark.parametrize("tibetan, expected", concludingParticleCases, ids=[case[1] for case in concludingParticleCases])
def test_concluding_particles(tibetan, expected):
    assert_equal_phonetics("KVP", tibetan, expected)

otherCases = [
  [ "འགལ་རྐྱེན་བར་ཆད", "galkyen barché" ],
  [ "བསྐྲུན", "trün" ],
  [ "རྟག་ཏུ", "tak tu" ],
  [ "ལ་འཇམ་དཔལ", "la jampal" ],
  [ "བཀའ་བརྒྱད་", "kagyé" ],
  [ "ཉི་ཟླ་བའི", "nyi dawé" ],
  [ "ཡེ་ཤེས་སེམས་དཔའ", "yeshesempa" ],
  [ "དམ་ཚིག་སེམས་དཔའ", "damtsigsempa" ],
  [ "བསྔོའོ", "ngo'o" ],
  [ "ལས་འབྲས", "le dré" ],
  [ "གོ་འཕང", "gopang" ],
  [ "གཡོ་སྒྱུ་མེད་པའི", "yogyu mepé" ],
  [ "སྐུ་བཞི", "ku zhi" ],
  [ "རྩ་ཐིག", "tsa tik" ],
  [ "བསྙེན་སྒྲུབ", "nyen drub" ],
  [ "དབབ", "wab" ],
  [ "དྷཱུ་ཏི", "dhuti" ],
  [ "ལུས་སེམས", "lü sem" ],
  [ "བྱིན་བརླབ", "jinlab" ],
  [ "དགག་སྒྲུབ", "gak drub" ],
  [ "ཆགས་སྡང", "chak dang" ],
  [ "རེ་དོགས", "ré dok" ],
  [ "སྤང་བླང", "pang lang" ],
  [ "བདག་དང་སེམས་ཅན", "dak dang semchen" ],
  [ "དགྲ་བགེགས", "dra gek" ],
  [ "ཤ་ཁྲག", "sha trak" ],
  [ "ཡང་ལེ་ཤོད", "yangleshö" ],
  [ "བཀའ་བསྒོས", "kagö" ],
  [ "ས་ལམ", "sa lam" ],
  [ "ལྷ་ཚོགས", "lha tsok" ],
  [ "སྣང་ཆ", "nangcha" ],
  [ "བཤེས་གཉེན", "shé nyen" ],
]

@pytest.mark.parametrize("tibetan, expected", otherCases, ids=[case[1] for case in otherCases])
def test_other_cases(tibetan, expected):
    assert_equal_phonetics("KVP", tibetan, expected)

sanskritPlaceholdersCases = [
  [ "ཧཱུྃ་", "(?)" ],
  [ "སྔགས་ཀྱི་ཕྲེང་བ་བཻ་ཌཱུ་རྱ་ཞུན་མའི་མདངས་ཅན", "ngagkyitrengwa (?) zhünmedangchen" ],
  [ "ནང་དུ་སྲོག་གི་སྙིང་པོ་ཧཱུྃ་ཡིག་མཐིང་ག་མར་མེ་ལྟར་འབར་བའི་མཐར་སྔགས་ཀྱི་ཕྲེང་བ་བཻཌཱུརྱ་ཞུན་མའི་མདངས་ཅན་གཡས་བསྐོར་དུ་འཁོད་པར་", "nangdusokginyingpo (?) yigtingamarmetarbarwetarngagkyitrengwa (?) zhünmedangchenyekordukhöpar" ],
]

@pytest.mark.parametrize("tibetan, expected", sanskritPlaceholdersCases, ids=[case[1] for case in sanskritPlaceholdersCases])
def test_sanskrit_placeholders(tibetan, expected):
    assert_equal_phonetics("KVP", tibetan, expected)