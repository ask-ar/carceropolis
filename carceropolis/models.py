"""Modelos definidos para o Projeto carcerópolis."""
import logging

from cidades.models import Cidade, STATE_CHOICES
from csv import DictReader, DictWriter
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from mezzanine.blog.models import BlogPost
from autoslug import AutoSlugField

from .options import current_month, current_year, MONTH_CHOICES, YEAR_CHOICES
from .validators import check_filetype

log = logging.getLogger(__name__)


class AreaDeAtuacao(models.Model):

    """Categorias Gerais de classificação de Especialistas e Publicações."""

    nome = models.CharField(max_length=250, unique=True,
                            verbose_name='Nome da área')
    descricao = models.TextField(verbose_name='Descrição')
    ordem = models.IntegerField(unique=True, verbose_name='Ordem')
    slug = AutoSlugField(populate_from='nome', always_update=True)

    def __str__(self):
        """String representation of an instance."""
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

    def __str__(self):
        """String representation of an instance."""
        return self.nome

    class Meta:
        verbose_name = 'Especialidade'
        verbose_name_plural = 'Especialidades'


class Especialista(models.Model):

    """Classe que define os especialistas para o 'Banco de Especialistas'."""

    nome = models.CharField(max_length=250)
    email = models.EmailField(blank=True)
    ddi = models.IntegerField(verbose_name='DDI', blank=True, null=True,
                              default=55)
    ddd = models.IntegerField(verbose_name='DDD', blank=True, null=True)
    telefone = models.IntegerField(verbose_name='Telefone', blank=True,
                                   null=True)
    mini_bio = models.CharField(max_length=600, blank=True)
    instituicao = models.CharField(max_length=250,
                                   verbose_name='Instituição')
    area_de_atuacao = models.ManyToManyField(AreaDeAtuacao,
                                             verbose_name='Área de atuação')
    especialidades = models.ManyToManyField(Especialidade)

    def __str__(self):
        """String representation of an instance."""
        return self.nome

    class Meta:
        verbose_name = 'Especialista'
        verbose_name_plural = 'Especialistas'


