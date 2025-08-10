# Modularizando o cálculo das gregas
from math import sqrt
import numpy as np
import scipy.stats as sps

def Delta(S0, K, r, sigma, T, mode):
    d1 = (np.log(S0/K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    
    if (mode == "call"):
        delta = sps.norm.cdf(d1)
    elif (mode == "put"):
        delta = sps.norm.cdf(d1) - 1
    else:
        print("Invalid mode.")
        
    return delta

def Gamma(S0, K, r, sigma, T):
    d1 = (np.log(S0/K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    gamma = sps.norm.pdf(d1) / (S0*sigma*sqrt(T))
    
    return gamma 

def Vega(S0, K, r, sigma, T):
    d1 = (np.log(S0/K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    vega = S0 * sps.norm.pdf(d1) * sqrt(T) 
    
    return vega

def Theta(S0, K, r, sigma, T, mode):
    d1 = (np.log(S0/K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    disc = np.exp(-r * T)
    
    if (mode == "call"):
        theta = -(S0 * sps.norm.pdf(d1) * sigma ) / (2*sqrt(T)) - r * K * disc  * sps.norm.cdf(d2)
    elif (mode == "put"):
        theta = -(S0 * sps.norm.pdf(d1) * sigma ) / (2*sqrt(T)) + r * K * disc * sps.norm.cdf(d2)    
    else:
        print("Invalid mode")
    
    return theta 

def Rho(S0, K, r, sigma, T, mode):
    d1 = (np.log(S0/K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    disc = np.exp(-r * T)
    
    if (mode == "call"):
        rho = K * T * disc * sps.norm.cdf(d2)
    elif (mode == "put"):
        rho = - K * T * disc * sps.norm.cdf(-d2) 
    else:
        print("Invalid mode")
        
    return rho

def Vanna(S0, K, r, sigma, T):
    d1 = (np.log(S0/K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    vanna = S0 * sps.norm.pdf(d1) * sqrt(T) * (1 - d1/sigma*sqrt(T))
    return vanna

def Vomma(S0, K, r, sigma, T):
    vega = Vega(S0, K, r, sigma, T)
    d1 = (np.log(S0/K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    vomma = vega * (d1*d2)/sigma
    
    return vomma

