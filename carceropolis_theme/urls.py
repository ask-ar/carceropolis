from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from . import views

urlpatterns = [
    url("^publicacoes/$", views.publicacoes)
]
