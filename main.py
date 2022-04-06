
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from page import *
import pandas as pd
from limpeza import *

from url_curta import *
import re
import url_curta




def webscrapping(di, df, cod):
    # conexão com o Google Drive e acesso ao site Comprasnet
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get("http://comprasnet.gov.br/Livre/Ata/ConsultaAta00.asp")
    driver.implicitly_wait(5)
    # insere data de inicio e fim da pesquisa
    data_inicio(driver, di)
    data_fim(driver, df)
    clica_pesquisa(driver)
    driver.switch_to.window(driver.window_handles[1])
    # insere valor do catmat do item a ser pesquisado
    sel_catmat(driver, str(cod))
    avancar_pesq(driver)
    checa_todos(driver)
    sel_checados(driver)
    driver.switch_to.window(driver.window_handles[0])
    consultar(driver)
    # formata os dados obtidos e salva em um Data Frame
    verts = cols(driver)
    #print(verts)
    list_horiz, horiz = rows(driver)
    res_ata = pd.DataFrame(horiz, columns=verts)
    #print(res_ata)
    id = id_licitacao(driver)
    #print(id_licitacao)
    valores = coleta_precos(driver, id, list_horiz)
    #print(valores)
    valores = pd.DataFrame(valores)
    # aplica a função de limpeza dos dados presente no script limpeza.py
    tab_final = limpeza(res_ata, valores)
    # retorna a tabela final
    return tab_final




    #tab_final.to_csv("tab_final.csv") para pegar com as marcas

    driver.close()








if __name__ == '__main__':
      
    begin_time = datetime.datetime.now()
    di = "06042022" # DATA INICIAL DA PESQUISA
    df = "06042022" # DATA FINAL DA PESQUISA
    
    
        
       
    # OBTÉM LISTA DE CATMATS
    catmat = pd.read_csv("catmat.csv", header=None,  sep=',')
  
    
    catmat.columns = ["ITEM", "CATMAT", "DESC", "QUANT"]
    
    codigos = catmat["CATMAT"]
    
    codigos = codigos[2:20]
    
    dimat = []
    result = pd.DataFrame()
    
    # LOOP PARA SALTAR OS ITENS QUE NÃO RETORNAREM NENHUM PREÇO
    for codigo in codigos:
        #print(codigo)
        if sem_preco(di, df, codigo)== True:
            continue
        #else:
        #    pass 
        
   
    
    # PARA BUSCAR UMA LISTA DE PREÇOS
        lista_links = prep_df_pdf(resultado)
        
        final = imp_result(resultado, lista_links, codigo)
     
        
        lista = final.to_numpy().tolist()
        for row in lista:
            dimat.append(row)
    print(datetime.datetime.now() - begin_time)
    
          
    colunas = ["TIPO_LICIT", "NB_LICIT", "QTD", "PRECO", "FIM_VIG", "LINK", "CATMAT"]
    dimat = pd.DataFrame(dimat, columns= colunas)
    #dimat.to_excel("pesquisa_abo.xlsx")
    #catmats = pd.read_csv('catmat_preco_medio_horm_2021.csv')
    #catmats.columns = ["GRUPO", "ITEM", "CATMAT", "ESPECIF", "QTD", "AVG"]

    #dimat['LINK'] = dimat.apply(convert, axis=1)
    #dimat['LINK'].head()
    # filtro de preços
    mergido = pd.merge(dimat, catmat, on='CATMAT')
    #mergido = mergido[mergido['PRECO'] <= 2 * mergido['AVG']]
    #mergido.to_excel("reagentes_2021/pesquisa_200122.xlsx")
    mergido.to_excel("reagentes_2021/pesquisa_24012022.xlsx")

    print(datetime.datetime.now() - begin_time)



'''

# para buscar um só preço
    cod = "19127"
    resultado = webscrapping(di, df, cod)
    lista_links = prep_df_pdf(resultado)
    final = imp_result(resultado, lista_links, cod)
    # print(resultado, lista_links)
    print(final)
'''    
     


