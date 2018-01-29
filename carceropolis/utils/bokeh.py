from bokeh import palettes
from bokeh.core.properties import value
from bokeh.models import ColumnDataSource


MAIN_PALLETE = palettes.Dark2_8


def get_legend(y, ys):
    '''
    Return a legend string for a column.
    A `value` is used to avoid Bokeh behavior of replacing
    the string with the column data when the name matches.
    If only one column will be plotted, uses empty legend.
    '''
    return value(y) if len(ys) > 1 else None


def create_source(df, x, y, color):
    '''
    Creates a datasource in the format needed for tooltips.
    '''
    return ColumnDataSource(data={
        x: df[x],
        'value': df[y],
        'value_name': [y]*len(df),
        'color': [color]*len(df),
    })


def plot_lines(fig, x, ys, df, palette=MAIN_PALLETE):
    '''
    Plot a line chart.
    '''
    for y, color in zip(ys, palette):
        source = create_source(df, x, y, color)
        fig.line(
            x, 'value', source=source, line_width=3, color=color,
            legend=get_legend(y, ys))
