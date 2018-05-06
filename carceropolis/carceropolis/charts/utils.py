import os
import numpy as np
import pandas as pd

from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.models import NumeralTickFormatter

from carceropolis.utils.bokeh import (
    create_figure, plot_vbar, plot_hbar, plot_lines, plot_circles)


# TODO: está usando , no lugar de .
NUMERAL_TICK_FORMATER = NumeralTickFormatter(format='0,0', language='pt-br')


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
        # data = data.sort_values(by=data.columns[1], ascending=False)
        content['xname'] = data.columns[0]
        content['ynames'] = list(data.columns[1:])
        content['dados'] = data
        return content


def create_figure_from_content(content, **kw):
    '''Helper to create a figure from content'''
    return create_figure(
        content['xname'], content['unidade'], title=content['titulo'], **kw)


def plot_simple_hbar_helper(content, width=.5, **kw):
    '''Helper for sigle category hbar chart'''
    dados = content['dados']
    y_col_name = dados.columns[0]
    dados = dados[~dados[y_col_name].isin(['ONU', 'BR'])]
    fig = create_figure_from_content(content, y_range=list(dados[y_col_name]), **kw)
    fig.xaxis.axis_label = content['unidade']
    fig.yaxis.axis_label = content['xname']
    fig.xaxis.formatter = NUMERAL_TICK_FORMATER
    plot_hbar(fig, content['xname'], content['ynames'], dados, width=width)
    return fig


def plot_simple_vbar_helper(content, width=.2, **kw):
    '''Helper for sigle category vbar chart'''
    dados = content['dados']
    x_col_name = dados.columns[0]
    dados = dados[~dados[x_col_name].isin(['total'])]
    fig = create_figure_from_content(content, x_range=list(dados[x_col_name]), **kw)
    fig.yaxis.axis_label = content['unidade']
    fig.xaxis.axis_label = content['xname']
    fig.yaxis.formatter = NUMERAL_TICK_FORMATER
    plot_vbar(fig, content['xname'], content['ynames'], dados, width=width)
    return fig


def plot_simple_lines(content, circles=True, circles_size=5, continuous=False):
    fig = create_figure_from_content(content)
    plot_lines(fig, content['xname'], content['ynames'], content['dados'],
               continuous=continuous)
    if circles_size:
        plot_circles(
            fig, content['xname'], content['ynames'], content['dados'],
            size=circles_size)
    fig.yaxis.formatter = NUMERAL_TICK_FORMATER
    return fig


def plot_charts(folder, charts):
    '''
    Plot charts and return context to be used by view template.
    `charts` should be a list of tuples:
    (plotter_function, path_to_data_csv, args).
    '''
    context = {}
    graficos = []
    for function, csv_path, *args in charts:
        if args:
            args = args[0]
        else:
            args = {}
        content = read_mini_csv(os.path.join(folder, csv_path) + '.csv')
        fig = function(content, **args)
        script, div = components(fig)
        content['graph'] = div
        content['script'] = script
        graficos.append(content)
    context['graficos'] = graficos

    # TODO: As duas linhas abaixo carregam o Bokeh de um CDN. Mas o
    # dashboard carrega de arquivos locais, logo não vão utilizar a mesma
    # cache. Talvez seja bom melhorar isso.
    context['bokeh_js'] = CDN.render_js()
    context['bokeh_css'] = CDN.render_css()
    return context
