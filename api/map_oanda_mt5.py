import MetaTrader5 as mt5
from api.lots_calculation import convert_units_to_volume
from api.mt5_constants import mt5_COEFF, MAGIC, DEVIATION
from api.oanda_mt5_symbols import oanda_mt5_symbols


def start_mt5():
    try:
        authorized = mt5.initialize()
        print(f"MT5 initialized: {authorized}")
    except Exception as error:
        print(f"Failed to initialize MT5: {error}")


def enable_symbol(symbol: str):
    # check if the symbol is available for trading
    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info.visible:
        # add the symbol to the "Market Watch" window
        if not mt5.symbol_select(symbol, True):
            print(f"Failed to add {symbol} to Market Watch")


def map_order_oanda_to_mt5(order_type, oanda_instrument, stop_loss, take_profit):
    # Map the Oanda trade order to MT5 format

    mt5_symbol = oanda_mt5_symbols[oanda_instrument]

    enable_symbol(mt5_symbol)

    price = mt5.symbol_info_tick(mt5_symbol).ask if order_type == mt5.ORDER_TYPE_BUY else \
        mt5.symbol_info_tick(mt5_symbol).bid

    mt5_trade_order = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": mt5_symbol,
        "type": order_type,
        "price": price,
        "sl": stop_loss,
        "tp": take_profit,
        "comment": "",
        "magic": MAGIC,
        "deviation": DEVIATION,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    return mt5_trade_order


def duplicate_to_mt5(mt5_trade, mt5_accounts, lots):

    # Send order to mt5
    for account in mt5_accounts:
        try:
            mt5.login(login=account.login, password=account.password, server=account.server)
            mt5_account_balance = mt5.account_info().balance
            account_balance_units = lots.calculate_units_per_trade(mt5_account_balance)
            volume = convert_units_to_volume(account_balance_units)
            mt5_trade["volume"] = abs(volume)
            order_result = mt5.order_send(mt5_trade)
            print(f'Trade {mt5_trade["symbol"]} duplicated success in MT5 account {account.login} '
                  f'with response: {order_result.comment}')
        except Exception as e:
            print(f'Error duplicating trade {mt5_trade["symbol"]}: {str(e)}')

    mt5.shutdown()
