import re
import requests
from bs4 import BeautifulSoup

url = 'https://www.quintoandar.com.br/condominio/home-boutique-brooklin-brooklin-sao-paulo-9p6js8oz3k'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}

requisicao = requests.get(url, headers=headers)
site = BeautifulSoup(requisicao.text, "html.parser")

elemento = site.find(
    'h3', class_='CozyTypography xih2fc wIyEP2 _8JKqPG r4Q8xM')

if elemento:
    print(elemento.get_text()[39:])
else:
    print('Texto não encontrado.')


#Resta fazer a verificação da url de alugueis, se batem com o mesmo nome de empreendimento