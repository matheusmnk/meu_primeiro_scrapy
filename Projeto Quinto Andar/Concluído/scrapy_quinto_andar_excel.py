import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from openpyxl import Workbook
from datetime import datetime

# Configuração do WebDriver para suprimir logs
options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument("log-level=3")  # Define o nível de log como "warning" (3)
driver = webdriver.Chrome(options=options)

url_prédio = input("Qual o link do prédio? ")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}

requisicao = requests.get(url_prédio, headers=headers)
driver.get(url_prédio)
html = driver.page_source
site = BeautifulSoup(html, "html.parser")
site2 = BeautifulSoup(requisicao.text, "html.parser")
url_apartamentos = site.find_all("a", href=True)

elemento = site.find(
    'h3', class_='CozyTypography xih2fc wIyEP2 _8JKqPG r4Q8xM')

# Lista para armazenar os links filtrados
links_filtrados = []

padrao = r"/imovel/[^/]+/alugar"
url_apartamentos_filtrados = [url_prédio["href"] for url_prédio in url_apartamentos if re.search(padrao, url_prédio["href"])]

url_apartamentos_formatados = ["https://www.quintoandar.com.br" + url_prédio for url_prédio in url_apartamentos_filtrados]

# Adicionando os links filtrados à lista
for link in url_apartamentos_formatados:
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        if elemento.get_text()[39:] in soup.get_text():
            links_filtrados.append(link)

# Fechar o navegador
driver.quit()

# Criar uma nova pasta de trabalho do Excel
wb = Workbook()

# Ativar a planilha ativa
ws = wb.active

# Adicionar cabeçalhos
ws.append(['Data de Publicação','Metragem', 'Aluguel', 'Valor Total', 'Link'])

# Adicionar dados coletados
for link in links_filtrados:
    response = requests.get(link)
    if response.status_code == 200:
        soup_apartamento = BeautifulSoup(response.content, "html.parser")

        metro_quadrado = soup_apartamento.find("p", class_="CozyTypography xih2fc EKXjIf Ci-jp3")
        metragem = metro_quadrado.get_text() if metro_quadrado else "Metragem não encontrada"

        aluguel = soup_apartamento.find("p", class_="CozyTypography xih2fc _72Hu5c wIyEP2 _8JKqPG r4Q8xM")
        aluguel_formatado = aluguel.get_text()[8:] if aluguel else "Aluguel não encontrado"

        valor_total = soup_apartamento.find("p", class_="CozyTypography xih2fc wIyEP2 _8JKqPG r4Q8xM")
        valor_total_formatado = valor_total.get_text()[6:] if valor_total else "Valor total não encontrado"

        publicado = re.compile(r"Publicado há \d+")
        data_publicacao = soup_apartamento.find("span", string=publicado)
        data = data_publicacao.text.strip()[13:] if data_publicacao else "Data de publicação não encontrada"

        # Adicionar os dados à planilha
        ws.append([data, metragem, aluguel_formatado, valor_total_formatado, link])

# Salvar o arquivo Excel com o nome especificado
agora = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
nome_arquivo = f"{elemento.get_text()[39:]}_{agora}.xlsx"
wb.save(nome_arquivo)
print(f"Arquivo salvo como '{nome_arquivo}'")
