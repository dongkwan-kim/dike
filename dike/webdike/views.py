from django.shortcuts import render

def base(request):
    return render(request, 'base.html')

def home(request):
    return render(request, 'home.html')

def get_judgement(request, jnum):
    # TODO Use model and jnum
    return render(request, 'judgement.html')
