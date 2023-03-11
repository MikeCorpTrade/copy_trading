import MetaTrader5 as mt5
from api.map_oanda_mt5 import start_mt5
from constants import SOURCE_ACCOUNT, DESTINATION_ACCOUNT
from api.mt5_accounts import accounts as mt5_accounts


# Example usage
source_account_id = SOURCE_ACCOUNT
destination_account_id = DESTINATION_ACCOUNT

if __name__ == "__main__":
    start_mt5()

    try:
        for account in mt5_accounts:
            mt5.login(login=account.login, password=account.password, server=account.server)
            mt5_account_balance = mt5.account_info().balance
            print(mt5_account_balance)

    except Exception as error:
        print("An error occurred:", error)
