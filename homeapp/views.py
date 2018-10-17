from django.shortcuts import render
from django.views.generic import TemplateView
from django.template import Template, Context
from .forms import RegForm
from django.conf import settings
import requests
import json
import os

# Reading configuration file
configFilePath =  os.path.join(settings.BASE_DIR, 'dmconfig.json') 
print (configFilePath)
with open(configFilePath, 'r') as conFile:
        dmConfig = json.load(conFile)

# Define constants
CLIENT_ID = dmConfig['DEFAULT']['CLIENT_ID'] 
CLIENT_SECRET = dmConfig['DEFAULT']['CLIENT_SECRET'] 
API_BASE_URL = dmConfig['DEFAULT']['API_BASE_URL'] 
DT_URL = dmConfig['DEFAULT']['DT_URL'] 
# ------------------

# Index/Home Page.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        getDict = request.GET
        for key in getDict:
                print (getDict[key])
        c={'metaDict': request.META,'getDict': request.GET}
        return render(request, 'index.html', context=c)

# Register Page.
class RegisterPageView(TemplateView):
    def get(self, request, **kwargs):
        infoDict = {'info':'Fill the following form to register'}
        form = RegForm()
        c={'form': form,'infoDict': infoDict}
        return render(request, 'register.html', context=c)

    def post(self, request, **kwargs):
        infoDict = {'info': 'post method'}
        if request.method == 'POST':
            form = RegForm(request.POST)
            if form.is_valid():
                inputData = {"username": form.cleaned_data['username'] ,"password": form.cleaned_data['password'],"firstname": form.cleaned_data['firstname'],"lastname": form.cleaned_data['lastname'] ,"email": form.cleaned_data['email']}
                apiURL = API_BASE_URL + '/users'
                result = requests.post(apiURL, json=inputData)
                infoDict=result.json()
            else:
                infoDict = {'info': 'form is not valid'}
        form=RegForm()	
        c={'form': form, 'infoDict': infoDict}
        return render(request, 'register.html', context=c)

