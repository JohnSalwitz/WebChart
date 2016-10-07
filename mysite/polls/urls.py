__author__ = 'John'

from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),

    # ex: /charts
    url(r'^charts/$', TemplateView.as_view(template_name="polls/charts.html")),

    # ex: /polls/5/my_json/
    url(r'^(?P<question_id>[0-9]+)/my_json/$', views.my_json, name='my_json'),
]


# sample...
# url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),