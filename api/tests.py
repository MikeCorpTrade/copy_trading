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

            # get all available symbols
            symbols = mt5.symbols_get()

            # filter out non-tradable symbols
            tradable_symbols = [s for s in symbols if s.trade_mode == mt5.SYMBOL_TRADE_MODE_FULL]

            # print the list of tradable symbols
            for s in tradable_symbols:
                print(s.name)

    except Exception as error:
        print("An error occurred:", error)
