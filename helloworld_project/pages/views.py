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


    # res = []
    # for hit in response:
    #     # res.append(str(hit.meta.id))
    #     res.append(str(hit.data.id))
    #     res.append(str(hit.data.projectName))
    #     res.append(str(hit.data.result))
    #     l = [item for item in hit.message if len(item)>1 and item[0]=='+']
    #     res.append(l)
    # return render_to_response('pages/base.html', {'jenkins_data': res})

    # projects = set()
    # for hit in response:
    #     projects.add(hit.data.projectName)
    # return render_to_response('pages/base.html', {'jenkins_data': projects})

    helloflask = {'count':0, 'success':0, 'failure':0}
    dummy = {'count':0, 'success':0, 'failure': 0}
    i = 0
    for hit in response:
        if(hit.data.projectName == 'helloflask'):
            helloflask['count'] += 1
            if(hit.data.result.lower() != 'failure'):
                helloflask['success'] += 1
            else:
                helloflask['failure'] += 1

        else:
            dummy['count'] += 1
            if(hit.data.result.lower() != 'failure'):
                dummy['success'] += 1
            else:
                dummy['failure'] += 1

    # return render_to_response('pages/base.html', {'jenkins_data': [helloflask['count'], helloflask['success'], dummy['count'], dummy['success']]})
    labels = ['Success', 'Failure']
    data_helloflask = [helloflask['success'], helloflask['failure']]
    data_dummy = [dummy['success'], dummy['failure']]
    return render_to_response('pages/base.html', {'labels': labels, 'data_helloflask': data_helloflask, 'data_dummy': data_dummy})

