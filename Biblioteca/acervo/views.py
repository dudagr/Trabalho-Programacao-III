from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse

from .models import Livro

def index(request):
    return HttpResponse("Página inicial do acervo")

def para_dict(p):
    return {"id": p.id,"titulo": p.titulo, "autor": p.autor, "ano de publicação": p.ano_publicacao, 
    "paginas": p.paginas, "disponível": p.disponivel, "isbn": p.isbn, "gênero": p.genero,
    "editora": p.editora}

def lista_livros(request):
    livros = Livro.objects.all()

    busca = request.GET.get("busca")
    if busca:
        livros = livros.filter(titulo__icontains=busca)
    
    if request.GET.get("disponivel") == "1":
        livros = livros.filter(disponivel=True)

    dados = []
    for p in Livro.objects.all():
        dados.append(para_dict(p))
    return JsonResponse({"livros": dados})

def livros(request, codigo):
    try:
        p = Livro.objects.get(pk=codigo)
    except Livro.DoesNotExist:
        return JsonResponse(
            {"erro": "Livro não encontrado"}, status=404
        )
    return JsonResponse(para_dict(p))