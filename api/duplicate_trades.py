import requests
from constants import API_KEY, BASE_URL, SOURCE_ACCOUNT, DESTINATION_ACCOUNT
import json
from crud_api import OandaAPI


def create_order(account_id, instrument, units, stop_loss, take_profit):
    url = BASE_URL + account_id + "/orders"
    headers = {
        "Authorization": "Bearer " + API_KEY,
        "Content-Type": "application/json"
    }
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
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        return {"error": error}


def get_open_trades(account_id):
    url = BASE_URL + "/v3/accounts/" + account_id + "/trades"
    headers = {
        "Authorization": "Bearer " + API_KEY,
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        return {"error": error}


def duplicate_trade(trade, destination_account_id):
    stop_loss = trade["stopLossOrder"]["price"]
    take_profit = trade["takeProfitOrder"]["price"]
    try:
        response = create_order(
            destination_account_id, trade["instrument"], trade["currentUnits"], stop_loss, take_profit)
        print(
            f"Trade {trade['id']} duplicated in target account with response: {response}")
    except Exception as e:
        print(f"Error duplicating trade {trade['id']}: {str(e)}")


def update_order(account_id, order_id, stop_loss):
    data = {
        "order": {
            "timeInForce": "GTC",
            "price": stop_loss,
            "type": "STOP_LOSS",
            "tradeID": "6368"
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer MOCKED_API_KEY"
    }
    response = requests.put(
        f"{BASE_URL}{account_id}/orders/{order_id}", headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        raise Exception(f"Failed to update order: {response.text}")
    return response.json()


if __name__ == "__main__":
    print("Duplication Trading Algorithm started")

    # Example usage
    source_account_id = SOURCE_ACCOUNT
    destination_account_id = DESTINATION_ACCOUNT

    while True:

        try:
            # Check for open trades in the source account
            trades = OandaAPI(account_id=source_account_id).get_open_trades()
            target_trades = OandaAPI(
                account_id=destination_account_id).get_open_trades()
            target_trade_ids = [trade['id']
                                for trade in target_trades]

            for trade in trades:
                # Duplicate the trade in the destination account
                if trade['id'] not in target_trade_ids:
                    duplicate_trade(trade, destination_account_id)

        except Exception as error:
            print("An error occurred:", error)
