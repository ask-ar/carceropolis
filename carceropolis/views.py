# coding: utf-8
import logging
import operator
from collections import OrderedDict
from csv import DictReader
from functools import reduce
import json

import plotly as py
import plotly.offline as opy
import plotly.graph_objs as go
import pandas as pd
import plotly.dashboard_objs as dashboard
import IPython.display
from IPython.display import Image

from requests.compat import json as _json
from plotly import utils

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.messages import info, error
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.text import slugify
from mezzanine.accounts import get_profile_form
from mezzanine.conf import settings
from mezzanine.generic.models import Keyword
from mezzanine.utils.email import send_verification_mail, send_approve_mail
from mezzanine.utils.views import paginate
from mezzanine.utils.urls import login_redirect, next_url

from .models import AreaDeAtuacao, Especialidade, Especialista, Publicacao

# from mezzanine.utils.views import render

User = get_user_model()

log = logging.getLogger(__name__)


# def setlanguage(request):
    # return render(request, 'set-language.html',
                  # {'LANGUAGES':settings.LANGUAGES,
                   # 'SELECTEDLANG':request.LANGUAGE_CODE})


###############################################################################
# PUBLICACOES
###############################################################################

def publicacao_home(request):
    """Display the Publicações Home page, which is a matrix with all available
    categories (only categories, not the items from the Publicação Class).
    """
    categorias = AreaDeAtuacao.objects.all()
    categorias = categorias.order_by('ordem')
    templates = ["carceropolis/publicacao/publicacao_home.html"]
    context = {'categorias': categorias}
    return TemplateResponse(request, templates, context)


def publicacao_list_tag(request, tag, extra_context=None):
    """Display a list of blog posts that are filtered by tag, year, month,
    author or categoria. Custom templates are checked for using the name
    ``carceropolis/publicacao/publicacao_list_XXX.html`` where ``XXX`` is
    either the categoria slug or author's username if given.
    """
    templates = []
    template = "carceropolis/publicacao/publicacao_list.html"
    publicacoes = Publicacao.objects.published()
    tag = get_object_or_404(Keyword, slug=tag)
    publicacoes = publicacoes.filter(keywords__keyword=tag)

    prefetch = ("categorias", "keywords__keyword")
    publicacoes = publicacoes.prefetch_related(*prefetch)
    publicacoes = paginate(publicacoes, request.GET.get("page", 1),
                           settings.PUBLICACAO_PER_PAGE,
                           settings.MAX_PAGING_LINKS)
    context = {"publicacoes": publicacoes, "tag": tag,}
    context.update(extra_context or {})
    templates.append(template)
    return TemplateResponse(request, templates, context)


