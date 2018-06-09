import os
import textwrap

import numpy as np
import pandas as pd
from bokeh.resources import CDN
from bokeh.embed import components
# from bokeh.models import NumeralTickFormatter
from bokeh import palettes
from bokeh.models import Title
from bokeh.plotting import figure
from bokeh.transform import dodge
from bokeh.models import HoverTool, FuncTickFormatter, CustomJSHover
from bokeh.core.properties import value, Auto
from bokeh.models import ColumnDataSource


# NUMERAL_TICK_FORMATER = NumeralTickFormatter(format='0,0', language='pt-br')
NUMERAL_TICK_FORMATER = FuncTickFormatter(code='''
    return tick.toLocaleString('pt-BR')
''')

MAIN_PALLETE = palettes.Dark2_8
# Orange before green
MAIN_PALLETE.insert(1, MAIN_PALLETE.pop(0))


def get_legend(y, ys):
    '''
    Return a legend string for a column.
    A `value` is used to avoid Bokeh behavior of replacing
    the string with the column data when the name matches.
    If only one column will be plotted, uses empty legend.
    '''
    return value(y) if len(ys) > 1 else None


def create_source(df, x, y, color):
    ''' Creates a datasource in the format needed for tooltips. '''
    return ColumnDataSource(data={
        x: df[x],
        'value': df[y],
        'value_name': [y]*len(df),
        'color': [color]*len(df),
    })


def create_figure(x_title, y_title, **kw):
    ''' Creates a figure using default style. `kw` can be used to customize.'''
    # default figure values
    attrs = {
        'plot_height': 600,
        'plot_width': 800,
        'background_fill_alpha': 0,
        'border_fill_alpha': 0,
        'tools': 'pan,box_zoom,reset,save',
        'custom_fn': None,

        'tooltip_value_format': '0,0',
        'tooltip_value_sufix': '',
        'tooltip_fn': add_tooltip,
    }
    # replace with arg values
    attrs.update(kw)
    tooltip_args = {
        'xname': x_title,
        'value_format': attrs.pop('tooltip_value_format'),
        'value_sufix': attrs.pop('tooltip_value_sufix'),
    }

    custom_fn = attrs.pop('custom_fn')
    title = attrs.pop('title')
    tooltip_fn = attrs.pop('tooltip_fn')
    fig = figure(**attrs)

    for text in reversed(textwrap.wrap(title, width=67)):
        fig.add_layout(Title(text=text, text_font_size='15pt', align='center'), 'above')

    fig.xaxis.axis_label = x_title
    fig.yaxis.axis_label = y_title
    if tooltip_fn:
        tooltip_fn(fig, tooltip_args)
    # more defaults
    fig.axis.axis_label_text_font_style = 'bold'
    fig.title.text_font_size = '14pt'
    fig.title.align = 'center'
    # fig.legend.location = 'top_left'
    # fig.legend.orientation = 'horizontal'

    if custom_fn:
        custom_fn(fig)

    return fig


def add_tooltip(fig, args, renderers='auto'):
    '''Adds tooltip to a figure.'''
    tooltips = '''
    <div class="mytooltip" style="color:@color;">
    <ul>
        <li>{xname}: @{{{xname}}}</li>
        <li>@value_name: @value{{{value_format}}}{value_sufix}</li>
    </ul>
    </div>
    '''.format(**args)

    locale_format = CustomJSHover(code='''
        return parseFloat(value).toLocaleString('pt-BR')
    ''')

    hover = HoverTool(
        tooltips=tooltips, formatters=dict(value=locale_format), renderers=renderers)
    fig.add_tools(hover)


def plot_lines(fig, x, ys, df, palette=MAIN_PALLETE, continuous=False):
    '''Plot a line chart.'''
    for y, color in zip(ys, palette):
        if continuous:
            source_df = df[[x, y]].dropna(axis=0, how='any')
        else:
            source_df = df
        source = create_source(source_df, x, y, color)
        fig.line(
            x, 'value', source=source, line_width=3, color=color,
            legend=get_legend(y, ys))
    fig.legend.location = 'top_left'
    fig.legend.orientation = 'horizontal'


