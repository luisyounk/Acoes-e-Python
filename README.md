# Ações e Python
 Projeto de Análise de Ações e Fechamento de Mercado

This script downloads daily financial data for two assets, the Bovespa index in Brazil (represented by the symbol "^BVSP") and the USD/BRL exchange rate (represented by the symbol "BRL=X"), over the last year. The data is processed to obtain closing prices, monthly and annual returns, and the last-day returns for both assets. Additionally, it generates two plots of the closing prices over the last year and sends the plots in an email.

The script makes use of several libraries, including Pandas, Matplotlib, and smtplib, to perform data processing, data visualization, and email sending tasks, respectively.