class Publicacao(BlogPost):

    """Publicações relacionadas à temática do site."""

    autoria = models.CharField(max_length=150, verbose_name='Autoria')
    categorias = models.ManyToManyField(AreaDeAtuacao,
                                        verbose_name='Categorias')
    ano_de_publicacao = models.IntegerField(verbose_name='Ano de publicação',
                                            choices=YEAR_CHOICES,
                                            default=current_year)
    arquivo_publicacao = models.FileField(upload_to='publicacoes/',
                                          verbose_name='Arquivo da publicação')

    class Meta:
        verbose_name = 'Publicação'
        verbose_name_plural = 'Publicações'

    def __str__(self):
        """String representation of an instance."""
        return self.title


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

    id_unidade = models.IntegerField()
    nome_unidade = models.CharField(max_length=255,
                                    verbose_name='Nome da Unidade')
    sigla_unidade = models.CharField(max_length=10)
    tipo_logradouro = models.CharField(max_length=20)
    nome_logradouro = models.CharField(max_length=255)
    numero = models.IntegerField(blank=True, null=True, verbose_name='Número')
    complemento = models.CharField(max_length=255, blank=True)
    bairro = models.CharField(max_length=255)
    municipio = models.ForeignKey(Cidade, verbose_name='Município')
    uf = models.CharField(max_length=2, choices=STATE_CHOICES)
    cep = models.CharField(max_length=8)
    ddd = models.IntegerField(verbose_name='DDD', null=True, blank=True)
    telefone = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    responsavel = models.CharField(blank=True, max_length=255,
                                   verbose_name='Responsável')
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = 'Unidade Prisional'
        verbose_name_plural = 'Unidades Prisionais'

    def __str__(self):
        """String representation of an instance."""
        return "%s (%s/%s)" % (self.nome_unidade, self.municipio, self.uf)

    @classmethod
    def _new_from_dict(cls, data):
        """Generate a new 'Unidade Prisional' and return it.

        The 'data' attribute is a dictionary with the necessary fields to
        generate a new Unidade Prisional.
        """
        unidade = UnidadePrisional()
        unidade.nome_unidade = data['nome_unidade']
        unidade.sigla_unidade = data['sigla_unidade']
        unidade.tipo_logradouro = data['tipo_logradouro']
        unidade.nome_logradouro = data['nome_logradouro']
        if isinstance(data['numero'], int):
            unidade.numero = data['numero']
        else:
            try:
                unidade.numero = int(data['numero'])
            except:
                unidade.numero = None
        unidade.complemento = data['complemento']
        unidade.bairro = data['bairro']
        unidade.municipio = Cidade.objects.get(nome=data['municipio'],
                                               estado=data['uf'])
        unidade.uf = data['uf']
        unidade.cep = data['cep']
        if isinstance(data['ddd'], int):
            unidade.ddd = data['ddd']
        else:
            try:
                unidade.ddd = int(data['ddd'])
            except:
                unidade.ddd = None
        if isinstance(data['telefone'], int):
            unidade.telefone = data['telefone']
        else:
            try:
                unidade.telefone = int(data['telefone'])
            except:
                unidade.telefone = None
        unidade.email = data['email']
        return unidade

    @classmethod
    def _export_to_csv(cls, path):
        ''' Export this class table to a CSV. '''
        fieldnames = [f.name for f in cls._meta.fields]
        with open(path, 'w') as csv_file:
            writer = DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            objects = cls.objects.all()
            for obj in objects:
                data = {field: getattr(obj, field, None)
                        for field in fieldnames}
                data['municipio'] = data['municipio'].nome
                writer.writerow(data)

    @classmethod
    def _import_from_csv(cls, path):
        """Populate the DB from CSV data.

        The 'path' attribute is the absolute path to the CSV file that must be
        inserted on the database.
        """
        atualizadas = []
        novas = []
        errors = []

        fieldnames = ['remove1', 'nome_unidade', 'sigla_unidade',
                      'tipo_logradouro', 'nome_logradouro', 'numero',
                      'complemento', 'bairro', 'municipio', 'uf', 'cep', 'ddd',
                      'telefone', 'email', 'remove2']
        with open(path, 'r') as csv_file:
            data = DictReader(csv_file, fieldnames=fieldnames)

            for row in data:
                if row['nome_unidade'] == 'nome_unidade':
                    row = data.next()

                del row['remove1']
                del row['remove2']

                try:
                    unidade = UnidadePrisional.objects.get(
                        nome_unidade=row['nome_unidade'],
                        municipio=Cidade.objects.get(nome=row['municipio'],
                                                     estado=row['uf']))
                    unidade._update_from_dict(row)
                    unidade.save()
                    atualizadas.append(unidade.nome_unidade)
                except ObjectDoesNotExist:
                    try:
                        unidade = UnidadePrisional._new_from_dict(row)
                        unidade.save()
                        novas.append(unidade.nome_unidade)
                    except Exception as e:
                        error = {'nome_unidade': row['nome_unidade'],
                                 'erro': str(e),
                                 'data': row}
                        errors.append(error)

        msg = 'Resumo da operação:\n'
        if atualizadas:
            msg += '    - '
            msg += '{} unidades foram atualizadas.\n'.format(len(atualizadas))
            log.info('    {}'.format(atualizadas))

        if novas:
            msg += '    - '
            msg += '{} unidades foram adicionadas.\n'.format(len(novas))

        if errors:
            msg += 'Ocorreram {} erros de importação:\n'.format(len(errors))
            for error in errors:
                msg += '    - '
                msg += 'Unidade: {:.30}'.format(error['nome_unidade'])
                msg += ' | {} | {}/{}\n'.format(error['erro'],
                                                error['data']['uf'],
                                                error['data']['municipio'])

        log.info(msg)

    def _update_from_dict(self, data):
        """Update a 'Unidade Prisional' based on its name and return it.

        The 'data' attribute is a dictionary with the necessary fields to
        generate a new Unidade Prisional.
        """
        self.sigla_unidade = data['sigla_unidade']
        self.tipo_logradouro = data['tipo_logradouro']
        self.nome_logradouro = data['nome_logradouro']
        if isinstance(data['numero'], int):
            self.numero = data['numero']
        else:
            try:
                self.numero = int(data['numero'])
            except:
                self.numero = None
        self.complemento = data['complemento']
        self.bairro = data['bairro']
        self.municipio = Cidade.objects.get(nome=data['municipio'],
                                            estado=data['uf'])
        self.uf = data['uf']
        self.cep = data['cep']
        if isinstance(data['ddd'], int):
            self.ddd = data['ddd']
        else:
            try:
                self.ddd = int(data['ddd'])
            except:
                self.ddd = None
        if isinstance(data['telefone'], int):
            self.telefone = data['telefone']
        else:
            try:
                self.telefone = int(data['telefone'])
            except:
                self.telefone = None
        self.email = data['email']


class BaseMJ(models.Model):

    """Manage the multiple versions of MJ Infopen raw database."""

    ano = models.IntegerField(choices=YEAR_CHOICES, default=current_year)
    mes = models.CharField(verbose_name='Mês', max_length=40,
                           choices=MONTH_CHOICES, default=current_month)
    arquivo = models.FileField(upload_to='base_bruta_mj/',
                               validators=[check_filetype])
    salvo_em = models.DateTimeField(verbose_name='Salvo em', auto_now_add=True)

    def __str__(self):
        """String representation of an instance."""
        return "{}/{}".format(self.mes, self.ano)

    class Meta:
        verbose_name = 'Base bruta MJ'
        verbose_name_plural = 'Bases brutas MJ'


class ArquivoBaseCarceropolis(models.Model):

    """Manage the multiple raw versions of the cleaned MJ/Infopen database."""

    ano = models.IntegerField(choices=YEAR_CHOICES, default=current_year)
    mes = models.CharField(verbose_name='Mês', max_length=40,
                           choices=MONTH_CHOICES, default=current_month)
    arquivo = models.FileField(upload_to='base_bruta_carceropolis/',
                               validators=[check_filetype])
    salvo_em = models.DateTimeField(verbose_name='Salvo em', auto_now_add=True)

    def __str__(self):
        """String representation of an instance."""
        return "{}/{}".format(self.mes, self.ano)

    class Meta:
        verbose_name = u'Base bruta Carcerópolis'
        verbose_name_plural = u'Bases brutas Carcerópolis'
