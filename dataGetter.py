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
    
# adicionais as estatisticas em geral
def viewData(stats):
    print(f"Lucro médio: {stats['meanProfit']:.2f}")
    print(f"Desvio padrão: {stats['stdProfit']:.2f}")
    print(f"Probabilidade de lucro: {stats['probPosProfit'] * 100:.2f}%")
    print(f"VaR 5% (quantil inferior): {stats['VaR5Pct']:.2f}")
    print(f"VaR 95% (quantil superior): {stats['VaR95Pct']:.2f}")
    print(f"Skewness (assimetria): {stats['skewness']:.2f}")
    print(f"Kurtosis (curtose): {stats['kurtosis']:.2f}")
    print(f"Sharpe Ratio: {stats['sharpeRatio']:.2f}")