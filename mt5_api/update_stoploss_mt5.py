import MetaTrader5 as mt5


def get_current_price(instrument):
    if not mt5.initialize():
        print("initialize() failed")
        return None

    prices = mt5.copy_rates_from_pos(instrument, mt5.TIMEFRAME_M1, 0, 1)
    mt5.shutdown()

    return prices[0].close


def update_stoploss_mt5(order_id, instrument):
    # Get the current market price
    current_price = get_current_price(instrument)

    # Get the order details
    order = get_order(order_id)

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
        update_order(order_id, current_price)
    elif risk_reward_ratio == 2.0:
        new_stop_loss = entry_price + (entry_price - stop_loss)
        update_order(order_id, new_stop_loss)
    elif risk_reward_ratio > 2.0:
        n = int(risk_reward_ratio)
        new_stop_loss = entry_price + (entry_price - stop_loss) * (n - 1)
        update_order(order_id, new_stop_loss)
