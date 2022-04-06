
### ALGORITMO QUE GERA PLANILHA PARA FORMATAR PESQUISA DE PREÇOS
### NOS MOLDES DO DECRETO Nº 39.453, DE 14 DE NOVEMBRO DE 2018.

import pandas as pd
import numpy as np
#df = pd.read_excel('pesquisa_0604_34.xlsx')
df = pd.read_excel("C:/Users/21458007863/Documents/Documentos_181021/algo_200421/reagentes_2021/balizamento_final.xlsx") # tabela originada do webscraping



df['PRECO'] = (df['PRECO'].replace('\.','', regex=True).replace(',','.', regex=True).astype(float))

# CÁLCULO DA MEDIANA
mediana = df[['CATMAT', 'PRECO']]

mediana = mediana.groupby('CATMAT')['PRECO'].median().to_frame()

mediana = mediana.reset_index()

mediana.rename(columns = {'PRECO' : 'MEDIANA'}, inplace = True)

# filtro da mediana

df = pd.merge(df, mediana, on = 'CATMAT')
df['LIM_INF'] = df["MEDIANA"] * 0.5
df['LIM_SUP'] = df['MEDIANA'] * 1.5

df['RESULTADO'] =  df['PRECO'].lt(df['LIM_SUP']) &  df['PRECO'].gt(df['LIM_INF'])
# nova mediana

mediana2 = df[df['RESULTADO']==True].groupby('ITEM')['PRECO'].median().to_frame()
mediana2 = mediana2.reset_index()
mediana2.rename(columns = {'PRECO' : 'MEDIANA_2'}, inplace = True)
df = pd.merge(df, mediana2, on = 'ITEM')


# CALCULO DA MÉDIA
media = df[['CATMAT', 'PRECO']]
media = media.groupby('CATMAT')['PRECO'].mean().to_frame()
media = media.reset_index()
media.rename(columns = {'PRECO' : 'MEDIA'}, inplace = True)
df = pd.merge(df, media, on = 'CATMAT')



# SEGUNDO FILTRO

df['PREÇO FINAL'] = np.where(df['MEDIANA_2']<=df['MEDIA'], df['MEDIANA_2'], df['MEDIA'])
# FORMATAÇÃO 
df = df.round({'LIM_INF': 2, 'LIM_SUP': 2, 'MEDIANA': 2, 'MEDIANA_2': 2, 'PRECO': 2, 'MÉDIA': 2, 'PREÇO FINAL': 2, 'TOTAL ESTIMADO':2})
df.rename(columns = {'LINK': 'TERMO DE HOMOLOGAÇÃO', 'LIM_INF': 'MÍNIMO (-50%)', 'LIM_SUP': 'MÁXIMO (+50%)',
                     'MEDIANA_2': 'MEDIANA FINAL', 'MEDIA': 'MÉDIA FINAL'}, inplace = True)


# TABELA PIVOT 
df_pivot = df.pivot_table(index = ['ITEM', 'QUANT', 'CATMAT', 'TERMO DE HOMOLOGAÇÃO', "PRECO", 'MEDIANA', 'MÍNIMO (-50%)', 
                                   'MÁXIMO (+50%)','MEDIANA FINAL', 'MÉDIA FINAL'  ],
                           values= 'PREÇO FINAL')

df_pivot.to_excel("planilha_pronta_040222.xlsx")

