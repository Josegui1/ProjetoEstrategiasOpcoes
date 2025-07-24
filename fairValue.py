# Modularizando a precificacao de ativos para auxiliar a estrategia de opcoes
import motionsAndPaths as mp
import numpy.random as npr
import numpy as np

# Se parece muito com precificacao de opcoes, mas ao inves de usar a taxa livre de riscos r, usamos um drift de 
# crescimento mu, de modo que o ativo nao tenha mais valor esperado futuro neutro S0. Isso eh o que
# ocorreria ao utilizar o r, que eh uma medida neutra de risco. Eh importante estimar esses parametros com
# retornos logaritmos e adaptar para o tempo que iremos trabalhar(Ex.: anual = mu* 252, etc)
def monteCarloGBMPricing(S0, mu, sigma, T, N):
    # Simulando N GBM
    St = mp.GBMPaths(S0, mu, sigma, T, N)
    
    # Tomando a media deles
    fairValue = np.mean(St)
    
    return fairValue

# Uma desvantagem desse modelo eh considerar que o drift de crescimento eh constante, o que se mostra irreal
# Para burlar isso, podemos com base na media e na variancia de mu fazer varias simulacoes. RD = randon drift
def monteCarloGBMRDPricing(S0, muMean, muStd, M, sigma, T, N):
    # Simulando M mus diferentes como drift
    mus = npr.normal(muMean, muStd, M)
    
    #Simulando caminhos agora usando cada mu diferente
    Z = npr.randn(M, N)
    St = S0 * np.exp((mus[:, None] - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    
    # Retornando a media de cada caminho com
    return np.mean(St)   

# Outro modelo interessante eh o de relativeValuation.Ele consiste no seguinte. Tome como proxy a media de uma
# metrica generica dos pares de um ativo. Compare com a metrica do ativo que queremos precificar. Se menor que a
# media, subprecificado; se maior, superprecificado. Vamos primeiro ver isso com indice Sharpe, pois eh uma metrica
# puramente de mercado. Considere SP = sharpe proxy, mu = retorno esperado, sigma = volatilidade, peers são listas  
def relativeValuationSPPricing(muAsset, sigmaAsset, muPeers, sigmaPeers, S0Asset):
    # Criando o sharpe dos pares
    sharpePeers = np.array(muPeers)/np.array(sigmaPeers)
    
    # Calculando a media do sharpe dos pares para usar como proxy
    avgSharpe = np.mean(sharpePeers)
    
    # Calculando o sharpe do ativo
    sharpeAsset = muAsset/sigmaAsset
    
    # Encontrando a razao entre o sharpe do ativo e o sharpe medio dos pares
    valuationRatio = sharpeAsset/avgSharpe
    
    # Encontrando o fair value
    fairValue = S0Asset * valuationRatio
    
    return fairValue

# A premissa disso eh basica: Se o ativo tiver um melhor retorno/risco do que seus pares, entao ele esta subvalorizado
# Se tiver um pior retorno/risco, está supervalorizado. Mas podemos fazer isso com varias outras metricas, como
# retorno, volatilidade, beta, correlacao

