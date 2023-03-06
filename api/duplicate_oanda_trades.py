from api.crud_api import OandaAPI


def duplicate_trade(trade, destination_account_id):
    stop_loss = trade["stopLossOrder"]["price"]
    take_profit = trade["takeProfitOrder"]["price"]
    try:
        response = OandaAPI(account_id=destination_account_id).create_order(
            trade["instrument"], trade["currentUnits"], stop_loss, take_profit)
        print(
            f"Trade {trade['id']} duplicated in target account with response: {response}")
    except Exception as e:
        print(f"Error duplicating trade {trade['id']}: {str(e)}")
