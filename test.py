# Baixando dados do yfinance considerando as novas atualizacoes e visualizando dados de adj close
import generalFunctions as gf
import datetime as dt


d1 = dt.date(2024, 1, 1)
d2 = dt.date(2025, 1, 1)

tickers = ["AAPL"]

dados = gf.getAdjCloseData(tickers, d1, d2)

print(dados)

gf.viewAdjCloseData(tickers, d1, d2)