from bokeh.embed import components

from carceropolis.utils.bokeh import plot_lines, plot_circles
from carceropolis.charts.utils import (
    create_figure_from_content, plot_simple_hbar_helper, read_mini_csv)


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
    context['graficos'] = graficos
    return context
