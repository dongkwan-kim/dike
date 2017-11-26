from django.shortcuts import render
from django.http import Http404, JsonResponse
import json
from .models import *


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
    return render(request, 'home.html', {'json_resp': json.dumps(resp)})


def get_judgement(request, jnum):
    doc = Document.objects.get(id=jnum)
    sentences = Sentence.objects.filter(document__id=jnum)
    resp = {
        'title': doc.title,
        'desc': doc.description,
        'sentences': [{'id': s.id, 'text': s.content} for s in sentences]
    }
    return render(request, 'judgement.html', {'json_resp': json.dumps(resp)})


def get_splitter(request, sentence_id):
    sentence = Sentence.objects.get(id=sentence_id)
    resp = {
        'id': sentence.id,
        'text': sentence.content,
    }
    return render(request, 'split.html', {'json_resp': json.dumps(resp)})


def get_polisher(request, step_id):
    parent_step = Step.objects.get(id=step_id).to_dict()
    # TODO use model and split number
    return render(request, 'polish.html', {'json_resp': json.dumps(parent_step)})


def get_connector(request, step_id):
    parent_step = Step.objects.get(id=step_id).to_dict()
    return render(request, 'connect.html', {'json_resp': json.dumps(parent_step)})


def get_explainer(request, step_id):
    parent_step = Step.objects.get(id=step_id).to_dict()
    return render(request, 'explain.html', {'json_resp': json.dumps(parent_step)})


def save_step(request, stage):
    payloads = json.loads(request.body)
    parent_step_id = payloads.get("parent_step_id", None)
    try:
        result = payloads["result"]
    except Exception:
        print('err!!')
        raise Http404("Failed to parse result")
    new_step = Step.objects.create(
        stage=stage,
        result=result,
        sentence_id = payloads["sentence_id"]
    )
    if parent_step_id:
        new_step.parent_step_id = parent_step_id
    new_step.save()

    # TODO Check it's redirecting to correct page
    return JsonResponse({"redirect": "/"})


def handle_vote(request):
    if request.method == "POST":
        return save_vote(request)
    else:
        return get_vote(request)


def get_vote(request):
    step1_id = int(request.GET['step1'])
    step2_id = int(request.GET['step2'])
    step1 = Step.objects.get(id=step1_id).to_dict()
    step2 = Step.objects.get(id=step2_id).to_dict()
    # TODO use model and split numbers
    return render(request, 'vote.html', {'step1': step1, 'step2': step2 })


def save_vote(request):
    payloads = json.loads(request.body)
    chosen_step_id = payloads['step_id']
    print(chosen_step_id)
    Step.objects.get(id=chosen_step_id).do_vote()
    # TODO Check it's redirecting to correct page
    return JsonResponse({"redirect": "/"})
