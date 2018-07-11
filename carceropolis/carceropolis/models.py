"""Modelos definidos para o Projeto carcerópolis."""
import logging
import re

from django_extensions.db.fields import AutoSlugField
from cidades.models import Cidade, STATE_CHOICES
from csv import DictReader, DictWriter
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import pandas as pd
from mezzanine.blog.models import BlogPost

from .options import (
    current_month, current_year,
    MONTH_CHOICES, YEAR_CHOICES)
from .validators import check_filetype

log = logging.getLogger(__name__)


class AreaDeAtuacao(models.Model):

    """Categorias Gerais de classificação de Especialistas e Publicações."""

    nome = models.CharField(max_length=250, unique=True,
                            verbose_name='Nome da área')
    descricao = models.TextField(verbose_name='Descrição')
    ordem = models.IntegerField(unique=True, verbose_name='Ordem')
    slug = AutoSlugField(populate_from='nome')

    def __str__(self):
        """Return a string representation of an instance."""
        return self.nome

    class Meta:
        verbose_name = 'Área de Atuação'
        verbose_name_plural = 'Áreas de Atuação'


class Especialidade(models.Model):

    """Definição das Especialidades principais mapeadas no projeto."""

    nome = models.CharField(max_length=80, unique=True,
                            verbose_name='Nome da especialidade')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    slug = AutoSlugField(populate_from='nome')

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


# Publicacao._meta.get_field('title').verbose_name = 'Título'
# Publicacao._meta.get_field('publish_date').verbose_name = 'Publicado em'
# Publicacao._meta.get_field('content').verbose_name = 'Descrição'
# Publicacao._meta.get_field('keywords').verbose_name = 'Tags'
# Publicacao._meta.get_field('related_posts').verbose_name = 'Posts Relacionados'
# Publicacao._meta.get_field('_meta_title').verbose_name = 'Tílulo'
# Publicacao._meta.get_field('description').verbose_name = 'Descrição curta'
# Publicacao._meta.get_field('gen_description').verbose_name = 'Gerar descrição'
Publicacao._meta.get_field('allow_comments').default = False


