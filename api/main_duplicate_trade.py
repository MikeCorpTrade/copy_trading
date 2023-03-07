from api.map_oanda_mt5 import login_mt5, duplicate_to_mt5
from api.mt5_accounts import accounts
from constants import SOURCE_ACCOUNT, DESTINATION_ACCOUNT
from api.crud_api import OandaAPI, duplicate_trade, is_old_trade

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
            target_trade_instruments = [trade['instrument']
                                        for trade in target_trades]

            for trade in trades:
                # Duplicate the trade in the OANDA destination account
                # TODO: add a security to check if the order was created in a range of time
                #  ( if the trade was opened more than 3sec ago for example, then don't duplicate it )

                if trade['instrument'] not in target_trade_instruments and not is_old_trade(trade):
                    duplicate_trade(trade, destination_account_id)
                    duplicate_to_mt5(oanda_trade=trade, accounts=accounts)

        except Exception as error:
            print("An error occurred:", error)