def plot_circles(fig, x, ys, df, palette=MAIN_PALLETE, size=10):
    '''Plot a scatter chart.'''
    for y, color in zip(ys, palette):
        source = create_source(df, x, y, color)
        fig.circle(
            x, 'value', size=size, source=source, color=color,
            legend=get_legend(y, ys))


def plot_bar_iterator(ys, outer_width, palette):
    '''Helper function that generates values used to plot bars.'''
    le = len(ys)
    for y, color, i in zip(ys, palette, range(0, le)):
        # Spreads bars based on the number of bars and their
        # width, so they don't overlap
        offset = round(-outer_width*le/2 + outer_width/2 + outer_width*i, 2)
        yield y, offset, color


def plot_vbar(fig, x, ys, df, palette=MAIN_PALLETE, width=0.2):
    '''Plot a vertical bar chart.'''
    for y, offset, color in plot_bar_iterator(ys, width+.03, palette):
        source = create_source(df, x, y, color)
        fig.vbar(
            x=x, width=width+.03,
            top='value', source=source, color=color, legend=get_legend(y, ys))


def plot_hbar(fig, x, ys, df, palette=MAIN_PALLETE, width=0.5):
    '''Plot a horizontal bar chart.'''
    for y, offset, color in plot_bar_iterator(ys, width+.03, palette):
        source = create_source(df, x, y, color)
        fig.hbar(
            y=dodge(x, offset, range=fig.y_range), height=width, right='value',
            source=source, color=color, legend=get_legend(y, ys))


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
        # data = data.sort_values(by=data.columns[1], ascending=True)
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


def plot_simple_lines(content, circles=True, circles_size=5, continuous=False, **kw):
    fig = create_figure_from_content(content, **kw)
    plot_lines(fig, content['xname'], content['ynames'], content['dados'],
               continuous=continuous)
    if circles_size:
        plot_circles(
            fig, content['xname'], content['ynames'], content['dados'],
            size=circles_size)
    fig.yaxis.formatter = NUMERAL_TICK_FORMATER
    return fig


def plot_stacked_hbar_helper(content, width=.5, **kw):
    dados = content['dados']
    y_col_name = dados.columns[0]
    categories = dados.columns[1:]
    indexes = list(dados[y_col_name])
    kw['tooltip_fn'] = False
    fig = create_figure_from_content(content, y_range=list(dados[y_col_name]), **kw)
    fig.xaxis.axis_label = content['unidade']
    fig.yaxis.axis_label = content['xname']
    fig.xaxis.formatter = NUMERAL_TICK_FORMATER

    original = dados.copy()
    data = dados
    tooltip_args = {
        'xname': content['xname'],
        'value_format': '0,0',
        'value_sufix': '',
    }
    for i in range(1, len(categories)):
        data[categories[i]] = [
            sum((float(i) for i in x))
            for x in zip(data[categories[i]], data[categories[i-1]])]
    for i in range(len(categories)):
        color = MAIN_PALLETE[i]
        rx = fig.hbar(
            y=indexes,
            left=data[categories[i-1]] if i else [0]*len(indexes),
            right=data[categories[i]],
            height=0.9,
            color=color,
            legend=categories[i])
        # TODO: refatorar
        rx.data_source.add(original[categories[i]], 'value')
        rx.data_source.add([categories[i]]*len(indexes), 'value_name')
        rx.data_source.add([color]*len(indexes), 'color')
        rx.data_source.add(indexes, y_col_name)
        add_tooltip(fig, tooltip_args, [rx])

    fig.legend.location = 'center_right'

    # fig.hbar_stack(
    #     categories, y=y_col_name, height=0.9, color=MAIN_PALLETE[:len(categories)],
    #     source=ColumnDataSource(dados), legend=[value(i) for i in categories])
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
