import re
from selenium import webdriver
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(options=options)

link = "https://www.quintoandar.com.br/condominio/home-boutique-brooklin-brooklin-sao-paulo-9p6js8oz3k"

driver.get(link)
html = driver.page_source
site = BeautifulSoup(html, "html.parser")
links = site.find_all("a", href=True)

padrao = r"/imovel/[^/]+/alugar" 
links_filtrados = [link["href"] for link in links if re.search(padrao, link["href"])]

# Adicionar prefixo aos links filtrados
links_completos = ["https://www.quintoandar.com.br" + link for link in links_filtrados]

# Imprimir os links filtrados
for link in links_completos:
    print(link)

# Fechar o navegador
driver.quit()