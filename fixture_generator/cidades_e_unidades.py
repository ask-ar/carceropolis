# coding:utf-8

import json

import pandas as pd


CIDADE_MODEL_NAME = "cidades.cidade"
UNIDADE_MODEL_NAME = "carceropolis.unidadeprisional"
# Translator from spreadsheet column name (first item in tuple) to model
# attribute name (second item in tuple). Use only one item in the tuple to use
# the same name for both.
UNIDADES_FIELDS = (
    ('nome_unidade',),
    ('sigla_unidade',),
    ('tipo_logradouro',),
    ('nome_logradouro',),
    ('numero',),
    ('complemento',),
    ('bairro',),
    ('municipio',),
    ('uf',),
    ('cep',),
    ('ddd_unidade', 'ddd'),
    ('telefone_unidade', 'telefone'),
    ('email_unidade', 'email'),
)


def convert(value, column):
    '''
    Converts unidades values based on column name.
    '''
    if value == '' and column not in [
            'sigla_unidade', 'complemento', 'bairro', 'nome_logradouro']:
        return None
    elif column in ['telefone_unidade', 'ddd_unidade', 'numero']:
        return int(value)
    elif column is 'municipio':
        return cidade_to_pk[value]
    else:
        return str(value)


fixtures = []
cidade_to_pk = {}

# --------------------------------
# Generate cidade fixtures
# --------------------------------
with open('brazil-cities-states.json') as data_file:
    data = json.load(data_file)
    cidade_pk = 0
    for state_object in data['estados']:
        state = state_object['sigla']
        for cidade in state_object['cidades']:
            cidade_pk += 1
            fixture_object = {
                 "model": CIDADE_MODEL_NAME,
                 "pk": cidade_pk,
                 "fields": {
                     "nome": cidade,
                     "estado": state
                 }
            }
            cidade_to_pk[cidade] = cidade_pk
            fixtures.append(fixture_object)


# --------------------------------
# Generate unidades fixtures
# --------------------------------
df = pd.read_excel(
    'BD_UNIDADES_FINAL_checado.xlsx',
    sheetname='tratamento',
    na_values=['-', ' - ', 's/n'],
)
df = df.fillna('')
unidade_pk = 0
for row in df.itertuples():
    unidade_pk += 1
    fixtures.append({
        'model': UNIDADE_MODEL_NAME,
        'pk': unidade_pk,
        'fields': {
            field[-1]: convert(getattr(row, field[0]), field[0])
            for field in UNIDADES_FIELDS
        }
    })

# --------------------------------
# Export fixtures
# --------------------------------
with open('cidades_e_unidades.json', 'w') as f:
    json.dump(fixtures, f)
