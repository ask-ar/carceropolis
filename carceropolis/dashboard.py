import base64
import threading
from urllib.parse import parse_qs

import pandas as pd

from tornado.ioloop import IOLoop
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.layouts import widgetbox, row
from bokeh.models import ColumnDataSource, RangeSlider, CustomJS
from bokeh.models.widgets.inputs import Select
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.models import HoverTool


def update_querystring(window=None, cb_obj=None):
    '''
    This callback will be converted to JS!
    '''
    params = []
    window.console.log(params)
    # TODO: não colocar vazios
    for c in cb_obj.document.roots()[0].children[0].children:
        value = c.value if c.value else c.range
        params.append(
            window.encodeURIComponent(c.name) + '=' +
            window.encodeURIComponent(value)
        )
    query = '?' + '&'.join(params)
    window.history.pushState({}, '', query)


def load_db():
    df = pd.read_csv('test.csv')
    df.ano = df.ano.astype(str)
    return df


def hide_widget(widget):
    if not widget.css_classes:
        widget.css_classes = []
    if 'hidden' not in widget.css_classes:
        widget.css_classes.append('hidden')


def show_widget(widget):
    if widget.css_classes and 'hidden' in widget.css_classes:
        widget.css_classes.remove('hidden')


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

        state = doc.session_context.request.arguments.get('state')
        # import IPython;IPython.embed()
        if state:
            state = parse_qs(base64.urlsafe_b64decode(state[0]).decode())
        else:
            state = {}

        self.chart_types = {
            'linha': self.plot_lines,
            'barras horizontais': self.plot_hbar,
            'barras verticais': self.plot_vbar,
            'círculos': self.plot_circles,
        }
        charts_names = list(self.chart_types)
        none_value = 'Nenhum'

        self.df = df
        self.doc = doc
        self.columns = sorted(df.columns)
        self.discrete = [x for x in self.columns if self.df[x].dtype == object]
        # continuous = [x for x in columns if x not in discrete]
        # discrete.append(continuous.pop(continuous.index('ano')))
        self.filter_options = [none_value]+self.columns

        gui_data = {
            'x_sel': {
                'name': 'x',
                'title': 'Eixo X',
                'value': 'ano',
                'options': self.columns,
                'class': Select,
            },
            'y_sel': {
                'name': 'y',
                'title': 'Eixo Y',
                'value': 'pop_masc',
                'options': self.columns,
                'class': Select,
            },
            'chart_type_sel': {
                'name': 'type',
                'title': 'Tipo de Gráfico',
                'value': charts_names[2],
                'options': charts_names,
                'class': Select,
            },
            'filter_sel': {
                'name': 'filter',
                'title': 'Filtro',
                'value': self.filter_options[0],
                'options': self.filter_options,
                'class': Select,
            },
            'filter_value_sel': {
                'name': 'f_value',
                'title': 'Valor',
                'value': none_value,
                'options': [none_value],
                'class': Select,
            },
            # TODO: this widget is bugged, but it seems they are improving it.
            'filter_range_sel': {
                'name': 'f_range',
                'title': 'Intervalo',
                'start': 0,
                'end': 10,
                'step': 1,
                'range': (0, 0),
                'class': RangeSlider,
            },
        }
        # TODO: validate state? Dangerous?
        if state:
            for gui, data in gui_data.items():
                value = state.get(data['name'])
                if value:
                    value = value[0]
                    if data.get('value'):
                        data['value'] = value
                    elif data.get('range'):
                        print(value)
                        data['range'] = tuple(float(i)
                                              for i in value.split(','))

        # Create gui inputs
        for k, v in gui_data.items():
            v = v.copy()
            class_ = v.pop('class')
            setattr(self, k, class_(**v))

        controls = [getattr(self, k) for k, v in gui_data.items()]

        # Bind callbacks
        js_update_querytstring = CustomJS.from_py_func(update_querystring)
        for control in controls:
            if hasattr(control, 'value'):
                control.on_change('value', self.update)
            elif hasattr(control, 'range'):
                control.on_change('range', self.update)
            control.callback = js_update_querytstring

        # TODO: seems to have no effect
        self.filter_range_sel.callback_policy = 'mouseup'

        controls = widgetbox(controls, width=200)
        self.layout = row(controls, self.create_figure())
        doc.add_root(self.layout)

    def update(self, attr, old, new):
        '''
        Called when chart options are modified.
        '''
        self.layout.children[1] = self.create_figure(attr, old, new)

    # TODO: move helpers (don't really need self) to a new file?
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
    # -----------------------------------------

    def handle_filtering(self, df):
        '''
        Update filter selectors widgets and use their values
        to filter `df`.
        '''
        frs = self.filter_range_sel
        fvs = self.filter_value_sel
        if self.filter_sel.value != self.filter_options[0]:
            filter_column = df[self.filter_sel.value]
            if self.filter_sel.value in self.discrete:
                # Discrete filter

                # update selector
                options = sorted(list(filter_column.unique()))
                fvs.options = options
                if fvs.value not in options:
                    fvs.value = options[0]

                show_widget(fvs)
                hide_widget(frs)

                # filter df
                df = df[filter_column == fvs.value]

            else:
                # Continuous filter

                min_val = filter_column.min()
                max_val = filter_column.max()

                # update slider
                frs.start = min_val
                frs.end = max_val
                if frs.range[0] < min_val or frs.range[1] > max_val:
                    frs.range = (min_val, max_val)
                frs.step = (max_val-min_val)/10

                show_widget(frs)
                hide_widget(fvs)

                # filter df
                df = df[filter_column >= frs.range[0]]
                df = df[filter_column <= frs.range[1]]
        else:
            # No filter
            hide_widget(fvs)
            hide_widget(frs)

        return df

    def create_figure(self, attr=None, old=None, new=None):
        '''
        Creates the chart.
        '''
        print(attr, old, new)
        df = self.handle_filtering(self.df)
        df = df.groupby(self.x_sel.value).sum()
        source = ColumnDataSource(data=df)

        xs = self.df[self.x_sel.value].values
        ys = self.df[self.y_sel.value].values
        x_title = self.x_sel.value.title()
        y_title = self.y_sel.value.title()

        kw = dict()
        if self.x_sel.value in self.discrete:
            kw['x_range'] = sorted(set(xs))
        if self.y_sel.value in self.discrete:
            kw['y_range'] = sorted(set(ys))
        kw['title'] = "%s vs %s" % (x_title, y_title)

        fig = figure(plot_height=600, plot_width=800,
                     tools='pan,box_zoom,reset,save', **kw)
        fig.xaxis.axis_label = x_title
        fig.yaxis.axis_label = y_title

        if self.x_sel.value in self.discrete:
            fig.xaxis.major_label_orientation = pd.np.pi / 4

        self.chart_types[self.chart_type_sel.value](
            fig, self.x_sel.value, self.y_sel.value, source)

        hover = HoverTool(tooltips=[
            ("index", "$index"),
            (self.x_sel.value, '@'+self.x_sel.value),
            (self.y_sel.value, '@'+self.y_sel.value),
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
