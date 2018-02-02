import os
import numpy as np
import pandas as pd
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.models import NumeralTickFormatter

from carceropolis.utils.bokeh import (
    create_figure, plot_lines, plot_circles, plot_hbar)


def read_mini_csv(csv_path):
    '''Read content from CSV'''
    content = {}
    with open(os.path.join('carceropolis/static/data', csv_path), 'r') as fo:
        content['data_file_url'] = os.path.join('data', csv_path)

        # read metadata
        for info in ['titulo', 'unidade', 'fonte', 'fonte_url', 'notas']:
            text = fo.readline().partition(',')[2].strip('"\n, ')
            content[info] = text if text else None
        if content['notas']:
            content['notas'] = content['notas'].split(';')

        next(fo)  # Pula uma linha em branco

        # read data
        data = (pd.read_csv(fo, decimal=",", quotechar='"')
                # Convert empty cells to nan
                .replace(r'^\s*$', np.nan, regex=True)
                # Remove columns with all nan cells
                .dropna(axis=1, how='all'))
        content['xname'] = data.columns[0]
        content['ynames'] = list(data.columns[1:])
        content['dados'] = data
        return content


def create_figure_from_content(content, **kw):
    '''Helper to create figure from content'''
    return create_figure(
        content['xname'], content['unidade'], title=content['titulo'], **kw)


def plot_simple_hbar_helper(content):
    ''' Helper for sigle category hbar chart'''
    dados = content['dados']
    dados = dados[~dados['Estado'].isin(['ONU', 'BR'])]
    fig = create_figure_from_content(content, y_range=list(dados['Estado']))
    fig.xaxis.axis_label = content['unidade']
    fig.yaxis.axis_label = content['xname']
    fig.xaxis.formatter = NumeralTickFormatter(format='0,0', language='pt-br')
    plot_hbar(fig, content['xname'], content['ynames'], dados)
    return fig


def pop_prisional_brasil(content):
    '''Plot chart 1'''
    fig = create_figure_from_content(content)
    plot_lines(fig, content['xname'], content['ynames'], content['dados'],
               ["#ea702e"])
    plot_circles(fig, content['xname'], content['ynames'], content['dados'],
                 ["#ea702e"], 5)
    return fig


def taxa_encarceramento_paises(content):
    '''Plot chart 2'''
    fig = create_figure_from_content(content)
    plot_circles(fig, content['xname'], content['ynames'], content['dados'],
                 size=5)
    plot_lines(fig, content['xname'], content['ynames'], content['dados'],
               continuous=True)
    return fig


def get_context():
    context = {}
    graficos = []

    for csv_path, function in [
            ('dados_gerais/01.csv', pop_prisional_brasil),
            ('dados_gerais/02.csv', taxa_encarceramento_paises),
            ('dados_gerais/03.csv', plot_simple_hbar_helper),
            ('dados_gerais/04.csv', plot_simple_hbar_helper),
    ]:
        content = read_mini_csv(csv_path)
        fig = function(content)
        script, div = components(fig)
        content['graph'] = div
        content['script'] = script
        graficos.append(content)

    # TODO: As duas linhas abaixo colocam todo o JS e CSS do Bokeh inline,
    # o que é ruim, já que não usa a cache do navegador. Melhorar!
    context['bokeh_js'] = INLINE.render_js()
    context['bokeh_css'] = INLINE.render_css()

    context['graficos'] = graficos
    return context


context = get_context()
