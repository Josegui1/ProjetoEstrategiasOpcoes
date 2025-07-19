import yfinance as yf
import numpy as np
import scipy.stats as sps
import numpy.random as npr
import matplotlib.pyplot as plt

#Funcoes para obter e visualizar dados 
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

# Funcoes auxiliares para monte carlo, que geram movimentos aleatorios conhecidos e importantes
def GBMPaths(S0, r, sigma, T, N):
    Z = npr.randn(N)
    St = S0*np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    return St

def hestonPaths(S0, v0, r, T, kappa, theta, ksi, rho, N, M):
    dt = T/M
    St = np.full(N, S0)
    vt = np.full(N, v0)
    
    for i in range(M):
        Z1 = npr.randn(N)
        Z2 = rho * Z1 + np.sqrt(1 - rho**2) * npr.randn(N)
        
        vt = np.maximum(vt + kappa * (theta - vt) * dt + ksi * np.sqrt(np.maximum(vt, 0)) * np.sqrt(dt) * Z2, 0)
        St = St * np.exp((r - 0.5 * vt) * dt + np.sqrt(vt * dt) * Z1)
        
    return St
        
#Funcoes para precificar opcoes
# S0 = preco inicial, K = strike, r = taxa de juros, T = maturacao em anos, N = num. simulacoes, mode = call ou put
def monteCarloOptionPricing(S0, K, r, sigma, T, N, mode):
    St = GBMPaths(S0, r, sigma, T, N)
    
    if (mode == "call"):
        payoffs = np.maximum(St - K, 0)
    elif (mode == "put"):
        payoffs = np.maximum(K - St, 0)
    else:
        print("Invalid mode.")
        
    price = np.exp(-r * T) * np.mean(payoffs)
    
    return price

# S0 = preco inicial, v0 = variancia inicial, T = maturacao em anos, K = strike, r = taxa de juros, N = num. simulacoes,
# M = num. passos (discretizacao) no tempo, kappa, theta, ksi, rho = parametros da volatilidade
def hestonMonteCarloOptionPricing(S0, K, r, T, v0, kappa, theta, ksi, rho, N, M, mode):
    St = hestonPaths(S0, v0, r, T, kappa, theta, ksi, rho, N, M)
        
    if (mode == "call"):
        payoffs = np.maximum(St - K, 0)
    elif (mode == "put"):
        payoffs = np.maximum(K - St, 0)
    else:
        print("Invalid mode.")
        
    price = np.exp(-r * T) * np.mean(payoffs)
    
    return price

# Estratégias
# Straddle: Duas opcoes, uma de call e outra de put, com mesmo T e K são compradas. Ganha se o preco do ativo se afastar muito do 
# preco de strike K, independente de sinal
def straddleMonteCarloSimulation(S0, K, r, sigma, T, N, plot):
    #Simulacao precos futuros
    St = GBMPaths(S0, r, sigma, T, N)
    
    # Calculo dos payoffs para cada simulacao
    callPayoff = np.maximum(St - K, 0)
    putPayoff = np.maximum(K - St, 0)
    grossPayoff = callPayoff + putPayoff
    
    #Calculo do preco das opcoes via monte carlo padrao
    callOptionPrice = monteCarloOptionPricing(S0, K, r, sigma, T, N, mode = "call")
    putOptionPrice = monteCarloOptionPricing(S0, K, r, sigma, T, N, mode = "put")
    
    #Calculando o preco da estraatégia
    straddleCost = callOptionPrice + putOptionPrice
    
    # Encontando o lucro da estratégia
    profit = grossPayoff - straddleCost
    
    # Montando um dicionario para armazenar as estatisticas
    stats = {
        "meanProfit": np.mean(profit),
        "stdProfit": np.std(profit),
        "probPosProfit": np.mean(profit > 0),
        "VaR5Pct": np.quantile(profit, 0.05),
        "VaR95Pct": np.quantile(profit, 0.95),
        "skewness": sps.skew(profit),
        "kurtosis": sps.kurtosis(profit, fisher=False),
        "sharpeRatio": np.mean(profit)/ np.std(profit) if np.std(profit) != 0 else np.nan
    }
    
    # Visualizacao
    if (plot == 1):
        plt.hist(profit, bins=100, density=True)
        plt.axvline(0, color='red', linestyle='--', label='Break-even')
        plt.title('Distribuição do Lucro (Straddle - Padrão)')
        plt.xlabel('Lucro')
        plt.ylabel('Densidade')
        plt.legend()
        plt.grid(True)
        plt.show()
        
    return stats

