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
        plt.title('Distribuição do Lucro (Straddle - Padrão)')
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
        plt.title('Distribuição do Lucro (Straddle - Padrão)')
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
        plt.title('Distribuição do Lucro (Strangle - Padrão)')
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
        plt.title('Distribuição do Lucro (Butterfly - Padrão)')
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
    
# ------------------------------------------------------------------
# PARÂMETROS GERAIS (muda se quiser testar outra combinação)
S0     = 100        # preço do ativo hoje
r      = 0.05       # taxa livre de risco anual
sigma  = 0.25       # volatilidade anual
T      = 0.5        # tempo até o vencimento (anos)
N      = 100_000    # número de simulações Monte Carlo
plot   = 1          # 1 = exibe gráfico, 0 = não exibe

# ------------------------------------------------------------------
# 1) STRADDLE (K único)
K      = 100        # strike comum da call e da put

print("\n=== STRADDLE (Black‑Scholes) ===")
stats_straddle = straddleBSSimulation(S0, K, r, sigma, T, N, plot)
viewData(stats_straddle)

# ------------------------------------------------------------------
# 2) STRANGLE (Put K1, Call K2)
K1     = 90         # strike da put
K2     = 110        # strike da call

print("\n=== STRANGLE (Black‑Scholes) ===")
stats_strangle = strangleBSSimulation(S0, K1, K2, r, sigma, T, N, plot)
viewData(stats_strangle)

# ------------------------------------------------------------------
# 3) LONG CALL BUTTERFLY (K1 < K2 < K3)
K1_bfly = 90
K2_bfly = 100
K3_bfly = 110

print("\n=== LONG CALL BUTTERFLY (Black‑Scholes) ===")
stats_bfly = longCallButterflyBSSimulation(S0, K1_bfly, K2_bfly, K3_bfly,
                                           r, sigma, T, N, plot)
viewData(stats_bfly)

# ------------------------------------------------------------------
print("\n✅  Fim das simulações.")

    

    









    