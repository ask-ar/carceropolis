# coding: utf-8
import json
import base64
import logging
import operator
from functools import reduce
from unidecode import unidecode
from collections import defaultdict

from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.messages import info, error
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from mezzanine.accounts import get_profile_form
from mezzanine.conf import settings
from mezzanine.generic.models import Keyword
from mezzanine.utils.email import send_verification_mail, send_approve_mail
from mezzanine.utils.views import paginate
from mezzanine.utils.urls import login_redirect, next_url
from bokeh.embed import server_document

from .models import (AreaDeAtuacao, Especialista, Publicacao,
                     UnidadePrisional)
from carceropolis.charts.utils import (
    plot_charts, plot_simple_lines, plot_simple_hbar_helper, plot_simple_vbar_helper)

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


def especialistas_list(request, extra_context=None, **kwargs):
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

    def build_filter_keywords(tipo):
        item = kwargs.get(tipo, None)
        outputs = set([unidecode(item).lower()]) if item else set()

        if tipo in request.GET.keys():
            items = request.GET.get(tipo)
            # Remove accents
            items = unidecode(items)
            # To Lowercase
            items = items.lower()
            # Remove leading and trailing spaces
            items = items.strip()
            # Replace '-' with spaces
            items = items.replace('-', ' ').replace(',',' ').replace(';', ' ')
            # Split on spaces into multiple items
            items = items.split(' ')
            # Update outputs set.
            outputs.update(items)

        if outputs:
            stop_words = ["", " ", "de"]
            _ = [outputs.discard(word) for word in stop_words]
            print(".",outputs,".")
            return outputs
        return []

    nomes = build_filter_keywords('nome')
    areas = build_filter_keywords('area_atuacao')
    especialidades = build_filter_keywords('especialidade')

    for nome in nomes:
        especialistas = especialistas.filter(
            nome__unaccent__icontains=nome)

    for area in areas:
        especialistas = especialistas.filter(
            area_de_atuacao__nome__unaccent__icontains=area)

    for especialidade in especialidades:
        especialistas = especialistas.filter(
            especialidades__nome__unaccent__icontains=especialidade)

    if nomes:
        context['nome'] = ' '.join(sorted(list(nomes)))

    if areas:
        context['area_atuacao'] = request.GET.get('area_atuacao')

    if especialidades:
        context['especialidade'] = ' '.join(sorted(list(especialidades)))

    prefetch = ("area_de_atuacao", 'especialidades')
    especialistas = especialistas.distinct()
    especialistas = especialistas.prefetch_related(*prefetch)
    especialistas = paginate(especialistas, request.GET.get("page", 1),
                             settings.PUBLICACAO_PER_PAGE,
                             settings.MAX_PAGING_LINKS)

    if not especialistas:
        especialistas = Especialista.objects.all()
        context['nome'] = ''
        context['area_atuacao'] = ''
        context['especialidade'] = ''
        context['error_message'] = ('Nenhum(a) especialista encontrado(a) com '
                                    'os parâmetros passados.')

    context['especialistas'] = especialistas

    templates = ['carceropolis/especialistas/especialistas.html']

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


def dados_home(request):
    """Display the Dados Home page, which is a matrix with all available
    categories (only categories, not the items from the Publicação Class).
    """
    templates = ["carceropolis/dados/dados.html"]
    context = {}

    return TemplateResponse(request, templates, context)


def dados_gerais(request):
    """Display the Dados Home page.

    It is a matrix with all available categories (only categories, not the
    items from the Publicação Class).
    """
    templates = ["carceropolis/dados/dados_gerais.html"]
    context = plot_charts('dados_gerais', [
        (plot_simple_lines, '01', {'continuous': True}),
        (plot_simple_lines, '02'),
        (plot_simple_hbar_helper, '03'),
        (plot_simple_hbar_helper, '04'),
    ])
    return TemplateResponse(request, templates, context)


def dados_perfil_populacional(request):
    """Perfil Populacional page"""
    templates = ['carceropolis/dados/perfil_populacional.html']
    context = plot_charts('perfil_populacional', [
        (plot_simple_lines, '01'),
        (plot_simple_lines, '02'),
        (plot_simple_vbar_helper, '03_raca_cor'),
        (plot_simple_vbar_helper, '04_faixa_etaria'),
    ])
    return TemplateResponse(request, templates, context)


def dados_infraestrutura(request):
    templates = [u'carceropolis/dados/infraestrutura.html']
    context = plot_charts('infraestrutura', [
        (plot_simple_hbar_helper, '01_ocupacao'),
        (plot_simple_hbar_helper, '02_deficit_vagas'),
        (plot_simple_hbar_helper, '03_coeficiente_entradas_saidas'),
    ])
    return TemplateResponse(request, templates, context)


def dados_juridico(request):
    templates = [u'carceropolis/dados/juridico.html']
    context = plot_charts([
        # TODO: faltam 2 gráficos
    ])
    return TemplateResponse(request, templates, context)


