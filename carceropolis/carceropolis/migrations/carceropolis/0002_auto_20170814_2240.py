# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-08-15 01:40
from __future__ import unicode_literals

import carceropolis.options
import carceropolis.validators
from django.db import migrations, models
from django_extensions.db.fields import AutoSlugField
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carceropolis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='areadeatuacao',
            name='descricao',
            field=models.TextField(verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='areadeatuacao',
            name='nome',
            field=models.CharField(max_length=250, unique=True, verbose_name='Nome da área'),
        ),
        migrations.AlterField(
            model_name='areadeatuacao',
            name='ordem',
            field=models.IntegerField(unique=True, verbose_name='Ordem'),
        ),
        migrations.AlterField(
            model_name='areadeatuacao',
            name='slug',
            field=AutoSlugField(editable=False, populate_from='nome'),
        ),
        migrations.AlterField(
            model_name='arquivobasecarceropolis',
            name='arquivo',
            field=models.FileField(upload_to='base_bruta_carceropolis/', validators=[carceropolis.validators.check_filetype]),
        ),
        migrations.AlterField(
            model_name='arquivobasecarceropolis',
            name='mes',
            field=models.CharField(choices=[('Janeiro', 'Janeiro'), ('Fevereiro', 'Fevereiro'), ('Março', 'Março'), ('Abril', 'Abril'), ('Maio', 'Maio'), ('Junho', 'Junho'), ('Julho', 'Julho'), ('Agosto', 'Agosto'), ('Setembro', 'Setembro'), ('Outubro', 'Outubro'), ('Novembro', 'Novembro'), ('Dezembro', 'Dezembro')], default=carceropolis.options.current_month, max_length=40, verbose_name='Mês'),
        ),
        migrations.AlterField(
            model_name='arquivobasecarceropolis',
            name='salvo_em',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Salvo em'),
        ),
        migrations.AlterField(
            model_name='basemj',
            name='arquivo',
            field=models.FileField(upload_to='base_bruta_mj/', validators=[carceropolis.validators.check_filetype]),
        ),
        migrations.AlterField(
            model_name='basemj',
            name='mes',
            field=models.CharField(choices=[('Janeiro', 'Janeiro'), ('Fevereiro', 'Fevereiro'), ('Março', 'Março'), ('Abril', 'Abril'), ('Maio', 'Maio'), ('Junho', 'Junho'), ('Julho', 'Julho'), ('Agosto', 'Agosto'), ('Setembro', 'Setembro'), ('Outubro', 'Outubro'), ('Novembro', 'Novembro'), ('Dezembro', 'Dezembro')], default=carceropolis.options.current_month, max_length=40, verbose_name='Mês'),
        ),
        migrations.AlterField(
            model_name='basemj',
            name='salvo_em',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Salvo em'),
        ),
        migrations.AlterField(
            model_name='especialidade',
            name='descricao',
            field=models.TextField(blank=True, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='especialidade',
            name='nome',
            field=models.CharField(max_length=80, unique=True, verbose_name='Nome da especialidade'),
        ),
        migrations.AlterField(
            model_name='especialidade',
            name='slug',
            field=AutoSlugField(editable=False, populate_from='nome'),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='area_de_atuacao',
            field=models.ManyToManyField(to='carceropolis.AreaDeAtuacao', verbose_name='Área de atuação'),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='ddd',
            field=models.IntegerField(blank=True, null=True, verbose_name='DDD'),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='ddi',
            field=models.IntegerField(blank=True, default=55, null=True, verbose_name='DDI'),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='instituicao',
            field=models.CharField(max_length=250, verbose_name='Instituição'),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='telefone',
            field=models.IntegerField(blank=True, null=True, verbose_name='Telefone'),
        ),
        migrations.AlterField(
            model_name='publicacao',
            name='ano_de_publicacao',
            field=models.IntegerField(choices=[(1900, 1900), (1901, 1901), (1902, 1902), (1903, 1903), (1904, 1904), (1905, 1905), (1906, 1906), (1907, 1907), (1908, 1908), (1909, 1909), (1910, 1910), (1911, 1911), (1912, 1912), (1913, 1913), (1914, 1914), (1915, 1915), (1916, 1916), (1917, 1917), (1918, 1918), (1919, 1919), (1920, 1920), (1921, 1921), (1922, 1922), (1923, 1923), (1924, 1924), (1925, 1925), (1926, 1926), (1927, 1927), (1928, 1928), (1929, 1929), (1930, 1930), (1931, 1931), (1932, 1932), (1933, 1933), (1934, 1934), (1935, 1935), (1936, 1936), (1937, 1937), (1938, 1938), (1939, 1939), (1940, 1940), (1941, 1941), (1942, 1942), (1943, 1943), (1944, 1944), (1945, 1945), (1946, 1946), (1947, 1947), (1948, 1948), (1949, 1949), (1950, 1950), (1951, 1951), (1952, 1952), (1953, 1953), (1954, 1954), (1955, 1955), (1956, 1956), (1957, 1957), (1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017)], default=carceropolis.options.current_year, verbose_name='Ano de publicação'),
        ),
        migrations.AlterField(
            model_name='publicacao',
            name='arquivo_publicacao',
            field=models.FileField(upload_to='publicacoes/', verbose_name='Arquivo da publicação'),
        ),
        migrations.AlterField(
            model_name='publicacao',
            name='autoria',
            field=models.CharField(max_length=150, verbose_name='Autoria'),
        ),
        migrations.AlterField(
            model_name='publicacao',
            name='categorias',
            field=models.ManyToManyField(to='carceropolis.AreaDeAtuacao', verbose_name='Categorias'),
        ),
        migrations.AlterField(
            model_name='unidadeprisional',
            name='ddd',
            field=models.IntegerField(blank=True, null=True, verbose_name='DDD'),
        ),
        migrations.AlterField(
            model_name='unidadeprisional',
            name='municipio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cidades.Cidade', verbose_name='Município'),
        ),
        migrations.AlterField(
            model_name='unidadeprisional',
            name='nome_unidade',
            field=models.CharField(max_length=255, verbose_name='Nome da Unidade'),
        ),
        migrations.AlterField(
            model_name='unidadeprisional',
            name='numero',
            field=models.IntegerField(blank=True, null=True, verbose_name='Número'),
        ),
        migrations.AlterField(
            model_name='unidadeprisional',
            name='uf',
            field=models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2),
        ),
    ]
