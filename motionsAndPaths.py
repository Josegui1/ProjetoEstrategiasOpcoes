# Modularizando os movimentos
import numpy.random as npr
import numpy as np

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