from crud_api import OandaAPI
from constants import BASE_URL, API_KEY


def update_stoploss(instrument):
    # Get the current market price
    current_price = OandaAPI(API_KEY, BASE_URL).get_current_price(instrument)

    # Get the trade details
    trade = OandaAPI(API_KEY, BASE_URL).get_instrument_trade(instrument)
    trade_id = trade["id"]
    stoploss_order_id = trade["stopLossOrder"]["id"]

    # Calculate the current risk reward ratio
    entry_price = float(trade["price"])
    stop_loss = float(trade["stopLossOrder"]["price"])
    take_profit = float(trade["takeProfitOrder"]["price"])
    risk = entry_price - stop_loss
    reward = take_profit - entry_price
    if risk == 0:  # Avoid division by zero
        risk_reward_ratio = None
    else:
        risk_reward_ratio = abs(reward / risk)

    # Update the stop loss if necessary
    if risk_reward_ratio == 1.0:
        OandaAPI(API_KEY, BASE_URL).update_stoploss_order_v2(trade_id, stoploss_order_id, current_price)
    elif risk_reward_ratio >= 2.0:
        n = int(risk_reward_ratio)
        new_stop_loss = entry_price + (entry_price - stop_loss) * (n-1)
        OandaAPI(API_KEY, BASE_URL).update_stoploss_order_v2(trade_id, stoploss_order_id, new_stop_loss)
