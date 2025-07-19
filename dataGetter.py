# Modularizando as funcoes de dados e visualizacoes
import yfinance as yf
import matplotlib.pyplot as plt

def getAdjCloseData(tickersList, initialDate, finalDate):
    data = yf.download(tickers = tickersList, start = initialDate, end = finalDate, auto_adjust=True)["Close"]
    return data

def viewAdjCloseData(tickersList, initialDate, finalDate):
    data = getAdjCloseData(tickersList, initialDate, finalDate)
    plt.figure(figsize=(10, 5))
    plt.plot(data)
    plt.title('Adj Close')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.grid(True)
    plt.show()