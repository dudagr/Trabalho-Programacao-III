import json
from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Livro

def index(request):
    return HttpResponse("Página inicial do acervo")

def para_dict(p):
    return {"id": p.id,"titulo": p.titulo, "autor": p.autor, "ano de publicação": p.ano_publicacao, 
    "paginas": p.paginas, "disponível": p.disponivel, "isbn": p.isbn, "gênero": p.genero,
    "editora": p.editora}

campos = [
    "titulo", "autor", "ano_publicacao", "paginas",
    "isbn", "genero", "editora",
]


def validar_livro(request, livro_atual=None):
    try:
        dados = json.loads(request.body)
    except json.JSONDecodeError:
        return None, JsonResponse({"erro": "JSON inválido"}, status=400)

    if not isinstance(dados, dict):
        return None, JsonResponse({"erro": "Envie um objeto JSON"}, status=400)

    faltando = [c for c in campos if dados.get(c) is None or dados.get(c) == ""]
    if faltando:
        return None, JsonResponse(
            {"erro": "Campos obrigatórios: " + ", ".join(faltando)}, status=400
        )

    titulo = dados["titulo"]
    autor = dados["autor"]
    ano_publicacao = dados["ano_publicacao"]
    paginas = dados["paginas"]
    disponivel = dados.get("disponivel", True)
    isbn = dados["isbn"]
    genero = dados["genero"]
    editora = dados["editora"]

    if not isinstance(disponivel, bool):
        return None, JsonResponse(
            {"erro": "disponivel deve ser true ou false"}, status=400
        )

    try:
        ano_publicacao = int(ano_publicacao)
        paginas = int(paginas)
    except (TypeError, ValueError):
        return None, JsonResponse(
            {"erro": "ano_publicacao e paginas devem ser números"}, status=400
        )

    if ano_publicacao <= 0 or paginas <= 0:
        return None, JsonResponse(
            {"erro": "ano_publicacao e paginas devem ser maiores que zero"},
            status=400,
        )
        
    if len(str(isbn)) > 13:
        return None, JsonResponse(
            {"erro": "isbn deve ter no máximo 13 caracteres"}, status=400
        )

    duplicados = Livro.objects.filter(isbn=isbn)
    if livro_atual is not None:
        duplicados = duplicados.exclude(pk=livro_atual.pk)
    if duplicados.exists():
        return None, JsonResponse({"erro": "Já existe um livro com esse isbn"}, status=400)

    return {
        "titulo": dados["titulo"],
        "autor": dados["autor"],
        "ano_publicacao": ano_publicacao,
        "paginas": paginas,
        "disponivel": disponivel,
        "isbn": isbn,
        "genero": dados["genero"],
        "editora": dados["editora"],
    }, None

@csrf_exempt
def lista_livros(request):
    if request.method == "POST":
        campos, erro = validar_livro(request)
        if erro:
            return erro
        livro = Livro.objects.create(**campos)
        return JsonResponse(para_dict(livro), status=201)

    livros = Livro.objects.all()

    busca = request.GET.get("busca")
    if busca:
        livros = livros.filter(titulo__icontains=busca)

    if request.GET.get("disponivel") == "1":
        livros = livros.filter(disponivel=True)

    return JsonResponse({"livros": [para_dict(p) for p in livros]})

@csrf_exempt
def livros(request, codigo):
    try:
        livro = Livro.objects.get(pk=codigo)
    except Livro.DoesNotExist:
        return JsonResponse(
            {"erro": "Livro não encontrado"}, status=404
        )

    if request.method == "PUT":
        campos, erro = validar_livro(request, livro_atual=livro)
        if erro:
            return erro
        for nome, valor in campos.items():
            setattr(livro, nome, valor)
        livro.save()
        return JsonResponse(para_dict(livro))
    
    if request.method == "DELETE":
        livro.delete()
        return HttpResponse(status=204)

    return JsonResponse(para_dict(livro))