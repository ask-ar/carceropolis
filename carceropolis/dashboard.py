import threading

import pandas as pd

from tornado.ioloop import IOLoop
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.layouts import widgetbox, row
from bokeh.models import ColumnDataSource, Slider
from bokeh.models.widgets.inputs import Select
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.models import HoverTool


def load_db():
    df = pd.read_csv('test.csv')
    df.ano = df.ano.astype(str)
    return df


class Dashboard(object):
    '''
    This class represents a dashboard and should be instanciated
    for each user.
    The `generate` static method is used by the Bokeh server to
    instanciate dashboards.
    '''

    # TODO: maybe remove this?
    df = load_db()

    @staticmethod
    def generate(doc):
        '''
        Generate a new dashboard. This function should be passed
        to the Bokeh FunctionHandler.
        '''
        return Dashboard(Dashboard.df.copy(), doc)

    def __init__(self, df, doc):
        '''
        Called when a user connects. This dashboard should be used
        while the connection remain, and is used by only one user.
        '''

        self.chart_types = {
            'linha': self.plot_lines,
            'barras horizontais': self.plot_hbar,
            'barras verticais': self.plot_vbar,
            'círculos': self.plot_circles,
        }

        self.df = df
        self.doc = doc
        self.columns = sorted(df.columns)
        self.discrete = [x for x in self.columns if self.df[x].dtype == object]
        # continuous = [x for x in columns if x not in discrete]
        # discrete.append(continuous.pop(continuous.index('ano')))

        self.x_selector = Select(
            title='X-Axis', value='ano', options=self.columns)
        self.x_selector.on_change('value', self.update)

        self.y_selector = Select(
            title='Y-Axis', value='pop_masc', options=self.columns)
        self.y_selector.on_change('value', self.update)

        charts_names = list(self.chart_types)
        self.chart_type_selector = Select(
            title='Tipo', value=charts_names[2], options=charts_names)
        self.chart_type_selector.on_change('value', self.update)

        filter_selector = Select(
            title='Y-Axis', value='pop_masc', options=self.columns)
        filter_selector.on_change('value', self.update)

        controls = widgetbox(
            [self.x_selector, self.y_selector, self.chart_type_selector],
            width=200)
        self.layout = row(controls, self.create_figure())

        doc.add_root(self.layout)

    def update(self, attr, old, new):
        '''
        Called when chart options are modified.
        '''
        self.layout.children[1] = self.create_figure()

    def plot_lines(self, fig, x, y, source):
        fig.line(x, y, source=source)
        # plot.line(x=xs, width=0.5, bottom=0, top=ys)

    def plot_vbar(self, fig, x, y, source):
        fig.vbar(x, 0.5, y, source=source)
        # plot.vbar(x=xs, width=0.5, bottom=0, top=ys)

    def plot_hbar(self, fig, x, y, source):
        fig.hbar(y=y, height=0.5, right=x, left=0, source=source)

    def plot_circles(self, fig, x, y, source):
        fig.circle(x, y, source=source)
        # plot.circle(x=xs, y=ys)

    def create_figure(self):
        '''
        Creates the chart.
        '''
        grouped_df = self.df.groupby(self.x_selector.value).sum()
        source = ColumnDataSource(data=grouped_df)

        xs = self.df[self.x_selector.value].values
        ys = self.df[self.y_selector.value].values
        x_title = self.x_selector.value.title()
        y_title = self.y_selector.value.title()

        kw = dict()
        if self.x_selector.value in self.discrete:
            kw['x_range'] = sorted(set(xs))
        if self.y_selector.value in self.discrete:
            kw['y_range'] = sorted(set(ys))
        kw['title'] = "%s vs %s" % (x_title, y_title)

        fig = figure(plot_height=600, plot_width=800,
                     tools='pan,box_zoom,reset,save', **kw)
        fig.xaxis.axis_label = x_title
        fig.yaxis.axis_label = y_title

        if self.x_selector.value in self.discrete:
            fig.xaxis.major_label_orientation = pd.np.pi / 4

        self.chart_types[self.chart_type_selector.value](
            fig, self.x_selector.value, self.y_selector.value, source)

        hover = HoverTool(tooltips=[
            ("index", "$index"),
            (self.x_selector.value, '@'+self.x_selector.value),
            (self.y_selector.value, '@'+self.y_selector.value),
        ])
        fig.add_tools(hover)

        return fig


class BackgroundBokeh(threading.Thread):

    def run(self):
        bokeh_app = Application(FunctionHandler(Dashboard.generate))
        io_loop = IOLoop.current()
        server = Server({'/bkapp': bokeh_app}, io_loop=io_loop,
                        allow_websocket_origin=["localhost:8000"])
        server.start()
        io_loop.start()

    def stop(self):
        IOLoop.current().stop()


bokeh_server = BackgroundBokeh()


def start_server():
    print('> Starting Bokeh server')
    bokeh_server.start()


def stop_server():
    print('> Stopping Bokeh server')
    bokeh_server.stop()
