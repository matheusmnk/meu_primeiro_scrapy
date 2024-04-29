import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from multiprocessing import Pool


def extrair_dados(link):
    if pd.notna(link):  # Verifica se o link não é NaN
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
        requisicao = requests.get(link, headers=headers)
        site = BeautifulSoup(requisicao.text, "html.parser")

        metro_quadrado = site.find(
            "p", class_="CozyTypography xih2fc EKXjIf Ci-jp3")
        aluguel = site.find(
            "p", class_="CozyTypography xih2fc _72Hu5c wIyEP2 _8JKqPG r4Q8xM")
        valor_total = site.find(
            "p", class_="CozyTypography xih2fc wIyEP2 _8JKqPG r4Q8xM")
        publicado = re.compile(r"Publicado há \d+")
        data_publicacao = site.find("span", string=publicado)

        return {
            'link': link,
            'metro_quadrado': metro_quadrado.get_text() if metro_quadrado else None,
            'aluguel': aluguel.get_text()[8:] if aluguel else None,
            'valor_total': valor_total.get_text()[6:] if valor_total else None,
            'data_publicacao': data_publicacao.text.strip()[13:] if data_publicacao else None
        }
    else:
        return None


if __name__ == '__main__':
    # Substitua 'Quinto Andar.xlsx' pelo caminho do seu arquivo Excel
    planilha = pd.read_excel('Quinto Andar.xlsx')
    # 'Link Anúncio' é a coluna onde estão os links
    links = planilha['Link Anúncio'].tolist()

    with Pool() as pool:  # Sem restrição de número de processos
        resultados = pool.map(extrair_dados, links)

    for resultado in resultados:
        if resultado:  # Verifica se o resultado não é None
            print("\nLink:", resultado['link'])
            print('Metragem:', resultado['metro_quadrado'])
            print('Aluguel:', resultado['aluguel'])
            print('Valor total:', resultado['valor_total'])
            print('Data de publicação:', resultado['data_publicacao'])