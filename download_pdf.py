# ESTE SCRIPTS BAIXA TODOS OS PDFs CONTENDO TERMOS DE HOMOLOGAÇÃO

from selenium import webdriver
import pandas as pd
from url_curta import unshorten_url
import wget
import pdfkit
import urllib.request

df = pd.read_excel("C:/Users/21458007863/Documents/Documentos_181021/algo_200421/reagentes_2021/balizamento_final.xlsx", header = 1)
#print(df.head())

links = df.iloc[ :, 6]
links = links.unique()




def longa_th(lista): # 
    nr_pregao = []
    for link in lista:
        longo= unshorten_url(link)
        novo = longo.split("prgcod=", 1)
        novo = novo[1]
        novo2 = novo.split("&co_no_uasg", 1)
        nr_pg = novo2[0]
        nr_pregao.append(nr_pg)

    termo = []

    for pregao in nr_pregao:
        termo.append(f'http://comprasnet.gov.br/livre/pregao/termoHom.asp?prgCod={pregao}&tipo=t')
    #print(termo)
    return  termo


### Salvar pesquisas de preço
#df = pd.read_csv('pesquisa_linkok_200421.csv')

# download de todos os pdfs
pasta = 'C:/Users/21458007863/Documents/Documentos_181021/algo_200421/reagentes_2021/comprasnet/'

arquivos = []
for num in range(0, len(links)):
    arquivos.append(f'termo_homolog_{num}.pdf')
#print(arquivos)
#print(arquivos)
#print(links)

path_wkhtml = r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf = path_wkhtml)
for link in links:
    for arq in arquivos:
        #wget.download(term, pasta+arq )
        pdfkit.from_url(link, pasta+arq, configuration = config)
'''

 
path_wkhtml = r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"
config = pdfkit.configuration(path_wkhtml)
for link in links:
    for arq in arquivos:
        pdfkit.from_url(link, (r'.\termos' + arq))
       
for link in links:
'''

