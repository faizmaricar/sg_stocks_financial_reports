import pandas as pd

from stock import Stock

stock = Stock("D05")

print(stock.income_statement)
print(stock.balance_sheet)
print(stock.cash_flows)