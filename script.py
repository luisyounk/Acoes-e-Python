import pandas as pd
import datetime
import yfinance as yf
from matplotlib import pyplot as plt
import mplcyberpunk
import win32com.client as win32
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os

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


#print(retorno_anual)
#print(retorno_anual_dolar)
#print(retorno_anual_ibov)

retorno_diario_dolar = round(retorno_diario_dolar * 100, 2)
retorno_diario_ibov = round(retorno_diario_ibov * 100, 2)

retorno_mensal_dolar = round(retorno_mensal_dolar * 100, 2)
retorno_mensal_ibov = round(retorno_mensal_ibov * 100, 2)

retorno_anual_dolar = round(retorno_anual_dolar * 100, 2)
retorno_anual_ibov = round(retorno_anual_ibov * 100, 2)

#print(retorno_diario_dolar)
#print(retorno_diario_ibov)

#FAZER OS GRAFICOS DA PERFORMANCE DO ULTIMO ANO DOS ATIVOS

plt.style.use("cyberpunk")
dados_fechamento.plot(y="ibovespa", use_index=True, legend=False)
plt.title("ibovespa")
plt.savefig('ibovespa.png', dpi=300)
#plt.show()

plt.style.use("cyberpunk")
dados_fechamento.plot(y="dolar", use_index=True, legend=False)
plt.title("dolar")
plt.savefig('dolar.png', dpi=300)
#plt.show()

#ENVIAR EMAIL

# Dados do remetente
email_user = 'luisyounk@gmail.com'
email_password = 'suasenha'
destinatarios = ['luisyounk@hotmail.com', 'brenno@varos.com.br']
email_destinatario = ', '.join(destinatarios)

# Configurações do e-mail
msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = email_destinatario
msg['Subject'] = "Explicação de Erro e Relatório"

# Corpo da mensagem
body = f'''
Prezado futuro chefe, segue o relatório diário:

Bolsa:

No anos o Ibovespa está tendo uma rentabilidade de {retorno_anual_ibov}%,
enquanto no mês a rentabilidade é de {retorno_mensal_ibov}%.

No último dia útil, o fechamento do Ibovespa foi de {retorno_diario_ibov}%.

Dólar:

No ano o Dólar está tendo uma rentabilidade de {retorno_anual_dolar}%,
enquanto no mês a rentabilidade é de {retorno_mensal_dolar}%.

No último dia útil, o fechamento do Dólar foi de {retorno_diario_dolar}%.

Abs,

Luis Alexandre Dias dos Santos, seu novo estágiario. 
 

'''
msg.attach(MIMEText(body,'plain'))

# Anexos
anexo_ibovespa = r'C:\Users\luisy\OneDrive\Área de Trabalho\python-ações\A--es-e-Python\ibovespa.png'
anexo_dolar = r'C:\Users\luisy\OneDrive\Área de Trabalho\python-ações\A--es-e-Python\dolar.png'

with open(anexo_ibovespa, 'rb') as f:
    img_ibovespa = MIMEImage(f.read())
    msg.attach(img_ibovespa)

with open(anexo_dolar, 'rb') as f:
    img_dolar = MIMEImage(f.read())
    msg.attach(img_dolar)

# Conexão com o servidor de e-mail
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(email_user, email_password)
text = msg.as_string()
server.sendmail(email_user, email_destinatario, text)
server.quit()

