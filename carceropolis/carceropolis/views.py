"""Carcerópolis views functions."""
import json
import base64
import logging
import operator
from functools import reduce
from unidecode import unidecode

from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.messages import info, error
from django.db.models import F, Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from mezzanine.accounts import get_profile_form
from mezzanine.conf import settings
from mezzanine.generic.models import Keyword
from mezzanine.utils.email import send_verification_mail, send_approve_mail
from mezzanine.utils.views import paginate
from mezzanine.utils.urls import login_redirect, next_url
from bokeh.embed import server_document

from .models import (AreaDeAtuacao, Especialista, Publicacao, Especialidade,
                     UnidadePrisional, DadosEncarceramento)

User = get_user_model()
log = logging.getLogger(__name__)

# def setlanguage(request):
#     return render(request, 'set-language.html',
#         {'LANGUAGES':settings.LANGUAGES,
#         'SELECTEDLANG':request.LANGUAGE_CODE})


###############################################################################
# PUBLICACOES
###############################################################################

def publicacao_home(request):
    """Display the Publicações Home page.

    It is a matrix with all available categories (only categories, not the
    items from the Publicação Class).
    """
    categorias = AreaDeAtuacao.objects.all()
    categorias = categorias.order_by('ordem')
    data = []
    for categoria in categorias:
        quantidade = Publicacao.objects.filter(categorias=categoria).count()
        data.append({'nome': categoria.nome,
                     'slug': categoria.slug,
                     'quantidade': quantidade})

    templates = ["carceropolis/publicacao/publicacao_home.html"]
    context = {'categorias': data}
    return TemplateResponse(request, templates, context)


