#!/usr/bin/env python
# coding: utf-8

# # Importar ficheiros de um site, transformar dados e criar dataset

# In[1]:


import os
import requests
import pandas as pd

# Definir localização do ficheiro
url_base = "https://www.omie.es/sites/default/files/dados/AGNO_{year}/MES_{month:02d}/XLV/INT_PBC_EV_H_1_{day:02d}_{month:02d}_{year}_{day:02d}_{month:02d}_{year}.XLS"
 
# Definir data inicial e final para extrair dados
data_inicial = pd.Timestamp('2018-01-01') 
data_final = pd.Timestamp('2024-04-22')
          
# Definir o Locar onde irão ser guardados os ficheiros
pasta = 'C:/Users/danil/Desktop/Projeto DSBI/dados'

# Criar a pasta caso não exista
if not os.path.exists(pasta):
    os.makedirs(pasta)

# Criação de uma Lista para guardar DataFrames de todos os ficheiros
dataframes = []

# Loop para obter todos os ficheiros
for data_atual in pd.date_range(data_inicial, data_final):
    
    # Formatar a data como string no formato 'YYYY-MM-DD'
    data_str = data_atual.strftime('%Y-%m-%d')
    
    # Construir o URL com base na data atual
    url_excel = url_base.format(year=data_atual.year, month=data_atual.month, day=data_atual.day)
    
    # Nome do ficheiro local onde será guardado
    nome_excel = f'INT_PBC_EV_H_1_{data_str}_{data_str}.XLS'
    
    # GET para o URL do arquivo
    req = requests.get(url_excel)
    
    # Verificar se o pedido foi bem-sucedido (código 200 indica sucesso)
    if req.status_code == 200:    
        # Guardar o conteúdo do pedido no ficheiro local
        caminho_excel = os.path.join(pasta, nome_excel)
        with open(caminho_excel, 'wb') as ficheiro:
            ficheiro.write(req.content)
        print(f"Download do arquivo Excel para {data_str} concluído com sucesso.")

    # Tratamento dos dados
        # Ler Excel e remover as três primeiras linhas
        df = pd.read_excel(caminho_excel, skiprows=3)

        # Transpor o DataFrame (trocar colunas pelas linhas)
        df_transposto = df.T
        
        # Adicionar colunas de ano, mês e dia ao DataFrame
        df_transposto.insert(0, 'Ano', data_atual.year)
        df_transposto.insert(1, 'Mês', data_atual.month)
        df_transposto.insert(2, 'Dia', data_atual.day)

        # Adicionar o DataFrame transposto à lista
        dataframes.append(df_transposto)

        print(f"Dados processados para {data_str}.")

    else:
        print(f"Ocorreu um erro ao fazer o download do ficheiro Excel para {data_str}. Código de estado: {req.status_code}")

# Juntar todos os DataFrames em um único DataFrame
df_final = pd.concat(dataframes, axis=0) # Adiciona cada ficheiro pelas linhas 

# Guardar o DataFrame final num único Excel
ficheiro_final = 'dataset_com_data.xlsx'
caminho_final = os.path.join(pasta, ficheiro_final)
df_final.to_excel(caminho_final)

print(f"Os dados foram unidos e salvos em '{caminho_final}'.")


# In[ ]:




