"""URL from carcerópolis project."""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sites.models import Site
from django.views.i18n import set_language
from mezzanine.accounts.views import logout
from mezzanine.blog.models import BlogPost
from mezzanine.conf import settings
from mezzanine.core.views import direct_to_template

from . import views
from carceropolis.charts.views import (
    dados_alas_exclusivas, dados_materno_infantil, dados_saude, dados_educacao,
    dados_juridico, dados_infraestrutura, dados_perfil_populacional,
    dados_gerais)

_slash = '/'

admin.autodiscover()
admin.site.unregister(BlogPost)
admin.site.unregister(Site)

dados_pattern = [
    url(r'^alas_exclusivas/$', dados_alas_exclusivas,
        name='dados_alas_exclusivas'),
    url(r'^materno_infantil/$', dados_materno_infantil,
        name='dados_materno_infantil'),
    url(r'^saude/$', dados_saude,
        name='dados_saude'),
    url(r'^educacao/$', dados_educacao,
        name='dados_educacao'),
    url(r'^juridico/$', dados_juridico,
        name='dados_juridico'),
    url(r'^infraestrutura/$', dados_infraestrutura,
        name='dados_infraestrutura'),
    url(r'^perfil_populacional/$', dados_perfil_populacional,
        name='dados_perfil_populacional'),
    url(r'^gerais/$', dados_gerais,
        name='dados_gerais'),
    url(r'^$', views.dados_home, name='dados_home')
]

# Publicacao patterns.
publicacao_pattern = [
    url(r'^tag/(?P<tag>.*)%s$' % _slash,
        views.publicacao_list_tag, name='publicacao_list_tag'),
    url(r'^categoria/(?P<categoria>.*)%s$' % _slash,
        views.publicacao_list_categoria, name='publicacao_list_categoria'),
    url(r'^(?P<slug>.*)%s$' % _slash, views.publicacao_detail,
        name='publicacao_detail'),
    url(r'^$', views.publicacao_home, name='publicacao_home'),
]

especialistas_pattern = [
    url(r'^area_de_atuacao/(?P<area_de_atuacao>.*)%s$' % _slash,
        views.especialistas_list, name='especialista_list_area_atuacao'),
    url(r'^especialidade/(?P<especialidade>.*)%s$' % _slash,
        views.especialistas_list, name='especialista_list_especialidade'),
    url(r'^(?P<slug>.*)%s$' % _slash, views.publicacao_detail,
        name='publicacao_detail'),
    url(r'^$', views.especialistas_list, name='especialista_list'),
]

unidades_pattern = [
    url(r'^$', views.unidades_map, name='unidades_map'),
    url(r'^card/(?P<id_unidade>.*)%s$' % _slash,
        views.card_unidade, name='card_unidade'),
]

urlpatterns = [
    # Change the admin prefix here to use an alternate URL for the
    # admin interface, which would be marginally more secure.
    url("^admin/", include(admin.site.urls)),
]

if settings.USE_MODELTRANSLATION:
    urlpatterns += [
        url('^i18n/$', set_language, name='set_language'),
    ]

urlpatterns += [
    url(r'^[Pp]ublicacoes/', include(publicacao_pattern)),
    url(r'^[Ee]specialistas/', include(especialistas_pattern)),
    url(r'^[Dd]ados/', include(dados_pattern)),
    url(r'^[Uu]nidades/', include(unidades_pattern)),
    url(r'^entrar/$', views.login_user),
    url(r'^sair/$', logout),
    url(r'^cadastro/$', views.register_user),
    url(r'^recuperar_senha/$', views.password_recovery),
    url(r'^painel_dados/$', views.data_dashboard),

    url("^$", direct_to_template, {"template": "index.html"}, name="home"),

    # MEZZANINE'S URLS
    # ----------------
    # ADD YOUR OWN URLPATTERNS *ABOVE* THE LINE BELOW.
    # ``mezzanine.urls`` INCLUDES A *CATCH ALL* PATTERN
    # FOR PAGES, SO URLPATTERNS ADDED BELOW ``mezzanine.urls``
    # WILL NEVER BE MATCHED!
    url("^", include("mezzanine.accounts.urls")),
    url("^", include("mezzanine.urls")),
]

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
