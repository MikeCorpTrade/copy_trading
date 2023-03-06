from api.map_oanda_mt5 import login_mt5, map_order_oanda_to_mt5
from api.mt5_accounts import accounts
from constants import SOURCE_ACCOUNT, DESTINATION_ACCOUNT
from api.crud_api import OandaAPI
from api.duplicate_oanda_trades import duplicate_trade
import MetaTrader5 as mt5

# Example usage
source_account_id = SOURCE_ACCOUNT
destination_account_id = DESTINATION_ACCOUNT

if __name__ == "__main__":
    print("Duplication Trading Algorithm started...")
    login_mt5()

    while True:

        try:
            # Check for open trades in the source account
            trades = OandaAPI(account_id=source_account_id).get_open_trades()
            target_trades = OandaAPI(
                account_id=destination_account_id).get_open_trades()
            target_trade_ids = [trade['id']
                                for trade in target_trades]

            for trade in trades:
                # Duplicate the trade in the OANDA destination account
                if trade['id'] not in target_trade_ids:
                    duplicate_trade(trade, destination_account_id)

                    # Map oanda order to mt5
                    for account in accounts:
                        # Connect to mt5 trading account
                        mt5.login(login=account.login, password=account.password, server=account.server)
                        mt5_trade_request = map_order_oanda_to_mt5(trade)

                        # Send order to mt5
                        order_result = mt5.order_send(mt5_trade_request)
                        print(order_result)

        except Exception as error:
            print("An error occurred:", error)
