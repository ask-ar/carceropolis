import requests
import pandas as pd
import yaml
import threading

from tornado.ioloop import IOLoop
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.layouts import column, widgetbox, row
from bokeh.models import ColumnDataSource, Slider
from bokeh.models.widgets.inputs import AutocompleteInput, Select
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.themes import Theme
from bokeh.models import HoverTool


def modify_doc(doc):
    df = pd.read_csv('test.csv')
    df.ano = df.ano.astype(str)
    columns = sorted(df.columns)
    discrete = [x for x in columns if df[x].dtype == object]
    # continuous = [x for x in columns if x not in discrete]
    # discrete.append(continuous.pop(continuous.index('ano')))

    source = ColumnDataSource(data=df)

    def plot_lines(fig, x, y, source):
        fig.line(x, y, source=source)
        # plot.line(x=xs, width=0.5, bottom=0, top=ys)

    def plot_vbar(fig, x, y, source):
        fig.vbar(x, 0.5, y, source=source)
        # plot.vbar(x=xs, width=0.5, bottom=0, top=ys)

    def plot_hbar(fig, x, y, source):
        fig.hbar(y=y, height=0.5, right=x, left=0, source=source)

    def plot_circles(fig, x, y, source):
        fig.circle(x, y, source=source)
        # plot.circle(x=xs, y=ys)

    chart_types = {
        'linha': plot_lines,
        'barras horizontais': plot_hbar,
        'barras verticais': plot_vbar,
        'círculos': plot_circles,
    }

    def create_figure():
        xs = df[x.value].values
        ys = df[y.value].values
        x_title = x.value.title()
        y_title = y.value.title()

        kw = dict()
        if x.value in discrete:
            kw['x_range'] = sorted(set(xs))
        if y.value in discrete:
            kw['y_range'] = sorted(set(ys))
        kw['title'] = "%s vs %s" % (x_title, y_title)

        fig = figure(plot_height=600, plot_width=800, tools='pan,box_zoom,reset,save', **kw)
        fig.xaxis.axis_label = x_title
        fig.yaxis.axis_label = y_title

        if x.value in discrete:
            fig.xaxis.major_label_orientation = pd.np.pi / 4

        chart_types[chart_type.value](fig, x.value, y.value, source)

        hover = HoverTool(tooltips=[
            ("index", "$index"),
            (x.value, '@'+x.value),
            (y.value, '@'+y.value),
        ])
        fig.add_tools(hover)

        return fig

    def update(attr, old, new):
        layout.children[1] = create_figure()

    x = Select(title='X-Axis', value='ano', options=columns)
    x.on_change('value', update)

    y = Select(title='Y-Axis', value='pop_masc', options=columns)
    y.on_change('value', update)

    charts_names = list(chart_types)
    chart_type = Select(title='Tipo', value=charts_names[2],
                        options=charts_names)
    chart_type.on_change('value', update)

    # size = Select(title='Size', value='None', options=['None'] + quantileable)
    # size.on_change('value', update)

    # color = Select(title='Color', value='None', options=['None'] + quantileable)
    # color.on_change('value', update)

    controls = widgetbox([x, y, chart_type], width=200)
    layout = row(controls, create_figure())

    doc.add_root(layout)
    doc.title = "Crossfilter"


class BackgroundBokeh(threading.Thread):
    def run(self):
        bokeh_app = Application(FunctionHandler(modify_doc))
        io_loop = IOLoop.current()
        server = Server({'/bkapp': bokeh_app}, io_loop=io_loop,
                        allow_websocket_origin=["localhost:8000"])
        server.start()
        io_loop.start()

    def stop(self):
        IOLoop.current().stop()


bokeh_server = BackgroundBokeh()


def start_server():
    print('= Starting Bokeh server')
    bokeh_server.start()


def stop_server():
    print('= Stopping Bokeh server')
    bokeh_server.stop()
