import MetaTrader5 as mt5
from api.mt5_constants import mt5_COEFF, MAGIC, DEVIATION
from api.oanda_mt5_symbols import oanda_mt5_symbols


def login_mt5():
    try:
        authorized = mt5.initialize()
        print(f"authorized accepted: {authorized}")
    except Exception as error:
        print(f"Failed to initialize MT5: {error}")


def map_order_oanda_to_mt5(trade):
    # Map the Oanda trade order to MT5 format

    mt5_SYMBOL = oanda_mt5_symbols[trade["instrument"]]
    units = float(trade["initialUnits"])
    stoploss = float(trade["stopLossOrder"]["price"])
    takeprofit = float(trade["takeProfitOrder"]["price"])

    # TODO: improve tha calculation of the COEFF for any units or volume
    volume = round(units * mt5_COEFF, 2)

    mt5_trade_order = {
        "action": mt5.TRADE_ACTION_DEAL,
        "volume": volume,
        "symbol": mt5_SYMBOL,
        "type": mt5.ORDER_TYPE_BUY if units > 0 else mt5.ORDER_TYPE_SELL,
        "price": mt5.symbol_info_tick(mt5_SYMBOL).ask,
        "sl": stoploss,
        "tp": takeprofit,
        "comment": "",
        "magic": MAGIC,
        "deviation": DEVIATION,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    return mt5_trade_order


def duplicate_to_mt5(oanda_trade, accounts):
    # Map oanda order to mt5
    mt5_trade_request = map_order_oanda_to_mt5(oanda_trade)
    # Send order to mt5
    for account in accounts:
        try:
            mt5.login(login=account.login, password=account.password, server=account.server)
            order_result = mt5.order_send(mt5_trade_request)
            print(f"duplicated success in MT5 with response: {order_result}")
        except Exception as e:
            print(f"Error duplicating trade {oanda_trade['instrument']}: {str(e)}")
