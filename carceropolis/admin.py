# -*- coding: utf-8 -*-
"""Admin module of Carceropolis project personalizations."""
from copy import deepcopy
from django.contrib import admin
from mezzanine.blog.admin import BlogPostAdmin
from .models import (AreaDeAtuacao, Especialidade, Especialista, Publicacao,
                     UnidadePrisional)

publicacao_fieldsets = deepcopy(BlogPostAdmin.fieldsets)
fields = publicacao_fieldsets[0][1]["fields"]
idx = fields.index('categories')
content_idx = fields.index('content')
fields[idx] = 'categorias'
fields.insert(content_idx, 'arquivo_publicacao')
fields.insert(fields.index('title') + 1, 'autoria')


class AreaDeAtuacaoAdmin(admin.ModelAdmin):
    fieldsets = [(None, {u'fields': ['nome_da_area', 'ordem', 'descricao']})]


class EspecialidadeAdmin(admin.ModelAdmin):
    fieldsets = [(None, {u'fields': [u'nome_da_especialidade', u'descricao']})]


class EspecialistaAdmin(admin.ModelAdmin):
    fieldsets = [(None, {u'fields': [u'nome', u'email', u'telefone',
                                     u'mini_bio', u'instituicao',
                                     u'area_de_atuacao', u'especialidades']})]


class PublicacaoAdmin(BlogPostAdmin):
    fieldsets = publicacao_fieldsets


class UnidadePrisionalAdmin(admin.ModelAdmin):
    fieldsets = [(None, {u'fields': [u'nome_unidade', u'sigla_unidade',
                                     u'tipo_logradouro', u'nome_logradouro',
                                     u'numero', u'complemento', u'bairro',
                                     u'municipio', u'uf', u'cep', u'ddd',
                                     u'telefone', u'email']})]


admin.site.register(AreaDeAtuacao, AreaDeAtuacaoAdmin)
admin.site.register(Especialidade, EspecialidadeAdmin)
admin.site.register(Especialista, EspecialistaAdmin)
admin.site.register(Publicacao, PublicacaoAdmin)
admin.site.register(UnidadePrisional, UnidadePrisionalAdmin)
