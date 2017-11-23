from django.shortcuts import render
import json
from webdike.models import *

def base(request):
    return render(request, 'base.html')

def home(request):
    judgements = Document.objects.all()
    resp = []
    for j in judgements:
        resp.append({
            "id": j.id,
            "title": j.title
        })
    return render(request, 'home.html', { 'json_resp': json.dumps(resp) })

def get_judgement(request, jnum):
    doc = Document.objects.get(id=jnum)
    sentences = Sentence.objects.filter(document__id=jnum)
    resp = {
        'title': doc.title,
        'desc': doc.description,
        'sentences': [{'id': s.id, 'text': s.content } for s in sentences]
    }
    return render(request, 'judgement.html', { 'json_resp': json.dumps(resp) })

def get_splitter(request, sentence_id):
    sentence = Sentence.objects.get(id=sentence_id)
    resp = {
        'id': sentence.id,
        'text': sentence.content,
    }
    return render(request, 'split.html', { 'json_resp': json.dumps(resp) })

def get_polisher(request, step_id):
    # TODO use model and split number
    return render(request, 'polish.html')

def get_connector(request, step_id):
    # TODO use model and split number
    return render(request, 'connect.html')

def get_explainer(request, step_id):
    # TODO use model and split number
    return render(request, 'explain.html')

def get_voter(request, step_id1, step_id2):
    # TODO use model and split numbers
    return render(request, 'vote.html')
