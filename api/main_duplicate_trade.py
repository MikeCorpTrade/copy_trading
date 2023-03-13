import MetaTrader5 as mt5
from api.lots_calculation import is_currency_pair, LotsCalculation
from api.map_oanda_mt5 import start_mt5, duplicate_to_mt5, map_order_oanda_to_mt5
from api.mt5_accounts import accounts as mt5_accounts
from constants import SOURCE_ACCOUNT, DESTINATION_ACCOUNT, oanda_accounts
from api.crud_api import OandaAPI, duplicate_to_oanda, is_old_trade, get_instrument, OandaTrade

if __name__ == "__main__":
    print("Duplication Trading Algorithm started...")
    list_currencies = OandaAPI().get_list_currencies()
    start_mt5()

    while True:

        try:
            # Check for open trades in the source account
            source_trades = OandaAPI(account_id=SOURCE_ACCOUNT).get_open_trades()
            source_balance = OandaAPI(account_id=SOURCE_ACCOUNT).get_account_balance()
            target_trades = OandaAPI(account_id=DESTINATION_ACCOUNT).get_open_trades()
            target_trade_instruments = [get_instrument(trade)
                                        for trade in target_trades]

            for trade in source_trades:
                oanda_trade = OandaTrade(trade)
                trade_instrument = oanda_trade.instrument

                if trade_instrument not in target_trade_instruments and not is_old_trade(oanda_trade):

                    # Get trade basic infos
                    stop_loss = oanda_trade.stop_loss
                    take_profit = oanda_trade.take_profit
                    trade_id = oanda_trade.id

                    is_currency = is_currency_pair(trade_instrument, list_currencies)
                    lots = LotsCalculation(oanda_trade, is_currency, source_balance)

                    # Duplicate the trade in the OANDA target accounts
                    duplicate_to_oanda(trade_id, trade_instrument, stop_loss, take_profit, lots, oanda_accounts)

                    # Map oanda order to mt5
                    order_type = mt5.ORDER_TYPE_BUY if lots.units > 0 else mt5.ORDER_TYPE_SELL
                    mt5_trade_request = map_order_oanda_to_mt5(order_type, trade_instrument, stop_loss, take_profit)
                    duplicate_to_mt5(mt5_trade=mt5_trade_request, mt5_accounts=mt5_accounts, lots=lots)

        except Exception as error:
            print("An error occurred:", error)
