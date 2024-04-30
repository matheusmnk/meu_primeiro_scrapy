import re #biblioteca Regex
import requests #biblioteca HTML
from bs4 import BeautifulSoup #biblioteca raspagem HTML
from selenium import webdriver #biblioteca raspagem HTML dinâmico
from openpyxl import Workbook #biblioteca para criar a planilha
from datetime import datetime #biblioteca para puxar data/hora
import time #biblioteca para definir delay

#Configuração do WebDriver para suprimir logs (Por padrão o Webdriver polui todo o código quando está rodando)
options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument("log-level=3")
driver = webdriver.Chrome(options=options)


#Definir o prédio que irá ser pesquisado
url_prédio = input("Qual o link do prédio? ")

#Adicionar texto no console para o usuário
Acessando_links_dos_apartamentos_disponíveis_para_alugar = "\nAcessando links dos apartamentos disponíveis para alugar..."
for char in Acessando_links_dos_apartamentos_disponíveis_para_alugar:
    print(char, end='', flush=True) # end='' evita quebrar linha, flush=True garante a impressão imediata
    time.sleep(0.05)#Definir delay

#Navegador que será usado
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}


requisicao = requests.get(url_prédio, headers=headers)#Usando Selenium para obter o HTML da página do prédio para se passar por usuário real
driver.get(url_prédio)#Usando Selenium para acessar a página do prédio
html = driver.page_source#puxando código fonte da página por Selenium
site = BeautifulSoup(html, "html.parser")#Analisando código fonte puxado pelo selenium
site2 = BeautifulSoup(requisicao.text, "html.parser")#Analisando código fonte puxado pelo requests
url_apartamentos = site.find_all("a", href=True)#Puxar todos elementos  <a href= xxx


elemento = site.find('h3', class_='CozyTypography xih2fc wIyEP2 _8JKqPG r4Q8xM')#Puxar o nome do empreendimento do link

#Lista para armazenar os links filtrados
links_filtrados = []

#Regex para puxar apenas links que possuem o padrão da URL "/imovel/[ID]/alugar"
padrao = r"/imovel/[^/]+/alugar"
url_apartamentos_filtrados = [url_prédio["href"] for url_prédio in url_apartamentos if re.search(padrao, url_prédio["href"])]

#Dentro do site, a URL não é puxado com o "https..." por isso precisei incluir manualmente para o código entender que se trata de um link
url_apartamentos_formatados = ["https://www.quintoandar.com.br" + url_prédio for url_prédio in url_apartamentos_filtrados]

#Adicionar texto no console para o usuário
Filtrando_links = "\nFiltrando links..."
for char in Filtrando_links:
    print(char, end='', flush=True)  # end='' evita quebrar linha, flush=True garante a impressão imediata
    time.sleep(0.02)  # espera 0.1 segundo entre cada caractere

#Adicionando os links filtrados à lista
for link in url_apartamentos_formatados:
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        if elemento.get_text()[39:] in soup.get_text():
            links_filtrados.append(link)

#Adicionar texto no console para o usuário
Coletando_informacoes = "\nColetando informações...\n"
for char in Coletando_informacoes:
    print(char, end='', flush=True)  # end='' evita quebrar linha, flush=True garante a impressão imediata
    time.sleep(0.02)  # espera 0.1 segundo entre cada caractere

# Fechar o navegador (Selenium)
driver.quit()

# Criar uma nova pasta de trabalho do Excel
wb = Workbook()

# Ativar a planilha ativa
ws = wb.active

# Adicionar cabeçalhos
ws.append(['Empreendimento','Data de Publicação','Metragem', 'Aluguel', 'Valor Total', 'Link'])

#Adicionar texto no console para o usuário
gerando_excel = "Gerando arquivo excel...\n"
for char in gerando_excel:
    print(char, end='', flush=True)  # end='' evita quebrar linha, flush=True garante a impressão imediata
    time.sleep(0.02)  # espera 0.1 segundo entre cada caractere

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
        ws.append([elemento.get_text()[39:], data, metragem, aluguel_formatado, valor_total_formatado, link])


# Salvar o arquivo Excel com o nome especificado
agora = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
nome_arquivo = f"{elemento.get_text()[39:]}_{agora}.xlsx"
wb.save(nome_arquivo)

#Adicionar texto no console para o usuário
excel_gerado = f"Arquivo salvo como '{nome_arquivo}'"
for char in excel_gerado:
    print(char, end='', flush=True)  # end='' evita quebrar linha, flush=True garante a impressão imediata
    time.sleep(0.05)  # espera 0.1 segundo entre cada caractere