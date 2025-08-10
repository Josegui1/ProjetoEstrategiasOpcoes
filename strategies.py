# Modulazrizando as estrategias. As abreviacoes sao MC = monte carlo, BS = black-Scholes, H = heston
import motionsAndPaths as mp
import optionPricing as op
import numpy as np
import scipy.stats as sps
import matplotlib.pyplot as plt

# Estratégias
# Straddle: Duas opcoes, uma de call e outra de put, com mesmo T e K são compradas. Ganha se o preco do ativo se afastar muito do 
# preco de strike K, independente de sinal
def straddleMCSimulation(S0, K, r, sigma, T, N, plot):
    #Simulacao precos futuros
    St = mp.GBMPaths(S0, r, sigma, T, N)
    
    # Calculo dos payoffs para cada simulacao
    callPayoff = np.maximum(St - K, 0)
    putPayoff = np.maximum(K - St, 0)
    grossPayoff = callPayoff + putPayoff
    
    #Calculo do preco das opcoes via monte carlo padrao
    callOptionPrice = op.monteCarloOptionPricing(S0, K, r, sigma, T, N, mode = "call")
    putOptionPrice = op.monteCarloOptionPricing(S0, K, r, sigma, T, N, mode = "put")
    
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
        plt.title('Distribuição do Lucro (Straddle - Monte Carlo)')
        plt.xlabel('Lucro')
        plt.ylabel('Densidade')
        plt.legend()
        plt.grid(True)
        plt.show()
        
    return stats

def straddleBSSimulation(S0, K, r, sigma,T, N, plot):
    # Simulando os caminhos
    St = mp.GBMPaths(S0, r, sigma, T, N)
    
    # Calculando o payoff de cada simulacao
    callPayoff = np.maximum(St - K, 0)
    putPayoff = np.maximum(K - St, 0)
    grossPayoff = callPayoff + putPayoff
    
    # Calculando o custo da estrategia agora
    callPrice = op.blackScholesOptionPricing(S0, K, r, sigma, T, mode = "call")
    putPrice = op.blackScholesOptionPricing(S0, K, r, sigma, T, mode = "put")
    straddleCost = callPrice + putPrice
    
    # Calculando o lucro da estrategia
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
        plt.title('Distribuição do Lucro (Straddle - Black-Scholes)')
        plt.xlabel('Lucro')
        plt.ylabel('Densidade')
        plt.legend()
        plt.grid(True)
        plt.show()
        
    return stats
    
    

# Strangle: Nesse caso, compramos duas opcoes com maturacao T. Uma de put a um strike K1 e outra de call a um strike K2, K1 < K2.
# Ganha se o preco estiver no complementar do intervalo [K1, K2]. Toma prejuizo se estiver nesse intervalo
def strangleMCSimulation(S0, K1, K2, r, sigma, T, N, plot):
    # Simulando caminhos para os precos do ativo com GBM
    St = mp.GBMPaths(S0, r, sigma, T, N)
    
    # Calculando os payoff
    callPayoff = np.maximum(St - K2, 0)
    putPayoff = np.maximum(K1 - St, 0)
    grossPayoff = callPayoff + putPayoff
    
    # Precificando agora as opcoes
    callPrice = op.monteCarloOptionPricing(S0, K2, r, sigma, T, N, mode="call")
    putPrice = op.monteCarloOptionPricing(S0, K1, r, sigma, T, N, mode="put")
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
        plt.title('Distribuição do Lucro (Strangle - Monte Carlo)')
        plt.xlabel('Lucro')
        plt.ylabel('Densidade')
        plt.legend()
        plt.grid(True)
        plt.show()

    return stats 

def strangleBSSimulation(S0, K1, K2, r, sigma, T, N, plot):
    # Simulando caminhos para os precos do ativo com GBM
    St = mp.GBMPaths(S0, r, sigma, T, N)
    
    # Calculando os payoff
    callPayoff = np.maximum(St - K2, 0)
    putPayoff = np.maximum(K1 - St, 0)
    grossPayoff = callPayoff + putPayoff
    
    # Precificando agora as opcoes
    callPrice = op.blackScholesOptionPricing(S0, K2, r, sigma, T, mode="call")
    putPrice = op.blackScholesOptionPricing(S0, K1, r, sigma, T, mode="put")
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
        plt.title('Distribuição do Lucro (Strangle - Black-Scholes)')
        plt.xlabel('Lucro')
        plt.ylabel('Densidade')
        plt.legend()
        plt.grid(True)
        plt.show()

    return stats 

