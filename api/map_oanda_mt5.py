import MetaTrader5 as mt5
from api.crud_api import get_stoploss_price, get_takeprofit_price, get_units_trade, get_instrument
from api.mt5_constants import mt5_COEFF, MAGIC, DEVIATION
from api.oanda_mt5_symbols import oanda_mt5_symbols


def start_mt5():
    try:
        authorized = mt5.initialize()
        print(f"MT5 initialized: {authorized}")
    except Exception as error:
        print(f"Failed to initialize MT5: {error}")


def map_order_oanda_to_mt5(trade):
    # Map the Oanda trade order to MT5 format

    stoploss = get_stoploss_price(trade)
    takeprofit = get_takeprofit_price(trade)
    units = get_units_trade(trade)
    oanda_instrument = get_instrument(trade)

    mt5_symbol = oanda_mt5_symbols[oanda_instrument]

    mt5_trade_order = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": mt5_symbol,
        "type": mt5.ORDER_TYPE_BUY if units > 0 else mt5.ORDER_TYPE_SELL,
        "price": mt5.symbol_info_tick(mt5_symbol).ask,
        "sl": stoploss,
        "tp": takeprofit,
        "comment": "",
        "magic": MAGIC,
        "deviation": DEVIATION,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    return mt5_trade_order


def duplicate_to_mt5(mt5_trade, mt5_account):
    try:
        order_result = mt5.order_send(mt5_trade)
        print(f'Trade {mt5_trade["symbol"]} duplicated success in MT5 account {mt5_account.login} '
              f'with response: {order_result.comment}')
    except Exception as e:
        print(f'Error duplicating trade {mt5_trade["symbol"]}: {str(e)}')
