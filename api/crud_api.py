import requests
import json
import datetime
import pytz
from constants import BASE_URL, API_KEY, SOURCE_ACCOUNT


class OandaAPI:
    def __init__(self, api_key: str = API_KEY, account_id: str = SOURCE_ACCOUNT) -> None:
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.account_id = account_id

    # GET

    def get_current_price(self, instrument: str) -> float:
        """
        Get the current price of the given instrument from Oanda API
        """
        url = f"{BASE_URL}{self.account_id}/pricing?instruments={instrument}"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            price = response.json()["prices"][0]["bids"][0]["price"]
            return float(price)
        except requests.exceptions.HTTPError as err:
            print(
                f"Error getting current price of the instrument {instrument} : {err}")

    def get_orders(self):
        """
        Get a list of orders from Oanda API
        """
        url = f"{BASE_URL}{self.account_id}/orders"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            orders = response.json()["orders"]
            return orders
        except requests.exceptions.HTTPError as err:
            print(f"Error getting orders : {err}")

    def get_order(self, order_id: str):
        """
        Get the details of the given order from Oanda API
        """
        url = f"{BASE_URL}{self.account_id}/orders/{order_id}"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            order = response.json()["order"]
            return order
        except requests.exceptions.HTTPError as err:
            print(f"Error getting order ID {order_id}: {err}")

    def get_instrument_trade(self, instrument: str):
        """
        Get the opening trade object of an instrument from Oanda API
        """
        url = f"{BASE_URL}{self.account_id}/trades"

        try:
            response = requests.get(url, headers=self.headers)
            data = json.loads(response.text)
            for trade in data['trades']:
                trade_instrument = get_instrument(trade)
                if trade_instrument == instrument:
                    return trade
        except requests.exceptions.HTTPError as err:
            print(
                f"Error retrieving trade ID for {instrument} : {err}")

    def get_stoploss_order_id(self, instrument: str):
        """
        Get the ID of the stoploss order of an instrument from Oanda API
        """
        url = f"{BASE_URL}{self.account_id}/trades"

        try:
            response = requests.get(url, headers=self.headers)
            data = json.loads(response.text)
            for trade in data['trades']:
                trade_instrument = get_instrument(trade)
                if trade_instrument == instrument:
                    return trade['stopLossOrder']['id']
        except requests.exceptions.HTTPError as err:
            print(
                f"Error retrieving stoploss Order ID for {instrument} : {err}")

    def get_open_trades(self):
        """
        Get the list of open trades from Oanda API
        """
        url = f"{BASE_URL}{self.account_id}/trades"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            trades = response.json()["trades"]
            return trades
        except requests.exceptions.HTTPError as error:
            return {"Error getting open Trades": error}

    def get_list_currencies(self):
        """
        Get a list of currencies tradeable from Oanda API
        """
        url = f"{BASE_URL}{self.account_id}/instruments"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            instruments = response.json()['instruments']
            forex_pairs = [instrument['name'] for instrument in instruments if instrument['type'] == 'CURRENCY']
            return forex_pairs
        except requests.exceptions.HTTPError as err:
            print(f"Error getting list of currencies : {err}")

    def get_account_balance(self):
        """
        Get the balance of an account from Oanda API
        """
        url = f"{BASE_URL}{self.account_id}"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            balance_account = response.json()["account"]["balance"]
            return float(balance_account)
        except requests.exceptions.HTTPError as error:
            return {"Error getting open Trades": error}

    # CREATE

    def create_order(self, instrument: str, units: float, stop_loss: float, take_profit: float):
        url = f"{BASE_URL}{self.account_id}/orders"

        data = {
            "order": {
                "instrument": instrument,
                "timeInForce": "FOK",
                "units": units,
                "type": "MARKET",
                "stopLossOnFill": {
                    "price": stop_loss
                },
                "takeProfitOnFill": {
                    "price": take_profit
                }
            }
        }

        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as error:
            return {f"Error creating an order for {instrument}": error}

    # UPDATE

    def update_stoploss_order_v1(self, instrument: str, stop_loss: float):
        """
        Update the stop loss of a given order in Oanda API by only through instrument
        """

        trade = self.get_instrument_trade(instrument)
        trade_id = trade["id"]
        stoploss_order_id = trade["stopLossOrder"]["id"]

        url = f"{BASE_URL}{self.account_id}/orders/{stoploss_order_id}"

        data = {
            "order": {
                "timeInForce": "GTC",
                "price": stop_loss,
                "type": "STOP_LOSS",
                "tradeID": trade_id
            }
        }

        try:
            response = requests.put(
                url, headers=self.headers, data=json.dumps(data))
            response.raise_for_status()
            print(f"Stop loss updated for trade ID {trade_id} to {stop_loss}")
        except requests.exceptions.HTTPError as err:
            print(f"Error updating stop loss for trade ID {trade_id}: {err}")

    def update_stoploss_order_v2(self, trade_id, stoploss_order_id, stop_loss: float):
        """
        Version 2 of the update_stoploss_order : Update the stop loss of a given order in Oanda API
        Please, provide the trade_id, the stoploss_order_id and the new stop_loss.
        """

        url = f"{BASE_URL}{self.account_id}/orders/{stoploss_order_id}"

        data = {
            "order": {
                "timeInForce": "GTC",
                "price": stop_loss,
                "type": "STOP_LOSS",
                "tradeID": trade_id
            }
        }

        try:
            response = requests.put(
                url, headers=self.headers, data=json.dumps(data))
            response.raise_for_status()
            print(f"Stop loss updated for trade ID {trade_id} to {stop_loss}")
        except requests.exceptions.HTTPError as err:
            print(f"Error updating stop loss for trade ID {trade_id}: {err}")

    # DELETE
    def close_positions(self, instrument: str, type: str):
        """
        Close all open positions of an account from Oanda API
        """
        url = f"{BASE_URL}{self.account_id}/positions/{instrument}/close"

        if type == "buy":
            data = {"longUnits": "ALL"}
        else:
            data = {"shortUnits": "ALL"}

        try:
            response = requests.put(
                url, headers=self.headers, data=json.dumps(data))
            response.raise_for_status()
            print(f"Position closed for instrument {instrument}")
        except requests.exceptions.HTTPError as err:
            print(f"Error closing position for instrument {instrument}: {err}")


