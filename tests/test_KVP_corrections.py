import sys
import os
import inspect
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import bophono
import csv

from test_helpers import assert_equal_phonetics


### Phonetics Key table

def test_vowels():
    assert_equal_phonetics("KVP", "ཨ", "a")
    assert_equal_phonetics("KVP", "ཨེ", "é")
    assert_equal_phonetics("KVP", "ཨོ", "o")
    assert_equal_phonetics("KVP", "ཨི", "i")
    assert_equal_phonetics("KVP", "ཨུ", "u")
    assert_equal_phonetics("KVP", "ཨུས", "ü")
    assert_equal_phonetics("KVP", "ཨའི", "é")
    assert_equal_phonetics("KVP", "འ", "a")
    assert_equal_phonetics("KVP", "འོད", "ö")

def test_ka():
    assert_equal_phonetics("KVP", "ཀ", "ka")
    assert_equal_phonetics("KVP", "རྐ", "ka")
    assert_equal_phonetics("KVP", "བཀའ", "ka")

def test_kha():
    assert_equal_phonetics("KVP", "ཁ", "kha")
    assert_equal_phonetics("KVP", "མཁའ", "kha")

def test_ga_consonant():
    assert_equal_phonetics("KVP", "ག", "ga")
    assert_equal_phonetics("KVP", "རྒ", "ga")
    assert_equal_phonetics("KVP", "དགའ", "ga")
    
def test_ga_suffix():
    assert_equal_phonetics("KVP", "བག", "bak") # Final consonant becomes k
    assert_equal_phonetics("KVP", "དགེ་ལུགས་", "geluk") # Final consonant becomes k
    assert_equal_phonetics("KVP", "དགེ་ལུགས་པ་", "gelugpa") # Not final consonant becomes g
    assert_equal_phonetics("KVP", "རིག་པ་", "rigpa") # Not final consonant becomes g
    assert_equal_phonetics("KVP", "རྫོགས་ཆེན་", "dzogchen") # Not final consonant becomes g
    assert_equal_phonetics("KVP", "སྤྱན་རས་གཟིགས་", "chenrezig") # Exception
    assert_equal_phonetics("KVP", "ངག་དབང་", "ngawang") # Exception
    assert_equal_phonetics("KVP", "འབྲུག་པ་", "drukpa") # Exception

def test_nga_consonant():
    assert_equal_phonetics("KVP", "ང", "nga")
    assert_equal_phonetics("KVP", "རྔ", "nga")

def test_cha_consonant():
    assert_equal_phonetics("KVP", "ཅ", "cha")
    assert_equal_phonetics("KVP", "ལྕ", "cha")

def test_cha_consonant():
    assert_equal_phonetics("KVP", "ཆ", "cha")

def test_ja_consonant():
    assert_equal_phonetics("KVP", "ཇ", "ja")
    assert_equal_phonetics("KVP", "རྗ", "ja")

def test_nya_consonant():
    assert_equal_phonetics("KVP", "ཉ", "nya")
    assert_equal_phonetics("KVP", "སྙ", "nya")

def test_ta_consonant():
    assert_equal_phonetics("KVP", "ཏ", "ta")
    assert_equal_phonetics("KVP", "རྟ", "ta")

def test_ta_consonant():
    assert_equal_phonetics("KVP", "ཐ", "ta")
    assert_equal_phonetics("KVP", "སྣར་ཐང་", "narthang") # Exception
    assert_equal_phonetics("KVP", "བུམ་ཐང་", "bumthang") # Exception
    
def test_da_consonant():
    assert_equal_phonetics("KVP", "ད", "da")
    assert_equal_phonetics("KVP", "རྡ", "da")

def test_na_consonant():
    assert_equal_phonetics("KVP", "ན", "na")
    assert_equal_phonetics("KVP", "རྣ", "na")

def test_pa_consonant():
    assert_equal_phonetics("KVP", "པ", "pa")
    assert_equal_phonetics("KVP", "སྤ", "pa")

