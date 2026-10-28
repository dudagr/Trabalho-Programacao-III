from django.shortcuts import render
from django.http import JsonResponse

from .models import Livro

def para_dict(l):
    return {"titulo": l.titulo, "autor": l.autor, "ano_publicacao": l.ano_publicacao, "paginas": l.paginas, 
            "disponivel": l.disponivel, "isbn": l.isbn, "genero": l.genero}


# Create your views here.
