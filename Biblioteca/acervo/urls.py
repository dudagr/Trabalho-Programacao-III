from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('livros/', views.lista_livros, name='lista_livros'),
    path('livros/<int:codigo>/', views.livros, name='livro'),
]