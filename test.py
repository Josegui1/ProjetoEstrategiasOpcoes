import dataGetter as dg
import optionPricing as op

S0, K, sigma, T, r, optionType = dg.getBSData("AAPL", 3, 250, "call")
print("=================================================================")
print(S0)
print(K)
print(sigma)
print(T)
print(r)
print(optionType)

o = op.blackScholesOptionPricing(S0, K, r, sigma, T, mode = optionType)
print(o)