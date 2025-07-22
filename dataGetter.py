# Modularizando as funcoes de dados e visualizacoes
import yfinance as yf
from datetime import datetime
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

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
    
# Fazendo um getter para dados de volatilidade implicita
def optionsDataGetter(tickerName, expirationIndex, optionType, targetStrike):
    # Convertendo para o atributo plural usado no yfinance: 'calls' ou 'puts'
    optionsAttr = optionType + "s"

    # Obtendo o ticker
    ticker = yf.Ticker(tickerName)
    
    # maturacao
    expirationDates = ticker.options
    expirationDateStr = expirationDates[expirationIndex]
    
    # Convertendo data de expiração para datetime
    expirationDate = datetime.strptime(expirationDateStr, "%Y-%m-%d")
    today = datetime.today()
    daysToExpiration = (expirationDate - today).days
    
    options = ticker.option_chain(expirationDates[expirationIndex])
    data = getattr(options, optionsAttr) # Essa funcao permite chamar um atributo de obj com o nome de uma string
    
    # Filtrando apenas as colunas desejadas e adicionando o tempo de maturacao
    desiredColumns = ["contractSymbol", "strike", "impliedVolatility"]
    optionData = data[desiredColumns]
    optionData["daysToExpiration"] = daysToExpiration
    
    # Adicionando o tipo da opcao como 'call' ou 'put'
    optionData["optionType"] = optionType
    
    # isolando apenas dados da opcao com strike mais proximo do preco alvo 
    optionData["strikeDiff"] = (optionData["strike"] - targetStrike).abs()
    optionData = optionData.sort_values(by="strikeDiff")
    
    closestData = optionData.iloc[0].drop(labels="strikeDiff")
    
    return closestData
    
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