def publicacao_list_categoria(request, categoria, extra_context=None):
    """Display a list of Publicacao for a specific Categoria with some filters.

    The list can be filtered by tag, year, author.
    """
    templates = []
    template = "carceropolis/publicacao/publicacao_list.html"

    log.debug('Getting list of Publicacoes for category %s', categoria)

    categoria = get_object_or_404(AreaDeAtuacao, slug=categoria)

    publicacoes = Publicacao.objects.filter(categorias=categoria)

    ano = request.GET.get('ano', None)
    if ano:
        log.debug('    filtering ano: %s', ano)
        publicacoes = publicacoes.filter(ano_de_publicacao=ano)

    autoria = request.GET.get('autoria', None)
    if autoria:
        log.debug('    filtering autoria: %s', autoria)
        publicacoes = publicacoes.filter(autoria__icontains=autoria)

    tags = request.GET.get('tag', None)
    if tags:
        log.debug('    filtering tags: %s', tags)
        publicacoes = publicacoes.filter(keywords__keyword__title__iregex=r'(' + '|'.join(tags.split()) + ')')

    search = request.GET.get('q', None)
    if search is not None and search:
        terms = search.split()
        log.debug('    general filtering: %s', terms)

        publicacoes = publicacoes.filter(reduce(operator.and_,
                                                (Q(title__icontains=q) for q in terms)) |
                                         reduce(operator.or_,
                                                (Q(autoria__icontains=q) for q in terms)) |
                                         reduce(operator.or_,
                                                (Q(content__icontains=q) for q in terms)) |
                                         reduce(operator.or_,
                                                (Q(description__icontains=q) for q in terms)) |
                                         reduce(operator.or_,
                                                (Q(keywords__keyword__title__icontains=q) for q in terms))
                                         )

    order_by = request.GET.get('order_by', None)
    sort = request.GET.get('sort', 'ASC')
    if order_by:
        if sort == 'ASC':
            publicacoes = publicacoes.order_by(order_by)
        else:
            publicacoes = publicacoes.order_by('-' + order_by)

    #: Get only unique results
    publicacoes = publicacoes.distinct()

    prefetch = ("categorias", "keywords__keyword")
    publicacoes = publicacoes.prefetch_related(*prefetch)
    publicacoes = paginate(publicacoes, request.GET.get("page", 1),
                           settings.PUBLICACAO_PER_PAGE,
                           settings.MAX_PAGING_LINKS)

    context = {"publicacoes": publicacoes, "ano": ano, "tag": tags,
               "categoria": categoria, "autoria": autoria, "q": search}
    context.update(extra_context or {})

    templates.append(template)

    return TemplateResponse(request, templates, context)


def publicacao_detail(request, slug, extra_context=None):
    """Presenting a specific publication (publicaço)."""
    template = "carceropolis/publicacao/publicacao_detail.html"
    publicacoes = Publicacao.objects.published().select_related()
    publicacao = get_object_or_404(publicacoes, slug=slug)
    related_posts = publicacao.related_posts.published()
    context = {"publicacao": publicacao, "editable_obj": publicacao,
               "related_posts": related_posts}
    context.update(extra_context or {})
    templates = [template]
    return TemplateResponse(request, templates, context)


def publicacao_feed(request, fmt, **kwargs):
    """Blog posts feeds - maps format to the correct feed view."""
    try:
        return {"rss": PostsRSS, "atom": PostsAtom}[fmt](**kwargs)(request)
    except KeyError:
        raise Http404()


###############################################################################
# ESPECIALISTAS
###############################################################################


def especialistas_list(request, extra_context=None):
    """Display a list of blog posts that are filtered by tag, year, month,
    author or categoria. Custom templates are checked for using the name
    ``carceropolis/publicacao/publicacao_list_XXX.html`` where ``XXX`` is
    either the categoria slug or author's username if given.
    """
    areas_de_atuacao = AreaDeAtuacao.objects.all()
    areas_de_atuacao = areas_de_atuacao.order_by('ordem')
    especialistas = Especialista.objects.all()
    especialistas = especialistas.order_by('nome')

    context = {
        'area_atuacao': '',
        'nome': '',
        'especialidade': '',
        'areas_de_atuacao': areas_de_atuacao,
        'especialistas': None,
        'error_message': ''
    }

    if 'nome' in request.GET.keys():
        nome = request.GET.get('nome'),
        nome = nome[0]
        especialistas = especialistas.filter(
            nome__icontains=nome)
        context['nome'] = nome

    if 'area_atuacao' in request.GET.keys():
        area_atuacao = request.GET.get('area_atuacao'),
        area_atuacao = area_atuacao[0]
        especialistas = especialistas.filter(
            area_de_atuacao__nome__in=[area_atuacao])
        context['area_atuacao'] = area_atuacao

    if 'especialidade' in request.GET.keys():
        especialidade = request.GET.get('especialidade'),
        especialidade = especialidade[0]
        especialistas = especialistas.filter(
            especialidades__nome__in=[especialidade])
        context['especialidade'] = especialidade

    prefetch = ("area_de_atuacao", 'especialidades')
    especialistas = especialistas.prefetch_related(*prefetch)
    especialistas = paginate(especialistas, request.GET.get("page", 1),
                             settings.PUBLICACAO_PER_PAGE,
                             settings.MAX_PAGING_LINKS)

    if not especialistas:
        especialistas = Especialista.objects.all()
        context['error_message'] = 'Nenhum(a) especialista encontrado(a) com '
        context['error_message'] += 'os parâmetros passados.'

    context['especialistas'] = especialistas

    templates = ['carceropolis/especialistas/especialistas.html']

    return TemplateResponse(request, templates, context)


