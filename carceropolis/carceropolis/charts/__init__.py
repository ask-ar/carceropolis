# import os
# import importlib

# from bokeh.resources import CDN

# '''
# Loads all files in this folder not starting with '__' as a chart context.
# They must have a "get_context" function that creates the context that
# will be passed to a view render.
# In views use it like:
# from carceropolis import charts
# render(charts.dados_gerais)
# '''

# for filename in os.listdir(os.path.dirname(os.path.abspath(__file__))):
#     if not filename.startswith('__'):
#         module_name = filename.rpartition('.')[0]
#         module = importlib.import_module(
#             'carceropolis.charts.%s' % module_name)
#         globals()[module_name] = module.get_context()


# def get_context(module_name):
#     ''' Returns the context to render a chart page. '''
#     context = importlib.import_module(
#         'carceropolis.charts.%s' % module_name).get_context()

#     # TODO: As duas linhas abaixo carregam o Bokeh de um CDN. Mas o
#     # dashboard carrega de arquivos locais, logo não vão utilizar a mesma
#     # cache. Talvez seja bom melhorar isso.
#     context['bokeh_js'] = CDN.render_js()
#     context['bokeh_css'] = CDN.render_css()
#     return context
