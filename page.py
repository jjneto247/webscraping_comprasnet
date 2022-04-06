from locator import *
import pandas as pd

# envia data de inicio da pesquisa
def data_inicio(driver, value):
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(dt_ini)
    )
    # para limpar alguma pesquisa
    element.clear()
    # envia data
    element.send_keys(value)

# envia a data de fim da pesquisa
def data_fim(driver, value):
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(dt_fim)
    )
    # para limpar alguma pesquisa
    element.clear()
    # envia data
    element.send_keys(value)

# clica na pesquisa
def clica_pesquisa(driver):
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(sel_I)
    )
    element.click()

# consulta as licitações
def consultar(driver):
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(consulta)
    )
    element.click()

# pode ser que não exista preços do ítem selecionado
def sem_preco(di, df, cod):
    # conexão com o Google Drive e acesso ao site Comprasnet
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get("http://comprasnet.gov.br/Livre/Ata/ConsultaAta00.asp")
    driver.implicitly_wait(5)
    # insere data de inicio e fim da pesquisa
    data_inicio(driver, di)
    data_fim(driver, df)
    clica_pesquisa(driver)
    driver.implicitly_wait(5)
    driver.switch_to.window(driver.window_handles[1])
    # insere valor do catmat do item a ser pesquisado
    sel_catmat(driver, str(cod))
    avancar_pesq(driver)
    checa_todos(driver)
    sel_checados(driver)
    driver.switch_to.window(driver.window_handles[0])
    consultar(driver)
    l = driver.find_elements_by_class_name("mensagem")
    # get list size with len
    s = len(l)
    
    # check condition, if list size > 0, element exists
    if (s > 0):
        #m = l.text
        #semcodigo.append(cod)
        #print("CATMAT " + str(cod)+ " não existe -" )
        driver.close()
        return True
    else:
        driver.close()
        return False
        
    
    

# pega o nome das colunas
def cols(driver):
    driver.implicitly_wait(5)
    columns = driver.find_elements_by_xpath(colunas)
    column_info = []
    for column in columns:
        column_info.append(str(column.text))
    column_info.pop(0)
    return column_info


def rows(driver):
    driver.implicitly_wait(5)
    lines = driver.find_elements_by_xpath(linhas)
    dados_linha = []
    for linha in lines:
        dados_linha.append(str(linha.text))
    dados_linha = [s for s in dados_linha if s != ""]
    lista_linhas = []
    lista_linhas = [dados_linha[i: i + 4] for i in range(0, len(dados_linha), 4)] 
    return dados_linha, lista_linhas
# identificadores das licitações
def id_licitacao(driver):
    driver.implicitly_wait(5)
    element = driver.find_elements_by_xpath(licita)
    id_licita = []
    for el in element:
        id_licita.append(el.get_attribute("value"))
    return id_licita

# coleta dos dados
def coleta_precos(driver, id_licita, dado_linha):
    price = []
    xispath = []

    for i in id_licita:
        b = "//tr/td[contains(@class, 'tex3a')]/input[contains(@value , '" + str(i) + "')]"
        xispath.append(b)

    for j in xispath:
        driver.find_element_by_xpath(str(j)).click()
        driver.implicitly_wait(5)
        driver.find_element_by_name('ok').click() # vai pra pesquisa de preço
        driver.implicitly_wait(5)
        # tentativa de contornar pesquisas com dois preços

        try:
            driver.find_element_by_name('NuItem').click()
            driver.find_element_by_name('ok').click()
            dados_price = driver.find_elements_by_class_name("tex3a")
            for campo in dados_price:
                price.append(campo.text)
            driver.implicitly_wait(5)
            driver.find_element_by_id('button1').click()
            driver.find_element_by_id('button1').click()
            driver.implicitly_wait(5)
        except:
            dados_price = driver.find_elements_by_class_name("tex3a")
            for campo in dados_price:
                price.append(campo.text)
            driver.implicitly_wait(5)
            driver.find_element_by_id('button1').click() #volta da pesquisa de preço
            driver.implicitly_wait(5)


    price = [s for s in price if s != "1"]
    price = [price[i: i + 5] for i in range(0, len(price), 5)]

    for el_price, el_id_licita in zip(price, id_licita):
        el_price.append(el_id_licita)
    return price


# define catmat
def sel_catmat(driver, value):
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(catmat)
    )
    # para limpar alguma pesquisa
    element.clear()
    # envia data
    element.send_keys(value)
def avancar_pesq(driver):
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(av_busca)
    )
    element.click()

def checa_todos(driver):
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(check_itens)
    )
    element.click()

def sel_checados(driver):
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(sel_itens)
    )
    element.click()

def termo_homologa(driver):
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(termo_homo)
    )
    element.click()
