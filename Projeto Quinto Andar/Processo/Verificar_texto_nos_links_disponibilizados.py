import requests
from bs4 import BeautifulSoup

links = [
    "https://www.quintoandar.com.br/imovel/893763796/alugar/apartamento-1-quarto-brooklin-sao-paulo",
    "https://www.quintoandar.com.br/imovel/893885820/alugar/studio-1-quarto-brooklin-sao-paulo",
    "https://www.quintoandar.com.br/imovel/894135197/alugar/apartamento-1-quarto-brooklin-sao-paulo",
    "https://www.quintoandar.com.br/imovel/893790608/alugar/apartamento-1-quarto-brooklin-sao-paulo",
    "https://www.quintoandar.com.br/imovel/894394171/alugar/studio-0-quarto-brooklin-sao-paulo",
    "https://www.quintoandar.com.br/imovel/892773869/alugar/studio-1-quarto-brooklin-paulista",
    "https://www.quintoandar.com.br/imovel/892778340/alugar/apartamento-1-quarto-cidade-moncoes",
    "https://www.quintoandar.com.br/imovel/892778544/alugar/apartamento-1-quarto-brooklin-paulista",
    "https://www.quintoandar.com.br/imovel/892779723/alugar/apartamento-1-quarto-brooklin-paulista",
    "https://www.quintoandar.com.br/imovel/892781495/alugar/apartamento-1-quarto-brooklin-paulista",
    "https://www.quintoandar.com.br/imovel/892786392/alugar/studio-1-quarto-brooklin-paulista",
    "https://www.quintoandar.com.br/imovel/892786393/alugar/studio-1-quarto-brooklin-paulista",
    "https://www.quintoandar.com.br/imovel/892787218/alugar/studio-1-quarto-brooklin-paulista",
    "https://www.quintoandar.com.br/imovel/892787956/alugar/studio-1-quarto-brooklin-paulista",
    "https://www.quintoandar.com.br/imovel/892788468/alugar/studio-1-quarto-brooklin-paulista"
]

for link in links:
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        if "Home Boutique Brooklin" in soup.get_text():
            print("O texto 'Home Boutique Brooklin' está presente no link:", link)

