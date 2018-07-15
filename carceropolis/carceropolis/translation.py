from modeltranslation.translator import translator, TranslationOptions
from .models import Publicacao, AreaDeAtuacao


class TranslatedAreaDeAtuacao(TranslationOptions):
    fields = ('nome', 'descricao')


class TranslatedPublicacao(TranslationOptions):
    fields = ()


translator.register(AreaDeAtuacao, TranslatedAreaDeAtuacao)
translator.register(Publicacao, TranslatedPublicacao)
