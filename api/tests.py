from api.lots_calculation import is_currency_pair, LotsCalculation
from constants import SOURCE_ACCOUNT, DESTINATION_ACCOUNT
from api.crud_api import OandaAPI

# Example usage
source_account_id = SOURCE_ACCOUNT
destination_account_id = DESTINATION_ACCOUNT

if __name__ == "__main__":
    list_currencies = OandaAPI().get_list_currencies()

    while True:

        try:
            # Check for open trades in the source account
            trades = OandaAPI(account_id=source_account_id).get_open_trades()
            source_balance = OandaAPI(account_id=source_account_id).get_account_balance()

            for trade in trades:
                is_currency = is_currency_pair(trade["instrument"], list_currencies)
                risk = LotsCalculation(trade, is_currency, source_balance).risk
                print(risk)

        except Exception as error:
            print("An error occurred:", error)
