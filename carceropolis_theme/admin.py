# -*- coding: utf-8 -*-
"""Admin module of Carceropolis project personalizations."""
from copy import deepcopy
from django.contrib import admin
from mezzanine.blog.admin import BlogPostAdmin
from .models import AreaDeAtuacao, Especialidade, Especialista, Publicacao

blog_fieldsets = deepcopy(BlogPostAdmin.fieldsets)
idx = blog_fieldsets[0][1]["fields"].index('categories')
content_idx = blog_fieldsets[0][1]["fields"].index('content')
blog_fieldsets[0][1]["fields"][idx] = 'categorias'
blog_fieldsets[0][1]["fields"].insert(content_idx, 'arquivo_publicacao')


class AreaDeAtuacaoAdmin(admin.ModelAdmin):
    fieldsets = [(None, {u'fields': ['nome_da_area', 'ordem', 'descricao']})]


class EspecialidadeAdmin(admin.ModelAdmin):
    fieldsets = [(None, {u'fields': [u'nome_da_especialidade', u'descricao']})]


class EspecialistaAdmin(admin.ModelAdmin):
    fieldsets = [(None, {u'fields': [u'nome', u'email', u'telefone',
                                     u'mini_bio', u'instituicao',
                                     u'area_de_atuacao', u'especialidades']})]

class PublicacaoAdmin(BlogPostAdmin):
    fieldsets = blog_fieldsets

admin.site.register(AreaDeAtuacao, AreaDeAtuacaoAdmin)
admin.site.register(Especialidade, EspecialidadeAdmin)
admin.site.register(Especialista, EspecialistaAdmin)
admin.site.register(Publicacao, PublicacaoAdmin)
