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
