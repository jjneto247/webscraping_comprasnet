import pandas as pd
from selenium import webdriver
from page import *




def limpeza(df, df2):
#res_ata: dataframe 1 -> colocar nomes, coluna identificador, ['licitação'] split by \n por " ",
#data é um DataFrame
    #df.drop(df.columns[0], axis = 1, inplace = True)
    novo = df.iloc[:, 0].str.split("-", n=1, expand=True)
    #df.join(novo)
    df = pd.concat([df,novo], axis = 1)
    df.drop(columns=df.columns[0], axis = 1, inplace=True)
    #print(df)

    novo2 = df.iloc[:, 0].str.split("-", n=1, expand=True)
    df = pd.concat([df,novo2], axis = 1)
    df.drop(columns=df.columns[0], axis = 1, inplace=True)
    #print(df)

    novo3 = df.iloc[:, 0].str.split("\n", n=1, expand=True)
    df = pd.concat([df,novo3], axis = 1)
    df.drop(columns=df.columns[0], axis = 1, inplace=True)
    #print(df)

    novo4 = df.iloc[:, 0].str.split("\n", n=1, expand=True)
    df = pd.concat([df,novo4], axis = 1)
    df.drop(columns=df.columns[0], axis = 1, inplace=True)
    #print(df)

    # limpando o DF valores
    #df2.drop(df2.columns[0], axis=1, inplace=True) #pra testar descomenta
    novo5 = df2.iloc[: , 0].str.replace("/", "").str.split(" - ", n=1, expand=True)
    df2.drop(df2.columns[0], axis=1, inplace=True)
    df2 = pd.concat([df2,novo5], axis = 1)
    pd.set_option("max_columns", 14)

    #print(df)
    #print(df2)

    # concatenando dois dfs

    final_df = pd.concat([df, df2], axis = 1)

    final_df.columns = ['NB_ORGAO', 'ORGAO', 'NB_UASG', 'UASG',
                            'TIPO_LICIT', 'NB_LICIT', 'INI_VIG', 'FIM_VIG', 'QTD',
                            'PRECO', 'VL_TOTAL', 'MARCA', 'ID', 'CNPJ', 'FORNECEDOR']

    return final_df

#junto = limpeza(data, datatwo)
#print(junto)

#tab_final.to_csv("tab_final.csv")

def prep_df_pdf(df):
    lista = df.loc[:, ["NB_UASG", "NB_LICIT"]]
    lista = lista.values.tolist()
    lista_limpa = []
    for row in lista:
        for col in range(len(row)):
            row[col] = row[col].strip()
        lista_limpa.append(row)
    lista = lista_limpa
    for d in lista:
        d[1] = d[1].lstrip("000")
    for d in lista:
        d[1] = d[1].replace("/", "")

    print(lista)
    lista_links = []
    for i, j in lista:
        '''
        link_homo ="http://comprasnet.gov.br/livre/pregao/termohom.asp?prgcod=817208&co_no_uasg={}&numprp={}&"\
                   "f_lstSrp=&f_Uf=&f_numPrp={}&f_coduasg={}&f_tpPregao=E&"\
                   "f_lstICMS=&f_dtAberturaIni=&f_dtAberturaFim=".format(i, j, j, i)
        '''
        link_homo = "http://comprasnet.gov.br/livre/pregao/ata2.asp?co_no_uasg={}&numprp={}&f_lstSrp=&"\
                    "f_Uf=&f_numPrp={}&f_codUasg={}&f_tpPregao=E&f_lstICMS=&f_dtAberturaIni=&f_dtAberturaFim=".format(i, j, j, i)

        driver = webdriver.Chrome("C:/Users/21458007863/Documents/Documentos_181021/algo_200421/chromedriver")
        driver.get(link_homo)
        termo_homologa(driver)
        linque = driver.current_url
        novo = linque.split("prgcod=", 1)
        novo = novo[1]
        novo2 = novo.split("&co_no_uasg", 1)
        nr_pg = novo2[0]
        
        lista_links.append(f'http://comprasnet.gov.br/livre/pregao/termoHom.asp?prgCod={nr_pg}&tipo=t')
        
        driver.close()
    return lista_links

# na tabela resultado vou acrescer a url curta e selecionar colunas
# "TIPO_LICIT", "NB_LICIT", "QTD", "PRECO", "FIM_VIG"
def imp_result(res, lista_links, cod):
    df = res[["TIPO_LICIT", "NB_LICIT", "QTD", "PRECO", "FIM_VIG"]] 
    temp = []
    
    for i in lista_links:
        #curta = make_shorten(i)
        temp.append(i)
   
    #temp_series = pd.Series(temp, index = df.columns)
    #df = df.append(temp_series, ignore_index = True)
    df["LINK"] = temp
    df["CATMAT"] = cod
    #df.QTD = df.QTD.str.replace(".", "").astype(int)
    #df.PRECO.astype(float)
    #df["QTD"] = df["QTD"].astype(int)
    #df["CATMAT"] = pd.to_numeric(df["CATMAT"])
    #print(df.dtypes)
    return df
