import MetaTrader5 as mt5
from api.map_oanda_mt5 import start_mt5
from constants import SOURCE_ACCOUNT, DESTINATION_ACCOUNT
from api.mt5_accounts import accounts as mt5_accounts


if __name__ == "__main__":
    start_mt5()

    try:
        account = mt5_accounts[0]
        mt5.login(login=account.login, password=account.password, server=account.server)

        # groups = ['Forex', 'CFD', 'Futures', 'Bonds', 'Crypto', 'Stocks']
        groups = ['*USD']

        for group in groups:

            # get all available symbols
            symbols = mt5.symbols_get(group=group)

            # filter out non-tradable symbols
            tradable_symbols = [s for s in symbols if s.trade_mode == mt5.SYMBOL_TRADE_MODE_FULL]

            print(f"Symbols available for {group}:")
            # print the list of tradable symbols
            for s in tradable_symbols:
                print(s.name)

        mt5.shutdown()

    except Exception as error:
        print("An error occurred:", error)
