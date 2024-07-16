import os

import yaml

from . import logger


class Translator:  #_instances = {}
    default_language = 'en'
    translations = {}
  
    def __init__(self):
        translation_dir = 'bot/translation'
        for filename in os.listdir(translation_dir):
            if filename.endswith('.yaml'):
                lang = filename.split('.')[0]
                self.translations[lang] = self.load_translations(lang)

    def load_translations(self, lang):
        translations = {}
        try:
            with open(os.path.join('bot/translation', f'{lang}.yaml'), 'r') as file:
                translations = yaml.safe_load(file)
        except FileNotFoundError:
            if lang != self.default_language:
                logger.warning(f"Translation file for language '{lang}' not found. Falling back to default language '{self.default_language}'.")
                return self.load_translations(self.default_language)
            else:
                logger.error(f"Translation file for default language '{self.default_language}' not found.")
        return translations

    
    def get(self, key, lang=None, **kwargs):
            if lang is None:
                lang = self.default_language

            translation = self.translations.get(lang, {}).get(key)
            if not translation:
                logger.warning(f"Missing translation for key '{key}' in language '{lang}'.")
                if lang != self.default_language:
                    translation = self.translations.get(self.default_language, {}).get(key, key)
                else:
                    translation = key
            if kwargs:
                translation = translation.format(**kwargs)
            return translation