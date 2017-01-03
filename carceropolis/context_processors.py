# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from mezzanine.accounts.forms import LoginForm, PasswordResetForm
from mezzanine.accounts import get_profile_form


def add_login_form(request):
    return {'login_form': LoginForm(None)}


def add_registration_form(request):
    profile_form = get_profile_form()
    form = profile_form(None)
    return {'registration_form': form}


def add_password_recover_form(request):
    return {'password_recovery_form': PasswordResetForm(None)}
