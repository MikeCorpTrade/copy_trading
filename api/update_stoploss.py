from crud_api import OandaAPI
from constants import SOURCE_ACCOUNT, BASE_URL, API_KEY


def update_stoploss(trade):
    # Get the current market price
    current_price = OandaAPI(API_KEY, BASE_URL).get_current_price(trade["instrument"])

    # Get the trade details
    trade_id = trade["id"]
    stoploss_order_id = trade["stopLossOrder"]["id"]

    # Calculate the current risk reward ratio
    entry_price = float(trade["price"])
    stop_loss = float(trade["stopLossOrder"]["price"])
    take_profit = float(trade["takeProfitOrder"]["price"])
    risk = entry_price - stop_loss
    reward = current_price - entry_price
    if risk == 0:  # Avoid division by zero
        risk_reward_ratio = None
    else:
        risk_reward_ratio = abs(reward / risk)

    # Calculate n
    n = int(risk_reward_ratio)

    # TODO Check if the order is buy or sell (for the direction of the stoploss)
    new_stop_loss = entry_price + (entry_price - stop_loss) * (n - 1)

    # Update the stop loss if necessary
    if 0.99 <= risk_reward_ratio < 1.99 and stop_loss != entry_price:
        OandaAPI(API_KEY, BASE_URL).update_stoploss_order_v2(trade_id, stoploss_order_id, entry_price)
    elif 1.99 <= risk_reward_ratio < n and n >= 2 and stop_loss != new_stop_loss:
        OandaAPI(API_KEY, BASE_URL).update_stoploss_order_v2(trade_id, stoploss_order_id, new_stop_loss)


if __name__ == "__main__":
    print("Update Stoploss Algorithm started...")

    while True:

        try:
            # Check for open trades in the source account
            trades = OandaAPI(account_id=SOURCE_ACCOUNT).get_open_trades()

            for trade in trades:
                # Update the stoploss of a trade
                update_stoploss(trade)

        except Exception as error:
            print("An error occurred:", error)