def dados_educacao(request):
    """Second test"""
    # TODO: Produto1 não tem texto de intro!
    templates = [u'carceropolis/dados/educacao.html']
    context = plot_charts([
        # TODO: faltam 3 gráficos
    ])
    return TemplateResponse(request, templates, context)


def dados_saude(request):
    # TODO: Produto1 não tem texto de intro!
    templates = [u'carceropolis/dados/saude.html']
    context = plot_charts([
        # TODO: faltam 2 gráficos
    ])
    return TemplateResponse(request, templates, context)


def dados_materno_infantil(request):
    # TODO: Produto1 não tem texto de intro!
    templates = [u'carceropolis/dados/materno_infantil.html']
    context = plot_charts([
        # TODO: faltam 2 gráficos
    ])
    return TemplateResponse(request, templates, context)


def dados_alas_exclusivas(request):
    # TODO: Produto1 não tem texto de intro!
    templates = [u'carceropolis/dados/alas_exclusivas.html']
    context = plot_charts([
        # TODO: faltam 4 gráficos
    ])
    return TemplateResponse(request, templates, context)


def dados_piramide_etaria(request):
    """Third test"""
    templates = [u'carceropolis/dados/piramide_etaria.html']
    context = {}

    return TemplateResponse(request, templates, context)


def unidades_map(request):
    """Display the Unidades Prisionais Map."""
    templates = ["carceropolis/unidades/mapa.html"]

    # Fields included in JSON sent to client
    fields = [
        f.name
        for f in UnidadePrisional._meta.get_fields()
        if f not in ['id', 'response']]
    fields.append('municipio__nome')

    # JSON with unidades grouped by uf
    states = defaultdict(list)
    for unidade in UnidadePrisional.objects.exclude(lat=None).values(*fields):
        unidade['municipio'] = unidade.pop('municipio__nome')

        # TODO: ---------- fake data ----------
        unidade.update({
            'tipo_gestao': 'Organização sem fins lucrativos',
            'visitacao': 'Domingos, 8h30-16h30',
            'indices': {
                'educacao': 9.5, 'trabalho': 2.5,
                'saude': 6.5, 'juridico': True},
            'pop_total': 1000,
            'vagas': 1000,
            'qualidade_info': 5.5,
            'pop_perc': {
                'provisoria': 20,
                'origem': [
                    {'label': 'brasileiros', 'value': 65},
                    {'label': 'naturalizados', 'value': 25},
                    {'label': 'estrangeiros', 'value': 10},
                ],
                'cor': [
                    {'label': 'preta', 'value': 45, 'color': 'rgb(11,102,176)'},
                    {'label': 'parda', 'value': 20, 'color': 'rgb(255,108,1)'},
                    {'label': 'branca', 'value': 10, 'color': 'rgb(2,161,19)'},
                    {'label': 'indígena', 'value': 5, 'color': 'rgb(228,0,121)'},
                    {'label': 'amarela', 'value': 5, 'color': 'rgb(150,73,185)'},
                    {'label': 'outros', 'value': 5, 'color': 'rgb(0,0,0)'},
                ],
            },
            'pyramid': {
                'ages': [
                    {'range': '+ de 70', 'male': 2, 'female': 1},
                    {'range': '61 a 70', 'male': 4, 'female': 2},
                    {'range': '46 a 60', 'male': 3, 'female': 1},
                    {'range': '35 a 45', 'male': 8, 'female': 2},
                    {'range': '30 a 34', 'male': 13, 'female': 7},
                    {'range': '25 a 29', 'male': 33, 'female': 10},
                    {'range': '18 a 24', 'male': 43, 'female': 11},
                ],
                'total': {
                    'perc': {'male': 75.52, 'female': 23.72},
                    'abs': {'male': 1006, 'female': 316},
                },
                'idade_media': 40
            }
        })
        # TODO: ---------- --------- ----------

        states[unidade['uf']].append(unidade)
    context = {
        'states': mark_safe(json.dumps(states))
    }

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


def data_dashboard(request, template="dashboard/dashboard.html"):
    """Data bokeh dashboard."""
    HOST = request.get_host().split(':' + str(request.get_port()))[0]
    if request.is_secure():
        PROTOCOL = 'https://'
    else:
        PROTOCOL = 'http://'
    script = server_document(url=PROTOCOL + HOST + ':5006/bkapp')
    if request.GET.urlencode():
        state = base64.urlsafe_b64encode(
            request.GET.urlencode().encode()).decode('utf8')
        mark = 'bokeh-absolute-url'
        insert = 'state=' + state + '&' + mark
        script = script.replace(mark, insert)
    context = {"script": script}
    # context = {"script": ' '.join(
    #     script.splitlines()).replace('/script', 'end-script')}
    templates = [template]

    return TemplateResponse(request, templates, context)
