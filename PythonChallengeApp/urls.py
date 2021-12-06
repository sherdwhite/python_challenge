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
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
