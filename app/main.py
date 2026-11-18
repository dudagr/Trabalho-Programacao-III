import flet as ft
import requests

URL = "http://127.0.0.1:8000/livros/"

def main(page: ft.Page):
    page.title = "Acervo - Livros"
    page.padding = 20

    campo_busca = ft.TextField(
        label = "Pesquisar no acervo (Título)",
        expand=True,
    )

    def buscar (e):
        termo = campo_busca.value.strip()

        if not termo:
            resultado_area.controls.clear()
            resultado_area.controls.append(
                ft.Text("Digite o título ou uma parte do título para pesquisar.", italic=True, color="grey")
            )
            page.update()
            return
        
        resultado_area.controls.clear()
        resultado_area.controls.append(ft.ProgressRing())
        page.update()

        try:
            resp = requests.get(URL, params={"q": termo}, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except Exception as ex:
            resultado_area.controls.clear()
            resultado_area.controls.append(
                ft.Text(f"Erro ao consultar a API: {ex}", color="red")
            )
            page.update()
            return
        
        livros = data.get("livros", []) if isinstance(data, dict) else data

        resultado_area.controls.clear()

        if not livros:
            resultado_area.controls.append(
                ft.Text("Nenhum livro encontrado.", italic=True)
            )
        else:
            for livro in livros:
                resultado_area.controls.append(criar_card(livro))

        page.update()

    resultado_area = ft.Column(spacing=8)

    def criar_card(livro: dict) -> ft.Card:
        disponivel = livro.get("disponível", False)
        cor_disp = "green" if disponivel else "red"
        texto_disp = "Disponível" if disponivel else "Indisponível"

        return ft.Card(
            content=ft.Container(
                padding=12,
                content=ft.Column(
                    [
                        ft.Text(
                            livro.get("titulo", "Sem título"),
                            weight=ft.FontWeight.BOLD,
                            size=16,
                        ),
                        ft.Text(f"Autor: {livro.get('autor', '-')}", size=13),
                        ft.Row(
                            [
                                ft.Text(f"Editora: {livro.get('editora', '-')}", size=12),
                                ft.Text(f"Ano: {livro.get('ano de publicação', '-')}", size=12),
                                ft.Text(f"Gênero: {livro.get('gênero', '-')}", size=12),
                                ft.Text(f"Páginas: {livro.get('paginas', '-')}", size=12),
                            ],
                            wrap=True,
                            spacing=16,
                        ),
                        ft.Row(
                            [
                                ft.Text(f"ISBN: {livro.get('isbn', '-')}", size=12),
                                ft.Text(f"ID: {livro.get('id', '-')}", size=12),
                                ft.Text(
                                    texto_disp,
                                    size=12,
                                    color=cor_disp,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                            spacing=16,
                        ),
                    ],
                    spacing=4,
                ),
            )
        )
    
    campo_busca.on_submit = buscar
    botao_buscar = ft.Button("Pesquisar", on_click=buscar)

    page.add(
        ft.Row([campo_busca, botao_buscar]),
        ft.Divider(),
        resultado_area,
    )


if __name__ == "__main__":
    ft.run(main)