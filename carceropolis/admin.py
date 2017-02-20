# -*- coding: utf-8 -*-
"""Admin module of Carceropolis project personalizations."""
from copy import deepcopy
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from mezzanine.blog.admin import BlogPostAdmin
from .models import (AreaDeAtuacao, BaseMJ, Especialidade, Especialista,
                     Publicacao, UnidadePrisional)


class EspecialistaAdmin(admin.ModelAdmin):
    search_fields = ['nome', 'instituicao', 'area_de_atuacao__nome',
                     'especialidades__nome']
    list_filter = ['area_de_atuacao', 'especialidades', 'instituicao']
    list_display = ['nome', 'instituicao', 'email', 'ddi', 'ddd', 'telefone']


def generate_publicacao_fieldset():
    publicacao_fieldsets = deepcopy(BlogPostAdmin.fieldsets)
    fields = publicacao_fieldsets[0][1]["fields"]

    cat_idx = fields.index('categories')
    fields[cat_idx] = 'categorias'

    dates_idx = fields.index((u'publish_date', u'expiry_date'))
    fields[dates_idx] = 'ano_de_publicacao'

    content_idx = fields.index('content')
    fields.insert(content_idx, 'arquivo_publicacao')

    fields.insert(fields.index('title') + 1, 'autoria')

    fields.remove('allow_comments')
    fields.remove('status')

    tags = publicacao_fieldsets[2][1]['fields'].remove('keywords')
    fields.append('keywords')

    return publicacao_fieldsets


class PublicacaoAdmin(BlogPostAdmin):
    fieldsets = generate_publicacao_fieldset()
    list_display = ['title', 'autoria', 'status', 'view_link']
    list_filter = ['ano_de_publicacao', 'categorias', 'status', 'keywords']
    search_fields = ['title', 'autoria']

    def view_link(self, obj):
        return mark_safe('<a href="{0}">{1}</a>'.format(obj.get_absolute_url(),
                                                        _("View on Site")))

    view_link.allow_tags = True
    view_link.short_description = _("View on Site")


class UnidadePrisionalAdmin(admin.ModelAdmin):
    fieldsets = [(None, {u'fields': [u'nome_unidade', u'sigla_unidade',
                                     u'tipo_logradouro', u'nome_logradouro',
                                     u'numero', u'complemento', u'bairro',
                                     u'municipio', u'uf', u'cep', u'ddd',
                                     u'telefone', u'email']})]
    list_display = ['nome_unidade', 'municipio', 'uf']
    search_fields = ['nome_unidade', 'municipio__nome', 'uf']
    list_filter = ['uf']


class BaseMJAdmin(admin.ModelAdmin):
    list_display = ['mes', 'ano', 'salvo_em']
    list_filter = ['mes', 'ano']
    readonly_fields=()

    def get_readonly_fields(self, request, obj=None):
        """Return the list of readyonly fields.

        If the user is creating a new object (ADD), then there are no readonly
        fields, otherwise, all fields are readonly.
        """
        if obj:
            return ['mes', 'ano', 'salvo_em', 'arquivo']
        else:
            return []


admin.site.register(AreaDeAtuacao)
admin.site.register(BaseMJ, BaseMJAdmin)
admin.site.register(Especialidade)
admin.site.register(Especialista, EspecialistaAdmin)
admin.site.register(Publicacao, PublicacaoAdmin)
admin.site.register(UnidadePrisional, UnidadePrisionalAdmin)
