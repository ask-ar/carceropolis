# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-07 13:51
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carceropolis', '0012_dadosencarceramento_card'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dadosencarceramento',
            name='card',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
        migrations.AlterField(
            model_name='dadosencarceramento',
            name='dados',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
    ]
