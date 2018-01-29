import plotly.offline as opy
import plotly.graph_objs as go
from requests.compat import json as _json
from plotly import utils
import pandas as pd
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.models import HoverTool
from bokeh.models import FixedTicker

from carceropolis.utils.bokeh import (
    plot_lines, plot_circles)


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

            for info in ['titulo', 'unidade', 'fonte', 'fonte_url', 'notas']:
                text = fo.readline().partition(',')[2].strip('"\n ')
                content[info] = text if text else None

            if content['notas']:
                content['notas'] = content['notas'].split(';')

            next(fo)  # Pula uma linha em branco

            data = pd.read_csv(fo, decimal=",", quotechar='"')

        if item == '01':
            fig = figure(
                title=content['titulo'],
                plot_height=600, plot_width=800, background_fill_alpha=0,
                border_fill_alpha=0, tools='pan,box_zoom,reset,save')

            x_name = 'Ano'
            y_name = 'População'

            fig.xaxis.axis_label = x_name
            fig.yaxis.axis_label = y_name + ' (em milhares)'
            fig.axis.axis_label_text_font_style = "bold"
            fig.title.text_font_size = '14pt'
            fig.title.align = 'center'
            # xticks = FixedTicker(ticks=list(data[x_name]))
            # fig.xaxis.ticker = xticks
            # fig.xgrid.ticker = xticks

            plot_lines(fig, x_name, [y_name], data, ["#ea702e"])
            plot_circles(fig, x_name, [y_name], data, ["#ea702e"], 5)

            # Tooltips
            tooltips = '''
            <div class="mytooltip" style="color:@color;">
                <ul>
                    <li>{xname}: @{xname}</li>
                    <li>@value_name: @value</li>
                </ul>
            </div>
            '''.format(xname=x_name)
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
