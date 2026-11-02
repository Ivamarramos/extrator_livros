# Extrator de Dados de Livros (Web Scraping)

Script em Python que coleta título, preço, nota e disponibilidade de livros
de um catálogo online e salva os dados em CSV e Excel.

Usa o site books.toscrape.com, criado para treinar web scraping.

## Como usar

```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python extrator.py
```

Os arquivos `livros.csv` e `livros.xlsx` serão gerados na pasta.

## Configuração

No início do `extrator.py` você pode alterar `TOTAL_PAGINAS`
(o site tem 50 páginas) e `PAUSA_SEGUNDOS`.

## Resultado

Cada livro vira uma linha com as colunas: título, preço (em libras),
nota de 1 a 5, disponibilidade e link da página do livro.

## Uso responsável

O script faz uma pausa entre as requisições. Em sites reais, consulte
o robots.txt e os termos de uso antes de coletar dados.

## Tecnologias

- Python 3
- requests
- BeautifulSoup
- pandas e openpyxl

## Autor

Ivamar Ramos - [GitHub](https://github.com/Ivamarramos)