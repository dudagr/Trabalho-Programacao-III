from django.db import models

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    ano_publicacao = models.IntegerField()
    paginas = models.IntegerField()
    disponivel = models.BooleanField(default=True)
    isbn = models.CharField(max_length=13, unique=True)
    genero = models.CharField(max_length=50)

    def __str__(self):
        return self.titulo 