def test_pha_consonant():
    assert_equal_phonetics("KVP", "ཕ", "pa")
    assert_equal_phonetics("KVP", "འཕ", "pa")
    assert_equal_phonetics("KVP", "འཕོ་བ་", "powa") # Exception
    assert_equal_phonetics("KVP", "མི་ཕམ་", "mipham") # Exception

def test_ba_consonant():
    assert_equal_phonetics("KVP", "བ", "ba")
    assert_equal_phonetics("KVP", "བར", "bar")
    assert_equal_phonetics("KVP", "བས", "bé")
    assert_equal_phonetics("KVP", "བད", "bé")
    assert_equal_phonetics("KVP", "བའི", "bé")
    assert_equal_phonetics("KVP", "བར་དུ་", "bardu")
    assert_equal_phonetics("KVP", "སྐང་བ་", "kangwa")
    assert_equal_phonetics("KVP", "རྦ", "ba")
    assert_equal_phonetics("KVP", "སྦ", "ba")
    assert_equal_phonetics("KVP", "འབའ", "ba")
    assert_equal_phonetics("KVP", "བྱང་ཆུབ་ བར་", "jangchub bar")
    assert_equal_phonetics("KVP", "རབ་གསལ་བས་", "rabsalwé")
    assert_equal_phonetics("KVP", "གྱིས་གཟིར་བའི་", "gyizirwé")
    
def test_ba_suffix():
    assert_equal_phonetics("KVP", "གང་བ་", "gangwa")
    assert_equal_phonetics("KVP", "སློབ་", "lob")
    assert_equal_phonetics("KVP", "སློབ་དཔོན་", "lopön")
    assert_equal_phonetics("KVP", "ཐུབ་བསྟན་", "tubten")
    
def test_ma_consonant():
    assert_equal_phonetics("KVP", "མ", "ma")
    assert_equal_phonetics("KVP", "མྲ", "ma")
    assert_equal_phonetics("KVP", "སྨྲ་བ་", "mawa")
    assert_equal_phonetics("KVP", "མྱ", "nya")
    assert_equal_phonetics("KVP", "མྱང་", "nyang")

def test_tsa_consonant():
    assert_equal_phonetics("KVP", "ཙ", "tsa")
    assert_equal_phonetics("KVP", "རྩ", "tsa")

def test_tsa_consonant():
    assert_equal_phonetics("KVP", "ཚ", "tsa")
    
def test_dza_consonant():
    assert_equal_phonetics("KVP", "ཛ", "dza") # dza at the beginning of a word
    assert_equal_phonetics("KVP", "འཛི་སྒར་", "dzigar") # dza at the beginning of a word
    assert_equal_phonetics("KVP", "ར་ཛ་", "raza") # za in the middle of a word

def test_zha_consonant():
    assert_equal_phonetics("KVP", "ཞ", "zha")
    assert_equal_phonetics("KVP", "བཞ", "zha")
    assert_equal_phonetics("KVP", "ཞེ་ཆེན་", "shechen") # Exception
    
def test_za_consonant():
    assert_equal_phonetics("KVP", "ཟ", "za")
    assert_equal_phonetics("KVP", "བཟ", "za")

def test_ya_consonant():
    assert_equal_phonetics("KVP", "ཡ", "ya")

def test_ra_consonant():
    assert_equal_phonetics("KVP", "ར", "ra")

def test_la_consonant():
    assert_equal_phonetics("KVP", "ལ", "la")

def test_lha_consonant():
    assert_equal_phonetics("KVP", "ལྷ", "lha")

def test_sha_consonant():
    assert_equal_phonetics("KVP", "ཤ", "sha")

def test_sa_consonant():
    assert_equal_phonetics("KVP", "ས", "sa")

def test_ha_consonant():
    assert_equal_phonetics("KVP", "ཧ", "ha")
    