# Long Call Butterfly: Temos a compra de duas opcoes de call com strike K1 e K3 e a venda de duas opcoes de call com strike K2; K1 < K2 < k3,
# de modo que K2 = (K1 + k3)/2, ou aproximado. Isso garante lucro máximo em K2 e prejuizo controlado fora das pontas K1 e K3. 
# A maturacao T eh idealmente a mesma para as tres opcoes que serao compradas
def longCallButterflyMCSimulation(S0, K1, K2, K3, r, sigma, T, N, plot):
    # Simulando trajetorias GBM
    St = mp.GBMPaths(S0, r, sigma, T, N)
    
    # Calculando Payoffs
    payoff = np.maximum(St - K1, 0) - 2 * np.maximum(St - K2, 0) + np.maximum(St - K3, 0)

    # Precos das opcoes
    callK1 = op.monteCarloOptionPricing(S0, K1, r, sigma, T, N, "call")
    callK2 = op.monteCarloOptionPricing(S0, K2, r, sigma, T, N, "call")
    callK3 = op.monteCarloOptionPricing(S0, K3, r, sigma, T, N, "call")
    
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
        plt.title('Distribuição do Lucro (Butterfly - Monte Carlo)')
        plt.xlabel('Lucro')
        plt.ylabel('Densidade')
        plt.legend()
        plt.grid(True)
        plt.show()

    return stats

def longCallButterflyBSSimulation(S0, K1, K2, K3, r, sigma, T, N, plot):
    # Simulando trajetorias GBM
    St = mp.GBMPaths(S0, r, sigma, T, N)
    
    # Calculando Payoffs
    payoff = np.maximum(St - K1, 0) - 2 * np.maximum(St - K2, 0) + np.maximum(St - K3, 0)

    # Precos das opcoes
    callK1 = op.blackScholesOptionPricing(S0, K1, r, sigma, T, "call")
    callK2 = op.blackScholesOptionPricing(S0, K2, r, sigma, T, "call")
    callK3 = op.blackScholesOptionPricing(S0, K3, r, sigma, T, "call")
    
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
        plt.title('Distribuição do Lucro (Butterfly - Black-Scholes)')
        plt.xlabel('Lucro')
        plt.ylabel('Densidade')
        plt.legend()
        plt.grid(True)
        plt.show()

    return stats

# Long Put Butterfly: Mesma ideia da long call, mas com opcoes de put
def longPutButterflyMCSimulation(S0, K1, K2, K3, r, sigma, T, N, plot):
    St = mp.GBMPaths(S0, r, sigma, T, N)

    # Payoff
    payoff = np.maximum(K1 - St, 0) - 2 * np.maximum(K2 - St, 0) + np.maximum(K3 - St, 0)

    # Preço das opções
    putK1 = op.monteCarloOptionPricing(S0, K1, r, sigma, T, N, "put")
    putK2 = op.monteCarloOptionPricing(S0, K2, r, sigma, T, N, "put")
    putK3 = op.monteCarloOptionPricing(S0, K3, r, sigma, T, N, "put")

    cost = putK1 - 2 * putK2 + putK3
    profit = payoff - cost

    stats = {
        "meanProfit": np.mean(profit),
        "stdProfit": np.std(profit),
        "probPosProfit": np.mean(profit > 0),
        "VaR5Pct": np.quantile(profit, 0.05),
        "VaR95Pct": np.quantile(profit, 0.95),
        "skewness": sps.skew(profit),
        "kurtosis": sps.kurtosis(profit, fisher=False),
        "sharpeRatio": np.mean(profit)/np.std(profit) if np.std(profit) != 0 else np.nan
    }

    if plot == 1:
        plt.hist(profit, bins=100, density=True)
        plt.axvline(0, color='red', linestyle='--')
        plt.title("Lucro - Long Put Butterfly (MC)")
        plt.xlabel("Lucro")
        plt.ylabel("Densidade")
        plt.grid(True)
        plt.show()

    return stats

