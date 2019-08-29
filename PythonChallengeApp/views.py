# Django imports for page display
from pyexpat import ExpatError

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Libraries required for data manipulation
import re
import json
import requests
import xmltodict

# Project imports for forms and models
from django.db import IntegrityError
from PythonChallengeApp.forms import FileForm

# Create your views here.  This is where all custom python code should reside for the project.
from PythonChallengeApp.models import IPAddresses


# https://docs.djangoproject.com/en/2.2/topics/http/file-uploads/
def index(request):
    context = {'title': 'Python Challenge Form'}
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            ip_addresses = read_ips_from_file(request.FILES['ip_file'])
            for ip in ip_addresses:
                try:
                    geo_ip_json = get_geo_ip_info(ip)
                    try:
                        geo_ip_result = geo_ip_json['results']['result']
                        IPAddresses.objects.create(ip_address=ip, geo_ip_isp=geo_ip_result['isp'],
                                                   geo_ip_city=geo_ip_result['city'],
                                                   geo_ip_country_code=geo_ip_result['countrycode'],
                                                   geo_ip_country_name=geo_ip_result['countryname'],
                                                   geo_ip_latitude=geo_ip_result['latitude'],
                                                   geo_ip_longitude=geo_ip_result['longitude'])
                    except (AttributeError, TypeError):
                        IPAddresses.objects.create(ip_address=ip)
                except IntegrityError:
                    pass
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
    geo_ip_url = 'http://api.geoiplookup.net/?query={}'.format(ip_address)
    try:
        geo_ip_info = requests.get(geo_ip_url, verify=False, timeout=10)
        if geo_ip_info.status_code == 200:
            geo_ip_content_str = str(geo_ip_info.text)
            geo_ip_dict = xmltodict.parse(geo_ip_content_str)
            geo_ip_json = json.dumps(geo_ip_dict)
        else:
            geo_ip_json = json.dumps({})
    except (ExpatError, ConnectionError):
        geo_ip_json = json.dumps({})
    return geo_ip_json


def results(request):
    ip_addresses = IPAddresses.objects.order_by('ip_address')
    if not ip_addresses:
        ip_addresses = []
    context = {'ip_addresses': ip_addresses, 'title': 'IP Addresses'}
    return render(request, 'PythonChallengeApp/results.html', context)
