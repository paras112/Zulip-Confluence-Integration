from django.shortcuts import render
import requests
import json
import zulip
from .models import ConfluenceData
from django.http import HttpResponse
# Create your views here.
def home(request):
    return(render(request,'core/home_1.html',{}))

def confluence_api(request):
    #In this i use ajax now but for realtime we use tornado server
    response={"status":False}
    if request.is_ajax:
        # use rest api to fetch data from confluence here
        # in authentication we provide confluence api token and then username
        params = (
            ('type', 'page'),
            # ('start', '0'),
            # ('limit', '10'),
            # ('expand', 'page'),
        )
        response = requests.get('https://paras112.atlassian.net/wiki/rest/api/content', params=params, auth=('xxx@gmail.com', 'xxxx'))
        res=response.json()
        ## length of json data
        l=len(res['results'])
        print(l)
        
        ## Fetch value from database models
        field_name = 'data'
        obj = ConfluenceData.objects.first()
        length_confluence_data = getattr(obj, field_name)
        # print(res['results'][l-1])
        #compare the lenth of json from database to the new length of json which is fetch from api
        #if length of fetch json from api  is greater than save length then we call zulip api
        # for i in range(l):
        # print(length_confluence_data)
        # print(res['results'][19])
        print(res['results'][l-1]['title'])
        if(l>length_confluence_data):
            test1_json=(res['results'][l-1]['_links']['webui'])
            title=res['results'][l-1]['title']

            get_spaces_and_pages=spacepage(test1_json)
            format_page_and_string="New {} is created with title {}".format(get_spaces_and_pages,title)
            client = zulip.Client(config_file="/home/paras/Downloads/zuliprc")
            request = {
            "type": "stream",
            "to": "confluence",
            "subject": "Page",
            "content": format_page_and_string
            }
            result = client.send_message(request)
            t = ConfluenceData.objects.get(id=1)
            t.data =l # change field
            t.save()
        elif(l<length_confluence_data):
            t = ConfluenceData.objects.get(id=1)
            t.data =l # change field
            t.save()
        response={'status':True}
        return HttpResponse(json.dumps(response))

def spacepage(get_spaces_and_pages):
    page_space=get_spaces_and_pages.split('/')
    if('pages' in page_space):
        return('page')
    else:
        return("space")