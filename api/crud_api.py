import requests
import json
from constants import BASE_URL, API_KEY, SOURCE_ACCOUNT

account_id = SOURCE_ACCOUNT


class OandaAPI:
    def __init__(self, api_key=API_KEY, account_id=account_id) -> None:
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.account_id = account_id

    # GET

    def get_current_price(self, instrument):
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

    def get_order(self, order_id):
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

    def get_instrument_trade(self, instrument):
        """
        Get the opening trade object of an instrument from Oanda API
        """
        url = f"{BASE_URL}{self.account_id}/trades"

        try:
            response = requests.get(url, headers=self.headers)
            data = json.loads(response.text)
            for trade in data['trades']:
                if trade['instrument'] == instrument:
                    return trade
        except requests.exceptions.HTTPError as err:
            print(
                f"Error retrieving trade ID for {instrument} : {err}")

    def get_stoploss_order_id(self, instrument):
        """
        Get the ID of the stoploss order of an instrument from Oanda API
        """
        url = f"{BASE_URL}{self.account_id}/trades"

        try:
            response = requests.get(url, headers=self.headers)
            data = json.loads(response.text)
            for trade in data['trades']:
                if trade['instrument'] == instrument:
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

    # CREATE

    def create_order(self, instrument, units, stop_loss, take_profit):
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

    def update_stoploss_order(self, instrument, stop_loss):
        """
        Update the stop loss of a given order in Oanda API by only through instrument
        """

        stoploss_order_id = self.get_stoploss_order_id(instrument)
        trade_id = self.get_instrument_trade_id(instrument)

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

    def update_stoploss_order_v2(self, trade_id, stoploss_order_id, stop_loss):
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


if __name__ == "__main__":
    print("Hello")
