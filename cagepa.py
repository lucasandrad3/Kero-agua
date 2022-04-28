#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import datetime
import ast
import os



URL = "https://sic.cagepa.pb.gov.br/falta_dagua/index.php?localidade=18&enviar=OK"

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}

site = requests.get(URL, headers=headers)

soup = BeautifulSoup(site.content, 'html.parser')

registros = soup.find_all('div', class_="card-body collapse")
AttList = []

ocorrenciasRegistradas = []
ocorrenciasNow = []

def showNotify(text):
    os.system("zenity --notification --text='%s'"%text)

try:
    arqOcorrencias = open('notify.txt', 'r')
    for arqOcorrencia in arqOcorrencias:
        dicion = ast.literal_eval(arqOcorrencia)['Código Ocorrência:']
        ocorrenciasRegistradas.append(dicion)
        


    arqOcorrencias.close()

except:
    pass
  

arqOcorrencias = open('notify.txt', 'w')


hoje = datetime.date.today()

# armazena as ocorrencias de falta de agua, em um arquivo, na forma de dicionário
for reg in registros:
    celulas = reg.find_all("tr")

    attElement = {}
    for elemento in celulas:
        chave = elemento.find("th").get_text().strip()
        valor = elemento.find("td").get_text().strip()
        
        attElement[chave] = valor

    ocorrenciasNow.append(attElement['Código Ocorrência:'])

    arqOcorrencias.write(str(attElement)+"\n")

    AttList.append(attElement)

arqOcorrencias.close()


'''
arqOcorrencias = open('notify.txt', 'r')


#Notificação

for arqOcorrencia in arqOcorrencias:
    dicion = ast.literal_eval(arqOcorrencia)['Código Ocorrência:']
    if(not(dicion in ocorrenciasNow)):
        showNotify("Faltará agua cod:%s"%dicion)
             

arqOcorrencias.close()
'''

def getOcorrencia(num_ocorrencia):
    with open('notify.txt', 'r') as arqOcorrencias:
        for ocorrencia in arqOcorrencias:
            codOcorrencia = ast.literal_eval(ocorrencia)['Código Ocorrência:']
            if(codOcorrencia==num_ocorrencia):
                return ast.literal_eval(ocorrencia)







if(ocorrenciasRegistradas==ocorrenciasNow):
    showNotify("Sem Notificação")

else:
    for ocorrenciaNow in ocorrenciasNow:
        if(not(ocorrenciaNow in ocorrenciasRegistradas)):
            d = getOcorrencia(ocorrenciaNow)
            showNotify("Faltará água em: {} \nInicio: {}\nFim: {}\nMotivo: {}".format(d['Área Afetada:'], d['Início Suspensão:'], d['Fim Suspensão:'], d['Motivo:']))