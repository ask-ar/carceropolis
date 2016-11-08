from __future__ import unicode_literals
from future.builtins import str
from future.builtins import int
from calendar import month_name

from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from .models import Publicacao, AreaDeAtuacao, Especialidade, Especialista
from mezzanine.conf import settings
from mezzanine.utils.views import paginate
# from mezzanine.utils.views import render

User = get_user_model()


# def setlanguage(request):
    # return render(request, 'set-language.html',
                  # {'LANGUAGES':settings.LANGUAGES,
                   # 'SELECTEDLANG':request.LANGUAGE_CODE})


def publicacao_list(request, tag=None, year=None, month=None, username=None,
                    categoria=None, template="carceropolis/publicacao/publicacao_list.html",
                    extra_context=None):
    """
    Display a list of blog posts that are filtered by tag, year, month,
    author or categoria. Custom templates are checked for using the name
    ``carceropolis/publicacao/publicacao_list_XXX.html`` where ``XXX`` is either the
    categoria slug or author's username if given.
    """
    templates = []
    publicacoes = Publicacao.objects.published()
    if tag is not None:
        tag = get_object_or_404(Keyword, slug=tag)
        publicacoes = publicacoes.filter(keywords__keyword=tag)
    if year is not None:
        publicacoes = publicacoes.filter(publish_date__year=year)
        if month is not None:
            publicacoes = publicacoes.filter(publish_date__month=month)
            try:
                month = month_name[int(month)]
            except IndexError:
                raise Http404()
    if categoria is not None:
        categoria = get_object_or_404(AreaDeAtuacao, slug=categoria)
        publicacoes = publicacoes.filter(categories=categoria)
        templates.append(u"carceropolis/publicacao/publicacao_list_%s.html" %
                         str(categoria.slug))
    author = None
    if username is not None:
        author = get_object_or_404(User, username=username)
        publicacoes = publicacoes.filter(user=author)
        templates.append(u"carceropolis/publicacao/publicacao_list_%s.html" %
                         username)

    prefetch = ("categorias", "keywords__keyword")
    publicacoes = publicacoes.select_related("user").prefetch_related(*prefetch)
    publicacoes = paginate(publicacoes, request.GET.get("page", 1),
                           settings.PUBLICACAO_PER_PAGE,
                           settings.MAX_PAGING_LINKS)
    context = {"publicacoes": publicacoes, "year": year, "month": month,
               "tag": tag, "categoria": categoria, "author": author,
               'teste': Publicacao.objects.all()}
    context.update(extra_context or {})
    templates.append(template)
    return TemplateResponse(request, templates, context)


def publicacao_detail(request, slug, year=None, month=None, day=None,
                     template="carceropolis/publicacao/publicacao_detail.html",
                     extra_context=None):
    """. Custom templates are checked for using the name
    ``carceropolis/publicacao/publicacao_detail_XXX.html`` where ``XXX`` is the blog
    posts's slug.
    """
    publicacoes = Publicacao.objects.published(
                                     for_user=request.user).select_related()
    publicacao = get_object_or_404(publicacoes, slug=slug)
    related_posts = publicacao.related_posts.published(for_user=request.user)
    context = {"publicacao": publicacao, "editable_obj": publicacao,
               "related_posts": related_posts}
    context.update(extra_context or {})
    templates = [u"carceropolis/publicacao/publicacao_detail_%s.html" % str(slug), template]
    return TemplateResponse(request, templates, context)


def publicacao_feed(request, format, **kwargs):
    """
    Blog posts feeds - maps format to the correct feed view.
    """
    try:
        return {"rss": PostsRSS, "atom": PostsAtom}[format](**kwargs)(request)
    except KeyError:
        raise Http404()


def especialistas_list(request, area_de_atuacao=None, especialidade=None):
    """Display a list of blog posts that are filtered by tag, year, month,
    author or categoria. Custom templates are checked for using the name
    ``carceropolis/publicacao/publicacao_list_XXX.html`` where ``XXX`` is
    either the categoria slug or author's username if given.
    """
    templates = []
    context = {}
    especialistas = Especialista.objects.all()
    if area_de_atuacao is not None:
        area_de_atuacao = get_object_or_404(AreaDeAtuacao, slug=area_de_atuacao)
        especialistas = especialistas.filter(area_de_atuacao=area_de_atuacao)
        templates.append(u"carceropolis/especialistas/area_atuacao.html")
        context['area_de_atuacao'] = area_de_atuacao
    if especialidade is not None:
        especialidade = get_object_or_404(Especialidade, slug=especialidade)
        especialistas = especialistas.filter(especialidade=especialidade)
        templates.append(u"carceropolis/especialistas/especialidade.html")
        context['especialidade'] = especialidade

    prefetch = ("area_de_atuacao", 'especialidades')
    especialistas = especialistas.prefetch_related(*prefetch)
    especialistas = paginate(especialistas, request.GET.get("page", 1),
                           settings.PUBLICACAO_PER_PAGE,
                           settings.MAX_PAGING_LINKS)
    context = {"especialistas": especialistas}
    templates.append(u'carceropolis/especialistas/especialistas.html')
    return TemplateResponse(request, templates, context)