class UnidadePrisional(models.Model):
    """Unidades Prisionais."""

    id_unidade = models.IntegerField(primary_key=True)
    nome_unidade = models.CharField(max_length=600,
                                    verbose_name='Nome da Unidade')
    sigla_unidade = models.CharField(max_length=600)
    tipo_logradouro = models.CharField(max_length=600)
    nome_logradouro = models.CharField(max_length=600)
    numero = models.IntegerField(blank=True, null=True, verbose_name='Número')
    complemento = models.CharField(max_length=600, blank=True)
    bairro = models.CharField(max_length=600)
    municipio = models.ForeignKey(Cidade, verbose_name='Município')
    uf = models.CharField(max_length=2, choices=STATE_CHOICES)
    cep = models.CharField(max_length=9)
    ddd = models.IntegerField(verbose_name='DDD', null=True, blank=True)
    telefone = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    responsavel = models.CharField(blank=True, max_length=600,
                                   verbose_name='Responsável')
    visitacao = models.TextField(blank=True, verbose_name='Visitação')
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = 'Unidade Prisional'
        verbose_name_plural = 'Unidades Prisionais'

    def __str__(self):
        """String representation of an instance."""
        return "%s (%s/%s)" % (self.nome_unidade, self.municipio, self.uf)

    @classmethod
    def _export_to_csv(cls, path):
        """Export this class table to a CSV."""
        fieldnames = [f.name for f in cls._meta.fields]
        with open(path, 'w') as csv_file:
            writer = DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            objects = cls.objects.all()
            for obj in objects:
                data = {field: getattr(obj, field, '')
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

        fieldnames = ['id_unidade', 'nome_unidade', 'sigla_unidade',
                      'tipo_logradouro', 'nome_logradouro', 'numero',
                      'complemento', 'bairro', 'municipio', 'uf', 'cep', 'ddd',
                      'telefone', 'email', 'responsavel', 'visitacao', 'lat',
                      'lon']
        with open(path, 'r') as csv_file:
            #  data = DictReader(csv_file, fieldnames=fieldnames)
            data = pd.read_csv(csv_file, sep=";", engine="python",
                               na_filter=False)

            data = data.to_dict("records")

            for row in data:
                nome_unidade = row.get('nome_unidade')
                if not nome_unidade or nome_unidade == 'nome_unidade':
                    continue

                try:
                    unidade = cls.objects.get(
                        id_unidade=row.get('id_unidade'),
                        municipio=Cidade.objects.get(nome=row.get('municipio'),
                                                     estado=row.get('uf')))
                    unidade = cls._update_from_dict(unidade, row)
                    unidade.save()
                    atualizadas.append(unidade.nome_unidade)
                except ObjectDoesNotExist:
                    try:
                        unidade = cls._new_from_dict(row)
                        unidade.save()
                        novas.append(unidade.nome_unidade)
                    except Exception as e:
                        error = {'nome_unidade': nome_unidade,
                                 'erro': str(e),
                                 'data': row}
                        errors.append(error)

        msg = 'Resumo da operação:\n'
        if atualizadas:
            msg += '    - '
            msg += f'{len(atualizadas)} unidades foram atualizadas.\n'

        if novas:
            msg += '    - '
            msg += f'{len(novas)} unidades foram adicionadas.\n'

        if errors:
            msg += f'Ocorreram {len(errors)} erros de importação:\n'
            for error in errors:
                msg += '    - '
                msg += f'Unidade: {error["nome_unidade"]:.30}'
                msg += f' | {error["erro"]} | {error["data"]["uf"]}/'
                msg += f'{error["data"]["municipio"]}\n'

        log.info(msg)
        print(msg)

    @classmethod
    def _new_from_dict(cls, data):
        """Generate a new 'Unidade Prisional' and return it.

        The 'data' attribute is a dictionary with the necessary fields to
        generate a new Unidade Prisional.
        """
        unidade = cls()

        return cls._update_from_dict(unidade, data)

    @staticmethod
    def _update_from_dict(unidade, data):
        """Update a 'Unidade Prisional' based on its name and return it.

        The 'data' attribute is a dictionary with the necessary fields to
        generate a new Unidade Prisional.
        """
        # Campos Obrigatórios
        unidade.id_unidade = int(data.get('id_unidade'))
        unidade.nome_unidade = data.get('nome_unidade').strip()
        unidade.sigla_unidade = data.get('sigla_unidade', "").strip()
        unidade.tipo_logradouro = data.get('tipo_logradouro', "").strip()
        unidade.nome_logradouro = data.get('nome_logradouro', "").strip()
        unidade.uf = data.get('uf').strip()
        unidade.municipio = Cidade.objects.get(nome=data.get('municipio'),
                                               estado=unidade.uf)
        cep = data.get('cep', "").strip()
        if re.match(r'\d{5}-\d{3}', cep):
            unidade.cep = cep
        elif re.match(r'\d{8}', cep):
            unidade.cep = str(cep)[:5] + "-" + str(cep)[5:]
        else:
            unidade.cep = ""
            # raise ValueError(f'Invalid CEP format {unidade.cep}.')

        # Campos opcionais
        unidade.complemento = data.get('complemento', '').strip()
        unidade.bairro = data.get('bairro', '').strip()
        unidade.email = data.get('email', '')
        unidade.responsavel = data.get('responsavel', '').strip()
        unidade.visitacao = data.get('visitacao', '').strip()
        try:
            unidade.lat = float(data.get('lat', '-15.7997067'))
            unidade.lon = float(data.get('lon', '-47.8663516'))
        except ValueError:
            pass

        try:
            unidade.numero = int(data.get('numero'))
        except (TypeError, ValueError, KeyError):
            pass

        try:
            ddd = data.get('ddd', 0)
            if isinstance(ddd, str):
                ddd = ddd.replace('(', '').replace(')', '').replace('-', '')
            ddd = int(ddd)
            if ddd < 10 or ddd >= 100:
                raise ValueError(f"Bad DDD value {ddd}")
            unidade.ddd = ddd
        except (ValueError, TypeError):
            pass

        try:
            telefone = data.get('telefone', None)
            if isinstance(telefone, str):
                telefone.replace('-', '').replace(' ', '')
            unidade.telefone = int(telefone)
        except (ValueError, TypeError):
            pass

        return unidade


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


class DadosEncarceramento(models.Model):
    """Contains all the historical prisional data for each UnidadePrisional."""

    ano = models.CharField(max_length=4)
    mes = models.CharField(max_length=2)
    unidade = models.ForeignKey(UnidadePrisional,
                                verbose_name='Unidade Prisional')
    dados = JSONField()
    card = JSONField()

    @classmethod
    def import_from_csv(cls, filepath):
        """Import data from CSV file."""
        dataset = None
        # data_dict = {2014: {6: {}, 12:{}}, 2015: {12: {}}, 2016: {6: {}}}

        dataset = pd.read_csv(filepath, sep=";", engine="python",
                              na_filter=False)

        dataset = dataset.to_dict("records")
        for data in dataset:
            cls.create_or_update_from_dict(data)

    @classmethod
    def create_or_update_from_dict(cls, data):
        ano = str(data.get("ano"))
        mes = str(data.get("mes"))
        id_unidade = int(data.get("id_unidade"))
        try:
            unidade = UnidadePrisional.objects.get(id_unidade=id_unidade)
            data['nome_unidade'] = unidade.nome_unidade
            try:
                item = cls.objects.get(ano=ano, mes=mes, unidade=unidade)
                item.dados = data
            except ObjectDoesNotExist:
                item = cls(ano=ano, mes=mes, unidade=unidade, dados=data)
            item.save()
            item._update_chart_data()
        except UnidadePrisional.DoesNotExist:
            print((f"id_unidade: {id_unidade} | "
                   f"ano: {ano} | "
                   f"mes: {mes} | "
                   f"nome_unidade: {data.get('nome_unidade')}"))

    def _update_chart_data(self):
        self.pop_total = self._asint(self.dados.get("pop_total"))
        card = {
            'nome_unidade': self.unidade.nome_unidade,
            'tipo_logradouro': self.unidade.tipo_logradouro,
            'nome_logradouro': self.unidade.nome_logradouro,
            'numero': self.unidade.numero,
            'complemento': self.unidade.complemento,
            'cep': self.unidade.cep,
            'municipio': self.unidade.municipio.nome,
            'uf': self.unidade.uf,
            'lat': self.unidade.lat,
            'lon': self.unidade.lon,
            'email': self.unidade.email,
            'telefone': self.unidade.telefone,
            'ddd': self.unidade.ddd,
            'tipo_gestao': self.dados.get("tipo_gestao") or "Não declarado",
            'visitacao': self.unidade.visitacao,
            'indices': {
                'educacao': self.dados.get("DTDI_educacao"),
                'trabalho': self.dados.get("DTDI_trabalho"),
                'saude': self.dados.get("DTDI_saude"),
                'juridico': self.dados.get("DTDI_juridico")
            },
            'pop_total': self.dados.get("pop_total"),
            'vagas': self.dados.get("vagas_total"),
            'qualidade_info': self.dados.get("ITQI"),
            'pop_perc': {
                'provisoria': self._percentual_presos_provisorios(),
                'origem': [
                    {'label': 'brasileiros',
                     'value': self._percentual_naturalidade("brasileiros")},
                    {'label': 'naturalizados',
                     'value': self._percentual_naturalidade("naturalizados")},
                    {'label': 'estrangeiros',
                     'value': self._percentual_naturalidade("estrangeiros")},
                ],
                'cor': [
                    {'label': 'preta', 'color': 'rgb(11,102,176)',
                     'value': self._percentual_grupo_pop("preta")},
                    {'label': 'parda', 'color': 'rgb(255,108,1)',
                     'value': self._percentual_grupo_pop("parda")},
                    {'label': 'branca', 'color': 'rgb(2,161,19)',
                     'value': self._percentual_grupo_pop("branca")},
                    {'label': 'indígena', 'color': 'rgb(228,0,121)',
                     'value': self._percentual_grupo_pop("indigena")},
                    {'label': 'amarela', 'color': 'rgb(150,73,185)',
                     'value': self._percentual_grupo_pop("amarela")},
                    {'label': 'outros', 'color': 'rgb(0,0,0)',
                     'value': self._percentual_grupo_pop("outros")},
                ],
            },
            'pyramid': {
                'ages': [
                    {'range': '+ de 70',
                     'male': self._perc_faixa_etaria("masculino",
                                                     "maisde70anos"),
                     'female': self._perc_faixa_etaria("feminino",
                                                       "maisde70anos")},
                    {'range': '61 a 70',
                     'male': self._perc_faixa_etaria("masculino",
                                                     "61a70anos"),
                     'female': self._perc_faixa_etaria("feminino",
                                                       "61a70anos")},
                    {'range': '46 a 60',
                     'male': self._perc_faixa_etaria("masculino",
                                                     "46a60anos"),
                     'female': self._perc_faixa_etaria("feminino",
                                                       "46a60anos")},
                    {'range': '35 a 45',
                     'male': self._perc_faixa_etaria("masculino",
                                                     "35a45anos"),
                     'female': self._perc_faixa_etaria("feminino",
                                                       "35a45anos")},
                    {'range': '30 a 34',
                     'male': self._perc_faixa_etaria("masculino",
                                                     "30a34anos"),
                     'female': self._perc_faixa_etaria("feminino",
                                                       "30a34anos")},
                    {'range': '25 a 29',
                     'male': self._perc_faixa_etaria("masculino",
                                                     "25a29anos"),
                     'female': self._perc_faixa_etaria("feminino",
                                                       "25a29anos")},
                    {'range': '18 a 24',
                     'male': self._perc_faixa_etaria("masculino",
                                                     "18a24anos"),
                     'female': self._perc_faixa_etaria("feminino",
                                                       "18a24anos")},
                ],
                'total': {
                    'perc': {
                        'male': self._perc_pop_sexo("masculino"),
                        'female': self._perc_pop_sexo("feminino")},
                    'abs': {
                        'male': self._asint(
                            self.dados.get("pop_masculino_total")
                        ),
                        'female': self._asint(
                            self.dados.get("pop_feminino_total")
                        )
                    },
                },
                'idade_media': self._idade_media()
            }
        }
        self.card = card
        self.save()

    @staticmethod
    def _asint(number):
        if not number:
            return 0
        try:
            return int(number)
        except ValueError:
            return 0

    def _percentual_presos_provisorios(self):
        provisorios = 0
        provisorios += self._asint(
            self.dados.get("pop_masculino_provisorio_just_estadual")
        )
        provisorios += self._asint(
            self.dados.get("pop_feminino_provisorio_just_estadual")
        )
        provisorios += self._asint(
            self.dados.get("pop_masculino_provisorio_just_federal")
        )
        provisorios += self._asint(
            self.dados.get("pop_feminino_provisorio_just_federal")
        )
        provisorios += self._asint(
            self.dados.get("pop_masculino_provisorio_outros")
        )
        provisorios += self._asint(
            self.dados.get("pop_feminino_provisorio_outros")
        )
        if self.pop_total:
            return round(100 * (provisorios / self.pop_total), 2)
        else:
            return None

    def _percentual_naturalidade(self, origem):
        if not self.pop_total:
            return None

        if origem == "basileiros":
            pop = self._asint(
                self.dados.get("nacionalidade_brasil_nato_masculino")
            )
            pop += self._asint(
                self.dados.get("nacionalidade_brasil_nato_feminino")
            )
        elif origem == "naturalizado":
            pop = self._asint(
                self.dados.get("nacionalidade_brasil_naturalizado_masculino")
            )
            pop += self._asint(
                self.dados.get("nacionalidade_brasil_naturalizado_feminino")
            )
        else:
            pop = self._asint(
                self.dados.get("nacionalidade_estrangeiro_masculino")
            )
            pop += self._asint(
                self.dados.get("nacionalidade_estrangeiro_feminino")
            )

        return round(100 * (pop / self.pop_total), 2)

    def _percentual_grupo_pop(self, grupo):
        if not self.pop_total:
            return None

        if grupo == "preta":
            pop = self._asint(self.dados.get("raca_preta_masculino"))
            pop += self._asint(self.dados.get("raca_preta_feminino"))
        elif grupo == "parda":
            pop = self._asint(self.dados.get("raca_parda_masculino"))
            pop += self._asint(self.dados.get("raca_parda_feminino"))
        elif grupo == "branca":
            pop = self._asint(self.dados.get("raca_branca_masculino"))
            pop += self._asint(self.dados.get("raca_branca_feminino"))
        elif grupo == "indigena":
            pop = self._asint(self.dados.get("raca_indigena_masculino"))
            pop += self._asint(self.dados.get("raca_indigena_feminino"))
        elif grupo == "amarela":
            pop = self._asint(self.dados.get("raca_amarela_masculino"))
            pop += self._asint(self.dados.get("raca_amarela_feminino"))
        elif grupo == "outros":
            pop = self._asint(self.dados.get("raca_outras_masculino"))
            pop += self._asint(self.dados.get("raca_outras_feminino"))
        else:
            return None

        return round(100 * (pop / self.pop_total), 2)

    def _perc_faixa_etaria(self, sexo, faixa):
        if not self.pop_total:
            return None

        pop = self._asint(self.dados.get(f"faixa_etaria_{faixa}_{sexo}"))

        return round(100 * (pop / self.pop_total), 2)

    def _perc_pop_sexo(self, sexo):
        if not self.pop_total:
            return None

        pop = self._asint(self.dados.get(f"pop_{sexo}_total"))
        return round(100 * (pop / self.pop_total), 2)

    def _idade_media(self):
        faixas = {
            "18a24anos": (24 + 18)/2,
            "25a29anos": (25 + 29)/2,
            "30a34anos": (30 + 34)/2,
            "35a45anos": (35 + 45)/2,
            "46a60anos": (46 + 60)/2,
        }
        total = 0
        qtdes = 0
        for faixa, central in faixas.items():
            qtd = self._asint(
                self.dados.get(f"faixa_etaria_{faixa}_masculino")
            )
            qtd += self._asint(
                self.dados.get(f"faixa_etaria_{faixa}_feminino")
            )
            total += central * qtd
            qtdes += qtd
        if qtdes:
            return int(total /qtdes)
        else:
            return None
