# Django imports for page display
from django.http import HttpResponseRedirect
from django.shortcuts import render

# General imports
import re
import json
import requests

# Project imports for exceptions
from django.db import IntegrityError
from urllib3.exceptions import ConnectTimeoutError
from pyexpat import ExpatError

# Project imports for forms and models
from PythonChallengeApp.forms import FileForm
from PythonChallengeApp.models import IPAddresses


# Create your views here.  This is where all custom python code should reside for the project.
# https://docs.djangoproject.com/en/2.2/topics/http/file-uploads/
def index(request):
    context = {'title': 'Python Challenge Form'}
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            ip_addresses = read_ips_from_file(request.FILES['ip_file'])
            count = 0
            for ip in ip_addresses:
                geo_ip_json = get_geo_ip_info(ip)
                print('city: {0}, count: {1}'.format(geo_ip_json.get('city'), count))
                count += 1
                if bool(geo_ip_json):
                    try:
                        IPAddresses.objects.create(ip_address=ip,
                                                   geo_ip_city=geo_ip_json.get('city'),
                                                   geo_ip_country_code=geo_ip_json.get('country_code'),
                                                   geo_ip_country_name=geo_ip_json.get('country_name'),
                                                   geo_ip_latitude=geo_ip_json.get('latitude'),
                                                   geo_ip_longitude=geo_ip_json.get('longitude'))
                    except (AttributeError, TypeError, IntegrityError):
                        if IntegrityError:
                            address = IPAddresses.objects.get(ip_address=ip)
                            try:
                                address.geo_ip_city = geo_ip_json.get('city'),
                                address.geo_ip_country_code = geo_ip_json.get('country_code'),
                                address.geo_ip_country_name = geo_ip_json.get('country_name'),
                                address.geo_ip_latitude = geo_ip_json.get('latitude'),
                                address.geo_ip_longitude = geo_ip_json.get('longitude')
                            except (AttributeError, TypeError):
                                pass
                            address.save()
                else:
                    IPAddresses.objects.create(ip_address=ip)
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
            geo_ip_json = json.loads(geo_ip_info.text)
        else:
            geo_ip_json = json.dumps({})
    except (ExpatError, requests.exceptions.ConnectionError, ConnectTimeoutError):
        geo_ip_json = json.dumps({})
    return geo_ip_json


def results(request):
    ip_addresses = IPAddresses.objects.order_by('ip_address')
    if not ip_addresses:
        ip_addresses = []
    context = {'ip_addresses': ip_addresses, 'title': 'IP Addresses'}
    return render(request, 'PythonChallengeApp/results.html', context)
