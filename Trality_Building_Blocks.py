# How to obtain data
@schedule(interval="5m", symbol="BTCUSDT")
def run(state, data):
    ''' data_object will contain information about BTCUSDT in the 5m interval '''
    data_object = data
    print(data_object)

# Limit Order
order_limit_amount(symbol="BTCUSDT", amount=0.05, limit_price=45000.00)

# Balance
btc = query_balance("BTC")
eth = query_balance("ETH")
print( btc.free, eth.free)

# Portfolio
query_portfolio()
query_portfolio_pnl()

# Plotting
@schedule(interval="10m",symbol="ETHUSDT")
def handler(state,data):
    with PlotScope.group("my_group", data.symbol):
        plot_line("foo", 1.5)
        plot_line("bar", 1.2)