def test_yatas():
    assert_equal_phonetics("KVP", "ཀྱི", "kyi")
    assert_equal_phonetics("KVP", "ཆོས་ཀྱི", "chökyi")
    assert_equal_phonetics("KVP", "བྱ", "ja")
    assert_equal_phonetics("KVP", "བྱང་ཆུབ་", "jangchub")
    assert_equal_phonetics("KVP", "པྱ", "cha")
    assert_equal_phonetics("KVP", "ཕྱ", "cha")
    assert_equal_phonetics("KVP", "ཕྱག་རྒྱ", "chakgya")

def test_ratas():
    assert_equal_phonetics("KVP", "ཀྲ", "tra")
    assert_equal_phonetics("KVP", "བཀྲ་བ་", "trawa")
    assert_equal_phonetics("KVP", "ཀྲོག་ཀྲོག་", "trogtrok")
    assert_equal_phonetics("KVP", "བཀྲ་ཤིས་", "tashi")
    assert_equal_phonetics("KVP", "གྲ", "dra")
    assert_equal_phonetics("KVP", "གྲ་པ་", "drapa")
    assert_equal_phonetics("KVP", "ལྷུན་གྲུབ་", "lhündrub")
    assert_equal_phonetics("KVP", "པྲ", "tra")
    assert_equal_phonetics("KVP", "ཕྲ", "tra")
    assert_equal_phonetics("KVP", "འཕྲིན་ལས་", "trinlé")
    assert_equal_phonetics("KVP", "སྤྲུལ་སྐུ་", "tulku")
    assert_equal_phonetics("KVP", "བྲ", "dra")
    assert_equal_phonetics("KVP", "མཉམ་འབྲེལ་", "nyamdrel")

def test_dao_wa():
    assert_equal_phonetics("KVP", "དབ", "dab")
    assert_equal_phonetics("KVP", "དབུ", "u")
    assert_equal_phonetics("KVP", "དབུས", "ü")
    assert_equal_phonetics("KVP", "དབི", "i")
    assert_equal_phonetics("KVP", "དབེ", "é")
    assert_equal_phonetics("KVP", "དབྱང", "yang")
    assert_equal_phonetics("KVP", "དབོ", "wo")
    assert_equal_phonetics("KVP", "དབོས", "wö")
    assert_equal_phonetics("KVP", "དབང", "wang")
    assert_equal_phonetics("KVP", "འཁོར་འདས", "khor dé")

### Additional Phonetics Instructions:

# The ö umlaut is used when the o is followed by d, n, ʼi, l, and s suffixes (in accordance with Tour- nadre’s MST). 
def test_o_umlaut():
    assert_equal_phonetics("KVP", "ཨོ", "o")
    assert_equal_phonetics("KVP", "ཨོད", "ö")
    assert_equal_phonetics("KVP", "ཨོས", "ö")
    assert_equal_phonetics("KVP", "ཨོའི", "ö")
    assert_equal_phonetics("KVP", "ཨོན", "ön")
    assert_equal_phonetics("KVP", "ཨོལ", "öl")
    assert_equal_phonetics("KVP", "གོལ", "göl")
    
# Use the ü umlaut.
def test_u_umlaut():
    assert_equal_phonetics("KVP", "ཨུ", "u")
    assert_equal_phonetics("KVP", "ཨུད", "ü")
    assert_equal_phonetics("KVP", "ཨུས", "ü")
    assert_equal_phonetics("KVP", "ཨུའི", "ü")
    assert_equal_phonetics("KVP", "ཨུན", "ün")
    assert_equal_phonetics("KVP", "ཨུལ", "ül")
    assert_equal_phonetics("KVP", "གུལ", "gül")

# The e accent should only be applied to the final e when there is a clear risk of mispronunciation (primarily for English words such as chime and dome).
def test_no_accent_on_e_apart_from_exceptions():
    assert_equal_phonetics("KVP", "མེ་", "mé")
    assert_equal_phonetics("KVP", "མེད", "mé")
    assert_equal_phonetics("KVP", "མིག་མེད་", "migmé")
    assert_equal_phonetics("KVP", "མེད་སྣང་", "menang")
    assert_equal_phonetics("KVP", "འཆི་མེད་", "chimé")
    assert_equal_phonetics("KVP", "མདོ་མེད་", "domé")
    assert_equal_phonetics("KVP", "རིས་མེད་", "rimé")
    assert_equal_phonetics("KVP", "ཨ་མེས་", "amé")
    assert_equal_phonetics("KVP", "ཅོ་ནེ་", "choné")
    
