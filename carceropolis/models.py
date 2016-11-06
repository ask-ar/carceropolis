# coding= utf-8
"""Modelos definidos para o Projeto carcerópolis."""
from cidades.models import Cidade, STATE_CHOICES
from django.db import models
from mezzanine.blog.models import BlogPost
from phonenumber_field.modelfields import PhoneNumberField


CATEGORIAS = (
    ('SISTEMA', 'FUNCIONAMENTO DO SISTEMA'),
    ('PERFIL', 'PERFIL POPULACIONAL'),
    (u'POLÍTICA', u'POLÍTICA CRIMINAL'),
    ('INTERNACIONAL', 'SISTEMAS INTERNACIONAIS'),
    (u'VIOLÊNCIA', u'VIOLÊNCIA INSTITUCIONAL'),
    ('OUTROS', 'OUTROS'),
)

class AreaDeAtuacao(models.Model):
    """Categorias Gerais de classificação de Especialistas e Publicações."""
    nome_da_area = models.CharField(max_length=250, unique=True)
    descricao = models.TextField()
    ordem = models.IntegerField(unique=True)

    def __unicode__(self):
        return self.nome_da_area

    class Meta:
        verbose_name = 'Área de Atuação'
        verbose_name_plural = 'Áreas de Atuação'


class Especialidade(models.Model):
    """Definição das Especialidades principais mapeadas no projeto."""
    nome_da_especialidade = models.CharField(max_length=80, unique=True)
    descricao = models.TextField(blank=True)
    # slug = models.CharField(max_length=250)

    def __unicode__(self):
        return self.nome_da_especialidade

    class Meta:
        verbose_name = 'Especialidade'
        verbose_name_plural = 'Especialidades'


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

    class Meta:
        verbose_name = 'Especialista'
        verbose_name_plural = 'Especialistas'


class Publicacao(BlogPost):
    """Publicações relacionadas à temática do site."""
    autoria = models.CharField(max_length=150)
    categorias = models.ManyToManyField(AreaDeAtuacao)
    arquivo_publicacao = models.FileField('Arquivo da Publicação',
                                          upload_to='publicacoes/')

    class Meta:
        verbose_name = 'Publicação'
        verbose_name_plural = 'Publicações'


class UnidadePrisional(models.Model):
    """Unidades Prisionais."""
    nome_unidade = models.CharField(max_length=255)
    sigla_unidade = models.CharField(max_length=10)
    tipo_logradouro = models.CharField(max_length=15)
    nome_logradouro = models.CharField(max_length=255)
    numero = models.IntegerField(blank=True)
    complemento = models.CharField(max_length=255, blank=True)
    bairro = models.CharField(max_length=255)
    municipio = models.ForeignKey(Cidade)
    uf = models.CharField(max_length=2, choices=STATE_CHOICES)
    cep = models.CharField(max_length=8)
    ddd = models.IntegerField()
    telefone = models.IntegerField()
    email = models.EmailField()

    class Meta:
        verbose_name = 'Unidade Prisional'
        verbose_name_plural = 'Unidades Prisionais'

