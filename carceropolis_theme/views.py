# coding=utf8
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Publicacao

def publicacoes(request):
    publicacoes = Publicacao.objects.all()
    template = loader.get_template('carceropolis_theme/templates/publicacoes.html')
    context = {'publicacoes': publicacoes}
    return HttpResponse(template.render(context, request))
