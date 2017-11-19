from django.shortcuts import render

def base(request):
    return render(request, 'base.html')

def home(request):
    return render(request, 'home.html')

def get_judgement(request, jnum):
    # TODO Use model and jnum
    return render(request, 'judgement.html')

def get_splitter(request, snum):
    # TODO Use model and sentence number
    return render(request, 'split.html')

def get_polisher(request, split_id):
    # TODO use model and split number
    return render(request, 'polish.html')

def get_connector(request, snum):
    # TODO use model and split number
    return render(request, 'connect.html')

def get_explainer(request, snum):
    # TODO use model and split number
    return render(request, 'explain.html')

def get_voter(request, snum1, snum2):
    # TODO use model and split numbers
    return render(request, 'vote.html')
