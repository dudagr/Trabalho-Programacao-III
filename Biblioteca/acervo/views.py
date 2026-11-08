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

@csrf_exempt
def lista_livros(request):
    if request.method == "POST":
        try:
            dados = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"erro": "JSON inválido"}, status=400)

        if not isinstance(dados, dict):
            return JsonResponse({"erro": "Envie um objeto JSON"}, status=400)

        campos = [
            "titulo", "autor", "ano_publicacao", "paginas",
            "isbn", "genero", "editora",
        ]
        faltando = [c for c in campos if dados.get(c) is None or dados.get(c) == ""]
        if faltando:
            return JsonResponse(
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
            return JsonResponse(
                {"erro": "disponivel deve ser true ou false"}, status=400
            )

        try:
            ano_publicacao = int(ano_publicacao)
            paginas = int(paginas)
        except (TypeError, ValueError):
            return JsonResponse(
                {"erro": "ano_publicacao e paginas devem ser números"}, status=400
            )

        if ano_publicacao <= 0 or paginas <= 0:
            return JsonResponse(
                {"erro": "ano_publicacao e paginas devem ser maiores que zero"},
                status=400,
            )

        if len(str(isbn)) > 13:
            return JsonResponse(
                {"erro": "isbn deve ter no máximo 13 caracteres"}, status=400
            )

        if Livro.objects.filter(isbn=isbn).exists():
            return JsonResponse({"erro": "Já existe um livro com esse isbn"}, status=400)

        livro = Livro.objects.create(
            titulo=titulo,
            autor=autor,
            ano_publicacao=ano_publicacao,
            paginas=paginas,
            disponivel=disponivel,
            isbn=isbn,
            genero=genero,
            editora=editora,
        )

        return JsonResponse(para_dict(livro), status=201)

    livros = Livro.objects.all()

    busca = request.GET.get("busca")
    if busca:
        livros = livros.filter(titulo__icontains=busca)

    if request.GET.get("disponivel") == "1":
        livros = livros.filter(disponivel=True)

    dados = []
    for p in livros:
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
