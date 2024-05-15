import re
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from openpyxl import Workbook
from datetime import datetime
import time
import os

# Configuração do WebDriver
options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument("log-level=3")
driver = None

try:
    driver = webdriver.Chrome(options=options)
except Exception as e:
    print(f"Erro ao inicializar o WebDriver: {e}")
    exit()

# Caminho para a planilha Excel
caminho_planilha = r'C:\Users\matheus.rocha_360sui\Documents\GitHub\meu_primeiro_scrapy\Projeto Quinto Andar\Coloque aqui a planilha\Quinto_Andar.xlsx'

# Adicionar texto no console para o usuário
print("\nAcessando links dos apartamentos disponíveis para alugar...")

# Ler a planilha Excel
try:
    puxar_planilha = pd.read_excel(caminho_planilha)
except Exception as e:
    print(f"Erro ao ler a planilha Excel: {e}")
    exit()

# Extrair os links da coluna 'link_predios'
lista_de_links = puxar_planilha['link_predios'].tolist()

# Iterar sobre os links e executar o restante do código para cada link
for url_prédio in lista_de_links:
    try:
        # Acessar a página do prédio
        driver.get(url_prédio)

        # Obter o HTML da página
        html = driver.page_source

        # Analisar o HTML
        site = BeautifulSoup(html, "html.parser")

        # Obter links dos apartamentos
        url_apartamentos = site.find_all("a", href=True)

        # Restante do código...

        # Adicionar texto no console para o usuário
        print("\nColetando informações...\n")

        # Criar uma nova pasta de trabalho do Excel
        wb = Workbook()

        # Ativar a planilha ativa
        ws = wb.active

        # Adicionar cabeçalhos
        ws.append(['Empreendimento', 'Data de Publicação', 'Metragem', 'Aluguel', 'Valor Total', 'Link'])

        # Adicionar dados coletados ao Excel

        # Salvar o arquivo Excel com o nome especificado
        agora = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        nome_arquivo = f"{re.sub(r'[<>:\"/\\|?*]', '_', url_prédio)}_{agora}.xlsx"
        caminho_arquivo = os.path.join(os.getcwd(), nome_arquivo)
        wb.save(caminho_arquivo)

        # Adicionar texto no console para o usuário
        print(f"Arquivo salvo como '{caminho_arquivo}'")

    except Exception as e:
        print(f"Erro durante a execução: {e}")

# Finalizar o WebDriver
if driver:
    driver.quit()
