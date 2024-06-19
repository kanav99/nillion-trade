from nada_dsl import *

def initialize_parties(nr_parties):
    parties = []
    for i in range(nr_parties):
        parties.append(Party(name="Party" + str(i)))

    return parties

def input_stocks(nr_stocks, nr_parties, parties):
    stocks = []
    for i in range(nr_parties):
        stocks.append([])
        for j in range(nr_stocks*2):
            stocks[i].append(SecretInteger(Input(name="stock_p" + str(i) + "_s" + str(j), party=parties[i])) - Integer(1))

    return stocks

def validate_stocks(stocks, nr_stocks, nr_parties):
    bit = Integer(1)
    one = Integer(1)
    for i in range(nr_parties):
        for j in range(nr_stocks):
            # either selling or buying side should be 0
            bit = bit * (one - stocks[i][j] * stocks[i][j + nr_stocks])
    return bit

def min(x, y):
    compare = (x < y)
    return compare.if_else(x, y)

def trade(stocks, nr_stocks):
    trade_stocks = []
    for i in range(nr_stocks):
        volume = min(stocks[0][i], stocks[1][i+nr_stocks]) + min(stocks[0][i+nr_stocks], stocks[1][i])
        trade_stocks.append(volume)
    return trade_stocks

def nada_main():
    nr_parties = 2
    nr_stocks = 5

    parties = initialize_parties(2)
    stocks = input_stocks(nr_stocks, nr_parties, parties)
    valid_bit = validate_stocks(stocks, nr_stocks, nr_parties)

    trade_stocks = trade(stocks, nr_stocks)

    outputs: list[Output] = [Output(valid_bit, "valid_bit", parties[0])]
    for i in range(nr_stocks):
        outputs.append(Output(
            trade_stocks[i],
            "trade_" + str(i),
            parties[0]
        ))

    return outputs
