import flet as ft
import requests

URL = "http://127.0.0.1:8000/livros/"

def main(page: ft.Page):
    page.title = "Acervo - Livros"
    page.padding = 20

    campo_busca = ft.TextField(
        label = "Pesquisar no acervo",
    )

    page.add(
        campo_busca,
    )


if __name__ == "__main__":
    ft.run(main)