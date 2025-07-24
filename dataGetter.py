# Modularizando as funcoes de dados e visualizacoes
import yfinance as yf
import numpy as np
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
 
# Encontra S0 atual para uso em estrategias de opcoes
def getActualS0(tickerName):
    data = yf.download(tickers = tickerName, period="1d", interval="1d", progress=False, auto_adjust=True)["Close"]
    return float(data.iloc[0])

# Encontra a volatilidade historica anualizada numa base de 5 anos
def getHistoricalVolatility(tickerName):
    window = 252 * 5  # 5 anos úteis
    data = yf.download(tickerName, period="6y", interval="1d", auto_adjust=True)["Close"]
    data = data.tail(window + 1)  # Garante pegar exatamente 5 anos úteis
    log_returns = np.log(data / data.shift(1)).dropna()
    sigma = np.std(log_returns) * np.sqrt(252)  # anualizada
    return sigma
    
# Fazendo um getter para dados de volatilidade implicita
def getOptionsData(tickerName, expirationIndex, optionType, targetStrike):
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
    optionData["timeToExpiration"] = daysToExpiration/365
    
    # Adicionando o tipo da opcao como 'call' ou 'put'
    optionData["optionType"] = optionType
    
    # isolando apenas dados da opcao com strike mais proximo do preco alvo 
    optionData = optionData.copy()
    optionData["strikeDiff"] = (optionData["strike"] - targetStrike).abs()
    optionData = optionData.sort_values(by="strikeDiff")
    
    closestData = optionData.iloc[0].drop(labels="strikeDiff")
    
    return closestData

# Montando uma função que escolhe automaticamente o ticker mais adequado para uma opcao norte-americana dado o tempo
# até a maturacao dela.Temos T <= 0.25 => IRX, tesouro 3 meses. T e [0.25, 2.5] => FVX, tesouro 5 anos. Por fim,
# T > 2.5 => tesouro 10 anos
def choseInterestRate(T):
    if(T <= 0.25):
        return "^IRX"
    elif(T > 2.5):
        return "^TNX"
    else:
        return "^FVX"

# Pegando a taxa de juros e ajustando para seu uso em black-scholes e GBM
def getInterestRate(T):
    ticker = choseInterestRate(T)
    data = yf.download(ticker, period="1d", interval="1d", progress=False)["Close"]
    decimalRate = float(data.iloc[0])/100
    r = np.log(1 + decimalRate)
    
    return r

# Pegando a media do retorno passado numa base de 5 anos
def getMuMean(tickerName):
    window = 252 * 5  # 5 anos úteis
    data = yf.download(tickerName, period="6y", interval="1d", auto_adjust=True)["Close"]
    data = data.tail(window + 1)
    log_returns = np.log(data / data.shift(1)).dropna()
    mu_daily = np.mean(log_returns)
    mu_annual = mu_daily * 252
    return mu_annual

# Pegando o std do retorno passado numa base de 5 anos
def getMuStd(tickerName):
    window = 252 * 5
    data = yf.download(tickerName, period="6y", interval="1d", auto_adjust=True)["Close"]
    data = data.tail(window + 1)
    log_returns = np.log(data / data.shift(1)).dropna()
    std_daily = np.std(log_returns)
    std_annual = std_daily * np.sqrt(252)
    return std_annual

# Montando um modelo de volatilidade misto, que considera um peso para a volatilidade historica
def getMixedVolatility(IV, HV, weight):
    return float(weight * HV + (1 - weight) * IV)

# Montando um modelo de volatilidad mista que conforme mais proximo do tempo de maturacao zerar, menos o 
# peso exponencialmente de HV
def getExponentialMixedVolatility(IV, HV, k, T):
    return float(np.exp(-k * T) * HV + (1 - np.exp(-k * T)) * IV)

def getBSData(tickerName, expirationIndex, targetStrike, optionType):
    S0 = getActualS0(tickerName)
    optionData = getOptionsData(tickerName, expirationIndex, optionType, targetStrike)
    K = optionData["strike"]
    sigma = optionData["impliedVolatility"]
    T = optionData["timeToExpiration"]
    r = getInterestRate(T)
    
    return S0, K, sigma, T, r, optionType
    
    
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


