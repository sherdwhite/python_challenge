from django.conf.urls import url
from django.urls import include, path
from PythonChallengeApp import views
from rest_framework import routers

# template tagging
app_name = 'PythonChallengeApp'

router = routers.DefaultRouter()
router.register(r'ip_addresses', views.IPAddressViewSet)

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^results/$', views.Results.as_view(), name='results'),
    url(r'^ip_addresses/$', views.IPAddressViewSet, name='ip_addresses'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