class OandaTrade:
    def __init__(self, trade):
        self.trade = trade
        self.take_profit = get_takeprofit_price(trade)
        self.stop_loss = get_stoploss_price(trade)
        self.stop_loss_id = get_stoploss_id(trade)
        self.open_price = get_open_price(trade)
        self.instrument = get_instrument(trade)
        self.units = get_units_trade(trade)
        self.id = get_trade_id(trade)
        self.open_time = get_open_time(trade)
        self.units = get_units_trade(trade)


def get_takeprofit_price(trade):
    return float(trade["takeProfitOrder"]["price"])


def get_stoploss_price(trade):
    return float(trade["stopLossOrder"]["price"])


def get_stoploss_id(trade):
    return float(trade["stopLossOrder"]["id"])


def get_open_price(trade):
    return float(trade["price"])


def get_units_trade(trade):
    return float(trade["initialUnits"])


def get_instrument(trade):
    return trade["instrument"]


def get_trade_id(trade):
    return trade["id"]


def get_open_time(trade):
    return trade["openTime"]


def duplicate_to_oanda(trade_id, instrument, stop_loss, take_profit, lots, oanda_accounts):
    for account in oanda_accounts:
        try:
            target_balance = OandaAPI(account_id=account).get_account_balance()
            units = int(lots.calculate_units_per_trade(target_balance))
            response = OandaAPI(account_id=account).create_order(
                instrument, units, stop_loss, take_profit)
            print(
                f"Trade {trade_id} duplicated in target account with response: {response}")
        except Exception as e:
            print(f"Error duplicating trade {trade_id}: {str(e)}")


def is_old_trade(trade: OandaTrade, time_limit: int = 2) -> bool:
    # get the time the trade was opened
    trade_time_str = trade.open_time

    # parse the datetime string without microseconds
    trade_time_obj = datetime.datetime.strptime(trade_time_str[:-4], "%Y-%m-%dT%H:%M:%S.%f")

    # add the microseconds component manually
    microseconds = int(trade_time_str[-4:-1]) * 1000  # convert to microseconds
    trade_time_obj = trade_time_obj.replace(microsecond=microseconds)

    # set the timezone to UTC
    trade_time_obj = trade_time_obj.replace(tzinfo=pytz.UTC)

    # get the current time
    current_time = datetime.datetime.now(pytz.UTC)

    # calculate the time difference between the trade time and current time
    time_diff = (current_time - trade_time_obj).total_seconds()

    if time_diff > time_limit:
        return True

    return False
