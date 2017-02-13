# coding= utf-8
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


def current_year():
    """Returns the current year (XXXX)."""
    return datetime.now().year
