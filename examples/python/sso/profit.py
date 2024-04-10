import requests
import json
from threading import Thread,Lock


def CalculateProfit(buy, sell, tax_rate, trading_fee):
    return sell - buy - sell * (tax_rate + trading_fee)

if __name__ == "__main__":
    buy = 90110000.00
    sell = 105000000.00
    tax_rate = 0.08
    trading_fee = 0.0234
    profit = CalculateProfit(buy, sell, tax_rate, trading_fee)
    
    print("Buy:", buy)
    print("Sell:", sell)
    print("Tax Rate:", tax_rate)
    print("Trading Fee:", trading_fee)
    print("Profit:", profit)