# g→k: If g ends the first syllable and the second syllable begins with a g, then it is spelled kg. For example: Chokgyur.
def test_gg_yields_kg():
    assert_equal_phonetics("KVP", "མཆོག་འགྱུར་", "chokgyur")
    assert_equal_phonetics("KVP", "ཕྱག་རྒྱ", "chakgya")

# ng+g: When a syllable that ends in ng is followed by a syllable starting with g, the second g is dropped. For example: Senge.
def test_ngg_yields_ng():
    assert_equal_phonetics("KVP", "སེང་གེ་", "sengé")
    assert_equal_phonetics("KVP", "གང་གི་", "gangi")

# a→e: When followed by an n (but not when followed by an l), unless a conventional spelling in English. For example: Palden, Namgyal, but Panchen.
def test_a_followed_by_n_or_l():
    assert_equal_phonetics("KVP", "འགན་", "gen")
    assert_equal_phonetics("KVP", "རྒྱན་", "gyen")
    assert_equal_phonetics("KVP", "དཔལ་ལྡན་", "palden")
    assert_equal_phonetics("KVP", "རྣམ་རྒྱལ་", "namgyal")
    assert_equal_phonetics("KVP", "པཎ་ཆེན་", "panchen")

# Names of contemporary masters, places, schools, and words that are commonly spelled in English (such as Dzongsar Khyentse, Drukpa Kagyu, Shechen, Shigatse, tonglen, chöd, rinpoche, and tulku) should be spelled according to convention.
def test_names_and_common_spellings():
    assert_equal_phonetics("KVP", "ཞེ་ཆེན་", "shechen")
    assert_equal_phonetics("KVP", "གཏོང་ལེན་", "tonglen")
    assert_equal_phonetics("KVP", "གཅོད་", "chöd")
    assert_equal_phonetics("KVP", "རིན་པོ་ཆེ་", "rinpoché")
    assert_equal_phonetics("KVP", "སྤྲུལ་སྐུ་", "tulku")
    assert_equal_phonetics("KVP", "སྡེ་དགེ་", "dergé")
    assert_equal_phonetics("KVP", "སྤྱན་རས་གཟིགས་", "chenrezig")
    assert_equal_phonetics("KVP", "མི་ཕམ་", "mipham")
    assert_equal_phonetics("KVP", "སྣར་ཐང་", "narthang")
    assert_equal_phonetics("KVP", "གན་ལྡན་", "ganden")
    assert_equal_phonetics("KVP", "པཎ་ཆེན་ བླ་མ་", "panchen lama")

# The achung should be ignored
def test_achung():
    assert_equal_phonetics("KVP", "མ་ཧཱ་", "maha")
    assert_equal_phonetics("KVP", "བདེ་ཆེན་ ནཱ་དའི་ དངོས", "dechen nadé ngö")


### Checking a few cases

def test_specific_cases():
    assert_equal_phonetics("KVP", "བར་དུ", "bardu")
    assert_equal_phonetics("KVP", "བར་ཆད", "barché")
    assert_equal_phonetics("KVP", "བར་དོ", "bardo")
    assert_equal_phonetics("KVP", "གཏིབས", "tib")

### Checking that things work as expected in KVP_corrections.csv

def load_corrections():
    csv_file_path = os.path.join(os.path.dirname(__file__), 'KVP_corrections.csv')
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first line (headers)
        return [(row[0], row[2]) for row in reader]

corrections = load_corrections()

@pytest.mark.parametrize("tibetan, expected", corrections)
def test_phonetics_tool_corrections(tibetan, expected):
    assert_equal_phonetics("KVP", tibetan, expected)
