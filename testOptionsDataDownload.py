# Importando dados de opcoes
import yfinance as yf

ticker = yf.Ticker("MSFT")

# Datas de vencimento de opcoes
expirationDates = ticker.options
print(expirationDates)

options = ticker.option_chain(expirationDates[10])
desiredColumns = ["contractSymbol", "strike"]

calls = options.calls[desiredColumns]
puts = options.puts[desiredColumns]

print(calls)
print(puts.head())