# Django and rest imports
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q

from rest_framework import viewsets

# General imports
import re
import json
import requests

# Project imports for exceptions
from django.db import IntegrityError
from urllib3.exceptions import ConnectTimeoutError
from pyexpat import ExpatError

# Project imports for forms, models, serializers
from PythonChallengeApp.forms import FileForm
from PythonChallengeApp.models import IPAddressInfo
from PythonChallengeApp.serializers import IPInfoSerializer


# Create your views here.  This is where all custom python code should reside for the project.
# https://docs.djangoproject.com/en/2.2/topics/http/file-uploads/
def index(request):
    context = {'title': 'Python Challenge Form'}
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            ip_addresses = read_ips_from_file(request.FILES['ip_file'])
            for ip in ip_addresses:
                geo_ip_dict = get_geo_ip_info(ip)
                if bool(geo_ip_dict):
                    try:
                        ip_info = IPAddressInfo()
                        ip_info.ip_address = ip
                        ip_info.geo_ip_city = geo_ip_dict.get('city', 'None')
                        ip_info.geo_ip_country_code = geo_ip_dict.get('country_code', 'None')
                        ip_info.geo_ip_country_name = geo_ip_dict.get('country_name', 'None')
                        ip_info.geo_ip_latitude = geo_ip_dict.get('latitude', 'None')
                        ip_info.geo_ip_longitude = geo_ip_dict.get('longitude', 'None')
                        ip_info.save()
                    except (AttributeError, TypeError, IntegrityError):
                        if IntegrityError:
                            address = IPAddressInfo.objects.get(ip_address=ip)
                            try:
                                address.geo_ip_city = geo_ip_dict.get('city')
                                address.geo_ip_country_code = geo_ip_dict.get('country_code')
                                address.geo_ip_country_name = geo_ip_dict.get('country_name')
                                address.geo_ip_latitude = geo_ip_dict.get('latitude')
                                address.geo_ip_longitude = geo_ip_dict.get('longitude')
                            except (AttributeError, TypeError):
                                pass
                            address.save()
                else:
                    IPAddressInfo.objects.create(ip_address=ip)
            return render(request, 'PythonChallengeApp/results.html')
    else:
        form = FileForm()
        context = {'title': 'Python Challenge Form', 'form': form}
    return render(request, 'PythonChallengeApp/index.html', context)


def read_ips_from_file(ip_file):
    data = ""
    for chunk in ip_file.chunks():
        data += str(chunk)
    ip_regex = r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})'
    ip_addresses = re.findall(ip_regex, data)
    return ip_addresses


def get_geo_ip_info(ip_address):
    geo_ip_url = 'http://api.ipstack.com/{}?access_key=c2ca6e08e41d2059cb9f81db0cd24f05'.format(ip_address)
    try:
        geo_ip_info = requests.get(geo_ip_url, timeout=10)
        if geo_ip_info.status_code == 200:
            geo_ip_dict = json.loads(geo_ip_info.text)
        else:
            geo_ip_dict = json.dumps({})
    except (ExpatError, requests.exceptions.ConnectionError, ConnectTimeoutError):
        geo_ip_dict = json.dumps({})
    return geo_ip_dict


class Results(ListView):
    context_object_name = 'ip_addresses'  # will now return gauges instead of gauges_list
    model = IPAddressInfo  # will return list called gauges_list if no context_object_name declared
    ordering = ['ip_address']
    template_name = 'PythonChallengeApp/results.html'

    def get_queryset(self):
        query = self.request.GET.get('ip_address', None)
        if query:
            addresses = IPAddressInfo.objects.filter(
                Q(ip_address__icontains=query)
            ).order_by('ip_address')
        else:
            addresses = IPAddressInfo.objects.order_by('ip_address')
        return addresses


class IPAddressViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows IP's to be viewed.
    """
    queryset = IPAddressInfo.objects.all().order_by('ip_address')
    serializer_class = IPInfoSerializer
