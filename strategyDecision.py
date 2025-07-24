# Modularizando a escolha de estrategias dadas certas caracteristicas dos ativos
import strategies as st
import dataGetter as dg
import fairValue as fv
import numpy as np

def choseAndRunStrategy(ticker, targetStrike, optionType, expirationIndex, method, N, plot):
    # Coletando dados reais da opcao e do drift
    S0, K2, sigma, T, r = dg.getBSData(ticker, expirationIndex, targetStrike, optionType)
    
    muMean = dg.getMuMean(ticker)
    muStd = dg.getMuStd(ticker)
    fair = fv.monteCarloGBMRDPricing(S0, muMean, muStd, 500, sigma, T, N)
    
    K1 = dg.getOptionsData(ticker, expirationIndex, optionType, 0.75 * targetStrike)["strike"]
    K3 = dg.getOptionsData(ticker, expirationIndex, optionType, 1.25 * targetStrike)["strike"]
    
    # Fazendo uma analise da diferenca do fair pelo S0
    diff = (fair - S0)

    # Decisão baseada no tipo da opção
    if optionType == "call":
        if diff > 0.1 * S0:
            print("🟢 Ativo subvalorizado. Estratégia: Bull Call Spread")
            return st.bullCallBSSimulation(S0, K1, K3, r, sigma, T, N, plot)
        elif abs(diff) <= 0.1 * S0 and sigma > 0.4:
            print("📈 Justo mas volátil. Estratégia: Straddle")
            return st.straddleBSSimulation(S0, K2, r, sigma, T, N, plot)
        elif abs(diff) <= 0.1 * S0 and sigma <= 0.2:
            print("📉 Justo e calmo. Estratégia: Iron Butterfly")
            return st.ironButterflyBSSimulation(S0, K1, K2, K3, r, sigma, T, N, plot)
        else:
            print("⚠️ Ambíguo. Fallback: Long Call")
            return st.longCallBSSimulation(S0, K2, r, sigma, T, N, plot)

    elif optionType == "put":
        if diff < -0.1 * S0:
            print("🔴 Ativo sobrevalorizado. Estratégia: Bear Put Spread")
            return st.bearPutBSSimulation(S0, K1, K3, r, sigma, T, N, plot)
        elif abs(diff) <= 0.1 * S0 and sigma > 0.4:
            print("📈 Justo mas volátil. Estratégia: Straddle")
            return st.straddleBSSimulation(S0, K2, r, sigma, T, N, plot)
        elif abs(diff) <= 0.1 * S0 and sigma <= 0.2:
            print("📉 Justo e calmo. Estratégia: Iron Butterfly")
            return st.ironButterflyBSSimulation(S0, K1, K2, K3, r, sigma, T, N, plot)
        else:
            print("⚠️ Ambíguo. Fallback: Long Put")
            return st.longPutBSSimulation(S0, K2, r, sigma, T, N, plot)

    else:
        raise ValueError("optionType deve ser 'call' ou 'put'.")
        
        
        
        
        
    
        
    
    
    
    
    
    
