import pandas as pd
import datetime
import yfinance as yf
from matplotlib import pyplot as plt
import mplcyberpunk
import win32com.client as win32

codigos_de_negociacao = ["^BVSP", "BRL=X"]

hoje = datetime.datetime.now()
um_ano_atras = hoje - datetime.timedelta(days=365)
dados_mercado = yf.download(codigos_de_negociacao, um_ano_atras, hoje)

# print(dados_mercado)

#filtrar tipo de dados
dados_fechamento = dados_mercado ['Adj Close']

#nomear colunas
dados_fechamento.columns = ['dolar', 'ibovespa']

#para excluir linhas com dados faltantes
dados_fechamento = dados_fechamento.dropna()

#mostra a quantidade de dados selecionada
#print(dados_fechamento.head(50))

#CRIANDO TABELAS EM OUTROS TIMEFRAMES
dados_anuais = dados_fechamento.resample("Y").last()
dados_mensais = dados_fechamento.resample("M").last()
#print(dados_mensais)
#print(dados_anuais)


#CALCULAR FECHAMENTO DO DIA, RETORNO NO ANO E RETORNO NO MÊS DOS ATIVOS

retorno_anual = dados_anuais.pct_change().dropna()
retorno_mensal = dados_mensais.pct_change().dropna()
retorno_diario = dados_fechamento.pct_change().dropna()

#print(retorno_anual)
#print(retorno_mensal)
#print(retorno_diario)

#LOCALIZAR FECHAMENTO DO DIA ANTERIOR, RETORNO DO MES E RETORNO DO ANO

#retorno_fev_11_2022 = retorno_diario.loc['2022-02-11', 'dolar']
# retorno_fev_11_2022 = retorno_diario.iloc[0,0]

retorno_diario_dolar = retorno_diario.iloc[-1, 0]
retorno_diario_ibov = retorno_diario.iloc[-1, 1]

retorno_mensal_dolar = retorno_mensal.iloc[-1, 0]
retorno_mensal_ibov = retorno_mensal.iloc[-1, 1]

retorno_anual_dolar = retorno_anual.iloc[-1, 0]
retorno_anual_ibov = retorno_anual.iloc[-1, 1]


print(retorno_anual)
print(retorno_anual_dolar)
print(retorno_anual_ibov)
