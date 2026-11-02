import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

URL_PAGINA = "https://books.toscrape.com/catalogue/page-{}.html"
URL_CATALOGO = "https://books.toscrape.com/catalogue/"
TOTAL_PAGINAS = 3
PAUSA_SEGUNDOS = 1
CABECALHOS = {"User-Agent": "Projeto de estudo em Python"}
NOTAS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

def baixar_pagina(numero):
    url = URL_PAGINA.format(numero)
    resposta = requests.get(url, headers=CABECALHOS, timeout=10)
    resposta.raise_for_status()
    resposta.encoding = "utf-8"
    return resposta.text  

def extrair_livros(html):
    sopa = BeautifulSoup(html, "html.parser")
    livros = []
    
    for item in sopa.select("article.product_pod"):
        link = item.h3.a
        texto_preco = item.select_one("p.price_color").text
        preco = float(re.search(r"\d+\.\d+", texto_preco).group())
        classes = item.select_one("p.star-rating")["class"]
        disponivel = "In stock" in item.select_one("p.availability").text
        
        livros.append(
            {
                "titulo": link["title"],
                "preco": preco,
                "nota": NOTAS.get(classes[1], 0),
                "disponivel": "Sim" if disponivel else "Não",
                "link": URL_CATALOGO + link["href"],
            }
        )
        
    return livros

def coletar(total_paginas):
    todos = []

    for numero in range(1, total_paginas + 1):
        try:
            html = baixar_pagina(numero)
        except requests.RequestException as erro:
            print(f"Falha na página {numero}: {erro}")
            continue

        livros = extrair_livros(html)
        todos.extend(livros)
        print(f"Página {numero}: {len(livros)} livros")
        time.sleep(PAUSA_SEGUNDOS)

    return todos


def salvar(livros):
    tabela = pd.DataFrame(livros)
    tabela.to_csv("livros.csv", index=False, encoding="utf-8-sig")
    tabela.to_excel("livros.xlsx", index=False)
    return tabela


def main():
    livros = coletar(TOTAL_PAGINAS)

    if not livros:
        print("Nenhum livro coletado. Verifique sua conexão e tente de novo.")
        return

    try:
        tabela = salvar(livros)
    except PermissionError:
        print("Feche livros.csv e livros.xlsx no Excel e tente de novo.")
        return

    print(f"\n{len(tabela)} livros salvos em livros.csv e livros.xlsx")
    print(f"Preço médio: £ {tabela['preco'].mean():.2f}")


if __name__ == "__main__":
    main()