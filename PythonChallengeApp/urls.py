from django.conf.urls import url
from PythonChallengeApp import views

# template tagging
app_name = 'PythonChallengeApp'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^results/$', views.results, name='results'),
]