def dados_home(request):
    """Display the Dados Home page, which is a matrix with all available
    categories (only categories, not the items from the Publicação Class).
    """
    templates = ["carceropolis/dados/dados.html"]
    context = {}

    return TemplateResponse(request, templates, context)


def dados_gerais(request):
    """Display the Dados Home page, which is a matrix with all available
    categories (only categories, not the items from the Publicação Class).
    """
    templates = ["carceropolis/dados/dados_gerais.html"]
    context = {}
    graficos = []

    data_files = {
        '01': 'carceropolis/static/data/dados_gerais/01.csv',
        '02': 'carceropolis/static/data/dados_gerais/02.csv',
        '03': 'carceropolis/static/data/dados_gerais/03.csv',
        '04': 'carceropolis/static/data/dados_gerais/04.csv'
    }

    for item, url in data_files.items():
        content = {}
        with open(url, 'r') as fo:
            content['data_file_url'] = url.split('/static/')[-1]
            content['titulo'] = fo.readline().split(',')[1].lstrip('"').rstrip('"')
            content['unidade'] = fo.readline().split(',')[1].lstrip('"').rstrip('"')
            content['fonte'] = fo.readline().split(',')[1].lstrip('"').rstrip('"')
            content['fonte_url'] = fo.readline().split(',')[1].lstrip('"').rstrip('"')
            notas = fo.readline().split(',')[1].lstrip('"').rstrip('"')
            content['notas'] = notas.split(';') if notas else None
            next(fo)  # Pula uma linha em branco
            data = pd.read_csv(fo, decimal=",", quotechar='"')

        if item == '01':
            data['Data'] = pd.to_datetime(data['Data'], format='%m/%Y')
            trace1 = go.Scatter(x=data['Data'], y=data['População'],
                                mode='lines',
                                line={'color': "#ea702e"})
            graf_data = go.Data([trace1])
            layout = go.Layout(title=content['titulo'],
                               yaxis={'rangemode': 'tozero'},
                               xaxis={
                                   'tickangle': -45,
                                   'dtick': "M6",
                                   'tick0': min(data['Data']),
                                   'tickformat': '%b-%y',
                                   'range': [min(data['Data']) - pd.DateOffset(months=1),
                                             max(data['Data'])]
                               })
        elif item == '02':
            # data['Ano'] = pd.to_datetime(data['Ano'], format='%Y')
            trace1 = go.Scatter(x=data['Ano'], y=data['EUA'], mode='lines',
                                name='EUA', connectgaps=True)
            trace2 = go.Scatter(x=data['Ano'], y=data['China'], mode='lines',
                                name='China', connectgaps=True)
            trace3 = go.Scatter(x=data['Ano'], y=data['Rússia'], mode='lines',
                                name='Rússia', connectgaps=True)
            trace4 = go.Scatter(x=data['Ano'], y=data['Brasil'], mode='lines',
                                name='Brasil', connectgaps=True)
            trace5 = go.Scatter(x=data['Ano'], y=data['ONU'], mode='lines',
                                name='ONU', connectgaps=True)
            graf_data = go.Data([trace1, trace2, trace3, trace4, trace5])
            layout = go.Layout(title=content['titulo'],
                               yaxis={'rangemode': 'tozero'},
                               xaxis={
                                   'tickangle': -45,
                                   'dtick': 1,
                                   'tick0': min(data['Ano']),
                                   'range': [min(data['Ano']),
                                             max(data['Ano'])]
                               })
        elif item == '03':
            dados_estados = data[(data['Estado'] != 'BR') &
                                 (data['Estado'] != 'ONU')]
            trace1 = go.Bar(x=dados_estados['População prisional'],
                            y=dados_estados['Estado'],
                            orientation='h',
                            marker={
                                'line':{
                                    'color': "#bb551d"
                                },
                                'color': '#ea702e'
                            })
            graf_data = go.Data([trace1])
            layout = go.Layout(title=content['titulo'],
                               xaxis={'rangemode': 'tozero'},
                               height=600)
        elif item == '04':
            dados_estados = data[(data['Estado'] != 'BR') &
                                 (data['Estado'] != 'ONU')]
            trace1 = go.Bar(x=dados_estados['Taxa de encarceramento'],
                            y=dados_estados['Estado'],
                            orientation='h',
                            marker={
                                'line':{
                                    'color': "#bb551d"
                                },
                                'color': '#ea702e'
                            })
            graf_data = go.Data([trace1])
            layout = go.Layout(title=content['titulo'],
                               xaxis={'rangemode': 'tozero'},
                               height=600)

        content['dados'] = data
        figure = go.Figure(data=graf_data, layout=layout)

        div = opy.plot(figure, auto_open=False, output_type='div',
                       include_plotlyjs=False)
        content['graph'] = div
        content['data'] = _json.dumps(figure.get('data', []),
                                      cls=utils.PlotlyJSONEncoder)
        content['layout'] = _json.dumps(figure.get('layout', {}),
                                        cls=utils.PlotlyJSONEncoder)
        graficos.append(content)

    context['graficos'] = graficos

    return TemplateResponse(request, templates, context)


