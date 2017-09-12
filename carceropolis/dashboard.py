import base64
import threading
from urllib.parse import parse_qs

import pandas as pd
from tornado.ioloop import IOLoop
from bokeh import palettes
from bokeh.plotting import figure
from bokeh.transform import dodge
from bokeh.models import HoverTool
from bokeh.server.server import Server
from bokeh.layouts import widgetbox, row
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.models.widgets.inputs import Select, MultiSelect
from bokeh.models import ColumnDataSource, RangeSlider, CustomJS


def update_querystring(window=None, cb_obj=None):
    '''
    This callback should be converted to JS! It updates
    the url querystring when chart options change.
    '''
    params = []
    for c in cb_obj.document.roots()[0].children[0].children:
        value = c.value
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


def plot_lines(fig, x, ys, source, palette):
    for y, color in zip(ys, palette):
        legend = y+' ' if len(ys) > 1 else None
        fig.line(x, y, source=source, line_width=3, color=color, legend=legend)
    # fig.line(x, 'pop_fem', source=source, line_width=3)


def plot_vbar(fig, x, ys, source, palette):
    # fig.vbar(x, 0.5, y, source=source, legend="b")
    # fig.vbar(x, 0.5, y, source=source, legend='m', line_dash='dotted')
    # fig.vbar(x, 0.5, 'pop_fem', source=source, legend="f", color='red')
    # source.data['dois'] = [[115, 8], [80, 25], [240, 20]]
    # print(source.data)
    # from bokeh.transform import factor_cmap
    # fig.vbar(x='cats', width=0.5, top='tops', source=source, line_color="white",
    #         fill_color=factor_cmap('cats', palette=palette, factors=['pop_masc', 'pop_fem'], start=1, end=2))

    # Bar width including margins
    outer_width = 0.25
    # Painted bar area
    inner_width = outer_width - 0.03
    l = len(ys)
    for y, color, i in zip(ys, palette, range(0, l)):
        # Spreads bars based on the number of bars and their
        # width, so they don't overlap
        offset = round(-outer_width*l/2 + outer_width/2 + outer_width*i, 2)
        legend = y+' ' if l > 1 else None
        fig.vbar(
            x=dodge(x, offset, range=fig.x_range), width=inner_width, top=y,
            source=source, color=color, legend=legend)


def plot_hbar(fig, x, ys, source, palette):
    # fig.hbar(y=y, height=0.5, right=x, left=0, source=source)
    # Bar width including margins
    outer_width = 0.25
    # Painted bar area
    inner_width = outer_width - 0.03
    l = len(ys)
    for y, color, i in zip(ys, palette, range(0, l)):
        offset = round(-outer_width*l/2 + outer_width/2 + outer_width*i, 2)
        legend = y+' ' if l > 1 else None
        fig.hbar(
            y=dodge(x, offset, range=fig.y_range), height=inner_width, right=y,
            source=source, color=color, legend=legend, )