# Strangle: Nesse caso, compramos duas opcoes com maturacao T. Uma de put a um strike K1 e outra de call a um strike K2, K1 < K2.
# Ganha se o preco estiver no complementar do intervalo [K1, K2]. Toma prejuizo se estiver nesse intervalo
def strangleMonteCarloSimulation(S0, K1, K2, r, sigma, T, N, plot):
    # Simulando caminhos para os precos do ativo com GBM
    St = GBMPaths(S0, r, sigma, T, N)
    
    # Calculando os payoff
    callPayoff = np.maximum(St - K2, 0)
    putPayoff = np.maximum(K1 - St, 0)
    grossPayoff = callPayoff + putPayoff
    
    # Precificando agora as opcoes
    callPrice = monteCarloOptionPricing(S0, K2, r, sigma, T, N, mode="call")
    putPrice = monteCarloOptionPricing(S0, K1, r, sigma, T, N, mode="put")
    strangleCost = callPrice + putPrice
    
    # Calculando lucro
    profit = grossPayoff - strangleCost
    
    # Dicionário de estatisticas
    stats = {
        "meanProfit": np.mean(profit),
        "stdProfit": np.std(profit),
        "probPosProfit": np.mean(profit > 0),
        "VaR5Pct": np.quantile(profit, 0.05),
        "VaR95Pct": np.quantile(profit, 0.95),
        "skewness": sps.skew(profit),
        "kurtosis": sps.kurtosis(profit, fisher=False),
        "sharpeRatio": np.mean(profit)/ np.std(profit) if np.std(profit) != 0 else np.nan
    }

    # Visualizacao
    if plot == 1:
        plt.hist(profit, bins=100, density=True)
        plt.axvline(0, color='red', linestyle='--', label='Break-even')
        plt.title('Distribuição do Lucro (Strangle - Padrão)')
        plt.xlabel('Lucro')
        plt.ylabel('Densidade')
        plt.legend()
        plt.grid(True)
        plt.show()

    return stats 

# Long Call Butterfly: Temos a compra de duas opcoes de call com strike K1 e K3 e a venda de duas opcoes de call com strike K2; K1 < K2 < k3,
# de modo que K2 = (K1 + k3)/2, ou aproximado. Isso garante lucro máximo em K2 e prejuizo controlado fora das pontas K1 e K3. 
# A maturacao T eh idealmente a mesma para as tres opcoes que serao compradas

def longCallButterflyMonteCarloSimulation(S0, K1, K2, K3, r, sigma, T, N, plot):
    # Simulando trajetorias GBM
    St = GBMPaths(S0, r, sigma, T, N)
    
    # Calculando Payoffs
    payoff = np.maximum(St - K1, 0) - 2 * np.maximum(St - K2, 0) + np.maximum(St - K3, 0)

    # Precos das opcoes
    callK1 = monteCarloOptionPricing(S0, K1, r, sigma, T, N, "call")
    callK2 = monteCarloOptionPricing(S0, K2, r, sigma, T, N, "call")
    callK3 = monteCarloOptionPricing(S0, K3, r, sigma, T, N, "call")
    
    # Custo da estrategia
    butterflyCost = callK1 - 2 * callK2 + callK3
    
    # Encontrando o lucro
    profit = payoff - butterflyCost
    
    # Estatisticas
    stats = {
        "meanProfit": np.mean(profit),
        "stdProfit": np.std(profit),
        "probPosProfit": np.mean(profit > 0),
        "VaR5Pct": np.quantile(profit, 0.05),
        "VaR95Pct": np.quantile(profit, 0.95),
        "skewness": sps.skew(profit),
        "kurtosis": sps.kurtosis(profit, fisher=False),
        "sharpeRatio": np.mean(profit)/ np.std(profit) if np.std(profit) != 0 else np.nan
    }

    # Visualização
    if plot == 1:
        plt.hist(profit, bins=100, density=True)
        plt.axvline(0, color='red', linestyle='--', label='Break-even')
        plt.title('Distribuição do Lucro (Butterfly - Padrão)')
        plt.xlabel('Lucro')
        plt.ylabel('Densidade')
        plt.legend()
        plt.grid(True)
        plt.show()

    return stats
    
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
    
ticker = "QQQ"
ativo = yf.Ticker(ticker)
S0 = ativo.history(period="1d")["Close"][-1]

# 2. Pegar a data de vencimento mais próxima
vencimento = ativo.options[0]
opcoes = ativo.option_chain(vencimento)
calls = opcoes.calls
puts = opcoes.puts

# 3. Strikes mais relevantes
strike_straddle = calls.iloc[(calls['strike'] - S0).abs().argsort()[:1]].strike.values[0]

strike_put = puts[puts['strike'] < S0].iloc[-1].strike
strike_call = calls[calls['strike'] > S0].iloc[0].strike

K1 = calls[calls['strike'] < S0].iloc[-2].strike
K2 = strike_straddle
K3 = calls[calls['strike'] > S0].iloc[1].strike

# 4. Volatilidade implícita média
iv_call = calls[calls['strike'] == K2]['impliedVolatility'].values[0]
iv_put = puts[puts['strike'] == K2]['impliedVolatility'].values[0]
sigma = np.mean([iv_call, iv_put])

# 5. Parâmetros
r = 0.05
from datetime import date
from datetime import datetime as dt
T = (dt.strptime(vencimento, "%Y-%m-%d").date() - date.today()).days / 365
N = 100000

# 6. Rodar as estratégias com suas funções
print("STRADDLE")
straddle_stats = straddleMonteCarloSimulation(S0, K2, r, sigma, T, N, plot=1)
viewData(straddle_stats)

print("\nSTRANGLE")
strangle_stats = strangleMonteCarloSimulation(S0, strike_put, strike_call, r, sigma, T, N, plot=1)
viewData(strangle_stats)

print("\nBUTTERFLY")
butterfly_stats = longCallButterflyMonteCarloSimulation(S0, K1, K2, K3, r, sigma, T, N, plot=1)
viewData(butterfly_stats)
    

    









    