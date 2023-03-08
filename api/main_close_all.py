from api.crud_api import OandaAPI
from constants import SOURCE_ACCOUNT, DESTINATION_ACCOUNT
import MetaTrader5 as mt5
from mt5_accounts import accounts as mt5_accounts

oanda_accounts = [SOURCE_ACCOUNT, DESTINATION_ACCOUNT]


def close_all_oanda(accounts):
    for oanda_account in accounts:
        try:
            # Check for open trades in the source account
            trades = OandaAPI(account_id=oanda_account).get_open_trades()

            if not trades:
                print(f"No open trades for account: {oanda_account}")

            for trade in trades:
                type = "buy" if float(trade["initialUnits"]) > 0 else "sell"
                instrument = trade["instrument"]
                OandaAPI(account_id=oanda_account).close_positions(instrument, type)

        except Exception as error:
            print("An error occurred:", error)


def close_all_mt5(accounts):
    # connect to the MetaTrader 5 terminal
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()

    for mt5_account in accounts:
        try:
            # get all open positions
            positions = mt5.positions_get()

            if not positions:
                print(f"No open trades for account: {mt5_account.login}")

            # iterate over the positions and close each one
            for position in positions:
                # determine the action type based on the position direction
                if position.type == mt5.ORDER_TYPE_BUY:
                    type_f = mt5.ORDER_TYPE_SELL
                    price = mt5.symbol_info_tick(position.symbol).bid
                elif position.type == mt5.ORDER_TYPE_SELL:
                    type_f = mt5.ORDER_TYPE_BUY
                    price = mt5.symbol_info_tick(position.symbol).ask

                # close the position using mt5.order_send()
                result = mt5.order_send({
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": position.symbol,
                    "volume": position.volume,
                    "type": type_f,
                    "position": position.ticket,
                    "price": price,
                    "comment": "python script close",
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": mt5.ORDER_FILLING_IOC,
                })

                # check if the order was closed successfully
                if result.retcode == mt5.TRADE_RETCODE_DONE:
                    print(f"Order {result.order} closed: {result.comment}")
                else:
                    print(f"Failed to close order {position.ticket}, error: {result.comment}")
        except Exception as error:
            print("An error occurred:", error)

    # shut down the MetaTrader 5 terminal connection
    mt5.shutdown()


if __name__ == "__main__":
    close_all_oanda(accounts=oanda_accounts)
    close_all_mt5(accounts=mt5_accounts)