def longPutButterflyBSSimulation(S0, K1, K2, K3, r, sigma, T, N, plot):
    St = mp.GBMPaths(S0, r, sigma, T, N)

    payoff = np.maximum(K1 - St, 0) - 2 * np.maximum(K2 - St, 0) + np.maximum(K3 - St, 0)

    putK1 = op.blackScholesOptionPricing(S0, K1, r, sigma, T, "put")
    putK2 = op.blackScholesOptionPricing(S0, K2, r, sigma, T, "put")
    putK3 = op.blackScholesOptionPricing(S0, K3, r, sigma, T, "put")

    cost = putK1 - 2 * putK2 + putK3
    profit = payoff - cost

    stats = {
        "meanProfit": np.mean(profit),
        "stdProfit": np.std(profit),
        "probPosProfit": np.mean(profit > 0),
        "VaR5Pct": np.quantile(profit, 0.05),
        "VaR95Pct": np.quantile(profit, 0.95),
        "skewness": sps.skew(profit),
        "kurtosis": sps.kurtosis(profit, fisher=False),
        "sharpeRatio": np.mean(profit)/np.std(profit) if np.std(profit) != 0 else np.nan
    }

    if plot == 1:
        plt.hist(profit, bins=100, density=True)
        plt.axvline(0, color='red', linestyle='--')
        plt.title("Lucro - Long Put Butterfly (BS)")
        plt.xlabel("Lucro")
        plt.ylabel("Densidade")
        plt.grid(True)
        plt.show()

    return stats

#Iron butterfly: Combinacao de uma short straddle em K2 central e uma call strangle em K1 e K3. Tem prejuizo se
# foge do intervalo [K1, K3] e maximo lucro em K2.
def ironButterflyMCSimulation(S0, K1, K2, K3, r, sigma, T, N, plot):
    # Simulando caminhos
    St = mp.GBMPaths(S0, r, sigma, T, N)
    
    # Payoff
    payoff = (-np.maximum(St - K2, 0) - np.maximum(K2 - St, 0) + np.maximum(St - K3, 0) + np.maximum(K1 - St, 0))
    
    # calculando o preco das opcoes e custo
    callSell = op.monteCarloOptionPricing(S0, K2, r, sigma, T, N, mode="call")
    putSell = op.monteCarloOptionPricing(S0, K2, r, sigma, T, N, mode="put")
    callBuy = op.monteCarloOptionPricing(S0, K3, r, sigma, T, N, mode="call")
    putBuy = op.monteCarloOptionPricing(S0, K1, r, sigma, T, N, mode="put")

    # Custo
    cost = (callSell + putSell) - (callBuy + putBuy) 
    
    # lucro
    profit = payoff + cost
    
    # Estatisticas
    stats = {
        "meanProfit": np.mean(profit),
        "stdProfit": np.std(profit),
        "probPosProfit": np.mean(profit > 0),
        "VaR5Pct": np.quantile(profit, 0.05),
        "VaR95Pct": np.quantile(profit, 0.95),
        "skewness": sps.skew(profit),
        "kurtosis": sps.kurtosis(profit, fisher=False),
        "sharpeRatio": np.mean(profit) / np.std(profit) if np.std(profit) != 0 else np.nan
    }

    # Visualização
    if plot == 1:
        plt.hist(profit, bins=100, density=True)
        plt.axvline(0, color='red', linestyle='--', label='Break-even')
        plt.title('Distribuição do Lucro (Iron Butterfly - Monte Carlo)')
        plt.xlabel('Lucro')
        plt.ylabel('Densidade')
        plt.legend()
        plt.grid(True)
        plt.show()

    return stats

