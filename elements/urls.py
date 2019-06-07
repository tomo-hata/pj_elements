from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.hello_world, name='hello_world'),
    url(r'^template/$', views.hello_template, name='hello_template'),
    url(r'^if/$', views.hello_if, name='hello_if'),
    # elements
    url(r'^issueasset/$', views.issueasset, name='issueasset'),
    url(r'^forms/$', views.hello_forms, name='hello_forms'),
    url(r'^models/$', views.elements_models, name='elements_models'),
]
