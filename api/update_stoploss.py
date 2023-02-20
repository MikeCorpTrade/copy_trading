from crud_api import OandaAPI
from constants import BASE_URL, API_KEY


def update_stoploss(order_id, instrument):
    # Get the current market price
    current_price = OandaAPI(API_KEY, BASE_URL).get_current_price(instrument)

    # Get the order details
    order = OandaAPI(API_KEY, BASE_URL).get_order(order_id)

    # Calculate the current risk reward ratio
    entry_price = float(order["price"])
    stop_loss = float(order["stopLossOnFill"]["price"])
    take_profit = float(order["takeProfitOnFill"]["price"])
    risk = entry_price - stop_loss
    reward = take_profit - entry_price
    if risk == 0:  # Avoid division by zero
        risk_reward_ratio = None
    else:
        risk_reward_ratio = abs(reward / risk)

    # Update the stop loss if necessary
    if risk_reward_ratio == 1.0:
        OandaAPI(API_KEY, BASE_URL).update_stoploss_order(
            instrument, current_price)
    elif risk_reward_ratio >= 2.0:
        n = int(risk_reward_ratio)
        new_stop_loss = entry_price + (entry_price - stop_loss) * (n-1)
        OandaAPI(API_KEY, BASE_URL).update_stoploss_order(
            instrument, new_stop_loss)