def plot_circles(fig, x, ys, source, palette):
    for y, color in zip(ys, palette):
        legend = y+' ' if len(ys) > 1 else None
        fig.circle(x, y, size=10, source=source, color=color, legend=legend)


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
        if state:
            state = parse_qs(base64.urlsafe_b64decode(state[0]).decode())
        else:
            state = {}

        self.chart_types = {
            'linha': {
                'fn': plot_lines
            },
            'barras horizontais': {
                'fn': plot_hbar,
                'invert_axies': True
            },
            'barras verticais': {
                'fn': plot_vbar
            },
            'círculos': {
                'fn': plot_circles
            },
        }
        charts_names = list(self.chart_types)
        none_value = 'Nenhum'

        self.df = df
        self.doc = doc
        self.columns = sorted(df.columns)
        self.palette = palettes.Dark2_8
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
                'value': ['pop_masc'],
                'options': self.columns,
                'class': MultiSelect,
                # 'multiple': True,
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
                'value': [1, 9],
                'class': RangeSlider,
            },
        }

        # If has a previous state (passed throught querystring)
        # restore it.
        # TODO: validate state? Dangerous?
        if state:
            for gui, data in gui_data.items():
                value = state.get(data['name'])
                if value:
                    value = value[0]
                    if data['name'] == 'f_range':
                        data['value'] = tuple(
                            float(i) for i in value.split(','))
                    elif data['name'] == 'y':
                        data['value'] = value.split(',')
                    else:
                        data['value'] = value

        self.js_update_querytstring = CustomJS.from_py_func(update_querystring)

        # Create gui inputs
        self.controls = {}
        for k, v in gui_data.items():
            v = v.copy()
            class_ = v.pop('class')
            # multiple = v.pop('multiple', None)
            control = self.create_control(class_, v)
            self.controls[k] = control # [control] if multiple else control

        # controls = [getattr(self, k) for k, v in gui_data.items()]

        # for control in controls:
        #     control.on_change('value', self.update)
        #     control.callback = js_update_querytstring

        # TODO: seems to have no effect
        self.controls['filter_range_sel'].callback_policy = 'mouseup'

        # Add one widgetbox for control. Controls with multiple... TODO
        # widgetboxes = [
        #     widgetbox(c, width=200)
        #     if isinstance(c, list) else widgetbox([c], width=200)
        #     for c in self.controls.values()]
        # self.layout = row(column(widgetboxes), self.create_figure())

        self.layout = row(
            widgetbox(list(self.controls.values()), width=200),
            self.create_figure())
        doc.add_root(self.layout)

    def create_control(self, class_, args):
        control = class_(**args)
        # Bind callbacks
        control.on_change('value', self.update)
        control.callback = self.js_update_querytstring
        return control

    def update(self, attr, old, new):
        '''
        Called when chart options are modified.
        '''
        # It seems sometimes, when restoring state, self has no layout.
        # This 'try' avoids that error.
        try:
            self.layout.children[1] = self.create_figure(attr, old, new)
        except AttributeError:
            pass

    def handle_filtering(self, df):
        '''
        Update filter selectors widgets and use their values
        to filter `df`.
        '''
        fs = self.controls['filter_sel']
        frs = self.controls['filter_range_sel']
        fvs = self.controls['filter_value_sel']
        if fs.value != self.filter_options[0]:
            filter_column = df[fs.value]
            if fs.value in self.discrete:
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
                if frs.value[0] < min_val or frs.value[1] > max_val:
                    frs.value = (min_val, max_val)
                frs.step = (max_val-min_val)/10

                show_widget(frs)
                hide_widget(fvs)

                # filter df
                df = df[filter_column >= frs.value[0]]
                df = df[filter_column <= frs.value[1]]
        else:
            # No filter
            hide_widget(fvs)
            # TODO: hide when RangeSlider css_classes work again
            # hide_widget(frs)

        return df

    def create_figure(self, attr=None, old=None, new=None):
        '''
        Creates the chart.
        '''
        df = self.handle_filtering(self.df)
        df = df.groupby(self.controls['x_sel'].value, as_index=False).sum()
        source = ColumnDataSource(data=df)

        # import itertools
        # tops = sum(zip(df['pop_masc'], df['pop_fem']), ())
        # cats = list(itertools.product(df['ano'], ['pop_masc', 'pop_fem']))
        # source = ColumnDataSource(data={'tops':tops, 'cats':cats})

        chart_type_info = self.chart_types[self.controls['chart_type_sel'].value]
        x_value = self.controls['x_sel'].value
        y_values = self.controls['y_sel'].value

        x_title = x_value.title()
        y_title = ', '.join(y.title() for y in y_values)


        kw = dict()
        if x_value in self.discrete:
            kw['x_range'] = sorted(set(df[x_value]))
        # TODO: os dois eixos podem ter valores discretos?
        # TODO: e múltiplos valores discretos no Y? e misto?
        # if y_value in self.discrete:
        #     kw['y_range'] = sorted(set(ys))

        # import IPython;IPython.embed()
        # kw['y_range'] = (0, max(sum(y_values, [])))
        kw['y_range'] = (0, max([max(df[y].values) for y in y_values]))

        if chart_type_info.get('invert_axies'):
            # x_value, y_value = y_value, x_value
            x_title, y_title = y_title, x_title
            kw['x_range'], kw['y_range'] = kw['y_range'], kw['x_range']


        # xs = df[x_value].values
        # ys = df[y_value].values

        # y_values = ['pop_masc', 'pop_fem', 'vagas']
        # y_values = ['pop_masc']


        kw['title'] = "%s vs %s" % (x_title, y_title)

        # from bokeh.models import FactorRange
        # fig = figure(x_range=FactorRange(*cats), plot_height=600, plot_width=800,
        #              tools='pan,box_zoom,reset,save')
        fig = figure(plot_height=600, plot_width=800,
                     tools='pan,box_zoom,reset,save', **kw)
        fig.xaxis.axis_label = x_title
        fig.yaxis.axis_label = y_title
        fig.xgrid.grid_line_color = None
        # fig.x_range.start = 0
        # fig.x_range.end = 100
        # fig.x_range.range_padding = 0.1

        # # TODO: fix needed for hbar, not sure why...
        # if chart_type_info.get('invert_axies'):
        #     fig.x_range.start = 0
        #     fig.x_range.end = xs.max()

        if x_value in self.discrete:
            fig.xaxis.major_label_orientation = pd.np.pi / 4

        chart_type_info['fn'](fig, x_value, y_values, source, self.palette)

        tooltips = [(y, '@'+y) for y in y_values]
        tooltips.insert(0, (x_value, '@'+x_value))

        # ("index", "$index"),
        hover = HoverTool(tooltips=tooltips)
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
