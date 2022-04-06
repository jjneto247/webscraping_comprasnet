from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



#  dá nome e valor pra submeter o locator
dt_ini = (By.NAME, "dt_ini")  # data
dt_fim = (By.NAME,"dt_fim")
sel_I = (By.NAME,"btMed")
consulta = (By.NAME, "consultar")
exclui_item = (By.XPATH, "/html/body/form[@id='form_licit_medic']/table[@id='TABLE1']/tbody/tr[4]/td[@class='TdTable']/table[@id='TABLE1']/tbody/tr[3]/td[2]/table[@class='campo']/tbody/tr/td[3]/input[@id='button']")
colunas =  "//table[contains(@width, '80%')]/tbody/tr/td[contains(@class, 'tex3b')]"
linhas = "//tr/td[contains(@class, 'tex3a')]"
licita = "//input[contains(@type, 'radio')]"


catmat = (By.NAME, "codigo1")
av_busca = (By.NAME, "btn_avancar")
check_itens = (By.NAME, "chkTodos")
sel_itens = (By.NAME, "btn_selecionar2")

presenca_preco = (By.CLASS_NAME, "mensagem")
termo_homo = (By.NAME, "termodehomologacao")

