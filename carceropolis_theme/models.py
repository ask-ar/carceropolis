# coding= utf-8
"""Modelos definidos para o Projeto carcerópolis."""
from django.db import models
from mezzanine.blog.models import BlogPost
from phonenumber_field.modelfields import PhoneNumberField


CATEGORIAS = (
    ('GERAL', 'GERAL'),
    ('SISTEMA', 'FUNCIONAMENTO DO SISTEMA'),
    ('PERFIL', 'PERFIL POPULACIONAL'),
    ('POLITICA', 'POLITICA CRIMINAL'),
    ('INTERNACIONAL', 'SISTEMAS INTERNACIONAIS'),
    ('VIOLENCIA', 'VIOLENCIA INSTITUCIONAL')
)


class AreaDeAtuacao(models.Model):
    """Categorias Gerais de classificação de Especialistas e Publicações."""
    nome_da_area = models.CharField(max_length=250)
    descricao = models.TextField()

    def __unicode__(self):
        return self.nome_da_area


class Especialidade(models.Model):
    """Definição das Especialidades principais mapeadas no projeto."""
    nome_da_especialidade = models.CharField(max_length=35)
    descricao = models.TextField(blank=True)
    # slug = models.CharField(max_length=250)

    def __unicode__(self):
        return self.nome_da_especialidade


class Especialista(models.Model):
    """Classe que define os especialistas para o 'Banco de Especialistas'."""
    nome = models.CharField(max_length=250)
    email = models.EmailField()
    telefone = PhoneNumberField(blank=True)
    mini_bio = models.CharField(max_length=250, blank=True)
    instituicao = models.CharField(max_length=250)
    area_de_atuacao = models.ManyToManyField(AreaDeAtuacao)
    especialidades = models.ManyToManyField(Especialidade)

    def __unicode__(self):
        return self.nome


class Publicacao(BlogPost):
    """Publicações relacionadas à temática do site."""
    categorias = models.ManyToManyField(AreaDeAtuacao)