def ironButterflyBSSimulation(S0, K1, K2, K3, r, sigma, T, N, plot):
    # Simulando caminhos
    St = mp.GBMPaths(S0, r, sigma, T, N)
    
    # Payoff
    payoff = (-np.maximum(St - K2, 0) - np.maximum(K2 - St, 0) + np.maximum(St - K3, 0) + np.maximum(K1 - St, 0))
    
    # calculando o preco das opcoes e custo
    callSell = op.blackScholesOptionPricing(S0, K2, r, sigma, T, mode="call")
    putSell = op.blackScholesOptionPricing(S0, K2, r, sigma, T, mode="put")
    callBuy = op.blackScholesOptionPricing(S0, K3, r, sigma, T, mode="call")
    putBuy = op.blackScholesOptionPricing(S0, K1, r, sigma, T, mode="put")

    # Custo
    cost = (callSell + putSell) - (callBuy + putBuy) 
    
    # lucro
    profit = payoff + cost
    
    # Estatisticas
    stats = {
        "meanProfit": np.mean(profit),
        "stdProfit": np.std(profit),
        "probPosProfit": np.mean(profit > 0),
        "VaR5Pct": np.quantile(profit, 0.05),
        "VaR95Pct": np.quantile(profit, 0.95),
        "skewness": sps.skew(profit),
        "kurtosis": sps.kurtosis(profit, fisher=False),
        "sharpeRatio": np.mean(profit) / np.std(profit) if np.std(profit) != 0 else np.nan
    }

    # Visualização
    if plot == 1:
        plt.hist(profit, bins=100, density=True)
        plt.axvline(0, color='red', linestyle='--', label='Break-even')
        plt.title('Distribuição do Lucro (Iron Butterfly - Black-Scholes)')
        plt.xlabel('Lucro')
        plt.ylabel('Densidade')
        plt.legend()
        plt.grid(True)
        plt.show()

    return stats

# Bull Call: Compramos uma call com K1 e vendemos uma call com K2, ambas com T e K1 < K2. Se St < K1, prejuizo.
# Se St pertence a [K1, K2], lucro parcial. Se St > K2, lucro máximo = K2 - K1 - custo. Espera-se que o ativo
# suba, mas nao demais, afinal a estrategia limita o lucro e o prejuizo
def bullCallMCSimulation(S0, K1, K2, r, sigma, T, N, plot):
    # Simulando caminhos
    St = mp.GBMPaths(S0, r, sigma, T, N)
    
    # Payoff 
    payoff = np.maximum(St - K1, 0) - np.maximum(St - K2, 0)
    
    # Calculando o custo das opcoes 
    callK1 = op.monteCarloOptionPricing(S0, K1, r, sigma, T, N, mode="call")
    callK2 = op.monteCarloOptionPricing(S0, K2, r, sigma, T, N, mode="call")
    cost = callK1 - callK2
    
    # Encontrando lucro líquido
    profit = payoff - cost
    
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

    if plot == 1:
        plt.hist(profit, bins=100, density=True)
        plt.axvline(0, color='red', linestyle='--', label='Break-even')
        plt.title('Distribuição do Lucro (Bull Call Spread - Monte Carlo)')
        plt.xlabel('Lucro')
        plt.ylabel('Densidade')
        plt.legend()
        plt.grid(True)
        plt.show()

    return stats

def bullCallBSSimulation(S0, K1, K2, r, sigma, T, N, plot):
    # Simulando caminhos
    St = mp.GBMPaths(S0, r, sigma, T, N)
    
    # Payoff 
    payoff = np.maximum(St - K1, 0) - np.maximum(St - K2, 0)
    
    # Calculando o custo das opcoes 
    callK1 = op.blackScholesOptionPricing(S0, K1, r, sigma, T, mode="call")
    callK2 = op.blackScholesOptionPricing(S0, K2, r, sigma, T, mode="call")
    cost = callK1 - callK2
    
    # Encontrando lucro líquido
    profit = payoff - cost
    
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

    if plot == 1:
        plt.hist(profit, bins=100, density=True)
        plt.axvline(0, color='red', linestyle='--', label='Break-even')
        plt.title('Distribuição do Lucro (Bull Call Spread - Black-Scholes)')
        plt.xlabel('Lucro')
        plt.ylabel('Densidade')
        plt.legend()
        plt.grid(True)
        plt.show()

    return stats

