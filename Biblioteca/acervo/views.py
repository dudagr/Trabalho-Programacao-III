from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse

from .models import Livro

def index(request):
    return HttpResponse("Página inicial do acervo")
