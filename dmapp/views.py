from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.conf import settings
from .forms import ArtefactForm
import requests
import json
import os

# Reading configuration file
configFilePath = os.path.join(settings.BASE_DIR, 'dmconfig.json') 
print (configFilePath)
with open(configFilePath, 'r') as conFile:
        dmConfig = json.load(conFile)

# Define constants
CLIENT_ID = dmConfig['DEFAULT']['CLIENT_ID'] 
CLIENT_SECRET = dmConfig['DEFAULT']['CLIENT_SECRET'] 
API_BASE_URL = dmConfig['DEFAULT']['API_BASE_URL'] 
DT_URL = dmConfig['DEFAULT']['DT_URL'] 
REPO_API_BASE_URL = dmConfig['DEFAULT']['REPO_API_BASE_URL']
REPOSITORY = dmConfig['DEFAULT']['REPOSITORY']
# ------------------
        
class DMDashboardPageView(TemplateView):
   # access_token = ''
    def get(self, request, **kwargs):
        
        # Obtain the necessary information from request meta
        url_scheme = request.META['REQUEST_SCHEME']
        url_server_name = request.META['SERVER_NAME']
        access_token = request.META['OIDC_access_token']
        id_token = request.META['OIDC_id_token']
        refresh_token = request.META['OIDC_refresh_token']

        user_name = request.META['OIDC_CLAIM_preferred_username']
        dm_link = DT_URL + access_token

        # Compose logout Link        
        logout_link = url_scheme + "://" + url_server_name + "/dmapp/redirect_uri?logout=" + url_scheme + "://" + url_server_name
        

        # call /userinfo/ CFGUM API.
        api_URL = API_BASE_URL + '/userinfo/' + access_token + '?client_id=' + CLIENT_ID + '&CLIENT_SECRET=' + CLIENT_SECRET
        user_info_dict = self.call_userinfo(api_URL)
       
        # call /artefacts/ REPO API.
        list_artefacts = self.call_listartefacts()

        # Check, if url contains query string params {There will querystring parameters, when the user wants to delete an artefact.}
        art_op_resp_dict={}
        if 'status_code' in request.GET and 'message' in request.GET:
            art_op_resp_dict={'status_code':request.GET['status_code'],'message':request.GET['message']}

        form = ArtefactForm()

        # Prepare context.
        c={'form': form,'accessToken': access_token,'idToken': id_token,'refreshToken': refresh_token,
        'userName':user_name,'dmLink':dm_link,'userInfoDict': user_info_dict,'logoutLink': logout_link,
        'list_artefacts':list_artefacts,'art_op_resp_dict':art_op_resp_dict}
        return render(request, 'dashboard.html', context=c)

    def post(self, request, **kwargs):
        access_token = request.META['OIDC_access_token']
        if request.method == 'POST':
            form = ArtefactForm(request.POST)
            if form.is_valid():
                art_id = form.cleaned_data['artefactid']
                art_op_resp_dict = self.call_delete_artefacts(access_token,art_id)
            else:
                art_op_resp_dict = {'info': 'form is not valid'}
        return redirect('/dmapp/dashboard?status_code=' + art_op_resp_dict['status_code'] +'&message=' + art_op_resp_dict['message'])
        

    def call_userinfo(self,apiURL):
        userInfoResp = requests.get(apiURL)
        userInfoDict=userInfoResp.json()  #json.loads(userInfoResp.content)
        return userInfoDict

    def call_listartefacts(self):
        api_URL = REPO_API_BASE_URL + '/artefacts?repository=' + REPOSITORY
        resp = requests.get(api_URL)
        list_artefacts = []
        if resp.status_code == 200:
            loaded_json = resp.json()
            list_artefacts = []
            for x in loaded_json['items']:
                cfg_dict = x['cfg']
                dict_item = {'id':x['id'],'version':cfg_dict['version'],'engineid':cfg_dict['engineId'],
                'groupid':cfg_dict['groupId'],'downloadurl':x['downloadUrl']}
                list_artefacts.append(dict_item)
        return list_artefacts

    def call_delete_artefacts(self,access_token,artefact_id):
        api_URL = REPO_API_BASE_URL + '/artefacts/' + artefact_id + '?access_token=' + access_token
        resp = requests.delete(api_URL)
        if resp.status_code == 204:
            mess_dict = {'status_code':'204','message':'OK: Request was successful'} 
        else:
            mess_dict = {'status_code':str(resp.status_code),'message':'Request was not successful. '}
        return mess_dict
