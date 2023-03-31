from googletrans import LANGUAGES
from googletrans import Translator as GoogleTranslatorAPI
from reverso_api.context import ReversoContextAPI
from enum import Enum


class TranslatorType(Enum):
    GOOGLE = 1
    REVERSO = 2

    @staticmethod
    def from_name(name):
        for member in TranslatorType:
            if member.name == name:
                return member
        raise ValueError(f"No member of TranslatorType has name {name}")


class Translator:
    def __init__(self, translator_type:str):
        self.translator_type = TranslatorType.from_name(translator_type)

        if self.translator_type == TranslatorType.GOOGLE:
            self.translator = GoogleTranslator()
        elif self.translator_type == TranslatorType.REVERSO:
            self.translator = ReversoTranslator()
        else:
            raise ValueError("not find this type of translator")

    def translate(self, text, from_lang, to_lang):
        return self.translator.translate(text, from_lang, to_lang)


class GoogleTranslator:
    def __init__(self):
        self.translator = GoogleTranslatorAPI()

    def translate(self, text, from_lang, to_lang):
        return self.translator.translate(text, src=from_lang, dest=to_lang).text


class ReversoTranslator:
    def __init__(self):
        pass

    def translate(self, text, from_lang, to_lang):
        api = ReversoContextAPI(
            text,
            '',
            from_lang,
            to_lang)
        for source_word, translation, frequency, part_of_speech, inflected_forms in api.get_translations():
            return translation