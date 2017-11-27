from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponseRedirect
import json
from .models import *
from .natural_selection import change_populations, get_work_routing_info


STEP_TO_URL = {
    '1': 'split',
    '2': 'polish',
    '3': 'connect',
    '4': 'explain',
}


def about(request):
    return render(request, 'about.html')


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


def get_judgement_watch(request, jnum):
    doc = Document.objects.get(id=jnum)
    sentences = Sentence.objects.filter(document__id=jnum)
    # TODO: Replace it with more plausible algorithm
    steps = []
    for sentence in sentences:
        step = Step.objects.filter(sentence__id=sentence.id).order_by('-id')[0]
        steps.append(step.to_dict())
    resp = {
        'title': doc.title,
        'desc': doc.description,
        'steps': steps
    }
    return render(request, 'watch.html', {'json_resp': json.dumps(resp)})


def get_sentence(request, sentence_id):
    sentence = Sentence.objects.get(id=sentence_id)
    sentence.add_hit()

    step = Step.objects.filter(stage=0, sentence__id=sentence_id)[0]
    todo = get_work_routing_info(step.id)
    if todo['creatable']:
        return HttpResponseRedirect('/editor/split/{}'.format(step.id))
    elif todo['votable']:
        step_list = todo["step_list"]
        rest_list = step_list[2:]
        return HttpResponseRedirect('/vote?step1={}&step2={}'
                                    .format(step_list[0], step_list[1]))


def get_splitter(request, step_id):
    parent_step = Step.objects.get(id=step_id).to_dict()
    return render(request, 'split.html', {'json_resp': json.dumps(parent_step)})


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
    if int(stage) not in range(1, 5):
        raise Http404("Invalid stage number")

    print('save_step', stage)

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

    if int(stage) == 4:
        return JsonResponse({"redirect": '/'})

    change_populations(new_step.stage)
    todo = get_work_routing_info(new_step.id)
    if todo['creatable']:
        next_step = STEP_TO_URL[str(int(new_step.stage) + 1)]
        next_url = '/editor/{}/{}'.format(
            next_step, str(new_step.id))
    else:  # todo['votable']:
        step_list = todo["step_list"]
        rest_list = step_list[2:]
        next_url = '/vote?step1={}&step2={}&rest={}'.format(
            step_list[0], step_list[1], rest_list)

    return JsonResponse({"redirect": next_url})


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


def get_stats(request, jnum):
    doc = Document.objects.get(id=jnum)
    sentences = Sentence.objects.filter(document__id=jnum)
    resp = {
        'title': doc.title,
        'desc': doc.description,
        'sentences': [{'id': s.id, 'text': s.content, 'hit': s.hit} for s in sentences]
    }
    return render(request, 'stats.html', {'json_resp': json.dumps(resp)})


def get_family_tree(request, step_id):
    step_cursor = Step.objects.get(id=step_id)
    stage = int(step_cursor.stage)

    families = []
    for i in range(stage + 1):
        families.insert(0, step_cursor.to_dict())
        families[0]['step'] = step_cursor.stage_name_korean()
        step_cursor = step_cursor.parent_step

    return JsonResponse({"family": families})

