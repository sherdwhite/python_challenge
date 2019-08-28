# Django imports for page display
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Libraries required for data manipulation
import re
import json
import requests

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
            print("form valid")
            ip_addresses = read_ips_from_file(request.FILES['ip_file'])
            ip_addresses.sort()
            context = {'title': 'IP Addresses', 'ip_addresses': ip_addresses}
            return render(request, 'PythonChallengeApp/results.html', context)
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
    for ip in ip_addresses:
        try:
            IPAddresses.objects.create(ip_address=ip)
        except IntegrityError as ex:
            if 'unique constraint' in ex.message:
                pass
    return ip_addresses


def results(request):
    ip_addresses = IPAddresses.objects.order_by('ip_address')
    if not ip_addresses:
        ip_addresses = []
    context = {'ip_addresses': ip_addresses, 'title': 'IP Addresses'}
    return render(request, 'PythonChallengeApp/results.html', context)