def _fileId_from_url(url):
    """Return fileId from a url."""
    index = url.find('~')
    fileId = url[index + 1:]
    # local_id_index = fileId.find('/')

    share_key_index = fileId.find('?share_key')
    if share_key_index == -1:
        return fileId.replace('/', ':')
    else:
        return fileId[:share_key_index].replace('/', ':')


def dados_perfil_populacional(request):
    """First test"""
    templates = [u'carceropolis/dados/perfil_populacional.html']
    context = {}

    return TemplateResponse(request, templates, context)


def dados_educacao(request):
    """Second test"""
    templates = [u'carceropolis/dados/educacao.html']
    context = {}

    return TemplateResponse(request, templates, context)


def dados_piramide_etaria(request):
    """Third test"""
    templates = [u'carceropolis/dados/piramide_etaria.html']
    context = {}

    return TemplateResponse(request, templates, context)


def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
        else:
            error(request, "Usuário e/ou senha inválidos.")
    return redirect(next_url(request) or request.META['HTTP_REFERER'])


def register_user(request):
    print("registrando um novo usuário")
    profile_form = get_profile_form()
    form = profile_form(request.POST or None, request.FILES or None)
    print(form)
    print(dir(form))
    print(form.is_valid())
    if request.method == "POST" and form.is_valid():
        print("Método post e form válido")
        new_user = form.save()
        if not new_user.is_active:
            if settings.ACCOUNTS_APPROVAL_REQUIRED:
                print('Usuário cadastrado, aguardando aprovação')
                send_approve_mail(request, new_user)
                info(request, "Obrigado por se cadastrar! Você receberá um "
                              "email quando sua conta for ativada.")
            else:
                print('Usuário cadastrado, aguardando confirmação')
                send_verification_mail(request, new_user, "signup_verify")
                info(request, "Um email de verificação foi enviado com um "
                              "link para ativação de sua conta.")
            return redirect(next_url(request) or "/")
        else:
            print('usuário cadastrado com sucesso')
            info(request, "Cadastro realizado com sucesso")
            login(request, new_user)
            return login_redirect(request)
    else:
        error(request, form)
        return redirect(request.META['HTTP_REFERER']+"#cadastro", kwargs={'registration_form': form})
    return redirect(next_url(request) or request.META['HTTP_REFERER'])


def password_recovery(request):
    # TODO
    pass
