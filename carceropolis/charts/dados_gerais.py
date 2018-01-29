import plotly.offline as opy
import plotly.graph_objs as go
from requests.compat import json as _json
from plotly import utils
import pandas as pd
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.models import HoverTool

from carceropolis.utils.bokeh import (
    plot_lines)


def get_context():
    context = {}
    graficos = []

    data_files = {
        '01': 'carceropolis/static/data/dados_gerais/01.csv',
        '02': 'carceropolis/static/data/dados_gerais/02.csv',
        '03': 'carceropolis/static/data/dados_gerais/03.csv',
        '04': 'carceropolis/static/data/dados_gerais/04.csv'
    }

    for item, url in data_files.items():
        content = {}
        with open(url, 'r') as fo:
            content['data_file_url'] = url.split('/static/')[-1]
            content['titulo'] = fo.readline().split(',')[1].lstrip('"').rstrip('"')
            content['unidade'] = fo.readline().split(',')[1].lstrip('"').rstrip('"')
            content['fonte'] = fo.readline().split(',')[1].lstrip('"').rstrip('"')
            content['fonte_url'] = fo.readline().split(',')[1].lstrip('"').rstrip('"')
            notas = fo.readline().split(',')[1].lstrip('"').rstrip('"')
            content['notas'] = notas.split(';') if notas else None
            next(fo)  # Pula uma linha em branco
            data = pd.read_csv(fo, decimal=",", quotechar='"')

        if item == '01':
            kw = {
                'x_range': [2005, 2016],
                # 'y_range': [0, 1000],
            }
            # layout = go.Layout(title=content['titulo'],
            #                    yaxis={'rangemode': 'tozero'},
            #                    xaxis={
            #                        'tickangle': -45,
            #                        'dtick': "M6",
            #                        'tick0': min(data['Data']),
            #                        'tickformat': '%b-%y',
            #                        'range': [min(data['Data']) - pd.DateOffset(months=1),
            #                                  max(data['Data'])]
            #                    })
            fig = figure(
                plot_height=600, plot_width=800, background_fill_alpha=0,
                border_fill_alpha=0, tools='pan,box_zoom,reset,save', **kw)

            plot_lines(fig, 'Ano', ['População'], data, ["#ea702e"])
            # fig.line(
            #     data['Ano'], data['População'], line_width=3)


            # Tooltips
            tooltips = '''
            <div class="mytooltip" style="color:@color;">
                <ul>
                    <li>{xname}: @{xname}</li>
                    <li>@value_name: @value</li>
                </ul>
            </div>
            '''.format(xname='Ano')
            hover = HoverTool(tooltips=tooltips)
            fig.add_tools(hover)
            script, div = components(fig)
        elif item == '02':
            # data['Ano'] = pd.to_datetime(data['Ano'], format='%Y')
            trace1 = go.Scatter(x=data['Ano'], y=data['EUA'], mode='lines',
                                name='EUA', connectgaps=True)
            trace2 = go.Scatter(x=data['Ano'], y=data['China'], mode='lines',
                                name='China', connectgaps=True)
            trace3 = go.Scatter(x=data['Ano'], y=data['Rússia'], mode='lines',
                                name='Rússia', connectgaps=True)
            trace4 = go.Scatter(x=data['Ano'], y=data['Brasil'], mode='lines',
                                name='Brasil', connectgaps=True)
            trace5 = go.Scatter(x=data['Ano'], y=data['ONU'], mode='lines',
                                name='ONU', connectgaps=True)
            graf_data = go.Data([trace1, trace2, trace3, trace4, trace5])
            layout = go.Layout(title=content['titulo'],
                               yaxis={'rangemode': 'tozero'},
                               xaxis={
                                   'tickangle': -45,
                                   'dtick': 1,
                                   'tick0': min(data['Ano']),
                                   'range': [min(data['Ano']),
                                             max(data['Ano'])]
                               })
        elif item == '03':
            dados_estados = data[(data['Estado'] != 'BR') &
                                 (data['Estado'] != 'ONU')]
            trace1 = go.Bar(x=dados_estados['População prisional'],
                            y=dados_estados['Estado'],
                            orientation='h',
                            marker={
                                'line':{
                                    'color': "#bb551d"
                                },
                                'color': '#ea702e'
                            })
            graf_data = go.Data([trace1])
            layout = go.Layout(title=content['titulo'],
                               xaxis={'rangemode': 'tozero'},
                               height=600)
        elif item == '04':
            dados_estados = data[(data['Estado'] != 'BR') &
                                 (data['Estado'] != 'ONU')]
            trace1 = go.Bar(x=dados_estados['Taxa de encarceramento'],
                            y=dados_estados['Estado'],
                            orientation='h',
                            marker={
                                'line':{
                                    'color': "#bb551d"
                                },
                                'color': '#ea702e'
                            })
            graf_data = go.Data([trace1])
            layout = go.Layout(title=content['titulo'],
                               xaxis={'rangemode': 'tozero'},
                               height=600)

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
