def calculatePercent(odd1, odd2):
    profit = odd1 - 1
    hedge = profit/odd2

    percentReturn = profit - hedge
    return percentReturn



print(calculatePercent(7, 1.81))
