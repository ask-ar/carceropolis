from modeltranslation.translator import translator, TranslationOptions
from .models import Publicacao


class TranslatedPublicacao(TranslationOptions):
    fields = ()


translator.register(Publicacao, TranslatedPublicacao)
