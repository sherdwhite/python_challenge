# Django imports for page display
# Libraries required for data manipulation
import json
import requests
from django.shortcuts import render

# Project imports for forms and models
from PythonChallengeApp.forms import FileForm


# Create your views here.  This is where all custom python code should reside for the project.

def index(request):
    form = FileForm()
    names = []
    if request.method == 'POST':
        form = FileForm(request.POST)
        if form.is_valid():
            ip_file = request.FILES.get('ip_file')
            ip_addresses = read_ips_from_file(ip_file)
            return_dict = {'title': 'Python Challenge Form',
                           'ip_addresses': ip_addresses}
        # else:
        # print("Form input invalid.")
    else:
        return_dict = {'title': 'Python Challenge Form'}
        return render(request, 'PythonChallengeApp/index.html', return_dict)


def read_ips_from_file(ip_file):
    return []
