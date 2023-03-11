from api.lots_calculation import is_currency_pair, LotsCalculation, convert_units_to_volume
import MetaTrader5 as mt5
from api.map_oanda_mt5 import start_mt5, duplicate_to_mt5, map_order_oanda_to_mt5
from api.mt5_accounts import accounts as mt5_accounts
from constants import SOURCE_ACCOUNT, DESTINATION_ACCOUNT, oanda_accounts
from api.crud_api import OandaAPI, duplicate_trade, is_old_trade, get_instrument


if __name__ == "__main__":
    print("Duplication Trading Algorithm started...")
    list_currencies = OandaAPI().get_list_currencies()
    start_mt5()

    while True:

        try:
            # Check for open trades in the source account
            trades = OandaAPI(account_id=SOURCE_ACCOUNT).get_open_trades()
            source_balance = OandaAPI(account_id=SOURCE_ACCOUNT).get_account_balance()
            target_trades = OandaAPI(account_id=DESTINATION_ACCOUNT).get_open_trades()

            target_trade_instruments = [trade['instrument']
                                        for trade in target_trades]

            for trade in trades:
                # Duplicate the trade in the OANDA destination account
                trade_instrument = get_instrument(trade)
                is_currency = is_currency_pair(trade_instrument, list_currencies)

                if trade_instrument not in target_trade_instruments and not is_old_trade(trade):

                    lots = LotsCalculation(trade, is_currency, source_balance)

                    for account in oanda_accounts:
                        target_balance = OandaAPI(account_id=account).get_account_balance()
                        units = lots.calculate_units_per_trade(target_balance)
                        duplicate_trade(trade, units, account)

                    # Map oanda order to mt5
                    mt5_trade_request = map_order_oanda_to_mt5(trade)

                    # Send order to mt5
                    for account in mt5_accounts:
                        mt5.login(login=account.login, password=account.password, server=account.server)
                        mt5_account_balance = mt5.account_info().balance
                        units = lots.calculate_units_per_trade(mt5_account_balance)
                        volume = convert_units_to_volume(units)
                        mt5_trade_request["volume"] = volume
                        duplicate_to_mt5(mt5_trade=mt5_trade_request, mt5_account=account)

        except Exception as error:
            print("An error occurred:", error)