def publicacao_list_tag(request, tag, extra_context=None):
    """Display a list of blog posts filtered by tag."""
    templates = []
    template = "carceropolis/publicacao/publicacao_list.html"
    tag = get_object_or_404(Keyword, slug=tag)
    prefetch = ("categorias", "keywords__keyword")
    publicacoes = Publicacao.objects.filter(
        keywords__keyword=tag
    ).prefetch_related(
        *prefetch
    ).published()

    publicacoes = paginate(publicacoes, request.GET.get("page", 1),
                           settings.PUBLICACAO_PER_PAGE,
                           settings.MAX_PAGING_LINKS)
    context = {"publicacoes": publicacoes, "tag": tag, }
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

    filtros = {
        "categorias": categoria
    }

    ano = request.GET.get('ano', None)
    if ano:
        log.debug('    filtering ano: %s', ano)
        filtros["ano_de_publicacao"] = ano

    autoria = request.GET.get('autoria', None)
    if autoria:
        log.debug('    filtering autoria: %s', autoria)
        filtros["autoria__icontains"] = autoria

    tags = request.GET.get('tag', None)
    if tags:
        log.debug('    filtering tags: %s', tags)
        regex = r'(' + '|'.join(tags.split()) + ')'
        filtros["keywords__keyword__title__iregex"] = regex

    publicacoes = Publicacao.objects.filter(**filtros)

    search = request.GET.get('q', None)
    if search is not None and search:
        terms = search.split()
        log.debug('    general filtering: %s', terms)

        publicacoes = publicacoes.filter(
            reduce(operator.and_,
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

###############################################################################
# ESPECIALISTAS
###############################################################################


def especialistas_list(request, extra_context=None, **kwargs):
    """Display a list of Especialistas."""
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
            items = items.replace('-', ' ').replace(',', ' ').replace(';', ' ')
            # Split on spaces into multiple items
            items = items.split(' ')
            # Update outputs set.
            outputs.update(items)

        if outputs:
            stop_words = ["", " ", "de"]
            [outputs.discard(word) for word in stop_words]
            log.debug(f".{outputs}.")
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
    context['nome_especialistas'] = Especialista.objects.values_list('nome',
                                                                     flat=True)
    context['especialidades'] = especialistas = Especialidade.objects.all()

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
    """Display the Dados Home page."""
    templates = ["carceropolis/dados/dados.html"]
    context = {}

    return TemplateResponse(request, templates, context)


def unidades_map(request):
    """Display the Unidades Prisionais Map."""
    templates = ["carceropolis/unidades/mapa.html"]

    fields = {
        "unidade__id_unidade": "id_unidade",
        "unidade__nome_unidade": "nome_unidade",
        "unidade__tipo_logradouro": "tipo_logradouro",
        "unidade__nome_logradouro": "nome_logradouro",
        "unidade__numero": "numero",
        "unidade__complemento": "complemento",
        "unidade__cep": "cep",
        "unidade__municipio__nome": "municipio",
        "unidade__uf": "uf",
        "unidade__lat": "lat",
        "unidade__lon": "lon",
        "unidade__email": "email",
        "unidade__telefone": "telefone",
        "unidade__ddd": "ddd",
        "unidade__visitacao": "visitacao",
    }

    registros = DadosEncarceramento.objects.filter(
        ano=2016
    ).exclude(
        unidade__lat=None
    ).only(
        "unidade"
    ).select_related(
        "unidade",
        "unidade__municipio"
    ).annotate(
        **{v: F(k) for k, v in fields.items()}
    ).values(
        *list(fields.values())
    )
    context = {"unidades": mark_safe(json.dumps(list(registros)))}
    return TemplateResponse(request, templates, context)


def card_unidade(request, id_unidade, ano=2016, mes=6):
    """Return a JSON with the data for an 'Unidade' Card."""
    try:
        unidade = UnidadePrisional.objects.get(id_unidade=id_unidade)
    except UnidadePrisional.DoesNotExist:
        raise Http404(f"Unidade com id {id_unidade} não encontrada")
    try:
        registro = DadosEncarceramento.objects.get(
            ano=ano,
            mes=mes,
            unidade=unidade
        )
    except DadosEncarceramento.DoesNotExist:
        raise Http404((f"Não existem dados para a unidade {unidade.nome} "
                       f"em {ano}/{mes}"))

    return HttpResponse(json.dumps(registro.card),
                        content_type='application/json')


def login_user(request):
    # TODO
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
            return redirect(request.META['HTTP_REFERER']+"#cadastro",
                            kwargs={'registration_form': ''})
    return redirect(next_url(request) or request.META['HTTP_REFERER'])


def register_user(request):
    log.debug("registrando um novo usuário")
    profile_form = get_profile_form()
    form = profile_form(request.POST or None, request.FILES or None)
    log.debug(form)
    log.debug(dir(form))
    log.debug(form.is_valid())
    if request.method == "POST" and form.is_valid():
        log.debug("Método post e form válido")
        new_user = form.save()
        if not new_user.is_active:
            if settings.ACCOUNTS_APPROVAL_REQUIRED:
                log.debug('Usuário cadastrado, aguardando aprovação')
                send_approve_mail(request, new_user)
                info(request, "Obrigado por se cadastrar! Você receberá um "
                              "email quando sua conta for ativada.")
            else:
                log.debug('Usuário cadastrado, aguardando confirmação')
                send_verification_mail(request, new_user, "signup_verify")
                info(request, "Um email de verificação foi enviado com um "
                              "link para ativação de sua conta.")
            return redirect(next_url(request) or "/")
        else:
            log.debug('usuário cadastrado com sucesso')
            info(request, "Cadastro realizado com sucesso")
            login(request, new_user)
            return login_redirect(request)
    else:
        error(request, form)
        return redirect(request.META['HTTP_REFERER']+"#cadastro",
                        kwargs={'registration_form': form})
    return redirect(next_url(request) or request.META['HTTP_REFERER'])


def password_recovery(request):
    # TODO
    pass


def data_dashboard(request, template="dashboard/dashboard.html"):
    """Return Data for bokeh dashboard."""
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
