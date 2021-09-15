def initialize(state):
    state.number_offset_trades = 0;

@schedule(interval="1h", symbol="CAKEUSDT")
def handler(state, data):

    macd_ind = data.macd(12,26,9)

    # In case of errors
    if macd_ind is None:
        return

    signal = macd_ind['macd_signal'].last
    macd = macd_ind['macd'].last

    current_price = data.close_last
    
    portfolio = query_portfolio()
    balance_quoted = portfolio.excess_liquidity_quoted
    buying_power = float(balance_quoted) * 0.85
    
    position = query_open_position_by_symbol(data.symbol,include_dust=False)
    has_position = position is not None

    if macd > signal and not has_position:
        print("---Buy Order---")
        print("Bought ", buying_power, " at market price: ", data.close_last)
        order_market_value(symbol=data.symbol, value=buying_power)
        
    elif macd < signal and has_position:
        print("---Sell Order---")
        logmsg = "Closing {} position with exposure {} at market price of {}"
        print(logmsg.format(data.symbol,float(position.exposure),data.close_last))
        close_position(data.symbol)
    
    if state.number_offset_trades < portfolio.number_of_offsetting_trades:
        
        pnl = query_portfolio_pnl()
        print("-------")
        print("Accumulated Pnl of Strategy: {}".format(pnl))
        
        offset_trades = portfolio.number_of_offsetting_trades
        number_winners = portfolio.number_of_winning_trades
        print("Number of winning trades {}/{}.".format(number_winners,offset_trades))
        print("Best trade Return : {:.2%}".format(portfolio.best_trade_return))
        print("Worst trade Return : {:.2%}".format(portfolio.worst_trade_return))
        print("Average Profit per Winning Trade : {:.2f}".format(portfolio.average_profit_per_winning_trade))
        print("Average Loss per Losing Trade : {:.2f}".format(portfolio.average_loss_per_losing_trade))
        # reset number offset trades
        state.number_offset_trades = portfolio.number_of_offsetting_trades