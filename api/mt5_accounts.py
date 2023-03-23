from demo_accounts import INITIAL_ACCOUNT_PASS, INITIAL_ACCOUNT_LOGIN, INITIAL_ACCOUNT_SERVER, VANTAGE_DEMO_1_LOGIN, \
    VANTAGE_DEMO_1_PASS, VANTAGE_DEMO_1_SERVER, VANTAGE_DEMO_2_LOGIN, VANTAGE_DEMO_2_PASS, VANTAGE_DEMO_2_SERVER, OANDA_DEMO_1_PASS, OANDA_DEMO_1_LOGIN, OANDA_DEMO_1_SERVER


class Account:
    def __init__(self, login, password, server):
        self.login = login
        self.password = password
        self.server = server


inital_account = Account(login=INITIAL_ACCOUNT_LOGIN, password=INITIAL_ACCOUNT_PASS, server=INITIAL_ACCOUNT_SERVER)
vantage_demo1 = Account(login=VANTAGE_DEMO_1_LOGIN, password=VANTAGE_DEMO_1_PASS, server=VANTAGE_DEMO_1_SERVER)
vantage_demo2 = Account(login=VANTAGE_DEMO_2_LOGIN, password=VANTAGE_DEMO_2_PASS, server=VANTAGE_DEMO_2_SERVER)
oanda_demo1 = Account(login=OANDA_DEMO_1_LOGIN, password=OANDA_DEMO_1_PASS, server=OANDA_DEMO_1_SERVER)

accounts = [oanda_demo1]