# Bear Put: Mais ou menos a mesma premissa da bull call, mas com put. Espera-se uma queda moderada no preco St
# Compramos uma put com K2 e vendemos uma put com K1, K1 < K2 e T.Tem prejuizo se St > K2
def bearPutMCSimulation(S0, K1, K2, r, sigma, T, N, plot):
    # Simulando caminhos
    St = mp.GBMPaths(S0, r, sigma, T, N)
    
    # Payoff
    payoff = np.maximum(K2 - St, 0) - np.maximum(K1 - St, 0)
    
    # Calculando o custo das opcoes
    putK2 = op.monteCarloOptionPricing(S0, K2, r, sigma, T, N, mode="put")
    putK1 = op.monteCarloOptionPricing(S0, K1, r, sigma, T, N, mode="put")
    cost = putK2 - putK1
    
    # lucro 
    profit = payoff - cost
    
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

    if plot == 1:
        plt.hist(profit, bins=100, density=True)
        plt.axvline(0, color='red', linestyle='--', label='Break-even')
        plt.title('Distribuição do Lucro (Bear Put Spread - Monte Carlo)')
        plt.xlabel('Lucro')
        plt.ylabel('Densidade')
        plt.legend()
        plt.grid(True)
        plt.show()

    return stats

def bearPutBSSimulation(S0, K1, K2, r, sigma, T, N, plot):
    # Simulando caminhos
    St = mp.GBMPaths(S0, r, sigma, T, N)
    
    # Payoff
    payoff = np.maximum(K2 - St, 0) - np.maximum(K1 - St, 0)
    
    # Calculando o custo das opcoes
    putK2 = op.blackScholesOptionPricing(S0, K2, r, sigma, T, mode="put")
    putK1 = op.blackScholesOptionPricing(S0, K1, r, sigma, T, mode="put")
    cost = putK2 - putK1
    
    # lucro 
    profit = payoff - cost
    
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

    if plot == 1:
        plt.hist(profit, bins=100, density=True)
        plt.axvline(0, color='red', linestyle='--', label='Break-even')
        plt.title('Distribuição do Lucro (Bear Put Spread - Black-Scholes)')
        plt.xlabel('Lucro')
        plt.ylabel('Densidade')
        plt.legend()
        plt.grid(True)
        plt.show()

    return stats

# Long call: A estrategia mais simples que ha. Apostamos que um ativo ira subir e compramos uma opcao de call com
# K e T. O lucro eh simplesmente max(St - K, 0) - premio pago pela call. Teoricamente ele eh ilimitado, mas o pre
# juizo eh limitado ao pago pelo premio
def longCallMCSimulation(S0, K, r, sigma, T, N, plot):
    # Simulando caminhos GBM
    St = mp.GBMPaths(S0, r, sigma, T, N)
    
    # Calculando o payoff
    payoff = np.maximum(St - K, 0)
    
    # Calculando o premio 
    cost = op.monteCarloOptionPricing(S0, K, r, sigma, T, N, mode="call")
    
    # lucro 
    profit =  payoff - cost
    
    stats = {
        "meanProfit": np.mean(profit),
        "stdProfit": np.std(profit),
        "probPosProfit": np.mean(profit > 0),
        "VaR5Pct": np.quantile(profit, 0.05),
        "VaR95Pct": np.quantile(profit, 0.95),
        "skewness": sps.skew(profit),
        "kurtosis": sps.kurtosis(profit, fisher=False),
        "sharpeRatio": np.mean(profit) / np.std(profit) if np.std(profit) != 0 else np.nan
    }

    if plot == 1:
        plt.hist(profit, bins=100, density=True)
        plt.axvline(0, color="red", linestyle="--", label="Break-even")
        plt.title("Distribuição do Lucro (Long Call - Monte Carlo)")
        plt.xlabel("Lucro")
        plt.ylabel("Densidade")
        plt.legend()
        plt.grid(True)
        plt.show()

    return stats

