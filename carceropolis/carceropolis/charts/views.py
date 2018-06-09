from django.template.response import TemplateResponse

from carceropolis.charts.utils import (
    plot_charts, plot_simple_lines, plot_simple_hbar_helper, plot_simple_vbar_helper,
    plot_stacked_hbar_helper)


def dados_gerais(request):
    '''Display the Dados Home page.

    It is a matrix with all available categories (only categories, not the
    items from the Publicação Class).
    '''

    templates = ['carceropolis/dados/dados_gerais.html']
    context = plot_charts('dados_gerais', [
        (plot_simple_lines, '01', {'continuous': True, 'xaxis_tick_interval': 2}),
        (plot_simple_lines, '02', {'xaxis_tick_interval': 2}),
        (plot_simple_hbar_helper, '03'),
        (plot_simple_hbar_helper, '04'),
    ])
    return TemplateResponse(request, templates, context)


def dados_perfil_populacional(request):
    '''Perfil Populacional page'''
    templates = ['carceropolis/dados/perfil_populacional.html']
    context = plot_charts('perfil_populacional', [
        (plot_simple_lines, '01', {'xaxis_tick_interval': 1}),
        (plot_simple_lines, '02', {'xaxis_tick_interval': 1}),
        (plot_simple_vbar_helper, '03_raca_cor',
         {'tooltip_value_sufix': '%'}),
        (plot_simple_vbar_helper, '04_faixa_etaria',
         {'tooltip_value_sufix': '%'}),
    ])
    return TemplateResponse(request, templates, context)


def dados_infraestrutura(request):
    templates = [u'carceropolis/dados/infraestrutura.html']
    context = plot_charts('infraestrutura', [
        (plot_simple_hbar_helper, '01_ocupacao', {'xaxis_tick_interval': .5}),
        (plot_simple_hbar_helper, '02_deficit_vagas'),
        (plot_simple_hbar_helper, '03_coeficiente_entradas_saidas'),
        (plot_simple_hbar_helper, '04_proporcao_agentes_pessoas_presas'),
    ])
    return TemplateResponse(request, templates, context)


def dados_juridico(request):
    templates = [u'carceropolis/dados/juridico.html']
    context = plot_charts('juridico', [
        (plot_simple_hbar_helper, '01_incidencias_criminais_por_sexo',
         {'width': .3, 'tooltip_value_sufix': '%'}),
        (plot_simple_hbar_helper, '02_percentual_presos_sem_condenacao',
         {'tooltip_value_sufix': '%'}),
        (plot_simple_hbar_helper, '03_percentual_unidades_com_visitacao',
         {'tooltip_value_sufix': '%', 'xaxis_tick_interval': 10}),
        (plot_simple_hbar_helper, '04_regimes_de_cumprimento_de_pena',
         {'width': .3, 'tooltip_value_sufix': '%'}),
    ])
    return TemplateResponse(request, templates, context)


def dados_educacao(request):
    templates = [u'carceropolis/dados/educacao.html']
    context = plot_charts('educacao', [
        (plot_simple_hbar_helper, '01_percentual_pessoas_trabalhando',
         {'tooltip_value_sufix': '%'}),
        (plot_simple_hbar_helper, '02_percentual_menos_de_34_de_SM',
         {'tooltip_value_sufix': '%', 'xaxis_tick_interval': 10}),
        (plot_simple_hbar_helper, '03_percentual_pessoas_estudando',
         {'tooltip_value_sufix': '%', 'xaxis_tick_interval': 5}),
        (plot_simple_hbar_helper, '04_escolaridade',
         {'tooltip_value_sufix': '%', 'width': .4, 'xaxis_tick_interval': 10}),
    ])
    return TemplateResponse(request, templates, context)


def dados_saude(request):
    templates = [u'carceropolis/dados/saude.html']
    context = plot_charts('saude', [
        (plot_simple_hbar_helper, '01_pessoas_com_agravo'),
        (plot_stacked_hbar_helper, '03_obitos_sistema_prisional',
         {'xaxis_tick_interval': 50}),
        (plot_simple_hbar_helper, '02_taxa_obitos', {'xaxis_tick_interval': 5}),
        (plot_simple_hbar_helper, '04_relacao_funcionarios_pessoas_presas',
         {'xaxis_tick_interval': 5}),
    ])
    return TemplateResponse(request, templates, context)


def dados_materno_infantil(request):
    templates = [u'carceropolis/dados/materno_infantil.html']
    context = plot_charts('materno', [
        (plot_simple_hbar_helper, '03_total_gestantes_lactantes_por_UF'),
        (plot_stacked_hbar_helper, '01_percentual_gestantes',
         {'tooltip_value_sufix': '%', 'xaxis_tick_interval': 10}),
        (plot_simple_hbar_helper, '02_total_criancas',
         {'tooltip_value_format': '0,0', 'xaxis_tick_interval': 100}),
        (plot_simple_hbar_helper, '04_percentual_unidades_com_crmi_por_UF',
         {'tooltip_value_sufix': '%'}),
    ])
    return TemplateResponse(request, templates, context)


def dados_alas_exclusivas(request):
    templates = [u'carceropolis/dados/alas_exclusivas.html']
    context = plot_charts('alas_exclusivas', [
        (plot_simple_hbar_helper, '01_percentual_ala_cela_lgbt',
         {'tooltip_value_sufix': '%'}),
        (plot_simple_hbar_helper, '02_percentual_ala_cela_idosos',
         {'tooltip_value_sufix': '%'}),
        (plot_simple_hbar_helper, '03_percentual_ala_cela_indigenas',
         {'tooltip_value_sufix': '%'}),
        (plot_simple_hbar_helper, '04_percentual_ala_cela_estrangeiros',
         {'tooltip_value_sufix': '%'}),
        (plot_simple_hbar_helper,
         '05_percentual_pessoas_com_deficiencia_fisica_desassistidas_de_vagas_adaptadas',
         {'tooltip_value_sufix': '%'}),
    ])
    return TemplateResponse(request, templates, context)
