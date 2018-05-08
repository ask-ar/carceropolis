import textwrap

from bokeh import palettes
from bokeh.models import Title
from bokeh.plotting import figure
from bokeh.transform import dodge
from bokeh.models import HoverTool
from bokeh.core.properties import value
from bokeh.models import ColumnDataSource


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

        'tooltip_value_format': '0,0.00',
        'tooltip_value_sufix': ''
    }
    # replace with arg values
    attrs.update(kw)
    tooltip_args = {
        'xname': x_title,
        'value_format': attrs.pop('tooltip_value_format'),
        'value_sufix': attrs.pop('tooltip_value_sufix'),
    }

    title = attrs.pop('title')
    fig = figure(**attrs)

    for text in reversed(textwrap.wrap(title, width=67)):
        fig.add_layout(Title(text=text, text_font_size='15pt', align='center'), 'above')

    fig.xaxis.axis_label = x_title
    fig.yaxis.axis_label = y_title
    add_tooltip(fig, tooltip_args)
    # more defaults
    fig.axis.axis_label_text_font_style = "bold"
    fig.title.text_font_size = '14pt'
    fig.title.align = 'center'
    fig.legend.location = 'top_right'
    return fig


def add_tooltip(fig, args):
    '''Adds tooltip to a figure.'''
    tooltips = '''
    <div class="mytooltip" style="color:@color;">
    <ul>
        <li>{xname}: @{{{xname}}}</li>
        <li>@value_name: @value{{{value_format}}}{value_sufix}</li>
    </ul>
    </div>
    '''.format(**args)
    hover = HoverTool(tooltips=tooltips)
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
