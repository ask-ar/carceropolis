# coding= utf-8
"""Modelos definidos para o Projeto carcerópolis."""
from datetime import datetime
from cidades.models import Cidade, STATE_CHOICES
from django.db import models
from mezzanine.blog.models import BlogPost
from phonenumber_field.modelfields import PhoneNumberField
from autoslug import AutoSlugField


CATEGORIAS = (
    ('SISTEMA', 'FUNCIONAMENTO DO SISTEMA'),
    ('PERFIL', 'PERFIL POPULACIONAL'),
    (u'POLÍTICA', u'POLÍTICA CRIMINAL'),
    ('INTERNACIONAL', 'SISTEMAS INTERNACIONAIS'),
    (u'VIOLÊNCIA', u'VIOLÊNCIA INSTITUCIONAL'),
    ('OUTROS', 'OUTROS'),
)


YEAR_CHOICES = [(r, r) for r in range(1900, datetime.now().year+1)]

def current_year():
    return datetime.now().year


class AreaDeAtuacao(models.Model):
    """Categorias Gerais de classificação de Especialistas e Publicações."""
    nome = models.CharField(max_length=250, unique=True,
                            verbose_name='Nome da área')
    descricao = models.TextField(verbose_name='Descrição')
    ordem = models.IntegerField(unique=True, verbose_name='Ordem')
    slug = AutoSlugField(populate_from='nome', always_update=True)

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = 'Área de Atuação'
        verbose_name_plural = 'Áreas de Atuação'


class Especialidade(models.Model):
    """Definição das Especialidades principais mapeadas no projeto."""
    nome = models.CharField(max_length=80, unique=True,
                            verbose_name='Nome da especialidade')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    slug = AutoSlugField(populate_from='nome',
                         always_update=True)

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = 'Especialidade'
        verbose_name_plural = 'Especialidades'


class Especialista(models.Model):
    """Classe que define os especialistas para o 'Banco de Especialistas'."""
    nome = models.CharField(max_length=250)
    email = models.EmailField()
    telefone = PhoneNumberField(blank=True)
    mini_bio = models.CharField(max_length=250, blank=True)
    instituicao = models.CharField(max_length=250,
                                   verbose_name='Instituição')
    area_de_atuacao = models.ManyToManyField(AreaDeAtuacao,
                                             verbose_name='Área de atuação')
    especialidades = models.ManyToManyField(Especialidade)

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = 'Especialista'
        verbose_name_plural = 'Especialistas'


class Publicacao(BlogPost):
    """Publicações relacionadas à temática do site."""
    autoria = models.CharField(max_length=150,
                               verbose_name='Autoria')
    categorias = models.ManyToManyField(AreaDeAtuacao,
                                        verbose_name='Categorias')
    data_de_publicacao = models.IntegerField(verbose_name='Data de publicacão',
                                             choices=YEAR_CHOICES,
                                             default=current_year)
    arquivo_publicacao = models.FileField(upload_to='publicacoes/',
                                          verbose_name='Arquivo da publicação')

    class Meta:
        verbose_name = 'Publicação'
        verbose_name_plural = 'Publicações'


Publicacao._meta.get_field('title').verbose_name = 'Título'
Publicacao._meta.get_field('publish_date').verbose_name = 'Publicado em'
Publicacao._meta.get_field('content').verbose_name = 'Descrição'
Publicacao._meta.get_field('keywords').verbose_name = 'Tags'
Publicacao._meta.get_field('related_posts').verbose_name = 'Posts Relacionados'
Publicacao._meta.get_field('_meta_title').verbose_name = 'Tílulo'
Publicacao._meta.get_field('description').verbose_name = 'Descrição curta'
Publicacao._meta.get_field('gen_description').verbose_name = 'Gerar descrição'
Publicacao._meta.get_field('allow_comments').default = False


class UnidadePrisional(models.Model):
    """Unidades Prisionais."""
    nome_unidade = models.CharField(max_length=255)
    sigla_unidade = models.CharField(max_length=10)
    tipo_logradouro = models.CharField(max_length=15)
    nome_logradouro = models.CharField(max_length=255)
    numero = models.IntegerField(blank=True, verbose_name='Número')
    complemento = models.CharField(max_length=255, blank=True)
    bairro = models.CharField(max_length=255)
    municipio = models.ForeignKey(Cidade, verbose_name='Município')
    uf = models.CharField(max_length=2, choices=STATE_CHOICES)
    cep = models.CharField(max_length=8)
    ddd = models.IntegerField()
    telefone = models.IntegerField()
    email = models.EmailField()

    class Meta:
        verbose_name = 'Unidade Prisional'
        verbose_name_plural = 'Unidades Prisionais'

