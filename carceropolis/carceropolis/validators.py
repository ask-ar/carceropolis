# coding= utf-8
"""Validators for carceropolis models"""
import os
from django.core.exceptions import ValidationError


def check_filetype(value):
    ext = os.path.splitext(value.name)[1]
    formats = ['.csv', '.ods', '.xlsx', '.xls']
    if ext not in formats:
        raise ValidationError('O formato do arquivo deve ser "csv", "ods", '
                              '"xls" ou "xlsx".')
