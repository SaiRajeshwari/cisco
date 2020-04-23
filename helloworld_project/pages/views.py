from django.shortcuts import render_to_response
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

# Create your views here.

def homePageView(request):
    client = Elasticsearch(['http://elasticsearch:9200'])
    s = Search(using=client, index='logstash', doc_type='jenkins')
    response = s.execute()

    helloflask = {'count':0, 'success':0, 'failure':0, 'jobs':[], 'cmds':[]}
    dummy = {'count':0, 'success':0, 'failure': 0, 'jobs':[], 'cmds':[]}
    i = 0
    j = 0

    for hit in response:
        if(hit.data.projectName == 'helloflask'):
            helloflask['count'] += 1
            helloflask['jobs'].append(hit.data.id)
            if(hit.data.result.lower() != 'failure'):
                helloflask['success'] += 1
            else:
                helloflask['failure'] += 1
            if(i == 0):
                messages = hit.message
                helloflask['cmds'] = [m for m in messages if len(m)>2 and m[0]=='+']
                i = 1

        else:
            dummy['count'] += 1
            dummy['jobs'].append(hit.data.id)
            if(hit.data.result.lower() != 'failure'):
                dummy['success'] += 1
            else:
                dummy['failure'] += 1
            if(j == 0):
                messages = hit.message
                dummy['cmds'] = [m for m in messages if len(m)>2 and m[0]=='+']
                j = 1

    labels = ['Success', 'Failure']
    data_helloflask = [helloflask['success'], helloflask['failure']]
    data_dummy = [dummy['success'], dummy['failure']]

    hf_success = helloflask['success']/(helloflask['count'])
    dummy_success = dummy['success']/(dummy['count'])
    return render_to_response('pages/base.html', {'labels': labels,
                                                  'data_helloflask': data_helloflask,
                                                  'data_dummy': data_dummy,
                                                  'hf_jobs': helloflask['jobs'],
                                                  'dummy_jobs': dummy['jobs'],
                                                  'hf_cmds': helloflask['cmds'],
                                                  'dummy_cmds': dummy['cmds'],
                                                  'success_percentages': [hf_success*100, dummy_success*100]})

