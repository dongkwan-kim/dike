from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
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
    sentences = Sentence.objects.filter(document__id=jnum).order_by('id')
    resp = {
        'title': doc.title,
        'desc': doc.description,
        'sentences': [{'id': s.id, 'text': s.content} for s in sentences]
    }
    return render(request, 'judgement.html', {'json_resp': json.dumps(resp)})


def get_judgement_watch(request, jnum):
    doc = Document.objects.get(id=jnum)
    sentences = Sentence.objects.filter(document__id=jnum).order_by('id')
    steps = []
    for sentence in sentences:
        step = Step.objects.filter(sentence__id=sentence.id).order_by('-stage', '-population')[0]
        steps.append(step.to_dict())
    resp = {
        'title': doc.title,
        'desc': doc.description,
        'steps': steps
    }
    return render(request, 'watch.html', {'json_resp': json.dumps(resp)})


def get_route_url_by_natural_select(request, target_step):
    target_sentence_id = target_step.sentence.id
    todo = get_work_routing_info(target_step.id)
    creatable = todo['creatable']
    votable = todo['votable']
    next_stage_numeric = int(todo['next_stage'])

    if not creatable and not votable:
        jnum = target_step.sentence.document.id
        url = "/judgement/{}".format(jnum)
        return url

    next_stage = STEP_TO_URL[str(todo['next_stage'])]
    if next_stage_numeric != int(target_step.stage) + 1:
        before = next_stage_numeric - 1
        next_step = Step.objects.filter(stage=before, sentence__id=target_sentence_id).order_by('-population')[0]
    else:
        next_step = target_step

    if votable:
        step_list = todo["step_list"]
        request.session['step_list'] = [s.id for s in step_list]
    else:
        request.session['step_list'] = []

    if creatable:
        url = '/editor/{}/{}'.format(next_stage, next_step.id)
        return url


@login_required
def get_sentence(request, sentence_id):
    sentence = Sentence.objects.get(id=sentence_id)
    sentence.add_hit()

    init_stage = 0

    init_step = Step.objects.filter(stage=init_stage, sentence__id=sentence_id)[0]
    url = get_route_url_by_natural_select(request, init_step)
    return HttpResponseRedirect(url)


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


def route_winner_or_new_to_editor(request, winner_or_new):
    change_populations(winner_or_new.stage, winner_or_new.sentence.id)
    url = get_route_url_by_natural_select(request, winner_or_new)
    return JsonResponse({"redirect": url})


def route_winner_or_new_to_vote(request, winner_or_new):
    step_list = [winner_or_new.id] + request.session['step_list']
    rest_list = step_list[2:]
    request.session['step_list'] = rest_list
    return JsonResponse({"redirect": '/vote?step1={}&step2={}'.format(step_list[0], step_list[1])})


def save_step(request, stage):
    if int(stage) not in range(1, 5):
        raise Http404("Invalid stage number")

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
        sentence_id=payloads["sentence_id"]
    )
    if parent_step_id:
        new_step.parent_step_id = parent_step_id
    new_step.save()

    rest_list = request.session['step_list']
    if rest_list:
        return route_winner_or_new_to_vote(request, new_step)
    else:
        return route_winner_or_new_to_editor(request, new_step)


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
    return render(request, 'vote.html', {'step1': step1, 'step2': step2})


def save_vote(request):
    payloads = json.loads(request.body)
    chosen_step_id = payloads['step_id']
    print(chosen_step_id)
    winner = Step.objects.get(id=chosen_step_id)
    winner.do_vote()

    try:
        return route_winner_or_new_to_vote(request, winner)
    except:
        return route_winner_or_new_to_editor(request, winner)


def get_stats(request, jnum):
    doc = Document.objects.get(id=jnum)
    sentences = Sentence.objects.filter(document__id=jnum).order_by('id')
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

