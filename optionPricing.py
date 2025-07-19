# Modularizacao para precificar opcoes
import motionsAndPaths as mp
import numpy as np
import scipy.stats as sps

# S0 = preco inicial, K = strike, r = taxa de juros, T = maturacao em anos, N = num. simulacoes, mode = call ou put
def monteCarloOptionPricing(S0, K, r, sigma, T, N, mode):
    St = mp.GBMPaths(S0, r, sigma, T, N)
    
    if (mode == "call"):
        payoffs = np.maximum(St - K, 0)
    elif (mode == "put"):
        payoffs = np.maximum(K - St, 0)
    else:
        print("Invalid mode.")
        
    price = np.exp(-r * T) * np.mean(payoffs)
    
    return price

# S0 = preco inicial do ativo, K = strike, r = taxa de juros, sigma = volatilidade ativo, mode = call ou put
def blackScholesOptionPricing(S0, K, r, sigma, T, mode):
    d1 = (np.log(S0/K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if (mode == "call"):
        return S0 * sps.norm.cdf(d1) - K * np.exp(-r * T) * sps.norm.cdf(d2)
    elif (mode == "put"):
        return K * np.exp(-r * T) * sps.norm.cdf(-d2) - S0 * sps.norm.cdf(-d1)
    else:
        print("Invalid mode.")
        
# Heston eh um modelo de volaitilidade estocastica, voltado para o trabalho de opcoes com smiles
# S0 = preco inicial, v0 = variancia inicial, T = maturacao em anos, K = strike, r = taxa de juros, N = num. simulacoes,
# M = num. passos (discretizacao) no tempo, kappa, theta, ksi, rho = parametros da volatilidade
def hestonMonteCarloOptionPricing(S0, K, r, T, v0, kappa, theta, ksi, rho, N, M, mode):
    St = mp.hestonPaths(S0, v0, r, T, kappa, theta, ksi, rho, N, M)
        
    if (mode == "call"):
        payoffs = np.maximum(St - K, 0)
    elif (mode == "put"):
        payoffs = np.maximum(K - St, 0)
    else:
        print("Invalid mode.")
        
    price = np.exp(-r * T) * np.mean(payoffs)
    
    return price



