from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def cadastro(request):
    return render(request, 'core/cadastro.html')
