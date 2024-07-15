import os

import yaml

from . import logger


class Translator:
  _instances = {}
  default_language = 'en'
  translation_cache = {}

  def __new__(cls, lang='en'):
      if lang not in cls._instances:
          instance = super(Translator, cls).__new__(cls)
          instance.lang = lang
          instance.translations = instance.load_translations(lang)
          cls._instances[lang] = instance
      return cls._instances[lang]

  def load_translations(self, lang):
      if lang in self.translation_cache:
          return self.translation_cache[lang]

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
      self.translation_cache[lang] = translations
      return translations

  def get(self, key, **kwargs):
      translation = self.translations.get(key)
      if not translation:
          logger.warning(f"Missing translation for key '{key}' in language '{self.lang}'.")
          if self.lang != self.default_language:
              translation = Translator(self.default_language).get(key, **kwargs)
          else:
              translation = key
      if kwargs:
          translation = translation.format(**kwargs)
      return translation.replace('\\n', '\n')

  def switch_language(self, new_lang):
      self.lang = new_lang
      if new_lang not in self._instances:
          self.translations = self.load_translations(new_lang)
          self._instances[new_lang] = self
      else:
          self.translations = self._instances[new_lang].translations
