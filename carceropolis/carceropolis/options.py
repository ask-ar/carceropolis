"""Arquivo que irá manter um conjunto de 'opções' (choices)."""
from datetime import datetime

CATEGORIAS = (
    ('SISTEMA', 'FUNCIONAMENTO DO SISTEMA'),
    ('PERFIL', 'PERFIL POPULACIONAL'),
    (u'POLÍTICA', u'POLÍTICA CRIMINAL'),
    ('INTERNACIONAL', 'SISTEMAS INTERNACIONAIS'),
    (u'VIOLÊNCIA', u'VIOLÊNCIA INSTITUCIONAL'),
    ('OUTROS', 'OUTROS'),
)


YEAR_CHOICES = [(r, r) for r in range(1900, datetime.now().year+1)]

MONTH_CHOICES = [('Janeiro', 'Janeiro'), ('Fevereiro', 'Fevereiro'),
                 ('Março', 'Março'), ('Abril', 'Abril'), ('Maio', 'Maio'),
                 ('Junho', 'Junho'), ('Julho', 'Julho'), ('Agosto', 'Agosto'),
                 ('Setembro', 'Setembro'), ('Outubro', 'Outubro'),
                 ('Novembro', 'Novembro'), ('Dezembro', 'Dezembro')]

INFOPEN_YEARS = [2014, 2015, 2016]
INFOPEN_MONTHS = [6, 12]
INFOPEN_DEFAULT_YEAR = 2016
INFOPEN_DEFAULT_MONTH = 6


def current_year():
    """Return the current year (XXXX)."""
    return datetime.now().year


def current_month():
    """Return the current month (text)."""
    return MONTH_CHOICES[datetime.now().month - 1]