def longCallBSSimulation(S0, K, r, sigma, T, N, plot):
    # Simulando caminhos GBM
    St = mp.GBMPaths(S0, r, sigma, T, N)
    
    # Calculando o payoff
    payoff = np.maximum(St - K, 0)
    
    # Calculando o premio 
    cost = op.blackScholesOptionPricing(S0, K, r, sigma, T, mode="call")
    
    # lucro 
    profit =  payoff - cost
    
    stats = {
        "meanProfit": np.mean(profit),
        "stdProfit": np.std(profit),
        "probPosProfit": np.mean(profit > 0),
        "VaR5Pct": np.quantile(profit, 0.05),
        "VaR95Pct": np.quantile(profit, 0.95),
        "skewness": sps.skew(profit),
        "kurtosis": sps.kurtosis(profit, fisher=False),
        "sharpeRatio": np.mean(profit) / np.std(profit) if np.std(profit) != 0 else np.nan
    }

    if plot == 1:
        plt.hist(profit, bins=100, density=True)
        plt.axvline(0, color="red", linestyle="--", label="Break-even")
        plt.title("Distribuição do Lucro (Long Call - Black-Scholes)")
        plt.xlabel("Lucro")
        plt.ylabel("Densidade")
        plt.legend()
        plt.grid(True)
        plt.show()

    return stats
    
# Long put: A ideia aqui eh como a long call, mas com queda agora. Compramos uma opcao de put no lugar da call.
# O lucro  eh max(K - St, 0) - premio da put

def longPutMCSimulation(S0, K, r, sigma, T, N, plot):
    # simulando caminhos
    St = mp.GBMPaths(S0, r, sigma, T, N)
    
    # Calculando o payoff
    payoff = np.maximum(K - St, 0)
    
    # Calculando o premio
    cost = op.monteCarloOptionPricing(S0, K, r, sigma, T, N, mode="put")
    
    # Encontrando o lucro 
    profit = payoff - cost
    
    stats = {
        "meanProfit": np.mean(profit),
        "stdProfit": np.std(profit),
        "probPosProfit": np.mean(profit > 0),
        "VaR5Pct": np.quantile(profit, 0.05),
        "VaR95Pct": np.quantile(profit, 0.95),
        "skewness": sps.skew(profit),
        "kurtosis": sps.kurtosis(profit, fisher=False),
        "sharpeRatio": np.mean(profit) / np.std(profit) if np.std(profit) != 0 else np.nan
    }

    if plot == 1:
        plt.hist(profit, bins=100, density=True)
        plt.axvline(0, color="red", linestyle="--", label="Break-even")
        plt.title("Distribuição do Lucro (Long Put - Monte Carlo)")
        plt.xlabel("Lucro")
        plt.ylabel("Densidade")
        plt.legend()
        plt.grid(True)
        plt.show()

    return stats

def longPutBSSimulation(S0, K, r, sigma, T, N, plot):
    # simulando caminhos
    St = mp.GBMPaths(S0, r, sigma, T, N)
    
    # Calculando o payoff
    payoff = np.maximum(K - St, 0)
    
    # Calculando o premio
    cost = op.blackScholesOptionPricing(S0, K, r, sigma, T, mode="put")

    
    # Encontrando o lucro 
    profit = payoff - cost
    
    stats = {
        "meanProfit": np.mean(profit),
        "stdProfit": np.std(profit),
        "probPosProfit": np.mean(profit > 0),
        "VaR5Pct": np.quantile(profit, 0.05),
        "VaR95Pct": np.quantile(profit, 0.95),
        "skewness": sps.skew(profit),
        "kurtosis": sps.kurtosis(profit, fisher=False),
        "sharpeRatio": np.mean(profit) / np.std(profit) if np.std(profit) != 0 else np.nan
    }

    if plot == 1:
        plt.hist(profit, bins=100, density=True)
        plt.axvline(0, color="red", linestyle="--", label="Break-even")
        plt.title("Distribuição do Lucro (Long Put - Black-Scholes)")
        plt.xlabel("Lucro")
        plt.ylabel("Densidade")
        plt.legend()
        plt.grid(True)
        plt.show()

    return stats


    




    



