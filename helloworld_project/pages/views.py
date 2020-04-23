from django.http import HttpResponse
from django.shortcuts import render_to_response
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

# Create your views here.

def homePageView(request):
    # return HttpResponse('Hello World')

    client = Elasticsearch(['http://elasticsearch:9200'])
    s = Search(using=client, index='logstash', doc_type='jenkins')
    response = s.execute()
    res = []
    for hit in response:
        res.append(str(hit.meta.id))
        res.append(str(hit.data.id))
        res.append(str(hit.data.projectName))
    return render_to_response('pages/base.html', {'jenkins_data': ' : '.join(res)})

