import pytest
from bot.core.translation import Translator

lang_dir = "tests/translation"
default_language = "en"

strings = Translator(dir=lang_dir, default_language=default_language)

def test_translation_loading():
    assert "hi" == "hi"
    
def test_translation_get():
    assert strings.get('greeting_message') == 'Hello user'
    assert strings.get('goodbye_message') == 'See you again'

def test_translation_default_language():
    assert strings.get('greeting_message', lang='es') == 'Hola user'
    assert strings.get('goodbye_message', lang='es') == 'See you again'
    assert strings.get('non_existent_key') == 'non_existent_key'
